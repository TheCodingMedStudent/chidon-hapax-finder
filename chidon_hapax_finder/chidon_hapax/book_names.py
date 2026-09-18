"""Book names in each interface language.

The corpus carries Hebrew and English. These are the rest, keyed by the OSIS
abbreviation so the order of the corpus can change without touching them.

Where a tradition differs, the naming follows the Hebrew ordering rather than
the Christian one: Samuel and Kings are numbered 1-2 each (not 1-4 Kingdoms),
and Chronicles is Chronicles rather than Paralipomenon.
"""

from __future__ import annotations

NAMES: dict[str, dict[str, str]] = {
    "fr": {
        "Gen": "Genèse", "Exod": "Exode", "Lev": "Lévitique", "Num": "Nombres",
        "Deut": "Deutéronome", "Josh": "Josué", "Judg": "Juges",
        "1Sam": "1 Samuel", "2Sam": "2 Samuel", "1Kgs": "1 Rois",
        "2Kgs": "2 Rois", "Isa": "Isaïe", "Jer": "Jérémie", "Ezek": "Ézéchiel",
        "Hos": "Osée", "Joel": "Joël", "Amos": "Amos", "Obad": "Abdias",
        "Jonah": "Jonas", "Mic": "Michée", "Nah": "Nahum", "Hab": "Habacuc",
        "Zeph": "Sophonie", "Hag": "Aggée", "Zech": "Zacharie",
        "Mal": "Malachie", "Ps": "Psaumes", "Prov": "Proverbes", "Job": "Job",
        "Song": "Cantique des cantiques", "Ruth": "Ruth",
        "Lam": "Lamentations", "Eccl": "Ecclésiaste", "Esth": "Esther",
        "Dan": "Daniel", "Ezra": "Esdras", "Neh": "Néhémie",
        "1Chr": "1 Chroniques", "2Chr": "2 Chroniques",
    },
    "es": {
        "Gen": "Génesis", "Exod": "Éxodo", "Lev": "Levítico", "Num": "Números",
        "Deut": "Deuteronomio", "Josh": "Josué", "Judg": "Jueces",
        "1Sam": "1 Samuel", "2Sam": "2 Samuel", "1Kgs": "1 Reyes",
        "2Kgs": "2 Reyes", "Isa": "Isaías", "Jer": "Jeremías",
        "Ezek": "Ezequiel", "Hos": "Oseas", "Joel": "Joel", "Amos": "Amós",
        "Obad": "Abdías", "Jonah": "Jonás", "Mic": "Miqueas", "Nah": "Nahúm",
        "Hab": "Habacuc", "Zeph": "Sofonías", "Hag": "Hageo",
        "Zech": "Zacarías", "Mal": "Malaquías", "Ps": "Salmos",
        "Prov": "Proverbios", "Job": "Job", "Song": "Cantar de los Cantares",
        "Ruth": "Rut", "Lam": "Lamentaciones", "Eccl": "Eclesiastés",
        "Esth": "Ester", "Dan": "Daniel", "Ezra": "Esdras", "Neh": "Nehemías",
        "1Chr": "1 Crónicas", "2Chr": "2 Crónicas",
    },
    "pt": {
        "Gen": "Génesis", "Exod": "Êxodo", "Lev": "Levítico", "Num": "Números",
        "Deut": "Deuteronómio", "Josh": "Josué", "Judg": "Juízes",
        "1Sam": "1 Samuel", "2Sam": "2 Samuel", "1Kgs": "1 Reis",
        "2Kgs": "2 Reis", "Isa": "Isaías", "Jer": "Jeremias",
        "Ezek": "Ezequiel", "Hos": "Oseias", "Joel": "Joel", "Amos": "Amós",
        "Obad": "Abdias", "Jonah": "Jonas", "Mic": "Miqueias", "Nah": "Naum",
        "Hab": "Habacuc", "Zeph": "Sofonias", "Hag": "Ageu",
        "Zech": "Zacarias", "Mal": "Malaquias", "Ps": "Salmos",
        "Prov": "Provérbios", "Job": "Job", "Song": "Cântico dos Cânticos",
        "Ruth": "Rute", "Lam": "Lamentações", "Eccl": "Eclesiastes",
        "Esth": "Ester", "Dan": "Daniel", "Ezra": "Esdras", "Neh": "Neemias",
        "1Chr": "1 Crónicas", "2Chr": "2 Crónicas",
    },
    "ru": {
        "Gen": "Бытие", "Exod": "Исход", "Lev": "Левит", "Num": "Числа",
        "Deut": "Второзаконие", "Josh": "Иисус Навин", "Judg": "Судьи",
        "1Sam": "1 Самуила", "2Sam": "2 Самуила", "1Kgs": "1 Царей",
        "2Kgs": "2 Царей", "Isa": "Исаия", "Jer": "Иеремия",
        "Ezek": "Иезекииль", "Hos": "Осия", "Joel": "Иоиль", "Amos": "Амос",
        "Obad": "Авдий", "Jonah": "Иона", "Mic": "Михей", "Nah": "Наум",
        "Hab": "Аввакум", "Zeph": "Софония", "Hag": "Аггей",
        "Zech": "Захария", "Mal": "Малахия", "Ps": "Псалмы", "Prov": "Притчи",
        "Job": "Иов", "Song": "Песнь песней", "Ruth": "Руфь",
        "Lam": "Плач Иеремии", "Eccl": "Экклезиаст", "Esth": "Эсфирь",
        "Dan": "Даниил", "Ezra": "Ездра", "Neh": "Неемия",
        "1Chr": "1 Хроник", "2Chr": "2 Хроник",
    },
}


def name(osis: str, lang: str, english: str) -> str:
    """The book's name in `lang`, falling back to the corpus's English."""
    return NAMES.get(lang, {}).get(osis, english)
