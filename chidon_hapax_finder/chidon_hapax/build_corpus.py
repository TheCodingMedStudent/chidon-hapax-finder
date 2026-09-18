"""Build a compact Tanach corpus file from the Open Scriptures Hebrew Bible (morphhb).

The source is the Westminster Leningrad Codex in OSIS XML, which is already
word-segmented (one <w> element per word, maqqef as a separate <seg>).

Output: data/tanach.json.gz
{
  "source": "...", "version": 1,
  "books": [
     {"osis": "Gen", "he": "\u05d1\u05e8\u05d0\u05e9\u05d9\u05ea", "en": "Genesis",
      "chapters": [ [ verse, verse, ... ], ... ] }
  ]
}
where verse = {"w": [word, ...], "m": [indices of words followed by maqqef],
               "k": {index: ketiv_text}}

Run standalone:  python -m chidon_hapax.build_corpus [--zip path/to/morphhb.zip]
"""

from __future__ import annotations

from .corpus import CORPUS_FORMAT_VERSION

import argparse
import re
import gzip
import io
import json
import os
import sys
import urllib.request
import xml.etree.ElementTree as ET
import zipfile

OSIS_NS = "{http://www.bibletechnologies.net/2003/OSIS/namespace}"
MORPHHB_ZIP = "https://codeload.github.com/openscriptures/morphhb/zip/refs/heads/master"

# Canonical Tanach order, with Hebrew and English names.
BOOKS = [
    ("Gen", "בראשית", "Genesis", "torah"),
    ("Exod", "שמות", "Exodus", "torah"),
    ("Lev", "ויקרא", "Leviticus", "torah"),
    ("Num", "במדבר", "Numbers", "torah"),
    ("Deut", "דברים", "Deuteronomy", "torah"),
    ("Josh", "יהושע", "Joshua", "neviim"),
    ("Judg", "שופטים", "Judges", "neviim"),
    ("1Sam", "שמואל א", "I Samuel", "neviim"),
    ("2Sam", "שמואל ב", "II Samuel", "neviim"),
    ("1Kgs", "מלכים א", "I Kings", "neviim"),
    ("2Kgs", "מלכים ב", "II Kings", "neviim"),
    ("Isa", "ישעיהו", "Isaiah", "neviim"),
    ("Jer", "ירמיהו", "Jeremiah", "neviim"),
    ("Ezek", "יחזקאל", "Ezekiel", "neviim"),
    ("Hos", "הושע", "Hosea", "neviim"),
    ("Joel", "יואל", "Joel", "neviim"),
    ("Amos", "עמוס", "Amos", "neviim"),
    ("Obad", "עובדיה", "Obadiah", "neviim"),
    ("Jonah", "יונה", "Jonah", "neviim"),
    ("Mic", "מיכה", "Micah", "neviim"),
    ("Nah", "נחום", "Nahum", "neviim"),
    ("Hab", "חבקוק", "Habakkuk", "neviim"),
    ("Zeph", "צפניה", "Zephaniah", "neviim"),
    ("Hag", "חגי", "Haggai", "neviim"),
    ("Zech", "זכריה", "Zechariah", "neviim"),
    ("Mal", "מלאכי", "Malachi", "neviim"),
    ("Ps", "תהלים", "Psalms", "ketuvim"),
    ("Prov", "משלי", "Proverbs", "ketuvim"),
    ("Job", "איוב", "Job", "ketuvim"),
    ("Song", "שיר השירים", "Song of Songs", "ketuvim"),
    ("Ruth", "רות", "Ruth", "ketuvim"),
    ("Lam", "איכה", "Lamentations", "ketuvim"),
    ("Eccl", "קהלת", "Ecclesiastes", "ketuvim"),
    ("Esth", "אסתר", "Esther", "ketuvim"),
    ("Dan", "דניאל", "Daniel", "ketuvim"),
    ("Ezra", "עזרא", "Ezra", "ketuvim"),
    ("Neh", "נחמיה", "Nehemiah", "ketuvim"),
    ("1Chr", "דברי הימים א", "I Chronicles", "ketuvim"),
    ("2Chr", "דברי הימים ב", "II Chronicles", "ketuvim"),
]


LEMMA_RE = re.compile(r"(\d+)")


def _lemma_id(attr: str | None) -> int:
    """OSHB lemma attribute -> the Strong's number of the word itself.

    Prefixes come first and are separated by '/', so the last segment is the
    word proper:  'c/1961' -> 1961,  'b/7704 b' -> 7704,  'm/1035+' -> 1035,
    'l' (a bare preposition) -> 0.
    """
    if not attr:
        return 0
    last = attr.split("/")[-1]
    m = LEMMA_RE.search(last)
    return int(m.group(1)) if m else 0


def _word_text(w_el) -> str:
    """Text of a <w>, dropping the '/' morpheme separators used by OSHB."""
    return "".join(w_el.itertext()).replace("/", "").strip()


def parse_book(xml_bytes: bytes, osis: str):
    """Return chapters: list of list of verse dicts."""
    root = ET.fromstring(xml_bytes)
    chapters: dict[int, dict[int, dict]] = {}

    for verse_el in root.iter(OSIS_NS + "verse"):
        osis_id = verse_el.get("osisID")
        if not osis_id:
            continue
        parts = osis_id.split(".")
        ch, vs = int(parts[-2]), int(parts[-1])
        words: list[str] = []
        lemmas: list[int] = []
        maqqef: list[int] = []
        ketiv: dict[str, str] = {}

        for child in verse_el:
            tag = child.tag[len(OSIS_NS):]
            if tag == "w":
                txt = _word_text(child)
                if not txt:
                    continue
                if child.get("type") == "x-ketiv":
                    # The qere reading follows in a <note type="variant">;
                    # remember the ketiv and let the qere words replace it.
                    ketiv[str(len(words))] = txt
                    words.append(txt)  # provisional, replaced below if qere found
                    lemmas.append(_lemma_id(child.get("lemma")))
                else:
                    words.append(txt)
                    lemmas.append(_lemma_id(child.get("lemma")))
            elif tag == "note" and child.get("type") == "variant":
                rdg = child.find(f"{OSIS_NS}rdg[@type='x-qere']")
                if rdg is None:
                    continue
                qere_pairs = [(_word_text(w), _lemma_id(w.get("lemma")))
                              for w in rdg.iter(OSIS_NS + "w")]
                qere_pairs = [q for q in qere_pairs if q[0]]
                if not qere_pairs:
                    continue
                # Replace the immediately preceding ketiv word with the qere.
                if words:
                    idx = len(words) - 1
                    kt = words.pop()
                    lemmas.pop()
                    ketiv.pop(str(idx), None)
                    ketiv[str(len(words))] = kt
                    words.extend(q[0] for q in qere_pairs)
                    lemmas.extend(q[1] for q in qere_pairs)
            elif tag == "seg" and child.get("type") == "x-maqqef":
                if words:
                    maqqef.append(len(words) - 1)

        verse = {"w": words, "l": lemmas}
        if maqqef:
            verse["m"] = maqqef
        if ketiv:
            verse["k"] = ketiv
        chapters.setdefault(ch, {})[vs] = verse

    out = []
    for ch in sorted(chapters):
        vs_map = chapters[ch]
        out.append([vs_map[v] for v in sorted(vs_map)])
    return out


STRONGS_XML = ("https://raw.githubusercontent.com/openscriptures/HebrewLexicon/"
               "master/HebrewStrong.xml")
LEX_NS = "{http://openscriptures.github.com/morphhb/namespace}"


def parse_lexicon(xml_bytes: bytes) -> dict:
    """Strong's number -> [Hebrew lemma, short gloss]."""
    root = ET.fromstring(xml_bytes)
    out = {}
    for entry in root.iter(LEX_NS + "entry"):
        eid = entry.get("id", "")
        if not eid.startswith("H") or not eid[1:].isdigit():
            continue
        w = entry.find(LEX_NS + "w")
        if w is None or not (w.text or "").strip():
            continue
        gloss = ""
        meaning = entry.find(LEX_NS + "meaning")
        if meaning is not None:
            d = meaning.find(LEX_NS + "def")
            if d is not None and d.text:
                gloss = " ".join(d.text.split())[:60]
        out[str(int(eid[1:]))] = [w.text.strip(), gloss]
    return out


def fetch_lexicon(log=print) -> dict:
    local = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                         "HebrewStrong.xml")
    if os.path.exists(local):
        blob = open(local, "rb").read()
    else:
        log("Downloading the Strong's Hebrew lexicon …")
        with urllib.request.urlopen(STRONGS_XML, timeout=180) as r:
            blob = r.read()
    lex = parse_lexicon(blob)
    log(f"  lexicon: {len(lex):,} entries")
    return lex


def build(zip_path: str | None, out_path: str, log=print,
          lexicon_path: str | None = None) -> str:
    if zip_path and os.path.exists(zip_path):
        log(f"Reading {zip_path} …")
        blob = open(zip_path, "rb").read()
    else:
        log("Downloading the Westminster Leningrad Codex (~20 MB) …")
        with urllib.request.urlopen(MORPHHB_ZIP, timeout=180) as r:
            blob = r.read()
        log("Download complete.")

    zf = zipfile.ZipFile(io.BytesIO(blob))
    names = {os.path.basename(n): n for n in zf.namelist() if "/wlc/" in n and n.endswith(".xml")}

    books = []
    total_words = 0
    for osis, he, en, section in BOOKS:
        fname = f"{osis}.xml"
        if fname not in names:
            raise RuntimeError(f"{fname} not found in the morphhb archive")
        chapters = parse_book(zf.read(names[fname]), osis)
        n = sum(len(v["w"]) for ch in chapters for v in ch)
        total_words += n
        log(f"  {he:<14} {len(chapters):>3} chapters, {n:>6} words")
        books.append({"osis": osis, "he": he, "en": en, "section": section,
                      "chapters": chapters})

    try:
        if lexicon_path and os.path.exists(lexicon_path):
            lexicon = parse_lexicon(open(lexicon_path, "rb").read())
            log(f"  lexicon: {len(lexicon):,} entries")
        else:
            lexicon = fetch_lexicon(log)
    except Exception as e:                      # roots are optional
        log(f"  (no lexicon: {e})")
        lexicon = {}

    data = {"version": CORPUS_FORMAT_VERSION, "lexicon": lexicon, "source": "Open Scriptures Hebrew Bible (WLC), CC-BY 4.0",
            "books": books}
    os.makedirs(os.path.dirname(os.path.abspath(out_path)), exist_ok=True)
    with gzip.open(out_path, "wt", encoding="utf-8", compresslevel=9) as f:
        json.dump(data, f, ensure_ascii=False)
    log(f"Wrote {out_path} — {total_words:,} words, "
        f"{os.path.getsize(out_path)/1e6:.1f} MB")
    return out_path


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--zip", dest="zip_path", default=None)
    ap.add_argument("--lexicon", dest="lexicon", default=None)
    ap.add_argument("--out", dest="out", default=os.path.join(
        os.path.dirname(os.path.abspath(__file__)), "data", "tanach.json.gz"))
    a = ap.parse_args()
    build(a.zip_path, a.out, lexicon_path=a.lexicon)
