"""The in-app guide, for people who never see the README.

Each language maps to a list of (heading, body) pairs. Bodies may contain the
few HTML tags the dialog renders: <b>, <i>, <br>, <ul>, <li>, <code>.
"""

from __future__ import annotations

GUIDE: dict[str, list[tuple[str, str]]] = {

    # ------------------------------------------------------------ English
    "en": [
        ("In one sentence",
         "You type the material you are learning; the app tells you which "
         "words and phrases in it appear <b>only once</b>, and hands you a PDF "
         "you can study from or hand out."),
        ("Three steps",
         "<ul>"
         "<li><b>1.</b> Type or paste your syllabus into the text box at the top "
         "left — or pick a book and chapters below it and press "
         "<b>Add</b>.</li>"
         "<li><b>2.</b> Press <b>Find hapaxes</b>. A few seconds, even for a "
         "whole year's material.</li>"
         "<li><b>3.</b> Press <b>Save PDF…</b>.</li>"
         "</ul>"
         "Everything in between is optional."),
        ("Writing the syllabus",
         "Write it the way the official sheet is printed, and it will be "
         "understood: <code>יהושע: א-יב</code>, <code>שמואל א: א-טו; יז-כ</code>, "
         "<code>ישעיהו א-לט</code>. Hebrew letters or digits both work, as do "
         "the usual abbreviations (<code>שמו״א</code>, <code>דהי״ב</code>). One "
         "book per line. A whole book needs no chapter numbers at all.<br>"
         "Under the box you will see <b>how many chapters, verses and words</b> "
         "were understood — check it against your sheet. If a line is unreadable or "
         "a book name is not recognised, a warning appears just underneath "
         "naming the line: nothing is dropped without telling you."),
        ("Unique within what?",
         "The most important setting. A word can be unique in one span of text "
         "and ordinary in another:"
         "<ul>"
         "<li><b>The whole Tanach</b> — a true hapax legomenon, once in all "
         "305,531 words. This is what the Chidon usually asks about.</li>"
         "<li><b>The syllabus</b> — once in what you typed, even if the word is "
         "common elsewhere.</li>"
         "<li><b>Its own book</b> — once in the book it sits in. If your syllabus "
         "spans several books you get a separate answer for each: the words "
         "unique within Jonah, then those unique within Amos.</li>"
         "<li><b>A section</b> — Torah, Nevi'im, Nevi'im Rishonim, Nevi'im "
         "Acharonim, Trei Asar, Ketuvim, Sifrei Emet, the Five Megillot.</li>"
         "<li><b>A range you type</b> — written like the syllabus, for example "
         "<code>ישעיהו א-לט</code>.</li>"
         "</ul>"),
        ("…the whole book, or only my part of it?",
         "The checkbox under the <b>Unique within</b> menu decides whether chapters "
         "you did <i>not</i> list are counted.<br>"
         "Say your material is ישעיהו א-לט. <b>Unchecked</b>, a word must occur "
         "once in all 66 chapters — one that returns in chapter 50 is rejected "
         "even though you are not studying it. <b>Checked</b>, only chapters "
         "1-39 count, and that word is reported.<br>"
         "Either way, <b>every result is a verse inside your syllabus</b>. This "
         "setting only removes results; it never sends you elsewhere."),
        ("Phrases, not just words",
         "Tick the lengths 1 to 5: the program looks for a single word just as "
         "readily as a run of two, three, four or five consecutive words.<br>"
         "Leave <b>minimal phrases only</b> on. Without it almost every long "
         "phrase is trivially unique — if a word is already unique, so is every "
         "phrase containing it, and you would drown in them. Minimal keeps only "
         "phrases that are unique while their shorter parts are <i>not</i>, "
         "which is where the interesting ones live.<br>"
         "<b>Each word occurs ≥ N</b> keeps only phrases whose words are <i>all</i> "
         "common: at 50, every word in the phrase appears at least 50 times in "
         "the Tanach. The phrase is then the surprising thing rather than its "
         "vocabulary — often the best questions."),
        ("Compare by",
         "What counts as \"the same word\":"
         "<ul>"
         "<li><b>Written form</b> (default) — letters only, nikkud ignored.</li>"
         "<li><b>With nikkud</b> — stricter; two spellings that differ only in "
         "vowels count as different words.</li>"
         "<li><b>Root</b> — every form of one root counts as a single word, so this "
         "finds unique <i>roots</i> rather than unique spellings. Far rarer, "
         "and far harder.</li>"
         "</ul>"),
        ("The report",
         "The PDF opens with a title page listing your settings and the totals per "
         "book, then the findings grouped by chapter in newspaper columns. "
         "Optional extras: the <b>full verse</b> under each entry with the word "
         "in bold, an <b>alphabetical index</b>, and a <b>practice sheet</b> "
         "with a separate answer key for testing yourself or a friend.<br>"
         "<b>Save HTML</b> and <b>Save CSV</b> are there too — CSV opens in Excel, "
         "and lends itself to other uses if you want to reuse the results in "
         "another program."),
        ("Verse numbers",
         "Printed editions and the Leningrad manuscript number a handful of "
         "chapters differently — the Ten Commandments above all. Choose "
         "<b>Printed editions</b> to match a Koren or Mikraot Gedolot in your "
         "hand, or <b>Leningrad</b> to match most software. It changes only the "
         "references that are printed, never which words are found."),
        ("The Root search tab",
         "Not to be confused with the <b>Compare by → Root</b> setting, which "
         "changes the search itself. This tab is a dictionary: type a word and "
         "it shows you where that root occurs, without re-running anything. "
         "Useful for checking a hunch about one particular word."),
        ("Where the text comes from",
         "The Westminster Leningrad Codex, via the Open Scriptures Hebrew "
         "Bible project — 39 books, 23,213 verses, 305,531 words, with nikkud "
         "and te'amim. It lives inside the app; nothing is downloaded and "
         "nothing you type ever leaves your computer.<br>"
         "The app is free software under the GPL, and the Tanach text stays "
         "under its own CC-BY licence. The PDFs you make are yours."),
    ],

    # ------------------------------------------------------------- Hebrew
    "he": [
        ("במשפט אחד",
         "מקלידים את החומר שלומדים, והתוכנה מראה אילו מילים וצירופים בו "
         "מופיעים <b>פעם אחת בלבד</b>, ומפיקה קובץ PDF ללימוד או לחלוקה."),
        ("שלושה צעדים",
         "<ul>"
         "<li><b>1.</b> מקלידים או מדביקים את חומר הבחינה בתיבת הטקסט שבצד ימין "
         "למעלה — או בוחרים ספר ופרקים ולוחצים <b>הוסף</b>.</li>"
         "<li><b>2.</b> לוחצים <b>מצא מילים ייחודיות</b>. כמה שניות, גם לחומר "
         "של שנה שלמה.</li>"
         "<li><b>3.</b> לוחצים <b>שמור PDF…</b>.</li>"
         "</ul>"
         "כל השאר הוא רשות."),
        ("כתיבת חומר הבחינה",
         "כותבים כפי שמודפס בדף הרשמי, והתוכנה תבין: <code>יהושע: א-יב</code>, "
         "<code>שמואל א: א-טו; יז-כ</code>, <code>ישעיהו א-לט</code>. אפשר "
         "אותיות או ספרות, וגם קיצורים (<code>שמו״א</code>, "
         "<code>דהי״ב</code>). ספר אחד בכל שורה. ספר שלם אינו דורש מספרי "
         "פרקים כלל.<br>"
         "מתחת לתיבה מופיע <b>כמה פרקים, פסוקים ומילים</b> נקלטו — כדאי להשוות "
         "לדף. אם שורה אינה קריאה או ששם ספר אינו מזוהה, מופיעה מיד מתחת "
         "אזהרה המציינת את השורה: שום דבר אינו מושמט בלי להודיע."),
        ("ייחודי בתוך מה?",
         "ההגדרה החשובה ביותר. מילה יכולה להיות ייחודית בקטע אחד ורגילה באחר:"
         "<ul>"
         "<li><b>כל התנ״ך</b> — הפקס לגומנון האמיתי, פעם אחת מתוך 305,531 "
         "מילים. זה מה שנשאל בדרך כלל בחידון.</li>"
         "<li><b>חומר הבחינה</b> — פעם אחת במה שהוקלד, גם אם המילה שכיחה במקום "
         "אחר.</li>"
         "<li><b>הספר שלו עצמו</b> — פעם אחת בספר שבו היא נמצאת. בחומר המשתרע "
         "על כמה ספרים מתקבלת תשובה נפרדת לכל ספר: המילים הייחודיות ביונה, "
         "ואחריהן הייחודיות בעמוס.</li>"
         "<li><b>חלק מהתנ״ך</b> — תורה, נביאים, נביאים ראשונים, נביאים "
         "אחרונים, תרי עשר, כתובים, ספרי אמ״ת, חמש מגילות.</li>"
         "<li><b>טווח שמקלידים</b> — נכתב כמו חומר הבחינה, למשל "
         "<code>ישעיהו א-לט</code>.</li>"
         "</ul>"),
        ("…כל הספר, או רק החלק שלי?",
         "תיבת הסימון שמתחת לתפריט <b>ייחודי בתוך</b> קובעת אם נספרים פרקים שלא "
         "נכללו.<br>"
         "נניח שהחומר הוא ישעיהו א-לט. <b>ללא סימון</b>, המילה צריכה להופיע "
         "פעם אחת בכל 66 הפרקים — מילה שחוזרת בפרק נ נפסלת אף שאינה נלמדת. "
         "<b>עם סימון</b>, נספרים רק פרקים א-לט, ואותה מילה תדווח.<br>"
         "בכל מקרה, <b>כל תוצאה נמצאת בתוך חומר הבחינה</b>. ההגדרה רק מסננת "
         "תוצאות; היא לעולם אינה מפנה למקום אחר."),
        ("צירופים, לא רק מילים",
         "מסמנים אורכים 1 עד 5: התוכנה מחפשת גם מילה בודדת וגם רצף של שתיים, "
         "שלוש, ארבע או חמש מילים רצופות.<br>"
         "מומלץ להשאיר <b>צירופים מינימליים בלבד</b>. בלעדיו כמעט כל צירוף ארוך "
         "ייחודי באופן חסר עניין — אם מילה ייחודית, גם כל צירוף המכיל אותה. "
         "האפשרות משאירה רק צירופים ייחודיים שחלקיהם הקצרים <i>אינם</i> "
         "ייחודיים, ושם נמצאים המעניינים.<br>"
         "<b>כל מילה מופיעה ≥ N</b> משאיר רק צירופים שכל מילותיהם שכיחות: ב-50, "
         "כל מילה בצירוף מופיעה לפחות חמישים פעם בתנ״ך. כך הצירוף עצמו הוא "
         "המפתיע ולא אוצר המילים — לרוב השאלות היפות ביותר."),
        ("השוואה לפי",
         "מה נחשב „אותה מילה”:"
         "<ul>"
         "<li><b>כתיב</b> (ברירת מחדל) — אותיות בלבד, ללא ניקוד.</li>"
         "<li><b>עם ניקוד</b> — מחמיר יותר; שתי צורות הנבדלות בניקוד בלבד "
         "נחשבות שונות.</li>"
         "<li><b>שורש</b> — כל נטיות אותו שורש נחשבות למילה אחת, ולכן מתקבלים "
         "<i>שורשים</i> ייחודיים ולא כתיבים ייחודיים. נדיר הרבה יותר וקשה "
         "הרבה יותר.</li>"
         "</ul>"),
        ("הדוח",
         "ה-PDF נפתח בעמוד שער ובו ההגדרות וסיכום לכל ספר, ואחריו הממצאים מסודרים "
         "לפי פרקים בטורים. תוספות לבחירה: <b>הפסוק המלא</b> תחת כל ערך "
         "כשהמילה מודגשת, <b>מפתח אלפביתי</b>, ו<b>דף תרגול</b> עם דף תשובות "
         "נפרד לבחינה עצמית או לחבר.<br>"
         "קיימות גם <b>שמירת HTML</b> ו<b>שמירת CSV</b> — קובץ CSV נפתח באקסל "
         "ומתאים גם לשימושים אחרים, אם רוצים להשתמש בתוצאות בתוכנה אחרת."),
        ("מספור הפסוקים",
         "המהדורות המודפסות וכתב יד לנינגרד ממספרים כמה פרקים אחרת — בעיקר "
         "עשרת הדיברות. בוחרים <b>מהדורות מודפסות</b> כדי להתאים לקורן או "
         "למקראות גדולות שביד, או <b>לנינגרד</b> כדי להתאים לרוב התוכנות. "
         "משפיע רק על המראי מקום, לא על התוצאות."),
        ("לשונית חיפוש שורשים",
         "אין לבלבל עם ההגדרה <b>השוואה לפי → שורש</b>, המשנה את החיפוש עצמו. "
         "הלשונית הזו היא מילון: מקלידים מילה ורואים היכן מופיע השורש שלה, בלי "
         "להריץ מחדש דבר. נוח לבדיקת השערה על מילה מסוימת."),
        ("מקור הנוסח",
         "כתב יד לנינגרד (WLC) מתוך מיזם Open Scriptures — 39 ספרים, "
         "23,213 פסוקים, 305,531 מילים, עם ניקוד וטעמים. הנוסח נמצא בתוך "
         "התוכנה; שום דבר אינו יורד מהרשת ושום דבר שמקלידים אינו יוצא מהמחשב.<br>"
         "התוכנה חופשית תחת רישיון GPL, ונוסח התנ״ך נשאר תחת רישיון CC-BY שלו. "
         "קובצי ה-PDF שיוצרים שייכים לך."),
    ],

    # ------------------------------------------------------------- French
    "fr": [
        ("En une phrase",
         "Vous saisissez le programme que vous étudiez ; l'application vous "
         "indique quels mots et expressions n'y apparaissent <b>qu'une seule "
         "fois</b>, et produit un PDF à étudier ou à distribuer."),
        ("Trois étapes",
         "<ul>"
         "<li><b>1.</b> Saisissez ou collez le programme dans la zone de texte "
         "en haut à gauche — ou choisissez un livre et des chapitres puis "
         "<b>Ajouter</b>.</li>"
         "<li><b>2.</b> Cliquez sur <b>Trouver les hapax</b>. Quelques secondes, "
         "même pour toute une année.</li>"
         "<li><b>3.</b> Cliquez sur <b>Enregistrer le PDF…</b>.</li>"
         "</ul>"
         "Tout le reste est facultatif."),
        ("Écrire le programme",
         "Écrivez-le comme il est imprimé sur la feuille officielle : "
         "<code>יהושע: א-יב</code>, <code>שמואל א: א-טו; יז-כ</code>. Lettres "
         "hébraïques ou chiffres, abréviations usuelles comprises. Un livre par "
         "ligne ; un livre entier ne demande aucun numéro de chapitre.<br>"
         "Sous la zone s'affiche le <b>nombre de chapitres, versets et mots</b> "
         "reconnus — comparez-le à votre feuille. Si une ligne est illisible ou "
         "si un nom de livre n'est pas reconnu, un avertissement apparaît juste "
         "en dessous en indiquant la ligne en cause : rien n'est laissé de côté "
         "sans vous le dire."),
        ("Unique au sein de quoi ?",
         "Le réglage le plus important. Un mot peut être unique dans un passage "
         "et banal dans un autre :"
         "<ul>"
         "<li><b>Tout le Tanakh</b> — le véritable hapax, une fois sur 305 531 "
         "mots. C'est ce que demande le Chidon.</li>"
         "<li><b>Le programme</b> — une fois dans ce que vous avez saisi, même "
         "si le mot est courant ailleurs.</li>"
         "<li><b>Son propre livre</b> — une fois dans le livre où il se trouve. "
         "Si votre programme couvre plusieurs livres, vous obtenez une réponse "
         "distincte pour chacun : les mots uniques dans Yona, puis ceux uniques "
         "dans Amos.</li>"
         "<li><b>Une section</b> — Torah (Pentateuque), Nevi'im, Nevi'im Rishonim, "
         "Nevi'im Acharonim, Trei Asar, Ketouvim, Sifrei Emet, Cinq "
         "Meguilot.</li>"
         "<li><b>Une plage que vous saisissez</b> — écrite comme le programme, "
         "par exemple <code>ישעיהו א-לט</code>.</li>"
         "</ul>"),
        ("…tout le livre, ou seulement ma partie ?",
         "La case à cocher sous le menu « Unique au sein de » décide si les "
         "chapitres que vous n'avez pas listés sont comptés.<br>"
         "Programme ישעיהו א-לט : <b>décochée</b>, le mot doit apparaître une "
         "fois dans les 66 chapitres — un mot qui revient au chapitre 50 est "
         "rejeté. <b>Cochée</b>, seuls les chapitres 1-39 comptent, et ce mot "
         "est retenu.<br>"
         "Dans les deux cas, <b>chaque résultat est un verset de votre "
         "programme</b>. Ce réglage ne fait que retirer des résultats."),
        ("Expressions, pas seulement des mots",
         "Cochez les longueurs 1 à 5 : l'application cherche aussi bien un mot "
         "isolé qu'une suite de deux, trois, quatre ou cinq mots consécutifs.<br>"
         "Laissez <b>expressions minimales seulement</b> activé. Sans cela, "
         "presque toute longue expression est trivialement unique : si un mot "
         "est déjà unique, toute expression qui le contient l'est aussi. "
         "L'option ne garde que les expressions uniques dont les parties plus "
         "courtes ne le sont <i>pas</i>.<br>"
         "<b>Chaque mot apparaît ≥ N</b> ne garde que les expressions dont "
         "<i>tous</i> les mots sont fréquents : avec 50, chaque mot de "
         "l'expression apparaît au moins 50 fois dans le Tanakh. C'est "
         "l'expression qui est alors surprenante, et non le vocabulaire — "
         "souvent les plus belles questions."),
        ("Comparer par",
         "Ce qui compte comme « le même mot » :"
         "<ul>"
         "<li><b>Forme écrite</b> (défaut) — lettres seules, sans voyelles.</li>"
         "<li><b>Avec voyelles</b> — plus strict.</li>"
         "<li><b>Racine</b> — toutes les formes d'une même racine comptent pour "
         "un seul mot. Cherche donc les <i>racines</i> uniques, et non les "
         "formes : bien plus rare, et bien plus difficile.</li>"
         "</ul>"),
        ("Le rapport",
         "Le PDF s'ouvre sur une page de garde rappelant vos réglages et les "
         "totaux par livre, puis les résultats groupés par chapitre en colonnes. En "
         "option : le <b>verset entier</b> sous chaque entrée avec le mot en "
         "gras, un <b>index alphabétique</b> et une <b>feuille d'exercices</b> "
         "avec corrigé séparé.<br>"
         "<b>HTML</b> et <b>CSV</b> sont également proposés ; le CSV s'ouvre "
         "dans Excel et se prête à d'autres usages, par exemple si vous voulez "
         "réutiliser les résultats dans un autre programme."),
        ("Numérotation des versets",
         "Les éditions imprimées et le manuscrit de Léningrad numérotent "
         "quelques chapitres différemment — surtout le Décalogue. Choisissez "
         "<b>Éditions imprimées</b> pour suivre un Koren, ou <b>Léningrad</b> "
         "pour suivre la plupart des logiciels. Cela ne change que les "
         "références, jamais les résultats."),
        ("L'onglet Recherche de racine",
         "À ne pas confondre avec le réglage « Comparer par → Racine », qui "
         "concerne la recherche elle-même. Cet onglet-ci est un dictionnaire : "
         "vous tapez un mot et il vous montre où cette racine apparaît, sans "
         "relancer la recherche. Pratique pour vérifier une intuition sur un "
         "mot précis."),
        ("D'où vient le texte",
         "Le Codex de Léningrad (WLC), via Open Scriptures Hebrew Bible — 39 "
         "livres, 23 213 versets, 305 531 mots, avec voyelles et cantillation. "
         "Le texte est inclus dans l'application ; rien n'est téléchargé et rien "
         "de ce que vous saisissez ne quitte votre ordinateur.<br>"
         "Logiciel libre sous licence GPL ; le texte du Tanakh reste sous sa "
         "licence CC-BY. Les PDF que vous produisez vous appartiennent."),
    ],

    # ------------------------------------------------------------ Spanish
    "es": [
        ("En una frase",
         "Escriba el material que estudia y la aplicación le dirá qué palabras "
         "y expresiones aparecen <b>una sola vez</b>, y le entregará un PDF "
         "para estudiar o repartir."),
        ("Tres pasos",
         "<ul>"
         "<li><b>1.</b> Escriba o pegue el temario en el cuadro de texto arriba a "
         "la izquierda — o elija un libro y capítulos y pulse "
         "<b>Añadir</b>.</li>"
         "<li><b>2.</b> Pulse <b>Buscar hápax</b>. Unos segundos, incluso para "
         "el material de todo un año.</li>"
         "<li><b>3.</b> Pulse <b>Guardar PDF…</b>.</li>"
         "</ul>"
         "Todo lo demás es opcional."),
        ("Escribir el temario",
         "Escríbalo como aparece impreso en la hoja oficial: "
         "<code>יהושע: א-יב</code>, <code>שמואל א: א-טו; יז-כ</code>. Letras "
         "hebreas o cifras, y las abreviaturas habituales. Un libro por línea; "
         "un libro entero no necesita números de capítulo.<br>"
         "Debajo del cuadro verá <b>cuántos capítulos, versículos y palabras</b> "
         "se han entendido — compárelo con su hoja. Si una línea es ilegible o no "
         "se reconoce el nombre de un libro, aparece un aviso justo debajo "
         "indicando la línea: nada se descarta sin decírselo."),
        ("¿Único dentro de qué?",
         "El ajuste más importante. Una palabra puede ser única en un pasaje y "
         "corriente en otro:"
         "<ul>"
         "<li><b>Todo el Tanaj</b> — el hápax verdadero, una vez entre 305.531 "
         "palabras. Es lo que suele preguntar el Jidón.</li>"
         "<li><b>El temario</b> — una vez en lo que ha escrito, aunque la palabra "
         "sea común en otro sitio.</li>"
         "<li><b>Su propio libro</b> — una vez en el libro donde está. Si su "
         "temario abarca varios libros obtiene una respuesta distinta para "
         "cada uno: las palabras únicas en Jonás, luego las únicas en "
         "Amós.</li>"
         "<li><b>Una sección</b> — Torá (Pentateuco), Nevi'im, Nevi'im "
         "Rishonim, Nevi'im Acharonim, Trei Asar, Ketuvim, Sifrei Emet, los "
         "Cinco Meguilot.</li>"
         "<li><b>Un rango que usted escribe</b> — escrito como el temario, por "
         "ejemplo <code>ישעיהו א-לט</code>.</li>"
         "</ul>"),
        ("…¿todo el libro o solo mi parte?",
         "La casilla bajo el menú <b>Único dentro de</b> decide si se cuentan los "
         "capítulos que no ha listado.<br>"
         "Con ישעיהו א-לט: <b>sin marcar</b>, la palabra debe aparecer una vez "
         "en los 66 capítulos — una que reaparece en el capítulo 50 se rechaza. "
         "<b>Marcada</b>, solo cuentan los capítulos 1-39 y esa palabra sí "
         "aparece.<br>"
         "En ambos casos, <b>cada resultado es un versículo de su temario</b>."),
        ("Expresiones, no solo palabras",
         "Marque las longitudes 1 a 5: el programa busca tanto una palabra suelta "
         "como una sucesión de dos, tres, cuatro o cinco palabras "
         "consecutivas.<br>"
         "Deje activado <b>solo expresiones mínimas</b>. Sin ello casi toda "
         "expresión larga es únicamente trivial: si una palabra ya es única, "
         "también lo es cualquier expresión que la contenga. La opción conserva "
         "solo las expresiones únicas cuyas partes más cortas <i>no</i> lo "
         "son.<br>"
         "<b>Cada palabra aparece ≥ N</b> conserva solo las expresiones cuyas "
         "palabras son <i>todas</i> frecuentes: con 50, cada palabra aparece al "
         "menos 50 veces en el Tanaj. Lo sorprendente es entonces la expresión "
         "y no el vocabulario — a menudo las mejores preguntas."),
        ("Comparar por",
         "Qué cuenta como «la misma palabra»:"
         "<ul>"
         "<li><b>Forma escrita</b> (predeterminado) — solo letras.</li>"
         "<li><b>Con vocales</b> — más estricto.</li>"
         "<li><b>Raíz</b> — todas las formas de una misma raíz cuentan como una "
         "palabra, de modo que busca <i>raíces</i> únicas y no grafías únicas. "
         "Mucho más raro y mucho más difícil.</li>"
         "</ul>"),
        ("El informe",
         "El PDF abre con una página inicial con sus ajustes y los totales por "
         "libro, "
         "y luego los hallazgos agrupados por capítulo en columnas. Opcional: el "
         "<b>versículo completo</b> bajo cada entrada con la palabra en negrita, "
         "un <b>índice alfabético</b> y una <b>hoja de práctica</b> con "
         "soluciones aparte.<br>"
         "También hay <b>HTML</b> y <b>CSV</b>; el CSV se abre en Excel y sirve "
         "para otros usos si quiere reutilizar los resultados en otro programa."),
        ("Numeración de versículos",
         "Las ediciones impresas y el manuscrito de Leningrado numeran algunos "
         "capítulos de forma distinta — sobre todo el Decálogo. Elija "
         "<b>Ediciones impresas</b> para seguir un Koren, o <b>Leningrado</b> "
         "para seguir la mayoría de programas. Solo cambia las referencias."),
        ("La pestaña Búsqueda de raíz",
         "No confundir con el ajuste <b>Comparar por → Raíz</b>, que cambia la "
         "búsqueda en sí. Esta pestaña es un diccionario: escriba una palabra y "
         "le muestra dónde aparece esa raíz, sin volver a ejecutar nada. Útil "
         "para comprobar una intuición sobre una palabra concreta."),
        ("De dónde viene el texto",
         "El Códice de Leningrado (WLC), del proyecto Open Scriptures Hebrew "
         "Bible — 39 libros, 23.213 versículos, 305.531 palabras, con vocales y "
         "cantilación. El texto va dentro de la aplicación; no se descarga nada "
         "y nada de lo que escriba sale de su ordenador.<br>"
         "Software libre bajo licencia GPL; el texto del Tanaj sigue bajo su "
         "licencia CC-BY. Los PDF que produzca son suyos."),
    ],

    # --------------------------------------------------------- Portuguese
    "pt": [
        ("Numa frase",
         "Escreve a matéria que está a estudar e a aplicação mostra que "
         "palavras e expressões aparecem <b>apenas uma vez</b>, e produz um PDF "
         "para estudar ou distribuir."),
        ("Três passos",
         "<ul>"
         "<li><b>1.</b> Escreva ou cole o programa na caixa de texto no canto "
         "superior esquerdo — ou escolha um livro e capítulos e prima "
         "<b>Adicionar</b>.</li>"
         "<li><b>2.</b> Prima <b>Encontrar hápax</b>. Alguns segundos, mesmo "
         "para a matéria de um ano inteiro.</li>"
         "<li><b>3.</b> Prima <b>Guardar PDF…</b>.</li>"
         "</ul>"
         "Todo o resto é opcional."),
        ("Escrever o programa",
         "Escreva-o tal como está impresso na folha oficial: "
         "<code>יהושע: א-יב</code>, <code>שמואל א: א-טו; יז-כ</code>. Letras "
         "hebraicas ou algarismos, e as abreviaturas habituais. Um livro por "
         "linha; um livro inteiro não precisa de números de capítulo.<br>"
         "Por baixo da caixa vê <b>quantos capítulos, versículos e palavras</b> "
         "foram compreendidos — compare com a sua folha. Se uma linha for ilegível "
         "ou o nome de um livro não for reconhecido, aparece um aviso logo "
         "abaixo indicando a linha: nada é descartado sem lho dizer."),
        ("Único dentro de quê?",
         "A definição mais importante. Uma palavra pode ser única numa passagem "
         "e comum noutra:"
         "<ul>"
         "<li><b>Todo o Tanach</b> — o hápax verdadeiro, uma vez em 305 531 "
         "palavras. É o que o Chidon costuma perguntar.</li>"
         "<li><b>O programa</b> — uma vez no que escreveu, mesmo que a palavra seja "
         "comum noutro lado.</li>"
         "<li><b>O seu próprio livro</b> — uma vez no livro onde está. Se o seu "
         "programa abranger vários livros obtém uma resposta separada para "
         "cada um: as palavras únicas em Jonas, depois as únicas em Amós.</li>"
         "<li><b>Uma secção</b> — Torá (Pentateuco), Nevi'im, Nevi'im Rishonim, "
         "Nevi'im Acharonim, Trei Asar, Ketuvim, Sifrei Emet, os Cinco "
         "Meguilot.</li>"
         "<li><b>Um intervalo que escreve</b> — escrito como o programa, por "
         "exemplo <code>ישעיהו א-לט</code>.</li>"
         "</ul>"),
        ("…o livro inteiro ou só a minha parte?",
         "A caixa por baixo do menu <b>Único dentro de</b> decide se os capítulos "
         "que não listou são contados.<br>"
         "Com ישעיהו א-לט: <b>desmarcada</b>, a palavra tem de ocorrer uma vez "
         "nos 66 capítulos — uma que volta no capítulo 50 é rejeitada. "
         "<b>Marcada</b>, só contam os capítulos 1-39 e essa palavra aparece.<br>"
         "Em ambos os casos, <b>cada resultado é um versículo do seu "
         "programa</b>."),
        ("Expressões, não só palavras",
         "Marque os comprimentos 1 a 5: o programa procura tanto uma palavra "
         "isolada como uma sequência de duas, três, quatro ou cinco palavras "
         "consecutivas.<br>"
         "Deixe <b>apenas expressões mínimas</b> ligado. Sem isso quase toda a "
         "expressão longa é trivialmente única: se uma palavra já é única, "
         "também o é qualquer expressão que a contenha. A opção mantém apenas "
         "expressões únicas cujas partes mais curtas <i>não</i> o são.<br>"
         "<b>Cada palavra ocorre ≥ N</b> mantém apenas as expressões cujas palavras "
         "são <i>todas</i> frequentes: com 50, cada palavra ocorre pelo menos "
         "50 vezes no Tanach. O surpreendente passa a ser a expressão e não o "
         "vocabulário — muitas vezes as melhores perguntas."),
        ("Comparar por",
         "O que conta como «a mesma palavra»:"
         "<ul>"
         "<li><b>Forma escrita</b> (predefinição) — só letras.</li>"
         "<li><b>Com vogais</b> — mais estrito.</li>"
         "<li><b>Raiz</b> — todas as formas de uma mesma raiz contam como uma só "
         "palavra, pelo que procura <i>raízes</i> únicas e não grafias únicas. "
         "Muito mais raro e muito mais difícil.</li>"
         "</ul>"),
        ("O relatório",
         "O PDF abre com uma página inicial com as suas definições e os totais por "
         "livro, "
         "e depois os resultados agrupados por capítulo em colunas. Opcional: o "
         "<b>versículo completo</b> sob cada entrada com a palavra a negrito, um "
         "<b>índice alfabético</b> e uma <b>folha de exercícios</b> com "
         "soluções à parte.<br>"
         "Há também <b>HTML</b> e <b>CSV</b>; o CSV abre no Excel e presta-se a "
         "outros usos se quiser reutilizar os resultados noutro programa."),
        ("Numeração dos versículos",
         "As edições impressas e o manuscrito de Leninegrado numeram alguns "
         "capítulos de forma diferente — sobretudo o Decálogo. Escolha "
         "<b>Edições impressas</b> para seguir um Koren, ou <b>Leninegrado</b> "
         "para seguir a maioria dos programas. Muda apenas as referências."),
        ("O separador Pesquisa de raiz",
         "Não confundir com a definição <b>Comparar por → Raiz</b>, que muda a "
         "própria pesquisa. Este separador é um dicionário: escreve uma palavra "
         "e mostra onde essa raiz ocorre, sem voltar a correr nada. Útil para "
         "confirmar uma intuição sobre uma palavra concreta."),
        ("De onde vem o texto",
         "O Códice de Leninegrado (WLC), do projeto Open Scriptures Hebrew "
         "Bible — 39 livros, 23 213 versículos, 305 531 palavras, com vogais e "
         "cantilação. O texto está dentro da aplicação; nada é transferido e "
         "nada do que escreve sai do seu computador.<br>"
         "Software livre sob licença GPL; o texto do Tanach mantém a sua licença "
         "CC-BY. Os PDF que produzir são seus."),
    ],

    # ------------------------------------------------------------ Russian
    "ru": [
        ("В одном предложении",
         "Вы вводите материал, который учите; программа показывает, какие слова "
         "и выражения встречаются в нём <b>только один раз</b>, и выдаёт PDF "
         "для занятий или раздачи."),
        ("Три шага",
         "<ul>"
         "<li><b>1.</b> Введите или вставьте материал в текстовое поле слева "
         "вверху — или выберите книгу и главы и нажмите <b>Добавить</b>.</li>"
         "<li><b>2.</b> Нажмите <b>Найти гапаксы</b>. Несколько секунд даже для "
         "материала за целый год.</li>"
         "<li><b>3.</b> Нажмите <b>Сохранить PDF…</b>.</li>"
         "</ul>"
         "Всё остальное — по желанию."),
        ("Как записать материал",
         "Записывайте так, как напечатано на официальном листе: "
         "<code>יהושע: א-יב</code>, <code>שמואל א: א-טו; יז-כ</code>. Подходят "
         "и еврейские буквы, и цифры, и обычные сокращения. По одной книге в "
         "строке; для целой книги номера глав не нужны.<br>"
         "Под полем показано, <b>сколько глав, стихов и слов</b> распознано — "
         "сверьте с листом. Если строка не читается или название книги не "
         "распознано, прямо под полем появляется предупреждение с указанием "
         "строки: ничего не отбрасывается молча."),
        ("Уникально внутри чего?",
         "Самая важная настройка. Слово может быть уникальным в одном отрывке и "
         "обычным в другом:"
         "<ul>"
         "<li><b>Весь Танах</b> — настоящий гапакс, один раз на 305 531 слово. "
         "Именно это обычно спрашивают на Хидоне.</li>"
         "<li><b>Материал</b> — один раз в том, что вы ввели, даже если слово "
         "часто встречается в других местах.</li>"
         "<li><b>Своя книга</b> — один раз в той книге, где стоит слово. Если "
         "материал охватывает несколько книг, для каждой будет свой ответ: "
         "слова, уникальные в Ионе, затем уникальные в Амосе.</li>"
         "<li><b>Раздел</b> — Тора (Пятикнижие), Невиим, Невиим Ришоним, "
         "Невиим Ахароним, Трей Асар, Ктувим, Сифрей Эмет, Пять свитков.</li>"
         "<li><b>Указанный вами диапазон</b> — записывается как материал, "
         "например <code>ישעיהו א-לט</code>.</li>"
         "</ul>"),
        ("…вся книга или только моя часть?",
         "Флажок под меню <b>Уникально внутри</b> решает, считаются ли главы, "
         "которые вы не указали.<br>"
         "Материал ישעיהו א-לט: <b>снят</b> — слово должно встречаться один раз "
         "во всех 66 главах, и слово, повторяющееся в главе 50, отбрасывается. "
         "<b>Установлен</b> — считаются только главы 1-39, и это слово "
         "попадает в результат.<br>"
         "В обоих случаях <b>каждый результат — стих внутри вашего "
         "материала</b>."),
        ("Выражения, а не только слова",
         "Отметьте длины от 1 до 5: программа ищет и отдельное слово, и цепочку из "
         "двух, трёх, четырёх или пяти подряд идущих слов.<br>"
         "Оставьте <b>только минимальные выражения</b> включённым. Без этого "
         "почти любое длинное выражение уникально тривиально: если слово уже "
         "уникально, уникально и любое выражение с ним. Настройка оставляет "
         "только те выражения, чьи более короткие части <i>не</i> уникальны.<br>"
         "<b>Каждое слово встречается ≥ N</b> оставляет только те выражения, где "
         "<i>все</i> слова частотны: при 50 каждое слово выражения встречается "
         "в Танахе не менее 50 раз. Тогда удивительно само выражение, а не его "
         "лексика — часто это лучшие вопросы."),
        ("Сравнивать по",
         "Что считается «тем же словом»:"
         "<ul>"
         "<li><b>Написание</b> (по умолчанию) — только буквы.</li>"
         "<li><b>С огласовками</b> — строже.</li>"
         "<li><b>Корень</b> — все формы одного корня считаются одним словом, то "
         "есть ищутся уникальные <i>корни</i>, а не написания. Гораздо реже и "
         "гораздо труднее.</li>"
         "</ul>"),
        ("Отчёт",
         "PDF открывается титульной страницей с настройками и итогами по книгам, "
         "затем "
         "результаты по главам в колонках. По желанию: <b>полный стих</b> под "
         "каждой записью с выделенным словом, <b>алфавитный указатель</b> и "
         "<b>лист для тренировки</b> с отдельными ответами.<br>"
         "Есть также <b>HTML</b> и <b>CSV</b>; CSV открывается в Excel и подходит "
         "для других задач, если вы захотите использовать результаты в другой "
         "программе."),
        ("Нумерация стихов",
         "Печатные издания и Ленинградский кодекс нумеруют несколько глав "
         "по-разному — прежде всего Десятисловие. Выберите <b>печатные "
         "издания</b>, чтобы совпадало с изданием в руках, или "
         "<b>Ленинградский</b>, чтобы совпадало с большинством программ. "
         "Меняются только ссылки, но не результаты."),
        ("Вкладка «Поиск корня»",
         "Не путать с настройкой <b>Сравнивать по → Корень</b>, которая меняет "
         "сам поиск. Эта вкладка — словарь: вводите слово и видите, где "
         "встречается его корень, ничего не пересчитывая. Удобно проверить "
         "догадку об одном конкретном слове."),
        ("Откуда взят текст",
         "Ленинградский кодекс (WLC) из проекта Open Scriptures Hebrew Bible — "
         "39 книг, 23 213 стихов, 305 531 слово, с огласовками и кантилляцией. "
         "Текст находится внутри программы; ничего не скачивается и ничего из "
         "введённого вами не покидает компьютер.<br>"
         "Свободная программа под лицензией GPL; текст Танаха остаётся под "
         "своей лицензией CC-BY. Созданные вами PDF принадлежат вам."),
    ],
}


def guide(lang: str) -> list[tuple[str, str]]:
    return GUIDE.get(lang) or GUIDE["en"]
