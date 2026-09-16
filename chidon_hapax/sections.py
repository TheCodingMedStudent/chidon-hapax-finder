"""The canonical divisions of the Tanach, for "unique within …" searches.

Section names are proper nouns, so they are shown as "Hebrew · transliteration"
in every interface language rather than being translated.
"""

from __future__ import annotations

TORAH = ["Gen", "Exod", "Lev", "Num", "Deut"]
NEVIIM_RISHONIM = ["Josh", "Judg", "1Sam", "2Sam", "1Kgs", "2Kgs"]
TREI_ASAR = ["Hos", "Joel", "Amos", "Obad", "Jonah", "Mic", "Nah", "Hab",
             "Zeph", "Hag", "Zech", "Mal"]
NEVIIM_ACHARONIM = ["Isa", "Jer", "Ezek"] + TREI_ASAR
NEVIIM = NEVIIM_RISHONIM + NEVIIM_ACHARONIM
EMET = ["Ps", "Prov", "Job"]
MEGILLOT = ["Song", "Ruth", "Lam", "Eccl", "Esth"]
KETUVIM = EMET + MEGILLOT + ["Dan", "Ezra", "Neh", "1Chr", "2Chr"]

#: key -> (Hebrew name, transliteration, book list)
SECTIONS = {
    "torah": ("תורה", "Torah", TORAH),
    "neviim": ("נביאים", "Nevi'im", NEVIIM),
    "neviim_rishonim": ("נביאים ראשונים", "Nevi'im Rishonim", NEVIIM_RISHONIM),
    "neviim_acharonim": ("נביאים אחרונים", "Nevi'im Acharonim", NEVIIM_ACHARONIM),
    "trei_asar": ("תרי עשר", "Trei Asar", TREI_ASAR),
    "ketuvim": ("כתובים", "Ketuvim", KETUVIM),
    "emet": ("ספרי אמ״ת", "Sifrei Emet", EMET),
    "megillot": ("חמש מגילות", "Chamesh Megillot", MEGILLOT),
}

ORDER = ["torah", "neviim", "neviim_rishonim", "neviim_acharonim", "trei_asar",
         "ketuvim", "emet", "megillot"]

#: the section names per interface language. Transliterations are what a
#: Chidon participant says out loud, so they are kept even where a translated
#: form exists — except in Russian, where the Cyrillic form is what reads.
LOCAL = {
    "en": {"torah": "Torah", "neviim": "Nevi'im",
           "neviim_rishonim": "Nevi'im Rishonim",
           "neviim_acharonim": "Nevi'im Acharonim", "trei_asar": "Trei Asar",
           "ketuvim": "Ketuvim", "emet": "Sifrei Emet",
           "megillot": "The Five Megillot"},
    "fr": {"torah": "Torah (Pentateuque)", "neviim": "Nevi'im (Prophètes)",
           "neviim_rishonim": "Nevi'im Rishonim",
           "neviim_acharonim": "Nevi'im Acharonim", "trei_asar": "Trei Asar",
           "ketuvim": "Ketouvim (Écrits)", "emet": "Sifrei Emet",
           "megillot": "Cinq Meguilot"},
    "es": {"torah": "Torá (Pentateuco)", "neviim": "Nevi'im (Profetas)",
           "neviim_rishonim": "Nevi'im Rishonim",
           "neviim_acharonim": "Nevi'im Acharonim", "trei_asar": "Trei Asar",
           "ketuvim": "Ketuvim (Escritos)", "emet": "Sifrei Emet",
           "megillot": "Cinco Meguilot"},
    "pt": {"torah": "Torá (Pentateuco)", "neviim": "Nevi'im (Profetas)",
           "neviim_rishonim": "Nevi'im Rishonim",
           "neviim_acharonim": "Nevi'im Acharonim", "trei_asar": "Trei Asar",
           "ketuvim": "Ketuvim (Escritos)", "emet": "Sifrei Emet",
           "megillot": "Cinco Meguilot"},
    "ru": {"torah": "Тора (Пятикнижие)", "neviim": "Невиим (Пророки)",
           "neviim_rishonim": "Невиим Ришоним", "neviim_acharonim":
           "Невиим Ахароним", "trei_asar": "Трей Асар",
           "ketuvim": "Ктувим (Писания)", "emet": "Сифрей Эмет",
           "megillot": "Пять свитков"},
}


#: Unicode isolates. Without them a Latin or Cyrillic name that begins or ends
#: with a digit — "1 Самуила" — gets its digit dragged to the wrong end when it
#: sits beside Hebrew, because the whole line is laid out right-to-left.
RLI, LRI, PDI = "\u2067", "\u2066", "\u2069"


def bidi(hebrew: str, other: str) -> str:
    """Hebrew and a Latin/Cyrillic name side by side, each laid out properly."""
    if not other:
        return hebrew
    return f"{RLI}{hebrew}{PDI}  ·  {LRI}{other}{PDI}"


def label(key: str, lang: str = "en") -> str:
    he, en, _ = SECTIONS[key]
    if lang == "he":
        return he
    return bidi(he, LOCAL.get(lang, LOCAL["en"]).get(key, en))


def hebrew(key: str) -> str:
    return SECTIONS[key][0]


def book_indexes(corpus, key: str) -> set:
    """Book indexes of a section, for the corpus in hand."""
    osis = set(SECTIONS[key][2])
    return {i for i, b in enumerate(corpus.books) if b["osis"] in osis}


def section_of(corpus, book_index: int) -> str:
    """The narrowest standard section a book belongs to."""
    osis = corpus.books[book_index]["osis"]
    for key in ("torah", "neviim_rishonim", "neviim_acharonim", "ketuvim"):
        if osis in SECTIONS[key][2]:
            return key
    return "ketuvim"
