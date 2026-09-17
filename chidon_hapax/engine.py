"""The hapax engine.

Two questions can be asked of a syllabus:

  scope="tanach"    which words/phrases in the syllabus occur exactly once in
                    the *whole Tanach*  (the classic Chidon hapax legomenon);
  scope="syllabus"  which occur exactly once inside the syllabus itself.

For phrases of 2..5 words, only *minimal* unique phrases are reported by
default.  This matters: if a 2-word phrase is unique, then every 3-, 4- and
5-word phrase containing it is unique too, so listing all unique 5-grams would
return nearly the entire syllabus and be worthless.  A phrase is reported only
when it is unique *and* both of its (n-1)-word sub-phrases are **not** unique —
i.e. it is the shortest window at that spot that pins the location down.  That
is exactly the phrase a Chidon question can be built on.
"""

from __future__ import annotations

import time
from collections import Counter, defaultdict
from dataclasses import dataclass, field

from . import sections
from .corpus import Corpus, Verse, normalize


@dataclass
class Options:
    max_n: int = 5
    #: "tanach"   — once in the whole Tanach
    #: "syllabus" — once inside the syllabus
    #: "book"     — once inside its own book
    #: "section"  — once inside the section named by scope_section
    #: "custom"   — once inside the range given in scope_verses
    scope: str = "tanach"
    scope_section: str = "neviim_rishonim"
    #: how many times a word or phrase may occur and still be reported.
    #: 1 = a true hapax; 2 also finds the words occurring exactly twice
    #: (dis legomena), and so on. Every occurrence inside the syllabus is
    #: listed separately, which is the point: in a face-off each contestant
    #: has to name one of them.
    max_count: int = 1
    #: count only the verses that are also in the syllabus, so the scope
    #: becomes "my part of its own book" / "my part of that section"
    scope_in_syllabus: bool = False
    level: str = "consonantal"     # "root" | "consonantal" | "vocalized" | "full"
    minimal: bool = True
    fold_finals: bool = False
    cross_verses: bool = False     # let phrases run across a verse boundary
    min_word_freq: int = 1         # every word of a 2+-word phrase must be this
                                   # common in the Tanach (n=1 is exempt)
    include_n: tuple = (1, 2, 3, 4, 5)


@dataclass
class Hit:
    n: int
    positions: list                # [(Verse, word_index), ...] length n
    text: str                      # surface text of the occurrence
    syllabus_count: int
    tanach_count: int
    scope_count: int = 1           # occurrences inside the chosen scope
    rarest_word: int = 0           # Tanach frequency of the rarest word in it
    roots: tuple = ()              # Strong's numbers, when level == "root"

    @property
    def verse(self) -> Verse:
        return self.positions[0][0]

    @property
    def end_verse(self) -> Verse:
        return self.positions[-1][0]

    @property
    def word_index(self) -> int:
        return self.positions[0][1]

    @property
    def sort_key(self):
        v = self.verse
        return (v.book, v.chapter, v.verse, self.word_index)


@dataclass
class Result:
    options: Options
    hits: list = field(default_factory=list)
    n_verses: int = 0
    n_words: int = 0
    per_n: dict = field(default_factory=dict)        # n -> number of hits
    per_book: dict = field(default_factory=dict)     # book index -> Counter(n)
    elapsed: float = 0.0
    truncated: bool = False

    def by_n(self, n: int) -> list:
        return [h for h in self.hits if h.n == n]


# ---------------------------------------------------------------- internals
def _segments(verses, cross_verses: bool):
    """Group verses into runs inside which a phrase may run.

    Without cross_verses each verse is its own run; with it, consecutive
    verses of the same chapter (present in the list) are chained.
    """
    if not cross_verses:
        return [[v] for v in verses]
    runs, cur = [], []
    for v in verses:
        if cur and (v.book, v.chapter) == (cur[-1].book, cur[-1].chapter) \
                and v.verse == cur[-1].verse + 1:
            cur.append(v)
        else:
            if cur:
                runs.append(cur)
            cur = [v]
    if cur:
        runs.append(cur)
    return runs


def _flatten(run, ids_by_verse):
    """A run of verses -> (list of token ids, list of (verse, word_index))."""
    ids, pos = [], []
    for v in run:
        vids = ids_by_verse[v.idx]
        ids.extend(vids)
        pos.extend((v, i) for i in range(len(vids)))
    return ids, pos


def span_text(corpus: Corpus, positions: list) -> str:
    """Surface text of a run of (verse, word_index) positions."""
    chunks = []
    cur_v, start, last = positions[0][0], positions[0][1], positions[0][1]
    for v, i in positions[1:]:
        if v is cur_v:
            last = i
        else:
            chunks.append(corpus.join_words(cur_v, start, last + 1))
            cur_v, start, last = v, i, i
    chunks.append(corpus.join_words(cur_v, start, last + 1))
    return " / ".join(chunks) if len(chunks) > 1 else chunks[0]


def _buckets(corpus: Corpus, opts: Options, syll_idx: set,
             scope_verses: set | None) -> list:
    """bucket id per verse, or None for verses outside the scope.

    Counting is done per (bucket, phrase). One bucket for the whole scope
    means "unique in this scope"; one bucket per book means "unique in its
    own book", which is what makes a per-book search possible in one pass.
    """
    if opts.scope == "syllabus":
        return [0 if v.idx in syll_idx else None for v in corpus.verses]
    if opts.scope == "custom":
        sv = scope_verses or set()
        return [0 if v.idx in sv else None for v in corpus.verses]
    if opts.scope == "section":
        books = sections.book_indexes(corpus, opts.scope_section)
        buckets = [0 if v.book in books else None for v in corpus.verses]
    elif opts.scope == "book":
        buckets = [v.book for v in corpus.verses]
    else:
        buckets = [0] * len(corpus.verses)   # the whole Tanach
    if opts.scope_in_syllabus:
        buckets = [b if (b is not None and v.idx in syll_idx) else None
                   for b, v in zip(buckets, corpus.verses)]
    return buckets


def scope_label(corpus: Corpus, opts: Options) -> str:
    if opts.scope == "tanach":
        return "כל התנ״ך"
    if opts.scope == "syllabus":
        return "חומר הבחינה"
    part = "החלק שבחומר הבחינה מתוך " if opts.scope_in_syllabus else ""
    if opts.scope == "book":
        return part + "כל ספר בנפרד"
    if opts.scope == "section":
        return part + sections.hebrew(opts.scope_section)
    return part + "טווח שנבחר"


def _token_key(corpus: Corpus, v, i_w: int, opts: Options) -> str:
    """How one word is compared, under the chosen level."""
    if opts.level == "root":
        lemma = v.lemmas[i_w] if i_w < len(v.lemmas) else 0
        return f"L{lemma}" if lemma else normalize(v.words[i_w], "consonantal")
    return normalize(v.words[i_w], opts.level, opts.fold_finals)


def find_occurrences(corpus: Corpus, positions: list, opts: Options) -> list:
    """Every place in the Tanach where the same word or phrase occurs.

    Answers "the report says this appears twice — where is the other one?".
    Comparison follows the same level the search used, so a root-level hit
    finds the other forms of that root, not only the identical spelling.

    Returns a list of position-lists, in canonical order, each the same shape
    as a hit's own positions.
    """
    key = tuple(_token_key(corpus, v, i, opts) for v, i in positions)
    n = len(key)
    if not n:
        return []
    first = key[0]
    out = []
    for v in corpus.verses:
        words = v.words
        for i in range(len(words)):
            if _token_key(corpus, v, i, opts) != first:
                continue
            if i + n <= len(words):              # inside one verse
                run = [(v, i + k) for k in range(n)]
            elif opts.cross_verses:
                run = _span_across(corpus, v, i, n)
                if run is None:
                    continue
            else:
                continue
            if tuple(_token_key(corpus, vv, ii, opts) for vv, ii in run) == key:
                out.append(run)
    return out


def _span_across(corpus: Corpus, v, i: int, n: int):
    """n positions starting at (v, i), continuing into following verses."""
    run, vv, ii = [], v, i
    while len(run) < n:
        if ii < len(vv.words):
            run.append((vv, ii))
            ii += 1
            continue
        nxt = vv.idx + 1
        if nxt >= len(corpus.verses):
            return None
        nv = corpus.verses[nxt]
        if nv.book != vv.book or nv.chapter != vv.chapter:
            return None
        vv, ii = nv, 0
    return run


def analyze(corpus: Corpus, syllabus_verses: list, opts: Options,
            progress=None, scope_verses: set | None = None) -> Result:
    t0 = time.time()

    def report(frac, msg):
        if progress:
            progress(frac, msg)

    # 1. normalise every word in the Tanach once, interning to ints
    report(0.02, "Normalising the text…")
    vocab: dict[str, int] = {}
    ids_by_verse: list[list[int]] = [None] * len(corpus.verses)
    by_root = opts.level == "root"
    for v in corpus.verses:
        row = []
        for i_w, w in enumerate(v.words):
            if by_root:
                lemma = v.lemmas[i_w] if i_w < len(v.lemmas) else 0
                # words Strong's doesn't cover fall back to their written form
                key = f"L{lemma}" if lemma else normalize(w, "consonantal")
            else:
                key = normalize(w, opts.level, opts.fold_finals)
            i = vocab.get(key)
            if i is None:
                i = len(vocab)
                vocab[key] = i
            row.append(i)
        ids_by_verse[v.idx] = row

    global1: Counter = Counter()
    for row in ids_by_verse:
        global1.update(row)

    syll_runs = [_flatten(r, ids_by_verse)
                 for r in _segments(syllabus_verses, opts.cross_verses)]
    all_runs = [_flatten(r, ids_by_verse)
                for r in _segments(corpus.verses, opts.cross_verses)]

    syll_idx = {v.idx for v in syllabus_verses}
    bucket_of = _buckets(corpus, opts, syll_idx, scope_verses)

    n_words = sum(len(ids) for ids, _ in syll_runs)
    prev_scope_counts: dict = {}
    hits: list[Hit] = []

    for n in range(1, opts.max_n + 1):
        base = 0.05 + 0.9 * (n - 1) / opts.max_n
        report(base, f"Scanning {n}-word phrases…")

        # -- candidates: every n-gram of the syllabus, per scope bucket
        candidates: dict = {}          # ngram -> {bucket: positions}
        for ids, pos in syll_runs:
            for i in range(len(ids) - n + 1):
                key = tuple(ids[i:i + n])
                b = bucket_of[pos[i][0].idx]
                if b is None:          # this occurrence is outside the scope
                    continue
                seen = candidates.get(key)
                if seen is not None and len(seen.get(b, ())) >= opts.max_count:
                    continue                  # already have as many as we report
                # the floor is about phrases built from ordinary words; a
                # single-word hapax always has frequency 1, so n=1 is exempt
                if n > 1 and opts.min_word_freq > 1 and \
                        any(global1[t] < opts.min_word_freq for t in key):
                    continue
                if opts.minimal and n > 1:
                    # a phrase is only interesting if its shorter parts are
                    # themselves *not* rare enough to be reported already
                    if prev_scope_counts.get((b, key[:-1]), 1) <= opts.max_count:
                        continue
                    if prev_scope_counts.get((b, key[1:]), 1) <= opts.max_count:
                        continue
                candidates.setdefault(key, {}).setdefault(b, []).append(
                    pos[i:i + n])
        if not candidates:
            prev_scope_counts = {}
            continue

        # -- count them inside the syllabus and inside the whole Tanach
        syll_counts: Counter = Counter()
        for ids, _ in syll_runs:
            for i in range(len(ids) - n + 1):
                key = tuple(ids[i:i + n])
                if key in candidates:
                    syll_counts[key] += 1

        tanach_counts: Counter = Counter()
        scope_counts: Counter = Counter()      # keyed (bucket, ngram)
        report(base + 0.45 / opts.max_n,
               f"Comparing {n}-word phrases against the scope…")
        for ids, pos in all_runs:
            for i in range(len(ids) - n + 1):
                key = tuple(ids[i:i + n])
                if key not in candidates:
                    continue
                tanach_counts[key] += 1
                b = bucket_of[pos[i][0].idx]
                if b is not None:
                    scope_counts[(b, key)] += 1

        keep = n in opts.include_n
        if keep:
            for key, by_bucket in candidates.items():
                for b, occurrences in by_bucket.items():
                    count = scope_counts[(b, key)]
                    if count > opts.max_count:
                        continue
                    # one entry per occurrence that falls inside the syllabus
                    for positions in occurrences:
                        hits.append(Hit(
                            n=n, positions=positions,
                            text=span_text(corpus, positions),
                            syllabus_count=syll_counts[key],
                            tanach_count=tanach_counts[key],
                            scope_count=count,
                            rarest_word=min(global1[t] for t in key),
                            roots=tuple(vv.lemmas[ii] for vv, ii in positions)
                            if by_root else ()))

        prev_scope_counts = dict(scope_counts)

    hits.sort(key=lambda h: (h.n, h.sort_key))
    res = Result(options=opts, hits=hits,
                 n_verses=len(syllabus_verses), n_words=n_words,
                 elapsed=time.time() - t0)
    res.per_n = {n: sum(1 for h in hits if h.n == n) for n in range(1, opts.max_n + 1)}
    per_book = defaultdict(Counter)
    for h in hits:
        per_book[h.verse.book][h.n] += 1
    res.per_book = dict(per_book)
    report(1.0, "Done.")
    return res
