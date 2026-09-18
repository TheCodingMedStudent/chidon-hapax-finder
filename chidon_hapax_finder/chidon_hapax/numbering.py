"""Two verse-numbering schemes for the same text.

The bundled text is the Westminster Leningrad Codex, which numbers the
Decalogue by *ta'am tachton* — לֹא תִּרְצָח, לֹא תִּנְאָף and לֹא תִּגְנֹב each get
their own verse. Printed Hebrew Bibles (Koren, Mechon-Mamre and most others)
number it by *ta'am elyon*, one verse per commandment, so their numbers run
lower from the middle of Exodus 20 and Deuteronomy 5 onwards.

Two other places differ as well. Everything else in the Tanach — every other
chapter of all 39 books — is identical in both schemes, so this module only
ever touches four chapters.

Mappings verified against mechon-mamre.org (Exodus 20, Deuteronomy 5,
2 Kings 1) in September 2026.
"""

from __future__ import annotations

WLC = "wlc"
PRINTED = "printed"
SCHEMES = [WLC, PRINTED]

#: WLC verse -> printed verse, Exodus 20.
#: 2+3 become one verse (אנכי together with לא יהיה לך), and 13-16 become one
#: (לא תרצח / לא תנאף / לא תגנב / לא תענה), so 26 verses become 22.
_EXOD20 = {1: 1, 2: 2, 3: 2, 4: 3, 5: 4, 6: 5, 7: 6, 8: 7, 9: 8, 10: 9,
           11: 10, 12: 11, 13: 12, 14: 12, 15: 12, 16: 12, 17: 13}
_EXOD20.update({v: v - 4 for v in range(18, 27)})

#: WLC verse -> printed verse, Deuteronomy 5. Same two merges: 6+7, and 17-20.
_DEUT5 = {v: v for v in range(1, 6)}
_DEUT5.update({6: 6, 7: 6})
_DEUT5.update({v: v - 1 for v in range(8, 17)})
_DEUT5.update({17: 16, 18: 16, 19: 16, 20: 16})
_DEUT5.update({v: v - 4 for v in range(21, 34)})

_current = WLC


def set_scheme(scheme: str) -> None:
    global _current
    _current = scheme if scheme in SCHEMES else WLC


def scheme() -> str:
    return _current


def map_ref(osis: str, chapter: int, verse: int) -> tuple:
    """(chapter, verse, marker) in the current scheme.

    marker is "*" for the two verses of Joshua 21 that most printed editions
    do not have at all.
    """
    if _current == WLC:
        return chapter, verse, ""

    if osis == "Exod" and chapter == 20:
        return 20, _EXOD20.get(verse, verse), ""

    if osis == "Deut" and chapter == 5:
        return 5, _DEUT5.get(verse, verse), ""

    # ויהי אחרי המגפה: its own verse here, the opening of 26:1 in print
    if osis == "Num" and chapter == 25 and verse == 19:
        return 26, 1, ""

    # Joshua 21:36-37 (the Levitical cities of Reuben) are absent from most
    # printed editions; everything after them shifts back by two.
    if osis == "Josh" and chapter == 21:
        if verse in (36, 37):
            return 21, verse, "*"
        if verse >= 38:
            return 21, verse - 2, ""

    return chapter, verse, ""


def differs(osis: str, chapter: int) -> bool:
    """Whether this chapter is numbered differently in the two schemes."""
    return (osis, chapter) in {("Exod", 20), ("Deut", 5), ("Num", 25),
                               ("Josh", 21)}
