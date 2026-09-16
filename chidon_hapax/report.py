"""Turning a Result into a printable document.

The PDF is produced by Qt itself (QTextDocument -> QPdfWriter): Qt shapes
Hebrew, places nikkud and lays out right-to-left correctly, and it needs no
extra libraries beyond PyQt6, which the app already requires.
"""

from __future__ import annotations

import csv
import datetime as _dt
import html as _html

from . import BSD
from . import numbering
from .corpus import Corpus, int_to_gematria
from .engine import Options, Result
from .i18n import tr

FONT_STACK = ("'Taamey Frank CLM','SBL Hebrew','Ezra SIL','David','Frank Ruehl CLM',"
              "'Times New Roman','Arial Hebrew','Noto Serif Hebrew',FreeSerif,serif")

N_TITLES = {
    1: "מילים בודדות",
    2: "צירופים של שתי מילים",
    3: "צירופים של שלוש מילים",
    4: "צירופים של ארבע מילים",
    5: "צירופים של חמש מילים",
}
def _n_title_local(n: int) -> str:
    """The section subtitle, in the interface language."""
    return tr(f"pdf.n{n}") if 1 <= n <= 5 else str(n)


def _esc(s: str) -> str:
    return _html.escape(s, quote=False)


def _verses_html(corpus: Corpus, hits: list) -> str:
    """The full verse(s) covered by these hits, with every hit in bold."""
    out = []
    verses = []
    marked = set()
    for hit in hits:
        for v, i in hit.positions:
            marked.add((v.idx, i))
            if v not in verses:
                verses.append(v)
    verses.sort(key=lambda v: v.idx)
    for v in verses:
        parts = []
        for i, w in enumerate(v.words):
            token = _esc(w)
            if (v.idx, i) in marked:
                token = f"<b>{token}</b>"
            parts.append(token)
            if i < len(v.words) - 1:
                parts.append("־" if i in v.maqqef else " ")
        out.append("".join(parts))
    return " ".join(out)


def _columns_for(n: int) -> int:
    """Single words are short; long phrases need the width."""
    return {1: 3, 2: 2}.get(n, 1)


def _column_table(entries: list, cols: int) -> str:
    """Lay (ref, text) pairs out in `cols` newspaper-style columns.

    Filled column by column, so the eye runs down the rightmost column first,
    which is what a Hebrew reader expects.
    """
    if cols <= 1:
        rows = "".join(
            f"<tr><td align='right' width='12%' class='ref'>{r}</td>"
            f"<td align='right' width='88%' class='phrase'>{t}</td></tr>"
            for r, t in entries)
        return f"<table style='width:100%' width='100%' cellspacing='0'>{rows}</table>"

    per = -(-len(entries) // cols)          # ceil
    chunks = [entries[i * per:(i + 1) * per] for i in range(cols)]
    chunks.reverse()      # the table lays out LTR; chunk 0 must land on the right
    width = 100 // cols
    out = ["<table style='width:100%' width='100%' cellspacing='0'>"]
    for r in range(per):
        out.append("<tr>")
        for ch in chunks:
            if r < len(ch):
                ref, txt = ch[r]
                out.append(f"<td align='right' width='{width}%' class='phrase'>{txt}"
                           f" <span class='ref'>{ref}</span></td>")
            else:
                out.append(f"<td width='{width}%'></td>")
        out.append("</tr>")
    out.append("</table>")
    return "".join(out)


def _ref(corpus: Corpus, hit, hebrew=True) -> str:
    a = hit.verse
    b = hit.end_verse
    r = corpus.ref(a, hebrew)
    if b is not a:
        r += "-" + (int_to_gematria(b.verse) if hebrew else str(b.verse))
    return r


def build_html(corpus: Corpus, result: Result, syllabus_label: str,
               title: str = "", show_verses: bool = False,
               n_chapters: int = 0,
               alphabetical_index: bool = True,
               practice_sheet: bool = False,
               hebrew_refs: bool = True) -> str:
    o: Options = result.options
    title = title or "מילים וצירופים ייחודיים — Hapax legomena"
    today = _dt.date.today().isoformat()

    from .engine import scope_label
    scope_he = "ייחודי ב" + scope_label(corpus, o)
    scope_en = tr(f"scope.{o.scope}")
    if o.scope == "section":
        from . import sections as _sec
        from .i18n import current_language as _lang
        scope_en = _sec.label(o.scope_section, _lang())
    level_he = {"root": "שורש / ערך מילוני",
                "consonantal": "כתיב בלבד (ללא ניקוד)",
                "vocalized": "כתיב וניקוד",
                "full": "כתיב, ניקוד וטעמים"}[o.level]

    css = f"""
    body {{ font-family: {FONT_STACK}; font-size: 11pt; color: #111; }}
    h1 {{ font-size: 20pt; margin: 0 0 4pt 0; }}
    h2 {{ font-size: 15pt; margin: 18pt 0 6pt 0; color: #1a3c6e;
         border-bottom: 1px solid #9bb0cc; }}
    h3 {{ font-size: 12pt; margin: 10pt 0 3pt 0; color: #444; }}
    .sub {{ color: #555; font-size: 10pt; }}
    .phrase {{ font-size: 13pt; }}
    .ref {{ color: #1a3c6e; font-size: 10pt; }}
    .meta {{ color: #777; font-size: 8.5pt; }}
    .bsd {{ color: #666; font-size: 9pt; }}
    .verse {{ color: #555; font-size: 9.5pt; }}
    td {{ padding: 2px 6px; }}
    th {{ padding: 3px 6px; background: #e8eef6; font-size: 9.5pt; color: #24456f; }}
    """

    h = [f"<html><head><meta charset='utf-8'><style>{css}</style></head>",
         "<body dir='rtl'>"]

    # ------------------------------------------------------------- cover
    if BSD:
        h.append(f"<p class='bsd' dir='rtl' align='right'>{_esc(BSD)}</p>")
    h.append(f"<h1 dir='rtl' align='right'>{_esc(title)}</h1>")
    h.append(f"<p class='sub' dir='rtl' align='right'>חומר הבחינה: "
             f"<b>{_esc(syllabus_label)}</b></p>")
    h.append("<table width='100%' cellspacing='0'><tr>"
             f"<th align='right'>הגדרות</th><th align='right'>ערך</th></tr>")
    rows = [
        ("ייחודיות", f"{scope_he} ({scope_en})"),
        ("השוואה לפי", level_he),
        ("אורך הצירוף", ", ".join(str(n) for n in sorted(o.include_n))),
        ("צירופים מינימליים בלבד", "כן" if o.minimal else "לא"),
        ("מעבר בין פסוקים", "מותר" if o.cross_verses else "לא"),
        ("היקף", (f"{n_chapters} פרקים · " if n_chapters else "")
         + f"{result.n_verses:,} פסוקים · {result.n_words:,} מילים"),
        ("מספור פסוקים", tr("numbering.printed")
         if numbering.scheme() == numbering.PRINTED else tr("numbering.wlc")),
    ]
    if o.min_word_freq > 1:
        rows.append(("סף שכיחות לכל מילה", f"≥ {o.min_word_freq} בתנ״ך"))
    for k, v in rows:
        h.append(f"<tr><td align='right' width='35%'><b>{_esc(k)}</b></td>"
                 f"<td align='right'>{_esc(str(v))}</td></tr>")
    h.append("</table>")

    h.append("<h3 dir='rtl' align='right'>סיכום</h3>")
    h.append("<table width='100%' cellspacing='0'><tr><th align='right'>אורך</th>"
             "<th align='right'>מספר ממצאים</th></tr>")
    for n in sorted(o.include_n):
        h.append(f"<tr><td align='right'>{N_TITLES.get(n, n)}</td>"
                 f"<td align='right'>{result.per_n.get(n, 0):,}</td></tr>")
    h.append(f"<tr><td align='right'><b>סה״כ</b></td>"
             f"<td align='right'><b>{len(result.hits):,}</b></td></tr></table>")

    if result.per_book:
        h.append("<h3 dir='rtl' align='right'>לפי ספר</h3>")
        h.append("<table width='100%' cellspacing='0'><tr><th align='right'>ספר</th>"
                 + "".join(f"<th align='right'>{n}</th>" for n in sorted(o.include_n))
                 + "<th align='right'>סה״כ</th></tr>")
        for bi in sorted(result.per_book):
            c = result.per_book[bi]
            h.append(f"<tr><td align='right'>{_esc(corpus.book_he(bi))}</td>"
                     + "".join(f"<td align='right'>{c.get(n, 0)}</td>"
                               for n in sorted(o.include_n))
                     + f"<td align='right'><b>{sum(c.values())}</b></td></tr>")
        h.append("</table>")

    note = ("צירוף נחשב <b>מינימלי</b> כאשר הוא עצמו ייחודי, אך כל אחד "
            "מתת־הצירופים שלו (באורך פחות אחד) אינו ייחודי — כלומר זהו הקטע "
            "הקצר ביותר במקום הזה שמזהה את המיקום באופן חד־משמעי."
            if o.minimal else "")
    if note:
        h.append(f"<p class='meta' dir='rtl' align='right'>{note}</p>")
    if numbering.scheme() == numbering.PRINTED:
        h.append(f"<p class='meta' dir='rtl' align='right'>{tr('numbering.note')}</p>")
    h.append(f"<p class='meta' dir='rtl' align='right'>נוצר ב־{today} · "
             f"נוסח המקרא: {_esc(corpus.source)}</p>")

    # ------------------------------------------------------------ sections
    for n in sorted(o.include_n):
        hits = result.by_n(n)
        if not hits:
            continue
        cols = 1 if show_verses else _columns_for(n)
        h.append("<p style='page-break-before:always'></p>")
        h.append(f"<h2 dir='rtl' align='right'>{N_TITLES.get(n, n)} "
                 f"<span class='sub'>({_n_title_local(n)} — {len(hits):,})</span></h2>")

        chapter = None
        entries: list = []        # (ref, phrase html) for the current chapter
        verse_groups: list = []   # [[hits of one verse], ...] for the verse lines

        def flush_chapter():
            if not entries:
                return
            if show_verses:
                h.append("<table style='width:100%' width='100%' cellspacing='0'>")
                gi = 0
                for ref, phrase in entries:
                    h.append(f"<tr><td align='right' width='12%' class='ref'>{ref}</td>"
                             f"<td align='right' width='88%' class='phrase'>{phrase}</td></tr>")
                    gi += 1
                    # after the last hit of a verse, print that verse once
                    if verse_groups and gi == sum(len(g) for g in verse_groups[:1]):
                        h.append(f"<tr><td colspan='2' align='right' class='verse'>"
                                 f"{_verses_html(corpus, verse_groups.pop(0))}</td></tr>")
                        gi = 0
                h.append("</table>")
            else:
                h.append(_column_table(entries, cols))
            entries.clear()
            verse_groups.clear()

        cur_verse = None
        for hit in sorted(hits, key=lambda x: x.sort_key):
            v = hit.verse
            if (v.book, v.chapter) != chapter:
                flush_chapter()
                chapter, cur_verse = (v.book, v.chapter), None
                head_ch = corpus.ref_parts(v)[0]
                h.append(f"<h3 dir='rtl' align='right'>{_esc(corpus.book_he(v.book))} "
                         f"{int_to_gematria(head_ch) if hebrew_refs else head_ch}</h3>")
            if v.idx != cur_verse:
                cur_verse = v.idx
                verse_groups.append([])
            verse_groups[-1].append(hit)

            extra = ""
            if o.scope == "syllabus" and hit.tanach_count > 1:
                extra = f" <span class='meta'>({hit.tanach_count}×)</span>"
            ch2, vs2, mark = corpus.ref_parts(v)
            ref = (int_to_gematria(vs2) if hebrew_refs else str(vs2)) + mark
            if ch2 != head_ch:      # e.g. Num 25:19 becomes 26:1 in print
                ref = (f"{int_to_gematria(ch2)}:{ref}" if hebrew_refs
                       else f"{ch2}:{ref}")
            if hit.end_verse is not v:
                e_vs = corpus.ref_parts(hit.end_verse)[1]
                ref += "-" + (int_to_gematria(e_vs) if hebrew_refs else str(e_vs))
            entries.append((ref, _esc(hit.text) + extra))
        flush_chapter()

    # -------------------------------------------------------------- index
    if alphabetical_index and 1 in o.include_n and result.by_n(1):
        h.append("<p style='page-break-before:always'></p>")
        h.append("<h2 dir='rtl' align='right'>מפתח לפי א״ב "
                 f"<span class='sub'>({tr('pdf.index')})</span></h2>")
        from .corpus import strip_all_marks
        items = sorted(result.by_n(1), key=lambda x: strip_all_marks(x.text))
        h.append(_column_table(
            [(_esc(_ref(corpus, hit, hebrew_refs)), _esc(hit.text)) for hit in items],
            2))

    # ----------------------------------------------------------- practice
    if practice_sheet:
        h.append("<p style='page-break-before:always'></p>")
        h.append("<h2 dir='rtl' align='right'>דף תרגול "
                 f"<span class='sub'>({tr('pdf.practice')})</span></h2>")
        ordered = sorted(result.hits, key=lambda x: (x.n, x.sort_key))
        h.append("<table width='100%' cellspacing='0'>")
        for i, hit in enumerate(ordered, 1):
            h.append(f"<tr><td align='right' width='8%' class='meta'>{i}.</td>"
                     f"<td align='right' class='phrase'>{_esc(hit.text)}</td>"
                     f"<td align='left' width='30%' class='meta'>"
                     f"____________________</td></tr>")
        h.append("</table>")
        h.append("<p style='page-break-before:always'></p>")
        h.append(f"<h2 dir='rtl' align='right'>תשובות "
                 f"<span class='sub'>({tr('pdf.answers')})</span></h2>")
        h.append("<table width='100%' cellspacing='0'>")
        for i, hit in enumerate(ordered, 1):
            h.append(f"<tr><td align='right' width='8%' class='meta'>{i}.</td>"
                     f"<td align='right'>{_esc(hit.text)}</td>"
                     f"<td align='left' width='35%' class='ref'>"
                     f"{_esc(_ref(corpus, hit, hebrew_refs))}</td></tr>")
        h.append("</table>")

    h.append("</body></html>")
    return "\n".join(h)


# ------------------------------------------------------------------ export
def export_pdf(html: str, path: str, title: str = "Hapax") -> str:
    from PyQt6.QtCore import QMarginsF, QRectF, QSizeF, Qt
    from PyQt6.QtGui import (QFont, QPageLayout, QPageSize, QPainter,
                             QPdfWriter, QTextDocument, QTextOption)

    writer = QPdfWriter(path)
    writer.setPageSize(QPageSize(QPageSize.PageSizeId.A4))
    writer.setPageMargins(QMarginsF(14, 14, 14, 16), QPageLayout.Unit.Millimeter)
    writer.setResolution(300)
    writer.setTitle(title)

    doc = QTextDocument()
    doc.setDefaultFont(QFont("FreeSerif", 11))
    opt = QTextOption()
    opt.setTextDirection(Qt.LayoutDirection.RightToLeft)
    doc.setDefaultTextOption(opt)
    doc.setHtml(html)

    painter = QPainter()
    if not painter.begin(writer):
        raise RuntimeError("could not open the PDF for writing")
    try:
        # Lay the document out in 96-dpi logical units (so that "11pt" means
        # 11pt), then scale the painter up to the writer's real resolution.
        dpi = writer.resolution()
        painter.scale(dpi / 96.0, dpi / 96.0)
        page_px = QRectF(writer.pageLayout().paintRectPixels(96))
        footer_h = 96 * 0.30
        body = QSizeF(page_px.width(), page_px.height() - footer_h)
        doc.setPageSize(body)
        pages = doc.pageCount()
        for i in range(pages):
            painter.save()
            painter.translate(0, -i * body.height())
            painter.setClipRect(QRectF(0, i * body.height(),
                                       body.width(), body.height()))
            doc.drawContents(painter, QRectF(0, i * body.height(),
                                             body.width(), body.height()))
            painter.restore()
            f = QFont("FreeSerif")
            f.setPixelSize(11)          # logical (96-dpi) units
            painter.setFont(f)
            painter.drawText(QRectF(0, body.height(), body.width(), footer_h),
                             int(Qt.AlignmentFlag.AlignHCenter
                                 | Qt.AlignmentFlag.AlignVCenter),
                             f"{i + 1} / {pages}")
            if i < pages - 1:
                writer.newPage()
    finally:
        painter.end()
    return path


def export_html(html: str, path: str) -> str:
    with open(path, "w", encoding="utf-8") as f:
        f.write(html)
    return path


def export_csv(corpus: Corpus, result: Result, path: str) -> str:
    with open(path, "w", encoding="utf-8-sig", newline="") as f:
        w = csv.writer(f)
        w.writerow(["words", "phrase", "book", "chapter", "verse", "reference",
                    "count_in_syllabus", "count_in_tanach", "rarest_word_freq"])
        for h in sorted(result.hits, key=lambda x: (x.n, x.sort_key)):
            v = h.verse
            w.writerow([h.n, h.text, corpus.book_he(v.book), v.chapter, v.verse,
                        corpus.ref(v), h.syllabus_count, h.tanach_count,
                        h.rarest_word])
    return path
