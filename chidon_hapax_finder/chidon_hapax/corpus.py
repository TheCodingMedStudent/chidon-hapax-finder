"""Loading the Tanach corpus + Hebrew text utilities."""

from __future__ import annotations

import gzip
import json
import os
import re
from dataclasses import dataclass

from . import paths

#: the copy shipped with the program (read-only once frozen)
DATA_DIR = paths.resource("data")
CORPUS_PATH = os.path.join(DATA_DIR, "tanach.json.gz")

#: where a rebuilt or downloaded corpus is written — always writable
USER_CORPUS_PATH = os.path.join(paths.user_data_dir(), "tanach.json.gz")


#: bumped whenever build_corpus.py changes how the corpus is generated, so
#: that a corrected corpus shipped with an update replaces one the user built
#: from an older version of the program
CORPUS_FORMAT_VERSION = 2


def corpus_version(path: str) -> int:
    """The format version of a corpus file, or 0 if it cannot be read.

    Reads only the head of the stream: the version is the first key written,
    so there is no need to decompress 2 MB of text to find it.
    """
    try:
        with gzip.open(path, "rt", encoding="utf-8") as f:
            head = f.read(200)
    except Exception:
        return 0
    m = re.search(r'"version"\s*:\s*(\d+)', head)
    return int(m.group(1)) if m else 0


def corpus_path() -> str:
    """Which corpus to load.

    A corpus the user rebuilt themselves normally wins — they asked for it,
    presumably to pick up fresher upstream text. But if the bundled copy has a
    *newer format version*, the program has been updated with a corpus fix
    since they rebuilt, and the fix has to reach them: otherwise a bug stays
    invisible on their machine forever.
    """
    if not os.path.exists(USER_CORPUS_PATH):
        return CORPUS_PATH
    user_v = corpus_version(USER_CORPUS_PATH)
    if user_v == 0:                     # unreadable or truncated: ignore it
        return CORPUS_PATH
    if corpus_version(CORPUS_PATH) > user_v:
        return CORPUS_PATH
    return USER_CORPUS_PATH

# U+05B0-U+05BC, U+05C1, U+05C2, U+05C7 = vowel points (nikkud)
# everything else in U+0591-U+05C7 = cantillation / scribal marks
_NIKKUD = set(range(0x05B0, 0x05BD)) | {0x05C1, 0x05C2, 0x05C7}
_ALL_MARKS = set(range(0x0591, 0x05C8))
_TEAMIM = _ALL_MARKS - _NIKKUD

_DROP_TEAMIM = {c: None for c in _TEAMIM}
_DROP_ALL = {c: None for c in _ALL_MARKS}

FINALS = {"ך": "כ", "ם": "מ", "ן": "נ", "ף": "פ", "ץ": "צ"}

#: comparison levels, from loosest to strictest (plus "root", which compares
#: dictionary words rather than written forms)
LEVELS = ["root", "consonantal", "vocalized", "full"]


def strip_teamim(s: str) -> str:
    """Drop cantillation marks, keep nikkud."""
    return s.translate(_DROP_TEAMIM)


def strip_all_marks(s: str) -> str:
    """Drop every point and accent — bare consonants."""
    return s.translate(_DROP_ALL)


def normalize(word: str, level: str = "consonantal", fold_finals: bool = False) -> str:
    if level == "consonantal":
        w = strip_all_marks(word)
    elif level == "vocalized":
        w = strip_teamim(word)
    else:
        w = word
    w = re.sub(r"[^\u0590-\u05F4]", "", w)
    if fold_finals:
        w = "".join(FINALS.get(c, c) for c in w)
    return w


# ----------------------------------------------------------------- gematria
_LETTER_VALUES = {
    "א": 1, "ב": 2, "ג": 3, "ד": 4, "ה": 5, "ו": 6, "ז": 7, "ח": 8, "ט": 9,
    "י": 10, "כ": 20, "ך": 20, "ל": 30, "מ": 40, "ם": 40, "נ": 50, "ן": 50,
    "ס": 60, "ע": 70, "פ": 80, "ף": 80, "צ": 90, "ץ": 90, "ק": 100, "ר": 200,
    "ש": 300, "ת": 400,
}
_HUNDREDS = [(400, "ת"), (300, "ש"), (200, "ר"), (100, "ק")]
_TENS = [(90, "צ"), (80, "פ"), (70, "ע"), (60, "ס"), (50, "נ"), (40, "מ"),
         (30, "ל"), (20, "כ"), (10, "י")]
_ONES = [(9, "ט"), (8, "ח"), (7, "ז"), (6, "ו"), (5, "ה"), (4, "ד"),
         (3, "ג"), (2, "ב"), (1, "א")]


def gematria_to_int(s: str) -> int | None:
    s = re.sub(r"[\"'׳״\s]", "", s)
    if not s or any(c not in _LETTER_VALUES for c in s):
        return None
    return sum(_LETTER_VALUES[c] for c in s)


def int_to_gematria(n: int) -> str:
    """15 -> טו, 16 -> טז, 116 -> קטז."""
    if n <= 0:
        return str(n)
    out = ""
    while n >= 100:
        for v, letter in _HUNDREDS:
            if n >= v:
                out += letter
                n -= v
                break
    if n == 15:
        return out + "טו"
    if n == 16:
        return out + "טז"
    for v, letter in _TENS:
        if n >= v:
            out += letter
            n -= v
            break
    for v, letter in _ONES:
        if n >= v:
            out += letter
            n -= v
            break
    return out


# ------------------------------------------------------------------- corpus
@dataclass
class Verse:
    idx: int           # position in Corpus.verses
    book: int          # index into Corpus.books
    chapter: int       # 1-based
    verse: int         # 1-based
    words: list        # surface forms, with nikkud + te'amim
    lemmas: list       # Strong's number per word (0 = none)
    maqqef: set        # word indices followed by a maqqef
    ketiv: dict        # word index -> ketiv spelling (the word itself is the qere)


class Corpus:
    def __init__(self, data: dict):
        self.source = data.get("source", "")
        #: Strong's number (as str) -> [Hebrew lemma, short gloss]
        self.lexicon: dict = data.get("lexicon", {})
        self.books = data["books"]
        self.verses: list[Verse] = []
        self.by_book: list[list[list[Verse]]] = []   # [book][chapter-1] -> [Verse]
        for bi, b in enumerate(self.books):
            chapters = []
            for ci, ch in enumerate(b["chapters"]):
                vs = []
                for vi, v in enumerate(ch):
                    verse = Verse(len(self.verses), bi, ci + 1, vi + 1, v["w"],
                                  v.get("l") or [0] * len(v["w"]),
                                  set(v.get("m", ())),
                                  {int(k): val for k, val in v.get("k", {}).items()})
                    vs.append(verse)
                    self.verses.append(verse)
                chapters.append(vs)
            self.by_book.append(chapters)

    # -- lookups ----------------------------------------------------------
    def book_index(self, osis: str) -> int:
        for i, b in enumerate(self.books):
            if b["osis"] == osis:
                return i
        raise KeyError(osis)

    def n_chapters(self, bi: int) -> int:
        return len(self.by_book[bi])

    def n_verses(self, bi: int, ch: int) -> int:
        return len(self.by_book[bi][ch - 1])

    def book_he(self, bi: int) -> str:
        return self.books[bi]["he"]

    def book_en(self, bi: int) -> str:
        return self.books[bi]["en"]

    def total_words(self) -> int:
        return sum(len(v.words) for v in self.verses)

    # -- display ----------------------------------------------------------
    def ref_parts(self, v: Verse) -> tuple:
        """(chapter, verse, marker) under the active numbering scheme."""
        from .numbering import map_ref
        return map_ref(self.books[v.book]["osis"], v.chapter, v.verse)

    def ref(self, v: Verse, hebrew: bool = True) -> str:
        ch, vs, mark = self.ref_parts(v)
        if hebrew:
            return (f"{self.book_he(v.book)} "
                    f"{int_to_gematria(ch)}:{int_to_gematria(vs)}{mark}")
        return f"{self.book_en(v.book)} {ch}:{vs}{mark}"

    @staticmethod
    def join_words(verse: Verse, start: int, end: int) -> str:
        """Surface text of words [start, end) with maqqef where the text has it."""
        out = []
        for i in range(start, end):
            out.append(verse.words[i])
            if i < end - 1:
                out.append("־" if i in verse.maqqef else " ")
        return "".join(out)

    def verse_text(self, verse: Verse) -> str:
        return self.join_words(verse, 0, len(verse.words))


    # -- roots ------------------------------------------------------------
    def lemma_text(self, lemma: int) -> str:
        """The dictionary form, e.g. 8199 -> שָׁפַט."""
        e = self.lexicon.get(str(lemma))
        return e[0] if e else (f"#{lemma}" if lemma else "")

    def lemma_gloss(self, lemma: int) -> str:
        e = self.lexicon.get(str(lemma))
        return e[1] if e else ""

    def build_lemma_index(self):
        """Cached: lemma -> [(verse, word_index), ...] over the whole Tanach,
        and a lookup from any written form to the lemmas it can carry."""
        if getattr(self, "_lemma_index", None) is not None:
            return self._lemma_index, self._form_index
        occ: dict = {}
        forms: dict = {}
        for v in self.verses:
            for i, lemma in enumerate(v.lemmas):
                if lemma:
                    occ.setdefault(lemma, []).append((v, i))
                key = strip_all_marks(v.words[i])
                forms.setdefault(key, set()).add(lemma)
        self._lemma_index, self._form_index = occ, forms
        return occ, forms

    def find_lemmas(self, query: str) -> list:
        """Lemmas matching a query: a written form, a dictionary form, a
        Strong's number, or a bare root such as שפט."""
        occ, forms = self.build_lemma_index()
        q = strip_all_marks(query).strip()
        if not q:
            return []
        if query.strip().lstrip("Hh#").isdigit():
            n = int(query.strip().lstrip("Hh#"))
            return [n] if n in occ else []
        hits = list(forms.get(q, ()))
        if hits:
            return sorted(h for h in hits if h)
        # dictionary form, or a root spelled without prefixes
        out = [lemma for lemma in occ
               if strip_all_marks(self.lemma_text(lemma)) == q]
        if out:
            return sorted(out)
        return sorted(lemma for lemma in occ
                      if q and strip_all_marks(self.lemma_text(lemma)).find(q) == 0)


def corpus_exists(path: str | None = None) -> bool:
    return os.path.exists(path or corpus_path())


def load_corpus(path: str | None = None) -> Corpus:
    path = path or corpus_path()
    if not os.path.exists(path):
        raise FileNotFoundError(
            f"Corpus not found at {path}. Build it with "
            f"'python -m chidon_hapax.build_corpus', or use the "
            f"'Download Tanach text' button in the app.")
    with gzip.open(path, "rt", encoding="utf-8") as f:
        return Corpus(json.load(f))
