"""Interface translations.

Only the interface is translated — the biblical text itself is always Hebrew.
Add a language by adding its code to LANGUAGES and a column to STRINGS; any
key a language is missing falls back to English.
"""

from __future__ import annotations

LANGUAGES = [
    ("en", "English"),
    ("he", "עברית"),
    ("fr", "Français"),
    ("es", "Español"),
    ("pt", "Português"),
    ("ru", "Русский"),
]

RTL_LANGUAGES = {"he"}

_current = "en"


def set_language(code: str) -> None:
    global _current
    _current = code if any(c == code for c, _ in LANGUAGES) else "en"


def current_language() -> str:
    return _current


def tr(key: str, **kw) -> str:
    row = STRINGS.get(key)
    if row is None:
        return key
    s = row.get(_current) or row.get("en") or key
    return s.format(**kw) if kw else s


def is_rtl() -> bool:
    return _current in RTL_LANGUAGES


S = STRINGS = {
    # ---------------------------------------------------------- window
    "app.title": {
        "en": "Chidon HaTanach — Hapax Finder",
        "he": "חידון התנ״ך — מילים וצירופים ייחודיים",
        "fr": "Chidon HaTanach — Chercheur d'hapax",
        "es": "Jidón HaTanaj — Buscador de hápax",
        "pt": "Chidon HaTanach — Localizador de hápax",
        "ru": "Хидон ха-Танах — поиск гапаксов",
    },
    "lang.label": {"en": "Language", "he": "שפה", "fr": "Langue",
                   "es": "Idioma", "pt": "Idioma", "ru": "Язык"},
    # ---------------------------------------------------------- corpus
    "corpus.loaded": {
        "en": "✓ Tanach text loaded — {verses} verses, {words} words",
        "he": "✓ נוסח המקרא נטען — {verses} פסוקים, {words} מילים",
        "fr": "✓ Texte du Tanakh chargé — {verses} versets, {words} mots",
        "es": "✓ Texto del Tanaj cargado — {verses} versículos, {words} palabras",
        "pt": "✓ Texto do Tanach carregado — {verses} versículos, {words} palavras",
        "ru": "✓ Текст Танаха загружен — стихов: {verses}, слов: {words}",
    },
    "corpus.missing": {
        "en": "The Tanach text has not been downloaded yet (≈20 MB, once).",
        "he": "נוסח המקרא טרם הורד (כ־20 מ״ב, פעם אחת).",
        "fr": "Le texte du Tanakh n'a pas encore été téléchargé (≈20 Mo, une fois).",
        "es": "El texto del Tanaj aún no se ha descargado (≈20 MB, una vez).",
        "pt": "O texto do Tanach ainda não foi baixado (≈20 MB, uma vez).",
        "ru": "Текст Танаха ещё не загружен (≈20 МБ, один раз).",
    },
    "corpus.download": {
        "en": "Download the Tanach text", "he": "הורדת נוסח המקרא",
        "fr": "Télécharger le texte du Tanakh", "es": "Descargar el texto del Tanaj",
        "pt": "Baixar o texto do Tanach", "ru": "Загрузить текст Танаха",
    },
    "corpus.loading": {"en": "Tanach text found — loading…",
                       "he": "נוסח המקרא נמצא — טוען…",
                       "fr": "Texte trouvé — chargement…",
                       "es": "Texto encontrado — cargando…",
                       "pt": "Texto encontrado — carregando…",
                       "ru": "Текст найден — загрузка…"},
    "corpus.downloading": {"en": "Downloading…", "he": "מוריד…",
                           "fr": "Téléchargement…", "es": "Descargando…",
                           "pt": "Baixando…", "ru": "Загрузка…"},
    # -------------------------------------------------------- syllabus
    "group.syllabus": {"en": "Syllabus", "he": "חומר הבחינה", "fr": "Programme",
                       "es": "Temario", "pt": "Programa", "ru": "Материал"},
    "syllabus.example": {
        "en": "# One book or range per line. Names in Hebrew, English, French,\n"
              "# Spanish, Portuguese or Russian; chapters in letters or digits.\n"
              "# Paste an official sheet as it is.\n",
        "he": "# ספר או טווח בכל שורה. שמות בעברית, אנגלית, צרפתית, ספרדית,\n"
              "# פורטוגזית או רוסית; פרקים באותיות או בספרות.\n"
              "# אפשר להדביק גיליון רשמי כמות שהוא.\n",
        "fr": "# Un livre ou une plage par ligne. Noms en hébreu, anglais, français,\n"
              "# espagnol, portugais ou russe ; chapitres en lettres ou en chiffres.\n"
              "# Collez la feuille officielle telle quelle.\n",
        "es": "# Un libro o rango por línea. Nombres en hebreo, inglés, francés,\n"
              "# español, portugués o ruso; capítulos en letras o cifras.\n"
              "# Pegue la hoja oficial tal cual.\n",
        "pt": "# Um livro ou intervalo por linha. Nomes em hebraico, inglês, francês,\n"
              "# espanhol, português ou russo; capítulos em letras ou algarismos.\n"
              "# Cole a folha oficial como está.\n",
        "ru": "# По одной книге или диапазону в строке. Названия на иврите,\n"
              "# английском, французском, испанском, португальском или русском;\n"
              "# главы буквами или цифрами. Можно вставить официальный лист.\n",
    },
    "ph.chapters": {
        "en": "chapters, e.g. א-יב or 1-12 (blank = whole book)",
        "he": "פרקים, למשל א-יב או 1-12 (ריק = כל הספר)",
        "fr": "chapitres, ex. א-יב ou 1-12 (vide = livre entier)",
        "es": "capítulos, p. ej. א-יב o 1-12 (vacío = libro entero)",
        "pt": "capítulos, ex. א-יב ou 1-12 (vazio = livro inteiro)",
        "ru": "главы, напр. א-יב или 1-12 (пусто = вся книга)",
    },
    "btn.add": {"en": "Add", "he": "הוסף", "fr": "Ajouter", "es": "Añadir",
                "pt": "Adicionar", "ru": "Добавить"},
    "btn.open": {"en": "Open…", "he": "פתח…", "fr": "Ouvrir…", "es": "Abrir…",
                 "pt": "Abrir…", "ru": "Открыть…"},
    "btn.save": {"en": "Save…", "he": "שמור…", "fr": "Enregistrer…",
                 "es": "Guardar…", "pt": "Salvar…", "ru": "Сохранить…"},
    "syl.summary": {
        "en": "✓ {chapters} chapters · {verses} verses · {words} words",
        "he": "✓ {chapters} פרקים · {verses} פסוקים · {words} מילים",
        "fr": "✓ {chapters} chapitres · {verses} versets · {words} mots",
        "es": "✓ {chapters} capítulos · {verses} versículos · {words} palabras",
        "pt": "✓ {chapters} capítulos · {verses} versículos · {words} palavras",
        "ru": "✓ глав: {chapters} · стихов: {verses} · слов: {words}",
    },
    "syl.matchesTotal": {
        "en": "✓ matches the total printed on the sheet ({total})",
        "he": "✓ תואם לסך הכל הרשום בגיליון ({total})",
        "fr": "✓ correspond au total indiqué sur la feuille ({total})",
        "es": "✓ coincide con el total indicado en la hoja ({total})",
        "pt": "✓ corresponde ao total indicado na folha ({total})",
        "ru": "✓ совпадает с итогом на листе ({total})",
    },
    "syl.skipped": {
        "en": "skipped {n} line(s): {lines}", "he": "דולגו {n} שורות: {lines}",
        "fr": "{n} ligne(s) ignorée(s) : {lines}",
        "es": "{n} línea(s) omitida(s): {lines}",
        "pt": "{n} linha(s) ignorada(s): {lines}",
        "ru": "пропущено строк: {n} — {lines}",
    },
    # --------------------------------------------------------- options
    "group.unique": {
        "en": "What counts as unique", "he": "מה נחשב ייחודי",
        "fr": "Ce qui compte comme unique", "es": "Qué cuenta como único",
        "pt": "O que conta como único", "ru": "Что считается уникальным",
    },
    "scope.tanach": {
        "en": "Unique in the whole Tanach", "he": "ייחודי בכל התנ״ך",
        "fr": "Unique dans tout le Tanakh", "es": "Único en todo el Tanaj",
        "pt": "Único em todo o Tanach", "ru": "Уникально во всём Танахе",
    },
    "scope.syllabus": {
        "en": "Unique inside the syllabus only", "he": "ייחודי בחומר הבחינה בלבד",
        "fr": "Unique dans le programme seulement",
        "es": "Único sólo dentro del temario",
        "pt": "Único apenas dentro do programa",
        "ru": "Уникально только внутри материала",
    },
    "label.compareBy": {"en": "Compare by:", "he": "השוואה לפי:",
                        "fr": "Comparer par :", "es": "Comparar por:",
                        "pt": "Comparar por:", "ru": "Сравнивать по:"},
    "level.root": {
        "en": "Root / dictionary word (שורש)", "he": "שורש / ערך מילוני",
        "fr": "Racine / mot du dictionnaire (שורש)",
        "es": "Raíz / palabra del diccionario (שורש)",
        "pt": "Raiz / palavra do dicionário (שורש)",
        "ru": "Корень / словарная форма (שורש)",
    },
    "level.consonantal": {
        "en": "Written form, no nikkud (כתיב)", "he": "צורת הכתיב, ללא ניקוד",
        "fr": "Forme écrite, sans nikoud (כתיב)",
        "es": "Forma escrita, sin nikud (כתיב)",
        "pt": "Forma escrita, sem nikud (כתיב)",
        "ru": "Написание без огласовок (כתיב)",
    },
    "level.vocalized": {
        "en": "Written form + nikkud (מנוקד)", "he": "כתיב וניקוד",
        "fr": "Forme écrite + nikoud (מנוקד)", "es": "Forma escrita + nikud (מנוקד)",
        "pt": "Forma escrita + nikud (מנוקד)", "ru": "Написание с огласовками (מנוקד)",
    },
    "level.full": {
        "en": "+ nikkud and te'amim (מוטעם)", "he": "כתיב, ניקוד וטעמים",
        "fr": "+ nikoud et te'amim (מוטעם)", "es": "+ nikud y te'amim (מוטעם)",
        "pt": "+ nikud e te'amim (מוטעם)", "ru": "+ огласовки и кантилляция (מוטעם)",
    },
    "label.lengths": {"en": "Phrase lengths:", "he": "אורך הצירוף:",
                      "fr": "Longueur des expressions :", "es": "Longitud de frases:",
                      "pt": "Tamanho das expressões:", "ru": "Длина сочетаний:"},
    "opt.minimal": {
        "en": "Minimal phrases only (recommended)",
        "he": "צירופים מינימליים בלבד (מומלץ)",
        "fr": "Expressions minimales seulement (recommandé)",
        "es": "Sólo frases mínimas (recomendado)",
        "pt": "Somente expressões mínimas (recomendado)",
        "ru": "Только минимальные сочетания (рекомендуется)",
    },
    "tip.minimal": {
        "en": "A phrase is listed only if it is unique AND neither of its\n"
              "shorter sub-phrases is already unique. Without this, every\n"
              "longer phrase containing a unique short one is listed too,\n"
              "which floods the report.",
        "he": "צירוף ייכלל רק אם הוא ייחודי, ואף אחד מתת־הצירופים הקצרים\n"
              "שלו אינו ייחודי בעצמו. בלי זה, כל צירוף ארוך שמכיל צירוף\n"
              "קצר ייחודי ייכלל גם הוא, והדוח יוצף.",
        "fr": "Une expression n'est listée que si elle est unique ET qu'aucune\n"
              "de ses sous-expressions plus courtes ne l'est déjà. Sans cela,\n"
              "le rapport est submergé.",
        "es": "Una frase se lista sólo si es única Y ninguna de sus subfrases\n"
              "más cortas ya lo es. Sin esto, el informe se satura.",
        "pt": "Uma expressão só é listada se for única E nenhuma das suas\n"
              "subexpressões mais curtas já o for. Sem isto, o relatório inunda.",
        "ru": "Сочетание попадает в список, только если оно уникально И ни одно\n"
              "из его более коротких подсочетаний не уникально. Иначе отчёт\n"
              "переполняется.",
    },
    "opt.cross": {
        "en": "Allow phrases to run across a verse boundary",
        "he": "אפשר צירופים שחוצים גבול פסוק",
        "fr": "Autoriser les expressions à franchir la limite d'un verset",
        "es": "Permitir frases que crucen el límite de un versículo",
        "pt": "Permitir expressões que cruzem o limite de um versículo",
        "ru": "Разрешить сочетания через границу стиха",
    },
    "label.freq": {
        "en": "In phrases, each word occurs ≥", "he": "בצירופים, כל מילה מופיעה ≥",
        "fr": "Dans les expressions, chaque mot apparaît ≥",
        "es": "En las frases, cada palabra aparece ≥",
        "pt": "Nas expressões, cada palavra ocorre ≥",
        "ru": "В сочетаниях каждое слово встречается ≥",
    },
    "tip.freq": {
        "en": "Only list a phrase of 2+ words if every word in it occurs at\n"
              "least this often in the Tanach. Raise it to get phrases built\n"
              "from ordinary words whose combination happens once — usually\n"
              "the better questions. Single words are never filtered by this.",
        "he": "צירוף של שתי מילים ומעלה ייכלל רק אם כל מילה בו מופיעה בתנ״ך\n"
              "לפחות כך וכך פעמים. העלאת הסף נותנת צירופים של מילים רגילות\n"
              "שהצירוף שלהן יחיד — בדרך כלל השאלות הטובות. מילים בודדות\n"
              "אינן מסוננות כך לעולם.",
        "fr": "N'afficher une expression de 2 mots ou plus que si chacun de ses\n"
              "mots apparaît au moins aussi souvent dans le Tanakh. Les mots\n"
              "isolés ne sont jamais filtrés ainsi.",
        "es": "Mostrar una frase de 2+ palabras sólo si cada palabra aparece al\n"
              "menos esta cantidad de veces en el Tanaj. Las palabras sueltas\n"
              "nunca se filtran así.",
        "pt": "Listar uma expressão de 2+ palavras apenas se cada palavra ocorrer\n"
              "ao menos esta quantidade de vezes no Tanach. Palavras isoladas\n"
              "nunca são filtradas assim.",
        "ru": "Показывать сочетание из 2+ слов, только если каждое слово\n"
              "встречается в Танахе не реже указанного. Отдельные слова\n"
              "этим фильтром никогда не отсекаются.",
    },
    # ---------------------------------------------------------- report
    "group.report": {"en": "Report", "he": "הפלט", "fr": "Rapport",
                     "es": "Informe", "pt": "Relatório", "ru": "Отчёт"},
    "label.title": {"en": "Title:", "he": "כותרת:", "fr": "Titre :",
                    "es": "Título:", "pt": "Título:", "ru": "Заголовок:"},
    "ph.title": {"en": "title for the PDF (optional)",
                 "he": "כותרת ל־PDF (רשות)",
                 "fr": "titre du PDF (facultatif)",
                 "es": "título del PDF (opcional)",
                 "pt": "título do PDF (opcional)",
                 "ru": "заголовок PDF (необязательно)"},
    "opt.verses": {
        "en": "Print the full verse under each entry",
        "he": "הדפס את הפסוק המלא תחת כל ערך",
        "fr": "Imprimer le verset entier sous chaque entrée",
        "es": "Imprimir el versículo completo bajo cada entrada",
        "pt": "Imprimir o versículo completo sob cada entrada",
        "ru": "Печатать полный стих под каждой записью",
    },
    "opt.index": {
        "en": "Alphabetical index of single words",
        "he": "מפתח מילים בודדות לפי א״ב",
        "fr": "Index alphabétique des mots isolés",
        "es": "Índice alfabético de palabras sueltas",
        "pt": "Índice alfabético de palavras isoladas",
        "ru": "Алфавитный указатель отдельных слов",
    },
    "opt.practice": {
        "en": "Practice sheet + answer key", "he": "דף תרגול + פתרון",
        "fr": "Feuille d'exercices + corrigé",
        "es": "Hoja de práctica + solucionario",
        "pt": "Folha de exercícios + gabarito",
        "ru": "Лист для тренировки + ответы",
    },
    "opt.hebnum": {
        "en": "Hebrew letters for chapter/verse numbers",
        "he": "מספור פרק ופסוק באותיות",
        "fr": "Lettres hébraïques pour les numéros de chapitre/verset",
        "es": "Letras hebreas para capítulo/versículo",
        "pt": "Letras hebraicas para capítulo/versículo",
        "ru": "Еврейские буквы для номеров глав и стихов",
    },
    # --------------------------------------------------------- actions
    "btn.run": {"en": "Find hapaxes", "he": "חפש מילים ייחודיות",
                "fr": "Chercher les hapax", "es": "Buscar hápax",
                "pt": "Procurar hápax", "ru": "Найти гапаксы"},
    "btn.pdf": {"en": "Save PDF…", "he": "שמור PDF…", "fr": "Enregistrer le PDF…",
                "es": "Guardar PDF…", "pt": "Salvar PDF…", "ru": "Сохранить PDF…"},
    "btn.html": {"en": "Save HTML…", "he": "שמור HTML…", "fr": "Enregistrer HTML…",
                 "es": "Guardar HTML…", "pt": "Salvar HTML…", "ru": "Сохранить HTML…"},
    "btn.csv": {"en": "Save CSV…", "he": "שמור CSV…", "fr": "Enregistrer CSV…",
                "es": "Guardar CSV…", "pt": "Salvar CSV…", "ru": "Сохранить CSV…"},
    "status.searching": {"en": "Searching…", "he": "מחפש…", "fr": "Recherche…",
                         "es": "Buscando…", "pt": "Procurando…", "ru": "Поиск…"},
    "status.writing": {"en": "Writing the PDF…", "he": "כותב את ה־PDF…",
                       "fr": "Écriture du PDF…", "es": "Escribiendo el PDF…",
                       "pt": "Escrevendo o PDF…", "ru": "Запись PDF…"},
    "status.saved": {"en": "Saved {name}", "he": "נשמר {name}",
                     "fr": "{name} enregistré", "es": "{name} guardado",
                     "pt": "{name} salvo", "ru": "Сохранено: {name}"},
    "status.found": {
        "en": "Found {n} entries in {s}s", "he": "נמצאו {n} ערכים ב־{s} שניות",
        "fr": "{n} entrées trouvées en {s} s", "es": "{n} entradas en {s} s",
        "pt": "{n} entradas em {s} s", "ru": "Найдено записей: {n} за {s} с",
    },
    # ------------------------------------------------------------ tabs
    "tab.words": {"en": "{n} word(s)", "he": "{n} מילים", "fr": "{n} mot(s)",
                  "es": "{n} palabra(s)", "pt": "{n} palavra(s)",
                  "ru": "{n} сл."},
    "tab.roots": {"en": "Root search", "he": "חיפוש שורש",
                  "fr": "Recherche de racine", "es": "Búsqueda de raíz",
                  "pt": "Busca de raiz", "ru": "Поиск корня"},
    "col.phrase": {"en": "Word / phrase", "he": "המילה / הצירוף",
                   "fr": "Mot / expression", "es": "Palabra / frase",
                   "pt": "Palavra / expressão", "ru": "Слово / сочетание"},
    "col.place": {"en": "Place", "he": "מקום", "fr": "Référence",
                  "es": "Lugar", "pt": "Lugar", "ru": "Место"},
    "col.root": {"en": "Root", "he": "שורש", "fr": "Racine", "es": "Raíz",
                 "pt": "Raiz", "ru": "Корень"},
    "col.tanach": {"en": "Tanach", "he": "בתנ״ך", "fr": "Tanakh",
                   "es": "Tanaj", "pt": "Tanach", "ru": "Танах"},
    "col.syllabus": {"en": "Syllabus", "he": "בחומר", "fr": "Programme",
                     "es": "Temario", "pt": "Programa", "ru": "Материал"},
    # ----------------------------------------------------------- roots
    "roots.ph": {
        "en": "a word, a root, or a Strong's number — e.g. ויאמר, שפט, 8199",
        "he": "מילה, שורש או מספר סטרונג — למשל ויאמר, שפט, 8199",
        "fr": "un mot, une racine ou un numéro Strong — ex. ויאמר, שפט, 8199",
        "es": "una palabra, una raíz o un número Strong — p. ej. ויאמר, שפט, 8199",
        "pt": "uma palavra, uma raiz ou um número Strong — ex. ויאמר, שפט, 8199",
        "ru": "слово, корень или номер Стронга — напр. ויאמר, שפט, 8199",
    },
    "roots.search": {"en": "Search", "he": "חפש", "fr": "Chercher",
                     "es": "Buscar", "pt": "Buscar", "ru": "Найти"},
    "roots.onlySyllabus": {
        "en": "Only occurrences inside the syllabus",
        "he": "רק היקרויות בחומר הבחינה",
        "fr": "Seulement dans le programme",
        "es": "Sólo dentro del temario", "pt": "Apenas dentro do programa",
        "ru": "Только внутри материала",
    },
    "roots.none": {
        "en": "No root found for “{q}”. Try the word as it is written, the "
              "dictionary form, or a Strong's number.",
        "he": "לא נמצא שורש עבור „{q}”. נסה את המילה ככתיבה, את צורת המילון, "
              "או מספר סטרונג.",
        "fr": "Aucune racine pour « {q} ». Essayez le mot tel qu'écrit, la forme "
              "du dictionnaire ou un numéro Strong.",
        "es": "No se encontró raíz para «{q}». Pruebe la palabra tal como se "
              "escribe, la forma del diccionario o un número Strong.",
        "pt": "Nenhuma raiz para “{q}”. Tente a palavra como escrita, a forma do "
              "dicionário ou um número Strong.",
        "ru": "Корень для «{q}» не найден. Попробуйте слово как написано, "
              "словарную форму или номер Стронга.",
    },
    "roots.summary": {
        "en": "{lemma} — {gloss} · {tanach} occurrences in the Tanach, "
              "{syllabus} in the syllabus",
        "he": "{lemma} — {gloss} · {tanach} היקרויות בתנ״ך, {syllabus} בחומר הבחינה",
        "fr": "{lemma} — {gloss} · {tanach} occurrences dans le Tanakh, "
              "{syllabus} dans le programme",
        "es": "{lemma} — {gloss} · {tanach} apariciones en el Tanaj, "
              "{syllabus} en el temario",
        "pt": "{lemma} — {gloss} · {tanach} ocorrências no Tanach, "
              "{syllabus} no programa",
        "ru": "{lemma} — {gloss} · вхождений в Танахе: {tanach}, в материале: {syllabus}",
    },
    "roots.hint": {
        "en": "Tip: set “Compare by” to Root to list every word whose root "
              "occurs only once.",
        "he": "טיפ: בחר „השוואה לפי: שורש” כדי לקבל את כל המילים ששורשן מופיע פעם אחת.",
        "fr": "Astuce : choisissez « Comparer par : racine » pour lister tous les "
              "mots dont la racine n'apparaît qu'une fois.",
        "es": "Consejo: elija «Comparar por: raíz» para listar cada palabra cuya "
              "raíz aparece una sola vez.",
        "pt": "Dica: escolha “Comparar por: raiz” para listar cada palavra cuja "
              "raiz ocorre uma única vez.",
        "ru": "Совет: выберите «Сравнивать по: корень», чтобы получить все слова, "
              "корень которых встречается один раз.",
    },
    # -------------------------------------------------------- messages
    "msg.noTextTitle": {"en": "No text yet", "he": "אין נוסח", "fr": "Pas de texte",
                        "es": "Sin texto", "pt": "Sem texto", "ru": "Нет текста"},
    "msg.noText": {
        "en": "Download the Tanach text first.", "he": "יש להוריד תחילה את נוסח המקרא.",
        "fr": "Téléchargez d'abord le texte du Tanakh.",
        "es": "Primero descargue el texto del Tanaj.",
        "pt": "Baixe primeiro o texto do Tanach.",
        "ru": "Сначала загрузите текст Танаха.",
    },
    "msg.fixSyllabus": {
        "en": "Fix the syllabus first.", "he": "יש לתקן תחילה את חומר הבחינה.",
        "fr": "Corrigez d'abord le programme.", "es": "Corrija primero el temario.",
        "pt": "Corrija primeiro o programa.", "ru": "Сначала исправьте материал.",
    },
    "msg.longTitle": {
        "en": "That will be a very long list", "he": "זו תהיה רשימה ארוכה מאוד",
        "fr": "La liste sera très longue", "es": "Será una lista muy larga",
        "pt": "Será uma lista muito longa", "ru": "Список будет очень длинным",
    },
    "msg.longBody": {
        "en": "Without “minimal phrases only”, almost every 3–5 word phrase in "
              "the syllabus counts as unique, so the report will run to "
              "thousands of entries.\n\nCarry on anyway?",
        "he": "בלי „צירופים מינימליים בלבד”, כמעט כל צירוף של 3–5 מילים בחומר "
              "ייחשב ייחודי, והדוח יגיע לאלפי ערכים.\n\nלהמשיך בכל זאת?",
        "fr": "Sans « expressions minimales seulement », presque toute expression "
              "de 3 à 5 mots est unique ; le rapport atteindra des milliers "
              "d'entrées.\n\nContinuer ?",
        "es": "Sin «sólo frases mínimas», casi toda frase de 3–5 palabras resulta "
              "única y el informe tendrá miles de entradas.\n\n¿Continuar?",
        "pt": "Sem “somente expressões mínimas”, quase toda expressão de 3–5 "
              "palavras é única e o relatório terá milhares de entradas.\n\n"
              "Continuar?",
        "ru": "Без «только минимальные сочетания» почти каждое сочетание из 3–5 "
              "слов уникально, и отчёт составит тысячи записей.\n\nПродолжить?",
    },
    "msg.error": {"en": "Error", "he": "שגיאה", "fr": "Erreur", "es": "Error",
                  "pt": "Erro", "ru": "Ошибка"},
    "msg.wrong": {"en": "Something went wrong.", "he": "משהו השתבש.",
                  "fr": "Une erreur est survenue.", "es": "Algo salió mal.",
                  "pt": "Algo deu errado.", "ru": "Что-то пошло не так."},
    "dlg.openSyllabus": {"en": "Open a syllabus", "he": "פתיחת חומר בחינה",
                         "fr": "Ouvrir un programme", "es": "Abrir un temario",
                         "pt": "Abrir um programa", "ru": "Открыть материал"},
    "dlg.saveSyllabus": {"en": "Save the syllabus", "he": "שמירת חומר הבחינה",
                         "fr": "Enregistrer le programme", "es": "Guardar el temario",
                         "pt": "Salvar o programa", "ru": "Сохранить материал"},
    "dlg.savePdf": {"en": "Save the PDF", "he": "שמירת ה־PDF",
                    "fr": "Enregistrer le PDF", "es": "Guardar el PDF",
                    "pt": "Salvar o PDF", "ru": "Сохранить PDF"},
    # ------------------------------------------------------ PDF labels
    "pdf.n1": {"en": "Single words", "he": "מילים בודדות", "fr": "Mots isolés",
               "es": "Palabras sueltas", "pt": "Palavras isoladas",
               "ru": "Отдельные слова"},
    "pdf.n2": {"en": "Two-word phrases", "he": "צירופים של שתי מילים",
               "fr": "Expressions de deux mots", "es": "Frases de dos palabras",
               "pt": "Expressões de duas palavras", "ru": "Сочетания из двух слов"},
    "pdf.n3": {"en": "Three-word phrases", "he": "צירופים של שלוש מילים",
               "fr": "Expressions de trois mots", "es": "Frases de tres palabras",
               "pt": "Expressões de três palavras", "ru": "Сочетания из трёх слов"},
    "pdf.n4": {"en": "Four-word phrases", "he": "צירופים של ארבע מילים",
               "fr": "Expressions de quatre mots", "es": "Frases de cuatro palabras",
               "pt": "Expressões de quatro palavras", "ru": "Сочетания из четырёх слов"},
    "pdf.n5": {"en": "Five-word phrases", "he": "צירופים של חמש מילים",
               "fr": "Expressions de cinq mots", "es": "Frases de cinco palabras",
               "pt": "Expressões de cinco palavras", "ru": "Сочетания из пяти слов"},
    "pdf.index": {"en": "alphabetical index", "he": "מפתח לפי א״ב",
                  "fr": "index alphabétique", "es": "índice alfabético",
                  "pt": "índice alfabético", "ru": "алфавитный указатель"},
    "pdf.practice": {"en": "practice — answers at the end",
                     "he": "תרגול — התשובות בסוף",
                     "fr": "exercices — réponses à la fin",
                     "es": "práctica — respuestas al final",
                     "pt": "exercícios — respostas no fim",
                     "ru": "тренировка — ответы в конце"},
    "pdf.answers": {"en": "Answers", "he": "תשובות", "fr": "Réponses",
                    "es": "Respuestas", "pt": "Respostas", "ru": "Ответы"},
    "err.unknownBook": {
        "en": "unknown book in “{text}”", "he": "ספר לא מוכר ב„{text}”",
        "fr": "livre inconnu dans « {text} »", "es": "libro desconocido en «{text}»",
        "pt": "livro desconhecido em “{text}”", "ru": "неизвестная книга в «{text}»",
    },
    "err.whichBook": {
        "en": "“{name}” — which one? write {options}",
        "he": "„{name}” — איזה מהם? יש לכתוב {options}",
        "fr": "« {name} » — lequel ? écrivez {options}",
        "es": "«{name}» — ¿cuál? escriba {options}",
        "pt": "“{name}” — qual? escreva {options}",
        "ru": "«{name}» — какая именно? напишите {options}",
    },
    "err.chapters": {
        "en": "{book} has {n} chapters — “{piece}” is out of range",
        "he": "ב{book} יש {n} פרקים — „{piece}” מחוץ לטווח",
        "fr": "{book} compte {n} chapitres — « {piece} » hors limites",
        "es": "{book} tiene {n} capítulos — «{piece}» fuera de rango",
        "pt": "{book} tem {n} capítulos — “{piece}” fora do intervalo",
        "ru": "в книге {book} {n} глав — «{piece}» вне диапазона",
    },
    "err.verses": {
        "en": "{book} {chapter} has {n} verses",
        "he": "ב{book} {chapter} יש {n} פסוקים",
        "fr": "{book} {chapter} compte {n} versets",
        "es": "{book} {chapter} tiene {n} versículos",
        "pt": "{book} {chapter} tem {n} versículos",
        "ru": "в {book} {chapter} {n} стихов",
    },
    "err.reversed": {
        "en": "“{piece}” ends before it starts",
        "he": "„{piece}” מסתיים לפני שהוא מתחיל",
        "fr": "« {piece} » se termine avant de commencer",
        "es": "«{piece}» termina antes de empezar",
        "pt": "“{piece}” termina antes de começar",
        "ru": "«{piece}» заканчивается раньше, чем начинается",
    },
    "err.cantRead": {
        "en": "can't read “{piece}”", "he": "לא ניתן לקרוא „{piece}”",
        "fr": "impossible de lire « {piece} »", "es": "no se puede leer «{piece}»",
        "pt": "não é possível ler “{piece}”", "ru": "не удаётся прочитать «{piece}»",
    },
    "err.nothingSelected": {
        "en": "nothing selected for {book}", "he": "לא נבחר דבר עבור {book}",
        "fr": "rien de sélectionné pour {book}", "es": "nada seleccionado para {book}",
        "pt": "nada selecionado para {book}", "ru": "ничего не выбрано для {book}",
    },
    "err.noBooks": {
        "en": "nothing in this text looks like a book of the Tanach",
        "he": "אין בטקסט הזה דבר שנראה כמו ספר מספרי התנ״ך",
        "fr": "rien dans ce texte ne ressemble à un livre du Tanakh",
        "es": "nada en este texto parece un libro del Tanaj",
        "pt": "nada neste texto parece um livro do Tanach",
        "ru": "в этом тексте нет ничего похожего на книгу Танаха",
    },
    "err.empty": {
        "en": "the syllabus is empty", "he": "חומר הבחינה ריק",
        "fr": "le programme est vide", "es": "el temario está vacío",
        "pt": "o programa está vazio", "ru": "материал пуст",
    },
    "warn.countMismatch": {
        "en": "line {line} (“{body}”): the syllabus says {declared} chapters, "
              "this selects {got}",
        "he": "שורה {line} („{body}”): בגיליון רשום {declared} פרקים, ונבחרים {got}",
        "fr": "ligne {line} (« {body} ») : la feuille indique {declared} chapitres, "
              "la sélection en compte {got}",
        "es": "línea {line} («{body}»): la hoja dice {declared} capítulos, "
              "esto selecciona {got}",
        "pt": "linha {line} (“{body}”): a folha diz {declared} capítulos, "
              "isto seleciona {got}",
        "ru": "строка {line} («{body}»): на листе указано глав: {declared}, "
              "выбрано: {got}",
    },
    "warn.totalMismatch": {
        "en": "line {line}: “{body}” — the lines above it select {got} chapters",
        "he": "שורה {line}: „{body}” — השורות שמעליה בוחרות {got} פרקים",
        "fr": "ligne {line} : « {body} » — les lignes au-dessus sélectionnent "
              "{got} chapitres",
        "es": "línea {line}: «{body}» — las líneas anteriores seleccionan "
              "{got} capítulos",
        "pt": "linha {line}: “{body}” — as linhas acima selecionam {got} capítulos",
        "ru": "строка {line}: «{body}» — строки выше выбирают глав: {got}",
    },
    "note.subtotal": {
        "en": "line {line}: subtotal {value} chapters ✓",
        "he": "שורה {line}: סיכום ביניים {value} פרקים ✓",
        "fr": "ligne {line} : sous-total {value} chapitres ✓",
        "es": "línea {line}: subtotal {value} capítulos ✓",
        "pt": "linha {line}: subtotal {value} capítulos ✓",
        "ru": "строка {line}: промежуточный итог {value} глав ✓",
    },
    "note.total": {
        "en": "line {line}: total {value} chapters ✓",
        "he": "שורה {line}: סך הכל {value} פרקים ✓",
        "fr": "ligne {line} : total {value} chapitres ✓",
        "es": "línea {line}: total {value} capítulos ✓",
        "pt": "linha {line}: total {value} capítulos ✓",
        "ru": "строка {line}: всего {value} глав ✓",
    },
    "note.counted": {
        "en": "line {line}: {declared} chapters ✓",
        "he": "שורה {line}: {declared} פרקים ✓",
        "fr": "ligne {line} : {declared} chapitres ✓",
        "es": "línea {line}: {declared} capítulos ✓",
        "pt": "linha {line}: {declared} capítulos ✓",
        "ru": "строка {line}: {declared} глав ✓",
    },
    "about.button": {"en": "About", "he": "אודות", "fr": "À propos",
                     "es": "Acerca de", "pt": "Sobre", "ru": "О программе"},
    "about.tagline": {
        "en": "Every word and phrase that occurs only once, for any syllabus, "
              "with its reference.",
        "he": "כל מילה וכל צירוף שמופיעים פעם אחת בלבד, לכל חומר בחינה, "
              "עם המקום המדויק.",
        "fr": "Chaque mot et chaque expression n'apparaissant qu'une seule fois, "
              "pour n'importe quel programme, avec sa référence.",
        "es": "Cada palabra y frase que aparece una sola vez, para cualquier "
              "temario, con su referencia.",
        "pt": "Cada palavra e expressão que ocorre uma única vez, para qualquer "
              "programa, com a sua referência.",
        "ru": "Каждое слово и сочетание, встречающееся лишь один раз, для любого "
              "материала, с указанием места.",
    },
    "about.version": {"en": "Version {v}", "he": "גרסה {v}", "fr": "Version {v}",
                      "es": "Versión {v}", "pt": "Versão {v}", "ru": "Версия {v}"},
    "about.textHeading": {
        "en": "Text and data", "he": "הנוסח והנתונים", "fr": "Texte et données",
        "es": "Texto y datos", "pt": "Texto e dados", "ru": "Текст и данные",
    },
    "about.textBody": {
        "en": "Biblical text: the Open Scriptures Hebrew Bible, a morphologically "
              "tagged Westminster Leningrad Codex (CC-BY 4.0). Roots and glosses: "
              "the Open Scriptures HebrewLexicon (Strong's, public domain). "
              "Words joined by maqqef are counted separately; where there is a "
              "ketiv/qere the qere is used.",
        "he": "נוסח המקרא: Open Scriptures Hebrew Bible — כתר לנינגרד עם ניתוח "
              "דקדוקי (CC-BY 4.0). שורשים ופירושים: Open Scriptures HebrewLexicon "
              "(סטרונג, נחלת הכלל). מילים המחוברות במקף נספרות בנפרד; בכתיב/קרי "
              "משמש הקרי.",
        "fr": "Texte biblique : l'Open Scriptures Hebrew Bible, un Codex de "
              "Leningrad annoté morphologiquement (CC-BY 4.0). Racines et "
              "définitions : l'Open Scriptures HebrewLexicon (Strong, domaine "
              "public). Les mots liés par maqqef sont comptés séparément ; en cas "
              "de ketiv/qeré, c'est le qeré qui est retenu.",
        "es": "Texto bíblico: la Open Scriptures Hebrew Bible, un Códice de "
              "Leningrado con anotación morfológica (CC-BY 4.0). Raíces y "
              "glosas: el Open Scriptures HebrewLexicon (Strong, dominio "
              "público). Las palabras unidas por maqqef se cuentan por separado; "
              "en ketiv/qeré se usa el qeré.",
        "pt": "Texto bíblico: a Open Scriptures Hebrew Bible, um Códice de "
              "Leninegrado com anotação morfológica (CC-BY 4.0). Raízes e "
              "glosas: o Open Scriptures HebrewLexicon (Strong, domínio "
              "público). Palavras ligadas por maqqef são contadas separadamente; "
              "em ketiv/qerê usa-se o qerê.",
        "ru": "Библейский текст: Open Scriptures Hebrew Bible — Ленинградский "
              "кодекс с морфологической разметкой (CC-BY 4.0). Корни и значения: "
              "Open Scriptures HebrewLexicon (Стронг, общественное достояние). "
              "Слова, соединённые маккефом, считаются отдельно; при ктив/кри "
              "используется кри.",
    },
    "about.corpus": {
        "en": "Loaded: {books} books · {verses} verses · {words} words",
        "he": "נטען: {books} ספרים · {verses} פסוקים · {words} מילים",
        "fr": "Chargé : {books} livres · {verses} versets · {words} mots",
        "es": "Cargado: {books} libros · {verses} versículos · {words} palabras",
        "pt": "Carregado: {books} livros · {verses} versículos · {words} palavras",
        "ru": "Загружено: книг: {books} · стихов: {verses} · слов: {words}",
    },
    "about.license": {
        "en": "Released under the {license} licence — free to use, copy and change.",
        "he": "מופץ ברישיון {license} — חופשי לשימוש, להעתקה ולשינוי.",
        "fr": "Publié sous licence {license} — libre d'utilisation, de copie et "
              "de modification.",
        "es": "Publicado bajo la licencia {license} — libre de usar, copiar y "
              "modificar.",
        "pt": "Publicado sob a licença {license} — livre para usar, copiar e "
              "modificar.",
        "ru": "Распространяется по лицензии {license} — свободно использовать, "
              "копировать и изменять.",
    },
    "about.noAuthor": {
        "en": "No author set — edit __author__ in chidon_hapax/__init__.py.",
        "he": "לא הוגדר שם יוצר — ערוך את __author__ בקובץ chidon_hapax/__init__.py.",
        "fr": "Aucun auteur défini — modifiez __author__ dans "
              "chidon_hapax/__init__.py.",
        "es": "Sin autor definido — edite __author__ en chidon_hapax/__init__.py.",
        "pt": "Sem autor definido — edite __author__ em chidon_hapax/__init__.py.",
        "ru": "Автор не указан — измените __author__ в chidon_hapax/__init__.py.",
    },
    "about.thanks": {
        "en": "Built for anyone preparing for the Chidon. Good luck.",
        "he": "נבנה לכל מי שמתכונן לחידון. בהצלחה!",
        "fr": "Conçu pour celles et ceux qui préparent le Chidon. Bonne chance !",
        "es": "Hecho para quienes se preparan para el Jidón. ¡Mucha suerte!",
        "pt": "Feito para quem se prepara para o Chidon. Boa sorte!",
        "ru": "Сделано для всех, кто готовится к Хидону. Удачи!",
    },
    "btn.close": {"en": "Close", "he": "סגור", "fr": "Fermer", "es": "Cerrar",
                  "pt": "Fechar", "ru": "Закрыть"},
    "label.numbering": {
        "en": "Verse numbers:", "he": "מספור פסוקים:", "fr": "Numérotation :",
        "es": "Numeración:", "pt": "Numeração:", "ru": "Нумерация стихов:",
    },
    "numbering.wlc": {
        "en": "Leningrad Codex (this text)", "he": "כתר לנינגרד (נוסח התוכנה)",
        "fr": "Codex de Leningrad (ce texte)", "es": "Códice de Leningrado (este texto)",
        "pt": "Códice de Leninegrado (este texto)", "ru": "Ленинградский кодекс (этот текст)",
    },
    "numbering.printed": {
        "en": "Printed editions (Koren, Mamre)",
        "he": "מהדורות מודפסות (קורן, ממרא)",
        "fr": "Éditions imprimées (Koren, Mamre)",
        "es": "Ediciones impresas (Koren, Mamre)",
        "pt": "Edições impressas (Koren, Mamre)",
        "ru": "Печатные издания (Корен, Мамре)",
    },
    "tip.numbering": {
        "en": "Only four chapters are numbered differently: Exodus 20 and\n"
              "Deuteronomy 5 (the Decalogue is divided by ta'am elyon in print),\n"
              "Numbers 25 and Joshua 21. Everything else is identical, so this\n"
              "changes references only, never which words are found.",
        "he": "רק בארבעה פרקים המספור שונה: שמות כ ודברים ה (עשרת הדיברות\n"
              "מחולקות בטעם העליון בדפוס), במדבר כה ויהושע כא. כל השאר זהה,\n"
              "ולכן זה משנה רק את המראה־מקום, לא אילו מילים נמצאו.",
        "fr": "Seuls quatre chapitres sont numérotés différemment : Exode 20 et\n"
              "Deutéronome 5 (Décalogue divisé selon le ta'am elyon dans les\n"
              "éditions imprimées), Nombres 25 et Josué 21. Cela ne change que\n"
              "les références, jamais les mots trouvés.",
        "es": "Sólo cuatro capítulos se numeran distinto: Éxodo 20 y\n"
              "Deuteronomio 5 (Decálogo dividido por ta'am elyon en las ediciones\n"
              "impresas), Números 25 y Josué 21. Sólo cambian las referencias.",
        "pt": "Apenas quatro capítulos são numerados de forma diferente: Êxodo 20\n"
              "e Deuteronómio 5 (Decálogo dividido por ta'am elyon no impresso),\n"
              "Números 25 e Josué 21. Só mudam as referências.",
        "ru": "Иначе пронумерованы лишь четыре главы: Исход 20 и Второзаконие 5\n"
              "(Десятисловие делится по та'ам эльон), Числа 25 и Иисус Навин 21.\n"
              "Меняются только ссылки, а не найденные слова.",
    },
    "numbering.note": {
        "en": "References follow printed editions: the Decalogue in Exodus 20 and "
              "Deuteronomy 5 is numbered by ta'am elyon, Numbers 25:19 is counted "
              "as 26:1, and Joshua 21:36-37 (marked *) are absent from most "
              "printed editions, so the rest of that chapter runs two verses lower.",
        "he": "המראי־מקום לפי מהדורות מודפסות: עשרת הדיברות בשמות כ ובדברים ה "
              "ממוספרות בטעם העליון, במדבר כה:יט נחשב כו:א, ויהושע כא:לו-לז "
              "(מסומנים ב־*) חסרים ברוב המהדורות, ולכן המשך הפרק נמוך בשני פסוקים.",
        "fr": "Références selon les éditions imprimées : le Décalogue (Exode 20, "
              "Deutéronome 5) est numéroté selon le ta'am elyon, Nombres 25:19 "
              "compte comme 26:1, et Josué 21:36-37 (marqués *) manquent dans la "
              "plupart des éditions, d'où un décalage de deux versets ensuite.",
        "es": "Referencias según ediciones impresas: el Decálogo (Éxodo 20, "
              "Deuteronomio 5) se numera por ta'am elyon, Números 25:19 cuenta "
              "como 26:1, y Josué 21:36-37 (marcados *) faltan en la mayoría de "
              "las ediciones, por lo que el resto del capítulo baja dos versículos.",
        "pt": "Referências segundo edições impressas: o Decálogo (Êxodo 20, "
              "Deuteronómio 5) é numerado por ta'am elyon, Números 25:19 conta "
              "como 26:1, e Josué 21:36-37 (marcados *) faltam na maioria das "
              "edições, pelo que o resto do capítulo desce dois versículos.",
        "ru": "Ссылки по печатным изданиям: Десятисловие (Исход 20, Второзаконие 5) "
              "нумеруется по та'ам эльон, Числа 25:19 считается 26:1, а Иисус Навин "
              "21:36-37 (отмечены *) отсутствуют в большинстве изданий, поэтому "
              "дальше глава идёт на два стиха ниже.",
    },
    "label.scope": {
        "en": "Unique within:", "he": "ייחודי בתוך:", "fr": "Unique au sein de :",
        "es": "Único dentro de:", "pt": "Único dentro de:", "ru": "Уникально внутри:",
    },
    "scope.book": {
        "en": "Its own book", "he": "הספר שלו עצמו", "fr": "Son propre livre",
        "es": "Su propio libro", "pt": "O seu próprio livro", "ru": "Своей книги",
    },
    "scope.section": {
        "en": "A section of the Tanach", "he": "חלק מהתנ״ך",
        "fr": "Une section du Tanakh", "es": "Una sección del Tanaj",
        "pt": "Uma secção do Tanach", "ru": "Раздела Танаха",
    },
    "scope.custom": {
        "en": "A range I type below", "he": "טווח שאקליד למטה",
        "fr": "Une plage que je saisis", "es": "Un rango que escribo abajo",
        "pt": "Um intervalo que eu escrevo", "ru": "Указанного ниже диапазона",
    },
    "ph.scopeCustom": {
        "en": "e.g. ישעיהו א-לט   or   שמואל א; שמואל ב",
        "he": "למשל ישעיהו א-לט   או   שמואל א; שמואל ב",
        "fr": "ex. ישעיהו א-לט   ou   שמואל א; שמואל ב",
        "es": "p. ej. ישעיהו א-לט   o   שמואל א; שמואל ב",
        "pt": "ex. ישעיהו א-לט   ou   שמואל א; שמואל ב",
        "ru": "напр. ישעיהו א-לט   или   שמואל א; שמואל ב",
    },
    "tip.scope": {
        "en": "What the word or phrase has to be unique in. “Its own book”\n"
              "reports a word that occurs once in the book it appears in, so a\n"
              "syllabus spanning several books gets a separate answer for each.",
        "he": "בתוך מה המילה או הצירוף צריכים להיות ייחודיים. „הספר שלו עצמו”\n"
              "מחזיר מילה המופיעה פעם אחת בספר שבו היא נמצאת, כך שחומר\n"
              "המשתרע על כמה ספרים מקבל תשובה נפרדת לכל ספר.",
        "fr": "Ce à l'intérieur de quoi le mot doit être unique. « Son propre\n"
              "livre » donne un mot n'apparaissant qu'une fois dans le livre où\n"
              "il se trouve, séparément pour chaque livre du programme.",
        "es": "Dentro de qué debe ser único. «Su propio libro» da una palabra que\n"
              "aparece una vez en el libro en que se encuentra, por separado\n"
              "para cada libro del temario.",
        "pt": "Dentro de quê deve ser único. “O seu próprio livro” dá uma palavra\n"
              "que ocorre uma vez no livro em que aparece, separadamente para\n"
              "cada livro do programa.",
        "ru": "Внутри чего слово должно быть уникальным. «Своей книги» — слово,\n"
              "встречающееся один раз в той книге, где оно стоит, отдельно для\n"
              "каждой книги материала.",
    },
    "err.scopeEmpty": {
        "en": "The range to search in is empty or unreadable.",
        "he": "הטווח לחיפוש ריק או בלתי קריא.",
        "fr": "La plage de recherche est vide ou illisible.",
        "es": "El rango de búsqueda está vacío o no se puede leer.",
        "pt": "O intervalo de pesquisa está vazio ou ilegível.",
        "ru": "Диапазон поиска пуст или не читается.",
    },
    "col.scope": {
        "en": "In scope", "he": "בתחום", "fr": "Dans la portée",
        "es": "En el ámbito", "pt": "No âmbito", "ru": "В области",
    },
    "err.scopeNoOverlap": {
        "en": "None of the syllabus lies inside “{scope}”, so there is nothing "
              "to find. Pick a scope the material is part of.",
        "he": "אף חלק מחומר הבחינה אינו בתוך „{scope}”, ולכן אין מה למצוא. "
              "יש לבחור תחום שהחומר נמצא בתוכו.",
        "fr": "Aucune partie du programme ne se trouve dans « {scope} » ; il n'y "
              "a donc rien à trouver. Choisissez une portée qui contient le "
              "programme.",
        "es": "Ninguna parte del temario está dentro de «{scope}», así que no hay "
              "nada que encontrar. Elija un ámbito que contenga el material.",
        "pt": "Nenhuma parte do programa está dentro de “{scope}”, por isso não há "
              "nada a encontrar. Escolha um âmbito que contenha o material.",
        "ru": "Материал не входит в «{scope}», поэтому искать нечего. Выберите "
              "область, которая включает материал.",
    },
    "opt.scopeInSyllabus": {
        "en": "…but only the part of it that is in my syllabus",
        "he": "…אך רק החלק שנמצא בחומר הבחינה שלי",
        "fr": "…mais seulement la partie qui figure dans mon programme",
        "es": "…pero solo la parte que está en mi temario",
        "pt": "…mas apenas a parte que está no meu programa",
        "ru": "…но только ту часть, которая входит в мой материал",
    },
    "tip.scopeInSyllabus": {
        "en": "Off: a word must occur once in the whole book or section, even in\n"
              "chapters you did not list — stricter, fewer results.\n"
              "On: only the listed chapters are counted, so a word may well occur\n"
              "again in a chapter outside your material.\n"
              "Either way, every result is a verse inside your syllabus.",
        "he": "כבוי: המילה צריכה להופיע פעם אחת בכל הספר או החלק, גם בפרקים\n"
              "שלא נכללו — מחמיר יותר, פחות תוצאות.\n"
              "דלוק: נספרים רק הפרקים שנכללו, ולכן המילה עשויה להופיע שוב\n"
              "בפרק שמחוץ לחומר.\n"
              "בכל מקרה, כל תוצאה נמצאת בתוך חומר הבחינה.",
        "fr": "Désactivé : le mot doit apparaître une fois dans tout le livre ou\n"
              "la section, même dans les chapitres non listés — plus strict.\n"
              "Activé : seuls les chapitres listés sont comptés.\n"
              "Dans les deux cas, chaque résultat est dans votre programme.",
        "es": "Desactivado: la palabra debe aparecer una vez en todo el libro o\n"
              "sección, incluso en capítulos no listados — más estricto.\n"
              "Activado: solo se cuentan los capítulos listados.\n"
              "En ambos casos, cada resultado está dentro de su temario.",
        "pt": "Desligado: a palavra deve ocorrer uma vez em todo o livro ou secção,\n"
              "mesmo em capítulos não listados — mais estrito.\n"
              "Ligado: apenas os capítulos listados são contados.\n"
              "Em ambos os casos, cada resultado está dentro do seu programa.",
        "ru": "Выкл.: слово должно встречаться один раз во всей книге или разделе,\n"
              "включая неуказанные главы — строже, меньше результатов.\n"
              "Вкл.: считаются только указанные главы.\n"
              "В обоих случаях каждый результат находится внутри материала.",
    },
    "help.title": {
        "en": "How to use this program", "he": "כיצד להשתמש בתוכנה",
        "fr": "Comment utiliser ce programme", "es": "Cómo usar este programa",
        "pt": "Como usar este programa", "ru": "Как пользоваться программой",
    },
    "help.button": {
        "en": "How it works", "he": "כיצד זה עובד", "fr": "Mode d'emploi",
        "es": "Cómo funciona", "pt": "Como funciona", "ru": "Как это работает",
    },
    "help.close": {
        "en": "Close", "he": "סגור", "fr": "Fermer", "es": "Cerrar",
        "pt": "Fechar", "ru": "Закрыть",
    },
    "help.again": {
        "en": "Show this when the program starts",
        "he": "הצג זאת עם פתיחת התוכנה",
        "fr": "Afficher au démarrage du programme",
        "es": "Mostrar esto al iniciar el programa",
        "pt": "Mostrar isto ao iniciar o programa",
        "ru": "Показывать при запуске программы",
    },
    "opt.wholeTanach": {
        "en": "Whole Tanach", "he": "כל התנ״ך", "fr": "Tout le Tanakh",
        "es": "Todo el Tanaj", "pt": "Todo o Tanach", "ru": "Весь Танах",
    },
    "tip.wholeTanach": {
        "en": "Fill the syllabus with all 39 books — 23,213 verses. Searching "
              "the whole Tanach takes a few seconds longer than a normal "
              "syllabus. Unticking restores what you had typed.",
        "he": "ממלא את חומר הבחינה בכל 39 הספרים — 23,213 פסוקים. חיפוש בכל "
              "התנ״ך אורך כמה שניות יותר מחומר רגיל. ביטול הסימון מחזיר את מה "
              "שהוקלד קודם.",
        "fr": "Remplit le programme avec les 39 livres — 23 213 versets. La "
              "recherche sur tout le Tanakh prend quelques secondes de plus. "
              "Décocher rétablit ce que vous aviez saisi.",
        "es": "Rellena el temario con los 39 libros — 23.213 versículos. Buscar "
              "en todo el Tanaj tarda unos segundos más. Al desmarcar se "
              "recupera lo que había escrito.",
        "pt": "Preenche o programa com os 39 livros — 23 213 versículos. "
              "Pesquisar todo o Tanach demora alguns segundos mais. Desmarcar "
              "repõe o que tinha escrito.",
        "ru": "Заполняет материал всеми 39 книгами — 23 213 стихов. Поиск по "
              "всему Танаху занимает на несколько секунд больше. Снятие флажка "
              "возвращает то, что было введено.",
    },
    # ------------------------------------------------- the exported report
    "pdf.title": {
        "en": "Unique words and phrases — Hapax legomena",
        "he": "מילים וצירופים ייחודיים — Hapax legomena",
        "fr": "Mots et expressions uniques — Hapax legomena",
        "es": "Palabras y expresiones únicas — Hapax legomena",
        "pt": "Palavras e expressões únicas — Hapax legomena",
        "ru": "Уникальные слова и выражения — Hapax legomena",
    },
    "pdf.syllabus": {"en": "Syllabus", "he": "חומר הבחינה", "fr": "Programme",
                     "es": "Temario", "pt": "Programa", "ru": "Материал"},
    "pdf.setting": {"en": "Setting", "he": "הגדרות", "fr": "Réglage",
                    "es": "Ajuste", "pt": "Definição", "ru": "Настройка"},
    "pdf.value": {"en": "Value", "he": "ערך", "fr": "Valeur", "es": "Valor",
                  "pt": "Valor", "ru": "Значение"},
    "pdf.uniqueness": {"en": "Unique within", "he": "ייחודיות",
                       "fr": "Unique au sein de", "es": "Único dentro de",
                       "pt": "Único dentro de", "ru": "Уникально внутри"},
    "pdf.compareBy": {"en": "Compare by", "he": "השוואה לפי",
                      "fr": "Comparer par", "es": "Comparar por",
                      "pt": "Comparar por", "ru": "Сравнивать по"},
    "pdf.lengths": {"en": "Phrase lengths", "he": "אורך הצירוף",
                    "fr": "Longueurs", "es": "Longitudes",
                    "pt": "Comprimentos", "ru": "Длина сочетаний"},
    "pdf.minimalOnly": {"en": "Minimal phrases only",
                        "he": "צירופים מינימליים בלבד",
                        "fr": "Expressions minimales seulement",
                        "es": "Solo expresiones mínimas",
                        "pt": "Apenas expressões mínimas",
                        "ru": "Только минимальные выражения"},
    "pdf.crossVerses": {"en": "Across verse boundaries", "he": "מעבר בין פסוקים",
                        "fr": "À travers les versets",
                        "es": "A través de versículos",
                        "pt": "Através dos versículos",
                        "ru": "Через границы стихов"},
    "pdf.extent": {"en": "Extent", "he": "היקף", "fr": "Étendue",
                   "es": "Extensión", "pt": "Extensão", "ru": "Объём"},
    "pdf.numbering": {"en": "Verse numbers", "he": "מספור פסוקים",
                      "fr": "Numérotation", "es": "Numeración",
                      "pt": "Numeração", "ru": "Нумерация стихов"},
    "pdf.freqFloor": {"en": "Frequency floor per word",
                      "he": "סף שכיחות לכל מילה",
                      "fr": "Seuil de fréquence par mot",
                      "es": "Umbral de frecuencia por palabra",
                      "pt": "Limiar de frequência por palavra",
                      "ru": "Порог частоты для слова"},
    "pdf.inTanach": {"en": "in the Tanach", "he": "בתנ״ך",
                     "fr": "dans le Tanakh", "es": "en el Tanaj",
                     "pt": "no Tanach", "ru": "в Танахе"},
    "pdf.yes": {"en": "yes", "he": "כן", "fr": "oui", "es": "sí", "pt": "sim",
                "ru": "да"},
    "pdf.no": {"en": "no", "he": "לא", "fr": "non", "es": "no", "pt": "não",
               "ru": "нет"},
    "pdf.allowed": {"en": "allowed", "he": "מותר", "fr": "autorisé",
                    "es": "permitido", "pt": "permitido", "ru": "разрешено"},
    "pdf.summary": {"en": "Summary", "he": "סיכום", "fr": "Résumé",
                    "es": "Resumen", "pt": "Resumo", "ru": "Сводка"},
    "pdf.length": {"en": "Length", "he": "אורך", "fr": "Longueur",
                   "es": "Longitud", "pt": "Comprimento", "ru": "Длина"},
    "pdf.findings": {"en": "Findings", "he": "מספר ממצאים",
                     "fr": "Résultats", "es": "Resultados",
                     "pt": "Resultados", "ru": "Найдено"},
    "pdf.total": {"en": "Total", "he": "סה״כ", "fr": "Total", "es": "Total",
                  "pt": "Total", "ru": "Всего"},
    "pdf.byBook": {"en": "By book", "he": "לפי ספר", "fr": "Par livre",
                   "es": "Por libro", "pt": "Por livro", "ru": "По книгам"},
    "pdf.book": {"en": "Book", "he": "ספר", "fr": "Livre", "es": "Libro",
                 "pt": "Livro", "ru": "Книга"},
    "pdf.chapters": {"en": "chapters", "he": "פרקים", "fr": "chapitres",
                     "es": "capítulos", "pt": "capítulos", "ru": "глав"},
    "pdf.verses": {"en": "verses", "he": "פסוקים", "fr": "versets",
                   "es": "versículos", "pt": "versículos", "ru": "стихов"},
    "pdf.words": {"en": "words", "he": "מילים", "fr": "mots",
                  "es": "palabras", "pt": "palavras", "ru": "слов"},
    "pdf.minimalNote": {
        "en": "A phrase counts as <b>minimal</b> when it is unique while each "
              "of its sub-phrases (one word shorter) is not — the shortest "
              "run at this spot that identifies the place unambiguously.",
        "he": "צירוף נחשב <b>מינימלי</b> כאשר הוא עצמו ייחודי, אך כל אחד "
              "מתת־הצירופים שלו (באורך פחות אחד) אינו ייחודי — כלומר זהו הקטע "
              "הקצר ביותר במקום הזה שמזהה את המיקום באופן חד־משמעי.",
        "fr": "Une expression est <b>minimale</b> lorsqu'elle est unique alors "
              "qu'aucune de ses sous-expressions (un mot de moins) ne l'est — "
              "la plus courte suite qui identifie l'endroit sans ambiguïté.",
        "es": "Una expresión es <b>mínima</b> cuando es única mientras que "
              "ninguna de sus sub-expresiones (una palabra menos) lo es — la "
              "sucesión más corta que identifica el lugar sin ambigüedad.",
        "pt": "Uma expressão é <b>mínima</b> quando é única embora nenhuma das "
              "suas subexpressões (menos uma palavra) o seja — a sequência "
              "mais curta que identifica o lugar sem ambiguidade.",
        "ru": "Выражение считается <b>минимальным</b>, когда оно уникально, а "
              "каждое из его подвыражений (на одно слово короче) — нет: самая "
              "короткая цепочка, однозначно указывающая на это место.",
    },
    "pdf.generated": {"en": "Generated {date}", "he": "נוצר ב־{date}",
                      "fr": "Généré le {date}", "es": "Generado el {date}",
                      "pt": "Gerado em {date}", "ru": "Создано {date}"},
    "pdf.source": {"en": "Text", "he": "נוסח המקרא", "fr": "Texte",
                   "es": "Texto", "pt": "Texto", "ru": "Текст"},
}
