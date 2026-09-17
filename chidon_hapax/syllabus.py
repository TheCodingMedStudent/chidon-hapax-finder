"""Parsing a syllabus (חומר הבחינה) into a concrete list of verses.

Accepted, one entry per line or separated by ';':

    בראשית                     whole book
    בראשית א-יב                chapters (Hebrew letters)
    Genesis 1-12               chapters (digits, English name)
    שמואל א ג-ז, ט             several ranges for one book
    יהושע א:א-ה:טו             verse-level range
    מלכים ב יח:יג-כ            chapter:verse - verse
    # a comment line
"""

from __future__ import annotations

import re
import unicodedata
from dataclasses import dataclass, field, field

from .corpus import Corpus, gematria_to_int, int_to_gematria
from .i18n import tr

# Aliases in addition to the Hebrew and English names carried by the corpus.
ALIASES = {
    "Gen": ["בר", "בראשׁית", "bereshit", "bereishit", "bresishit"],
    "Exod": ["שמ", "shemot", "shmot"],
    "Lev": ["ויק", "vayikra"],
    "Num": ["במד", "bamidbar"],
    "Deut": ["דב", "devarim"],
    "Josh": ["יהו", "yehoshua"],
    "Judg": ["שופ", "שפטים", "shoftim"],
    "1Sam": ["שמואל א'", "שמו\"א", "שמ\"א", "שמואל1", "1 שמואל", "shmuel a",
             "shmuel 1", "1 samuel", "i samuel", "samuel a"],
    "2Sam": ["שמואל ב'", "שמו\"ב", "שמ\"ב", "שמואל2", "2 שמואל", "shmuel b",
             "shmuel 2", "2 samuel", "ii samuel", "samuel b"],
    "1Kgs": ["מלכים א'", "מל\"א", "מלכים1", "1 מלכים", "melachim a",
             "melachim 1", "1 kings", "i kings", "kings a"],
    "2Kgs": ["מלכים ב'", "מל\"ב", "מלכים2", "2 מלכים", "melachim b",
             "melachim 2", "2 kings", "ii kings", "kings b"],
    "Isa": ["ישע", "ישעיה", "yeshayahu", "yeshaya"],
    "Jer": ["ירמ", "ירמיה", "yirmiyahu", "yirmiya"],
    "Ezek": ["יחז", "yechezkel"],
    "Hos": ["hoshea"],
    "Joel": ["yoel"],
    "Amos": ["עמ"],
    "Obad": ["עוב", "ovadia", "ovadya"],
    "Jonah": ["yona"],
    "Mic": ["micha"],
    "Nah": ["nachum"],
    "Hab": ["chavakuk"],
    "Zeph": ["tzefania", "tzfania"],
    "Hag": ["chagai"],
    "Zech": ["zecharia", "zechariah"],
    "Mal": ["malachi"],
    "Ps": ["תה", "תהילים", "tehilim", "tehillim"],
    "Prov": ["mishlei"],
    "Job": ["iyov"],
    "Song": ["שיה\"ש", "שה\"ש", "שיר השירים", "shir hashirim"],
    "Ruth": ["rut"],
    "Lam": ["מגילת איכה", "eicha"],
    "Eccl": ["kohelet", "koheleth"],
    "Esth": ["מגילת אסתר", "ester"],
    "Dan": ["daniel"],
    "Ezra": ["ezra"],
    "Neh": ["נחמ", "nechemia", "nehemia"],
    "1Chr": ["דהי\"א", "דה\"א", "דברי הימים א'", "divrei hayamim a",
             "1 chronicles", "i chronicles", "chronicles a"],
    "2Chr": ["דהי\"ב", "דה\"ב", "דברי הימים ב'", "divrei hayamim b",
             "2 chronicles", "ii chronicles", "chronicles b"],
}

WHOLE_BOOK_WORDS = {"", "all", "*", "הכל", "כל", "כולו", "שלם"}


class SyllabusError(ValueError):
    """book_known distinguishes “this line names a book but the range is
    wrong” (a real error worth showing) from “this line isn't a reference at
    all” (a heading, which is simply skipped)."""

    def __init__(self, message: str, book_known: bool = False):
        super().__init__(message)
        self.book_known = book_known


@dataclass(frozen=True)
class Range:
    book: int
    start: tuple   # (chapter, verse)
    end: tuple     # (chapter, verse) inclusive

    def label(self, corpus: Corpus) -> str:
        b = corpus.book_he(self.book)
        full_start = self.start == (1, 1)
        last_ch = corpus.n_chapters(self.book)
        full_end = self.end == (last_ch, corpus.n_verses(self.book, last_ch))
        if full_start and full_end:
            return b
        g = int_to_gematria
        if self.start[1] == 1 and self.end[1] == corpus.n_verses(self.book, self.end[0]):
            if self.start[0] == self.end[0]:
                return f"{b} {g(self.start[0])}"
            return f"{b} {g(self.start[0])}-{g(self.end[0])}"
        return (f"{b} {g(self.start[0])}:{g(self.start[1])}"
                f"-{g(self.end[0])}:{g(self.end[1])}")


def _norm_name(s: str) -> str:
    s = s.rstrip(':：')
    s = s.strip().lower()
    s = re.sub(r"[\u0591-\u05c7]", "", s)      # points, if someone types them
    s = re.sub(r"[.'\"׳״\-_]", "", s)
    # strip accents, so Genèse / Genese and Isaías / Isaias both match
    s = "".join(c for c in unicodedata.normalize("NFD", s)
                if unicodedata.category(c) != "Mn" or "\u0591" <= c <= "\u05c7")
    s = unicodedata.normalize("NFC", s)
    s = re.sub(r"\s+", " ", s)
    return s


def build_name_index(corpus: Corpus) -> dict:
    """Every name a book may be typed under.

    Hebrew and English come from the corpus; the other interface languages
    come from book_names, so someone working in French can write "Josué" and
    someone in Russian "Судьи". Numbered books also accept the Hebrew letter
    form ("שמואל א"), a digit ("1 Samuel") and a Roman numeral ("I Samuel").
    """
    from .book_names import NAMES as LOCAL_NAMES
    idx = {}
    for i, b in enumerate(corpus.books):
        names = [b["he"], b["en"]] + ALIASES.get(b["osis"], [])
        for per_language in LOCAL_NAMES.values():
            local = per_language.get(b["osis"])
            if local:
                names.append(local)
                # "1 Rois" should also answer to "I Rois" and "Rois 1"
                m = re.match(r"^([12])\s+(.*)$", local)
                if m:
                    num, rest = m.groups()
                    roman = "I" if num == "1" else "II"
                    names += [f"{roman} {rest}", f"{rest} {num}",
                              f"{rest} {roman}"]
        # "שמואל א" also as "שמואל א" with the numeral written out
        for name in names:
            idx[_norm_name(name)] = i
    return idx


def _num(tok: str) -> int | None:
    tok = tok.strip()
    if re.fullmatch(r"\d+", tok):
        return int(tok)
    return gematria_to_int(tok)


def _parse_point(tok: str) -> tuple:
    """'ג' -> (3, None); 'ג:ה' -> (3, 5)"""
    parts = re.split(r"[:.,]|\s*פסוק\s*", tok, maxsplit=1)
    ch = _num(parts[0])
    if ch is None:
        raise SyllabusError(f"can't read the chapter number “{tok.strip()}”")
    vs = _num(parts[1]) if len(parts) > 1 and parts[1].strip() else None
    if len(parts) > 1 and parts[1].strip() and vs is None:
        raise SyllabusError(f"can't read the verse number in “{tok.strip()}”")
    return ch, vs


def _split_ranges(spec: str) -> list[str]:
    return [p for p in re.split(r"[,،]| ו(?=[א-ת])", spec) if p.strip()]


def _match_book(text: str, corpus: Corpus, name_index: dict):
    """Longest book name at the start of `text` -> (book_index, rest) or None."""
    tokens = text.split()
    for take in range(min(4, len(tokens)), 0, -1):
        cand = _norm_name(" ".join(tokens[:take]))
        if cand in name_index:
            return name_index[cand], " ".join(tokens[take:])
    return None


def _ranges_from_spec(bi: int, spec: str, corpus: Corpus) -> list:
    last_ch = corpus.n_chapters(bi)
    if _norm_name(spec) in WHOLE_BOOK_WORDS:
        return [Range(bi, (1, 1), (last_ch, corpus.n_verses(bi, last_ch)))]

    out = []
    for piece in _split_ranges(spec):
        piece = piece.strip()
        if not piece:
            continue
        halves = piece.split("-")
        if len(halves) > 2:
            raise SyllabusError(tr("err.cantRead", piece=piece))
        s_ch, s_vs = _parse_point(halves[0])
        if len(halves) == 1:
            e_ch, e_vs = s_ch, s_vs
        else:
            tail = halves[1].strip()
            if ":" in tail or "." in tail:
                e_ch, e_vs = _parse_point(tail)
            elif s_vs is not None:
                # "יח:יג-כ"  ->  same chapter, verse כ
                e_ch, e_vs = s_ch, _num(tail)
                if e_vs is None:
                    raise SyllabusError(tr("err.cantRead", piece=tail))
            else:
                e_ch, e_vs = _parse_point(tail)

        if not 1 <= s_ch <= last_ch or not 1 <= e_ch <= last_ch:
            raise SyllabusError(
                f"{corpus.book_he(bi)} has {last_ch} chapters — "
                f"“{piece}” is out of range")
        s_vs = 1 if s_vs is None else s_vs
        e_vs = corpus.n_verses(bi, e_ch) if e_vs is None else e_vs
        if not 1 <= s_vs <= corpus.n_verses(bi, s_ch):
            raise SyllabusError(tr("err.verses", book=corpus.book_he(bi),
                                   chapter=int_to_gematria(s_ch),
                                   n=corpus.n_verses(bi, s_ch)))
        if not 1 <= e_vs <= corpus.n_verses(bi, e_ch):
            raise SyllabusError(tr("err.verses", book=corpus.book_he(bi),
                                   chapter=int_to_gematria(e_ch),
                                   n=corpus.n_verses(bi, e_ch)))
        if (e_ch, e_vs) < (s_ch, s_vs):
            raise SyllabusError(tr("err.reversed", piece=piece))
        out.append(Range(bi, (s_ch, s_vs), (e_ch, e_vs)))
    if not out:
        raise SyllabusError(tr("err.nothingSelected", book=corpus.book_he(bi)))
    return out


TOTAL_RE = re.compile(r"^\s*(סך\s*הכל|סה[\"'׳״]?כ|בסך\s*הכל|total|סיכום)\b", re.I)
#: a trailing "(50)" / "(27)" chapter count, as printed on official syllabi
TRAILING_COUNT_RE = re.compile(r"[\(\[]\s*(\d+)\s*(?:פרקים|פרק|chapters?|ch\.?)?\s*[\)\]]\s*$")
HEADING_RE = re.compile(r"^\s*(חומר|תשע|תשפ|syllabus|chidon|חידון)", re.I)


def _strip_trailing_count(line: str):
    """'שמות: א-כד, לב-לד (27)' -> ('שמות: א-כד, לב-לד', 27)"""
    m = TRAILING_COUNT_RE.search(line)
    if not m:
        return line.strip(), None
    return line[:m.start()].strip(), int(m.group(1))


def parse_entry(line: str, corpus: Corpus, name_index: dict,
                default_book: int | None = None) -> tuple:
    """Return (ranges, book_index). `default_book` lets a fragment such as
    'יא-יד' (after a ';') continue the book named earlier on the same line."""
    text = line.strip()
    text = re.sub(r"[–—]", "-", text)
    if not text or text.startswith("#"):
        return [], default_book

    # longest matching book name at the start of the entry
    best = None
    tokens = re.split(r"\s+", text)
    for take in range(min(4, len(tokens)), 0, -1):
        cand = _norm_name(" ".join(tokens[:take])).rstrip(":")
        if cand in name_index:
            best = (name_index[cand], " ".join(tokens[take:]))
            break
    if best is None:
        # "שמות:א-כד" with no space, or a bare range continuing the last book
        m = re.match(r"^([^\d:]+?)\s*:\s*(.*)$", text)
        if m and _norm_name(m.group(1)) in name_index:
            best = (name_index[_norm_name(m.group(1))], m.group(2))
        elif default_book is not None:
            best = (default_book, text)
        else:
            head = _norm_name(tokens[0]).rstrip(":") if tokens else ""
            pairs = {"שמואל": "שמואל א / שמואל ב", "מלכים": "מלכים א / מלכים ב",
                     "דברי": "דברי הימים א / דברי הימים ב",
                     "samuel": "1 Samuel / 2 Samuel", "kings": "1 Kings / 2 Kings",
                     "chronicles": "1 Chronicles / 2 Chronicles"}
            if head in pairs:
                raise SyllabusError(tr("err.whichBook", name=tokens[0],
                                       options=pairs[head]), True)
            raise SyllabusError(tr("err.unknownBook", text=text))

    bi, spec = best
    spec = spec.strip().lstrip(":").strip()      # "שמות: א-כד"
    last_ch = corpus.n_chapters(bi)

    if _norm_name(spec) in WHOLE_BOOK_WORDS:
        return [Range(bi, (1, 1), (last_ch, corpus.n_verses(bi, last_ch)))], bi

    out = []
    for piece in _split_ranges(spec):
        piece = piece.strip()
        if not piece:
            continue
        halves = piece.split("-")
        if len(halves) > 2:
            raise SyllabusError(tr("err.cantRead", piece=piece), True)
        s_ch, s_vs = _parse_point(halves[0])
        if len(halves) == 1:
            e_ch, e_vs = s_ch, s_vs
        else:
            tail = halves[1].strip()
            if ":" in tail or "." in tail:
                e_ch, e_vs = _parse_point(tail)
            elif s_vs is not None:
                # "יח:יג-כ"  ->  same chapter, verse כ
                e_ch, e_vs = s_ch, _num(tail)
                if e_vs is None:
                    raise SyllabusError(tr("err.cantRead", piece=tail), True)
            else:
                e_ch, e_vs = _parse_point(tail)

        if not 1 <= s_ch <= last_ch or not 1 <= e_ch <= last_ch:
            raise SyllabusError(tr("err.chapters", book=corpus.book_he(bi),
                                   n=last_ch, piece=piece), True)
        s_vs = 1 if s_vs is None else s_vs
        e_vs = corpus.n_verses(bi, e_ch) if e_vs is None else e_vs
        if not 1 <= s_vs <= corpus.n_verses(bi, s_ch):
            raise SyllabusError(tr("err.verses", book=corpus.book_he(bi),
                                   chapter=int_to_gematria(s_ch),
                                   n=corpus.n_verses(bi, s_ch)), True)
        if not 1 <= e_vs <= corpus.n_verses(bi, e_ch):
            raise SyllabusError(tr("err.verses", book=corpus.book_he(bi),
                                   chapter=int_to_gematria(e_ch),
                                   n=corpus.n_verses(bi, e_ch)), True)
        if (e_ch, e_vs) < (s_ch, s_vs):
            raise SyllabusError(tr("err.reversed", piece=piece), True)
        out.append(Range(bi, (s_ch, s_vs), (e_ch, e_vs)))
    if not out:
        raise SyllabusError(tr("err.nothingSelected", book=corpus.book_he(bi)), True)
    return out, bi


def chapters_of(ranges: list, corpus: Corpus) -> set:
    """The distinct (book, chapter) pairs a list of ranges touches."""
    out = set()
    for r in ranges:
        for ch in range(r.start[0], r.end[0] + 1):
            out.add((r.book, ch))
    return out


@dataclass
class Parsed:
    ranges: list
    errors: list          # lines that named a book but made no sense
    ignored: list         # lines that named nothing recognisable (as text)
    notes: list           # count checks that passed
    warnings: list        # count checks that disagreed
    n_chapters: int = 0
    totals: list = field(default_factory=list)   # the "סך הכל" numbers found
    stated_total: int | None = None              # the largest of them
    title: str | None = None                     # heading line, if any

    def ok(self) -> bool:
        return bool(self.ranges) and not self.errors


def parse_document(text: str, corpus: Corpus) -> Parsed:
    """Parse a syllabus as printed/pasted, tolerating headings and totals.

    Understands the layout official syllabi are published in::

        חומר חידון התנ״ך העולמי תשפ״ז
        בראשית (50)
        שמות: א-כד, לב-לד (27)
        זכריה א-ד; יא-יד(8)
        סך הכל: 113

    The number in brackets is checked against the chapters actually selected,
    so a mistyped range is caught instead of silently shrinking the material.
    """
    name_index = build_name_index(corpus)
    ranges, errors, ignored, notes, warnings = [], [], [], [], []
    section: list = []          # chapters since the last "סך הכל" line
    cumulative: set = set()
    totals: list = []

    for lineno, raw_line in enumerate(text.splitlines(), 1):
        line = raw_line.split("#", 1)[0].split("//", 1)[0].strip()
        if not line:
            continue
        if TOTAL_RE.match(line):
            m = re.search(r"(\d+)", line)
            if m:
                value = int(m.group(1))
                totals.append(value)
                sec = set().union(*section) if section else set()
                if section and value == len(sec):
                    notes.append(tr("note.subtotal", line=lineno, value=value))
                elif value == len(cumulative):
                    notes.append(tr("note.total", line=lineno, value=value))
                else:
                    warnings.append(tr(
                        "warn.totalMismatch", line=lineno, body=line,
                        got=len(sec) if section else len(cumulative)))
            section = []
            continue

        body, declared = _strip_trailing_count(line)
        if not body:
            ignored.append(f"line {lineno}: {line}")
            continue

        line_ranges = []
        current_book = None
        failed = False
        for part in body.split(";"):
            if not part.strip():
                continue
            try:
                got, current_book = parse_entry(part, corpus, name_index,
                                                default_book=current_book)
                line_ranges.extend(got)
            except SyllabusError as e:
                if not getattr(e, "book_known", False) and not line_ranges:
                    # nothing on this line was recognised: a heading, a note…
                    ignored.append(f"line {lineno}: {line}")
                else:
                    errors.append(f"line {lineno}: {e}")
                failed = True
                break
        if failed or not line_ranges:
            continue

        got_chapters = chapters_of(line_ranges, corpus)
        if declared is not None:
            if len(got_chapters) == declared:
                notes.append(tr("note.counted", line=lineno, declared=declared))
            else:
                warnings.append(tr("warn.countMismatch", line=lineno, body=body,
                                   declared=declared, got=len(got_chapters)))
        ranges.extend(line_ranges)
        section.append(got_chapters)
        cumulative |= got_chapters

    all_chapters = chapters_of(ranges, corpus)
    if not ranges and not errors:
        errors.append(tr("err.noBooks"))

    title = None
    for text_line in ignored:
        body = text_line.split(": ", 1)[-1]
        if HEADING_RE.match(body):
            title = body
            break

    ranges.sort(key=lambda r: (r.book, r.start))
    return Parsed(ranges=ranges, errors=errors, ignored=ignored, notes=notes,
                  warnings=warnings, n_chapters=len(all_chapters),
                  totals=totals, stated_total=max(totals) if totals else None,
                  title=title)


def parse_syllabus_full(text: str, corpus: Corpus, lenient: bool = False) -> Parsed:
    """Parse and report everything found.

    lenient=True (what the app uses) only raises when nothing at all could be
    recognised; individual bad lines come back in .errors / .ignored so they
    can be shown next to the good ones.
    """
    p = parse_document(text, corpus)
    if not p.ranges:
        raise SyllabusError("; ".join(p.errors) or tr("err.noBooks"))
    if not lenient and p.errors:
        raise SyllabusError("; ".join(p.errors))
    return p


def parse_syllabus(text: str, corpus: Corpus) -> list[Range]:
    """Strict form: return the ranges or raise."""
    p = parse_document(text, corpus)
    if p.errors:
        raise SyllabusError("; ".join(p.errors))
    if not p.ranges:
        raise SyllabusError(tr("err.empty"))
    return p.ranges


def collect_verses(ranges: list[Range], corpus: Corpus) -> list:
    """Concrete, de-duplicated verse list, in canonical order."""
    seen = set()
    out = []
    for r in ranges:
        for ch in range(r.start[0], r.end[0] + 1):
            verses = corpus.by_book[r.book][ch - 1]
            first = r.start[1] if ch == r.start[0] else 1
            last = r.end[1] if ch == r.end[0] else len(verses)
            for v in verses[first - 1:last]:
                key = (v.book, v.chapter, v.verse)
                if key not in seen:
                    seen.add(key)
                    out.append(v)
    out.sort(key=lambda v: (v.book, v.chapter, v.verse))
    return out


def describe(ranges: list[Range], corpus: Corpus) -> str:
    """Compact label, grouping each book's ranges: 'שמות א-כד, לב-לד'."""
    groups = []
    for r in ranges:
        b = corpus.book_he(r.book)
        label = r.label(corpus)
        tail = label[len(b):].strip() if label.startswith(b) else label
        if groups and groups[-1][0] == r.book:
            if tail:
                groups[-1][1].append(tail)
        else:
            groups.append((r.book, [tail] if tail else []))
    parts = []
    for bi, tails in groups:
        b = corpus.book_he(bi)
        parts.append(f"{b} {', '.join(tails)}" if tails else b)
    return " · ".join(parts)
