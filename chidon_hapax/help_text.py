"""The in-app guide, for people who never see the README.

Each language maps to a list of (heading, body) pairs. Bodies may contain the
few HTML tags the dialog renders: <b>, <i>, <br>, <ul>, <li>, <code>.

The French and English texts are the ones the author reviewed and approved;
the other four follow them sentence by sentence. When editing, change French
and English first and bring the rest into line, rather than the other way
round.
"""

from __future__ import annotations

GUIDE: dict[str, list[tuple[str, str]]] = {

    # ------------------------------------------------------------- French
    "fr": [
        ("En une phrase",
         "Vous saisissez le programme que vous étudiez ; l'application vous "
         "indique quels mots et expressions n'y apparaissent qu'une seule "
         "fois, et produit un PDF à étudier ou à distribuer."),
        ("Trois étapes",
         "<ul>"
         "<li><b>1.</b> Saisissez ou collez le programme dans la grande zone "
         "en haut à gauche — ou choisissez un livre et des chapitres puis "
         "<b>Ajouter</b>.</li>"
         "<li><b>2.</b> Cliquez sur <b>Trouver les hapax</b>. Quelques "
         "secondes, même pour toute une année.</li>"
         "<li><b>3.</b> Cliquez sur <b>Enregistrer le PDF…</b>.</li>"
         "</ul>"
         "Tout le reste est facultatif."),
        ("Écrire le programme",
         "Écrivez-le comme il est imprimé sur la feuille officielle : "
         "<code>יהושע: א-יב</code>, <code>שמואל א: א-טו; יז-כ</code>. Lettres "
         "hébraïques ou chiffres, abréviations usuelles comprises. Un livre "
         "par ligne ; un livre entier ne demande aucun numéro de chapitre. Les noms de livres peuvent être écrits en hébreu, anglais, français, espagnol, portugais ou russe, avec ou sans accents.<br>"
         "Sous la zone s'affiche le <b>nombre de chapitres, versets et mots</b> "
         "reconnus. Si une ligne est illisible ou si un nom de livre n'est pas "
         "reconnu, un avertissement apparaît juste en dessous en indiquant la "
         "ligne en cause : rien n'est laissé de côté sans vous le dire."),
        ("Unique au sein de quoi ?",
         "Le réglage le plus important. Un mot peut être unique dans un "
         "passage et banal dans un autre :"
         "<ul>"
         "<li><b>Tout le Tanakh</b> — le véritable hapax, une fois sur les "
         "305 531 mots.</li>"
         "<li><b>Le programme</b> — une fois dans le programme d'étude que "
         "vous avez saisi.</li>"
         "<li><b>Son propre livre</b> — unique dans un livre. C'est-à-dire que "
         "le mot peut apparaître plusieurs fois dans le programme mais s'il "
         "est unique dans un livre il sera affiché. Ceci permet de répondre "
         "aux questions du type : « Où dans tel livre se trouve tel "
         "mot ? ».</li>"
         "<li><b>Une section</b> — unique dans une section du Tanakh : Torah, "
         "Nevi'im, Nevi'im Rishonim, Nevi'im Acharonim, Trei Asar, "
         "Ketouvim…</li>"
         "<li><b>Une plage que vous saisissez</b> — unique dans une plage que "
         "vous saisissez, écrite comme le programme, par exemple "
         "<code>ישעיהו א-לט</code>.</li>"
         "</ul>"),
        ("…tout le livre, ou seulement ma partie ?",
         "La case à cocher sous le menu « Unique au sein de » décide si les "
         "chapitres que vous n'avez pas listés dans le programme sont "
         "comptés.<br>"
         "Exemple : programme <code>ישעיהו א-לט</code>. <b>Décochée</b>, le mot "
         "doit apparaître une fois dans les 66 chapitres — un mot qui revient "
         "au chapitre 50 est rejeté. <b>Cochée</b>, seuls les chapitres 1-39 "
         "comptent, et ce mot est retenu.<br>"
         "Dans les deux cas, <b>chaque résultat est un verset de votre "
         "programme</b>. Ce réglage ne fait que retirer des résultats."),
        ("Deux fois, trois fois — pas seulement les hapax",
         "<b>Apparaît au plus</b> décide de ce qui est assez rare. À 1, vous "
         "obtenez les véritables hapax : les mots et expressions n'apparaissant "
         "qu'une seule fois. À 2, vous obtenez aussi ceux qui apparaissent "
         "exactement deux fois, à 3 trois fois, et ainsi de suite.<br>"
         "Les compteurs à côté de chaque entrée indiquent le nombre "
         "d'occurrences, ce qui permet de voir d'un coup d'œil si un mot "
         "apparaît une ou deux fois. Toutes les références nécessaires seront "
         "indiquées.<br>"
         "L'option <b>expressions minimales seulement</b> suit le même seuil : "
         "à 2, une expression n'est conservée que si ses parties plus courtes "
         "apparaissent plus de deux fois."),
        ("Expressions, pas seulement des mots",
         "Cochez les longueurs 1 à 5 : l'application cherche aussi bien un mot "
         "isolé qu'une suite de deux, trois, quatre ou cinq mots "
         "consécutifs.<br>"
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
         "<li><b>Racine</b> — toutes les formes d'une même racine comptent "
         "pour un seul mot. Cherche donc les <i>racines</i> uniques, et non "
         "les formes : bien plus rare, et bien plus difficile.</li>"
         "</ul>"),
        ("Exporter",
         "Vous pouvez exporter les résultats de votre recherche sous forme "
         "d'un PDF. Le PDF s'ouvre sur une page de garde rappelant vos "
         "réglages et les totaux par livre, puis les résultats groupés par "
         "chapitre en colonnes. En option : le <b>verset entier</b> sous "
         "chaque entrée avec le mot en gras, un <b>index alphabétique</b> et "
         "une <b>feuille d'exercices</b> avec corrigé séparé.<br>"
         "<b>HTML</b> et <b>CSV</b> sont également proposés ; le CSV s'ouvre "
         "dans Excel et se prête à d'autres usages, par exemple si vous voulez "
         "réutiliser les résultats dans un autre programme informatique."),
        ("Numérotation des versets",
         "Les éditions imprimées et le manuscrit de Léningrad numérotent "
         "quelques chapitres différemment — surtout le Décalogue. Choisissez "
         "<b>Éditions imprimées</b> pour suivre un Koren, ou <b>Léningrad</b> "
         "pour suivre la plupart des logiciels. Cela ne change que les "
         "références, jamais les résultats."),
        ("L'onglet racines",
         "À ne pas confondre avec le réglage « Comparer par → Racine », qui "
         "concerne la recherche elle-même. Cet onglet-ci est un dictionnaire : "
         "vous tapez un mot et il vous montre où cette racine apparaît, sans "
         "relancer la recherche. Pratique pour vérifier une intuition sur un "
         "mot précis."),
        ("D'où vient le texte",
         "Le Codex de Léningrad (WLC), via Open Scriptures Hebrew Bible — 39 "
         "livres, 23 213 versets, 305 531 mots, avec voyelles et cantillation. "
         "Le texte est inclus dans l'application ; rien n'est téléchargé et "
         "rien de ce que vous saisissez ne quitte votre ordinateur.<br>"
         "Logiciel libre sous licence GPL ; le texte du Tanakh reste sous sa "
         "licence CC-BY. Les PDF que vous produisez vous appartiennent."),
    ],

    # ------------------------------------------------------------ English
    "en": [
        ("In one sentence",
         "You type in the syllabus you are learning; the app tells you which "
         "words and phrases in it appear only once, and hands you a PDF you "
         "can study from or hand out."),
        ("Three steps",
         "<ul>"
         "<li><b>1.</b> Type or paste your syllabus into the text box at the "
         "top left — or pick a book and chapters below it and press "
         "<b>Add</b>.</li>"
         "<li><b>2.</b> Press <b>Find hapaxes</b>. A few seconds, even for the "
         "entire Tanach.</li>"
         "<li><b>3.</b> Press <b>Save PDF…</b>.</li>"
         "</ul>"
         "Everything in between is optional."),
        ("Writing the syllabus",
         "Write it the way the official sheet is printed, and it will be "
         "understood: <code>יהושע: א-יב</code>, <code>שמואל א: א-טו; יז-כ</code>, "
         "<code>ישעיהו א-לט</code>. Hebrew letters or digits both work, as do "
         "the usual abbreviations (<code>שמו״א</code>, <code>דהי״ב</code>). One "
         "book per line. A whole book needs no chapter numbers at all. Book names may be written in Hebrew, English, French, Spanish, Portuguese or Russian, with or without accents.<br>"
         "Under the box you will see <b>how many chapters, verses and words</b> "
         "were understood — check it against your sheet. If a line is "
         "unreadable or a book name is not recognised, a warning appears just "
         "underneath naming the line: nothing is dropped without telling you."),
        ("Unique within what?",
         "The most important setting. A word can be unique in one span of text "
         "and ordinary in another:"
         "<ul>"
         "<li><b>The whole Tanach</b> — a true hapax legomenon, once in all "
         "305,531 words.</li>"
         "<li><b>The syllabus</b> — once in the syllabus you typed, even if "
         "the word is common elsewhere.</li>"
         "<li><b>Its own book</b> — unique in a book. That is to say that the "
         "word can appear multiple times in the syllabus but if it is unique "
         "in a book of the syllabus it will be output. This allows you to "
         "answer questions such as “Where in this book does this word "
         "appear?”.</li>"
         "<li><b>A section</b> — Torah, Nevi'im, Nevi'im Rishonim, Nevi'im "
         "Acharonim, Trei Asar, Ketuvim, Sifrei Emet, the Five Megillot.</li>"
         "<li><b>A range you type</b> — unique in that range, written like the "
         "syllabus, for example <code>ישעיהו א-לט</code>.</li>"
         "</ul>"),
        ("…the whole book, or only my part of it?",
         "The checkbox under the <b>Unique within</b> menu decides whether "
         "chapters you did not list are counted.<br>"
         "Say your material is <code>ישעיהו א-לט</code>. <b>Unchecked</b>, a "
         "word must occur once in all 66 chapters — one that returns in "
         "chapter 50 is rejected even though you are not studying it. "
         "<b>Checked</b>, only chapters 1-39 count, and that word is "
         "reported.<br>"
         "Either way, <b>every result is a verse inside your syllabus</b>. "
         "This setting only removes results; it never sends you elsewhere."),
        ("Twice, three times — not only hapaxes",
         "<b>Appears at most</b> decides how rare is rare enough. At 1 you get "
         "true hapax legomena: words and phrases occurring exactly once. At 2 "
         "you also get those occurring exactly twice, at 3 three times, and so "
         "on.<br>"
         "The counts beside each entry tell you how many occurrences there "
         "are, so you can see at a glance whether a word occurs once or twice. "
         "All necessary references will be given.<br>"
         "The <b>minimal phrases only</b> rule follows the same threshold: at "
         "2, a phrase is kept only when its shorter parts occur more than "
         "twice."),
        ("Phrases, not just words",
         "Tick the lengths 1 to 5: the program looks for a single word just as "
         "readily as a run of two, three, four or five consecutive words.<br>"
         "Leave <b>minimal phrases only</b> on. Without it almost every long "
         "phrase is trivially unique — if a word is already unique, so is "
         "every phrase containing it, and you would drown in them. Minimal "
         "keeps only phrases that are unique while their shorter parts are "
         "<i>not</i>, which is where the interesting ones live.<br>"
         "<b>Each word occurs ≥ N</b> keeps only phrases whose words are "
         "<i>all</i> common: at 50, every word in the phrase appears at least "
         "50 times in the Tanach. The phrase is then the surprising thing "
         "rather than its vocabulary — often the best questions."),
        ("Compare by",
         "What counts as \"the same word\":"
         "<ul>"
         "<li><b>Written form</b> (default) — letters only, nikkud ignored.</li>"
         "<li><b>With nikkud</b> — stricter; two spellings that differ only in "
         "vowels count as different words.</li>"
         "<li><b>Root</b> — every form of one root counts as a single word, so "
         "this finds unique <i>roots</i> rather than unique spellings. Far "
         "rarer, and far harder.</li>"
         "</ul>"),
        ("Exporting",
         "You can export the output as a PDF. The PDF opens with a title page "
         "listing your settings and the totals per book, then the findings "
         "grouped by chapter in newspaper columns. Optional extras: the "
         "<b>full verse</b> under each entry with the word in bold, an "
         "<b>alphabetical index</b>, and a <b>practice sheet</b> with a "
         "separate answer key for testing yourself or a friend.<br>"
         "<b>Save HTML</b> and <b>Save CSV</b> are there too — CSV opens in "
         "Excel, and lends itself to other uses, for example if you want to "
         "reuse the results in another programming project."),
        ("Verse numbers",
         "Printed editions and the Leningrad manuscript number a handful of "
         "chapters differently — the Ten Commandments above all. Choose "
         "<b>Printed editions</b> to match a Koren or Mikraot Gedolot in your "
         "hand, or <b>Leningrad</b> to match most software. It changes only "
         "the references that are printed, never which words are found."),
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
         "מקלידים את חומר הבחינה שלומדים, והתוכנה מראה אילו מילים וצירופים בו "
         "מופיעים פעם אחת בלבד, ומפיקה קובץ PDF ללימוד או לחלוקה."),
        ("שלושה צעדים",
         "<ul>"
         "<li><b>1.</b> מקלידים או מדביקים את חומר הבחינה בתיבה הגדולה שבצד "
         "ימין למעלה — או בוחרים ספר ופרקים ולוחצים <b>הוסף</b>.</li>"
         "<li><b>2.</b> לוחצים <b>מצא מילים ייחודיות</b>. כמה שניות, גם לכל "
         "התנ״ך.</li>"
         "<li><b>3.</b> לוחצים <b>שמור PDF…</b>.</li>"
         "</ul>"
         "כל השאר הוא רשות."),
        ("כתיבת חומר הבחינה",
         "כותבים כפי שמודפס בדף הרשמי, והתוכנה תבין: <code>יהושע: א-יב</code>, "
         "<code>שמואל א: א-טו; יז-כ</code>. אפשר אותיות או ספרות, וגם הקיצורים "
         "המקובלים. ספר אחד בכל שורה; ספר שלם אינו דורש מספרי פרקים כלל. שמות הספרים אפשר לכתוב בעברית, אנגלית, צרפתית, ספרדית, פורטוגזית או רוסית.<br>"
         "מתחת לתיבה מופיע <b>כמה פרקים, פסוקים ומילים</b> נקלטו. אם שורה אינה "
         "קריאה או ששם ספר אינו מזוהה, מופיעה מיד מתחת אזהרה המציינת את השורה "
         "המדוברת: שום דבר אינו מושמט בלי להודיע לכם."),
        ("ייחודי בתוך מה?",
         "ההגדרה החשובה ביותר. מילה יכולה להיות ייחודית בקטע אחד ורגילה באחר:"
         "<ul>"
         "<li><b>כל התנ״ך</b> — הפקס לגומנון האמיתי, פעם אחת מתוך 305,531 "
         "מילים.</li>"
         "<li><b>חומר הבחינה</b> — פעם אחת בחומר הלימוד שהקלדתם.</li>"
         "<li><b>הספר שלו עצמו</b> — ייחודי בתוך ספר. כלומר, המילה יכולה "
         "להופיע כמה פעמים בחומר, אך אם היא ייחודית באחד הספרים היא תוצג. כך "
         "אפשר לענות על שאלות מסוג „היכן בספר פלוני מופיעה מילה פלונית?”.</li>"
         "<li><b>חלק מהתנ״ך</b> — ייחודי בתוך חלק מהתנ״ך: תורה, נביאים, נביאים "
         "ראשונים, נביאים אחרונים, תרי עשר, כתובים…</li>"
         "<li><b>טווח שמקלידים</b> — ייחודי בתוך טווח שאתם מקלידים, בכתיב של "
         "חומר הבחינה, למשל <code>ישעיהו א-לט</code>.</li>"
         "</ul>"),
        ("…כל הספר, או רק החלק שלי?",
         "תיבת הסימון שמתחת לתפריט „ייחודי בתוך” קובעת אם נספרים פרקים שלא "
         "נכללו בחומר הבחינה.<br>"
         "דוגמה: חומר <code>ישעיהו א-לט</code>. <b>ללא סימון</b>, המילה צריכה "
         "להופיע פעם אחת בכל 66 הפרקים — מילה שחוזרת בפרק נ נפסלת אף שאינה "
         "נלמדת. <b>עם סימון</b>, נספרים רק פרקים א-לט, ואותה מילה תדווח.<br>"
         "בכל מקרה, <b>כל תוצאה נמצאת בתוך חומר הבחינה</b>. ההגדרה רק מסננת "
         "תוצאות; היא לעולם אינה מפנה למקום אחר."),
        ("פעמיים, שלוש פעמים — לא רק מילים ייחודיות",
         "<b>מופיע לכל היותר</b> קובע מה נחשב נדיר מספיק. ב-1 מתקבלים הפקס "
         "לגומנון האמיתיים: מילים וצירופים המופיעים בדיוק פעם אחת. ב-2 מתקבלים "
         "גם המופיעים בדיוק פעמיים, ב-3 שלוש פעמים, וכן הלאה.<br>"
         "המספרים שליד כל ערך מציינים כמה הופעות יש, כך שאפשר לראות במבט אחד "
         "אם מילה מופיעה פעם אחת או פעמיים. כל המראי מקום הדרושים יינתנו.<br>"
         "האפשרות <b>צירופים מינימליים בלבד</b> פועלת לפי אותו סף: ב-2, צירוף "
         "נשמר רק אם חלקיו הקצרים יותר מופיעים יותר מפעמיים."),
        ("צירופים, לא רק מילים",
         "מסמנים אורכים 1 עד 5: התוכנה מחפשת גם מילה בודדת וגם רצף של שתיים, "
         "שלוש, ארבע או חמש מילים רצופות.<br>"
         "מומלץ להשאיר <b>צירופים מינימליים בלבד</b>. בלעדיו כמעט כל צירוף ארוך "
         "ייחודי באופן חסר עניין: אם מילה כבר ייחודית, גם כל צירוף המכיל אותה. "
         "האפשרות משאירה רק צירופים ייחודיים שחלקיהם הקצרים <i>אינם</i> "
         "ייחודיים.<br>"
         "<b>כל מילה מופיעה ≥ N</b> משאיר רק צירופים שכל מילותיהם שכיחות: ב-50, "
         "כל מילה בצירוף מופיעה לפחות חמישים פעם בתנ״ך. כך הצירוף עצמו הוא "
         "המפתיע ולא אוצר המילים — לרוב השאלות היפות ביותר."),
        ("השוואה לפי",
         "מה נחשב „אותה מילה”:"
         "<ul>"
         "<li><b>כתיב</b> (ברירת מחדל) — אותיות בלבד, ללא ניקוד.</li>"
         "<li><b>עם ניקוד</b> — מחמיר יותר.</li>"
         "<li><b>שורש</b> — כל נטיות אותו שורש נחשבות למילה אחת. כך מתקבלים "
         "<i>שורשים</i> ייחודיים ולא צורות ייחודיות: נדיר הרבה יותר וקשה הרבה "
         "יותר.</li>"
         "</ul>"),
        ("ייצוא",
         "אפשר לייצא את תוצאות החיפוש כקובץ PDF. ה-PDF נפתח בעמוד שער ובו "
         "ההגדרות וסיכום לכל ספר, ואחריו הממצאים מסודרים לפי פרקים בטורים. "
         "תוספות לבחירה: <b>הפסוק המלא</b> תחת כל ערך כשהמילה מודגשת, "
         "<b>מפתח אלפביתי</b>, ו<b>דף תרגול</b> עם דף תשובות נפרד.<br>"
         "קיימות גם <b>שמירת HTML</b> ו<b>שמירת CSV</b> — קובץ CSV נפתח באקסל "
         "ומתאים גם לשימושים אחרים, למשל אם תרצו להשתמש בתוצאות בפרויקט "
         "תכנות אחר."),
        ("מספור הפסוקים",
         "המהדורות המודפסות וכתב יד לנינגרד ממספרים כמה פרקים אחרת — בעיקר "
         "עשרת הדיברות. בוחרים <b>מהדורות מודפסות</b> כדי להתאים לקורן, או "
         "<b>לנינגרד</b> כדי להתאים לרוב התוכנות. משפיע רק על המראי מקום, לא "
         "על התוצאות."),
        ("לשונית חיפוש שורשים",
         "אין לבלבל עם ההגדרה „השוואה לפי → שורש”, הנוגעת לחיפוש עצמו. "
         "הלשונית הזו היא מילון: מקלידים מילה והיא מראה היכן מופיע השורש, בלי "
         "להריץ מחדש את החיפוש. נוח לבדיקת השערה על מילה מסוימת."),
        ("מקור הנוסח",
         "כתב יד לנינגרד (WLC) מתוך מיזם Open Scriptures — 39 ספרים, 23,213 "
         "פסוקים, 305,531 מילים, עם ניקוד וטעמים. הנוסח נמצא בתוך התוכנה; שום "
         "דבר אינו יורד מהרשת ושום דבר שמקלידים אינו יוצא מהמחשב.<br>"
         "תוכנה חופשית תחת רישיון GPL; נוסח התנ״ך נשאר תחת רישיון CC-BY שלו. "
         "קובצי ה-PDF שאתם מפיקים שייכים לכם."),
    ],

    # ------------------------------------------------------------ Spanish
    # Rewritten by a native speaker, and rather fuller than the other
    # languages: it splits the frequency floor into its own section and
    # explains each setting at more length.
    "es": [
        ("En una frase",
         "Escriba el temario que está estudiando y la aplicación le mostrará "
         "qué palabras y expresiones aparecen en él una sola vez. Después podrá "
         "generar un PDF para estudiar, imprimir o repartir."),
        ("Tres pasos",
         "<ul>"
         "<li><b>1.</b> Escriba o pegue el temario en el cuadro grande de la "
         "parte superior izquierda. También puede elegir un libro y sus "
         "capítulos y pulsar <b>Añadir</b>.</li>"
         "<li><b>2.</b> Pulse <b>Buscar hápax</b>. La búsqueda tarda solo unos "
         "segundos, incluso si abarca todo el Tanaj.</li>"
         "<li><b>3.</b> Pulse <b>Guardar PDF…</b> para exportar los "
         "resultados.</li>"
         "</ul>"
         "Todo lo demás es opcional."),
        ("Escribir el temario",
         "Escriba el temario tal como aparece en la hoja oficial. Por ejemplo: "
         "<code>יהושע: א-יב</code>, <code>שמואל א: א-טו; יז-כ</code>.<br>"
         "Puede utilizar letras hebreas o números, así como las abreviaturas "
         "habituales. Escriba un libro por línea; si quiere incluir un libro "
         "completo, no es necesario indicar capítulos. Los nombres de los "
         "libros pueden escribirse en hebreo, inglés, francés, español, "
         "portugués o ruso, con o sin acentos.<br>"
         "Debajo del cuadro de texto se indica <b>cuántos capítulos, "
         "versículos y palabras</b> ha reconocido la aplicación. Si una línea "
         "no puede interpretarse o el nombre de un libro no se reconoce, "
         "aparecerá un aviso justo debajo indicando cuál es la línea "
         "problemática: ninguna línea se ignora sin avisarle."),
        ("¿Único dentro de qué?",
         "Este es uno de los ajustes más importantes. Una palabra puede "
         "aparecer una sola vez dentro de un pasaje determinado y, sin "
         "embargo, ser muy frecuente en otra parte del Tanaj."
         "<ul>"
         "<li><b>Todo el Tanaj</b> — el hápax verdadero: una palabra o "
         "expresión que aparece una sola vez entre las 305.531 palabras del "
         "Tanaj.</li>"
         "<li><b>El temario</b> — palabras o expresiones que aparecen una sola "
         "vez dentro del temario que ha introducido.</li>"
         "<li><b>El libro correspondiente</b> — elementos únicos dentro de cada "
         "libro. Una palabra puede aparecer varias veces en todo el temario y "
         "aun así mostrarse si aparece una sola vez dentro de uno de los libros "
         "incluidos. Útil para responder preguntas como «¿dónde aparece esta "
         "palabra dentro de este libro?».</li>"
         "<li><b>Una sección</b> — palabras o expresiones únicas dentro de una "
         "sección completa del Tanaj: Torá, Nevi'im, Nevi'im Rishonim, Nevi'im "
         "Acharonim, Trei Asar, Ketuvim…</li>"
         "<li><b>Un rango personalizado</b> — también puede definir el rango en "
         "el que desea comprobar la frecuencia, utilizando el mismo formato que "
         "para el temario, por ejemplo <code>ישעיהו א-לט</code>.</li>"
         "</ul>"),
        ("¿Se cuenta todo el libro o solo la parte incluida en mi temario?",
         "La casilla situada debajo del menú «Único dentro de» determina si, al "
         "calcular la frecuencia, se cuentan también los capítulos que no ha "
         "incluido en su temario.<br>"
         "Ejemplo: su temario es <code>ישעיהו א-לט</code>. Si la casilla está "
         "<b>desmarcada</b>, la palabra debe aparecer una sola vez en los 66 "
         "capítulos completos de Isaías; por tanto, si aparece en los capítulos "
         "1-39 y vuelve a aparecer en el capítulo 50, no se considerará única. "
         "Si la casilla está <b>marcada</b>, solo se tendrán en cuenta los "
         "capítulos 1-39, y esa misma palabra sí se mostrará como única.<br>"
         "En ambos casos, los resultados que aparecen siempre pertenecen al "
         "temario que ha introducido. Este ajuste únicamente puede eliminar "
         "resultados; nunca añadirá resultados procedentes de capítulos que no "
         "forman parte de su temario."),
        ("Dos veces, tres veces… no solo hápax",
         "El ajuste «Aparece como máximo» determina cuántas apariciones puede "
         "tener una palabra o expresión para que se incluya en los "
         "resultados.<br>"
         "Si selecciona 1, obtendrá los hápax verdaderos: palabras y "
         "expresiones que aparecen exactamente una vez. Si selecciona 2, "
         "también aparecerán las que aparecen exactamente dos veces; con 3, las "
         "que aparecen tres veces, y así sucesivamente.<br>"
         "Junto a cada resultado se muestra su número de apariciones, de modo "
         "que puede ver inmediatamente si una palabra aparece una, dos o más "
         "veces. También se mostrarán todas las referencias "
         "correspondientes.<br>"
         "La opción «Solo expresiones mínimas» utiliza el mismo límite: si ha "
         "seleccionado un máximo de 2 apariciones, una expresión se conservará "
         "únicamente si sus partes más cortas aparecen más de dos veces."),
        ("Expresiones, no solo palabras",
         "La aplicación no se limita a buscar palabras individuales. Puede "
         "seleccionar longitudes del 1 al 5 para buscar una palabra, o dos, "
         "tres, cuatro o cinco palabras consecutivas.<br>"
         "En general, conviene mantener activada la opción <b>Solo expresiones "
         "mínimas</b>. Sin esta opción, muchas expresiones largas serían únicas "
         "de forma trivial: si una palabra ya aparece una sola vez en todo el "
         "rango, cualquier expresión de dos, tres o más palabras que contenga "
         "esa palabra también aparecerá una sola vez. La opción evita ese "
         "problema y conserva únicamente las expresiones únicas cuyas partes "
         "más cortas no son ya únicas."),
        ("Cada palabra aparece ≥ N",
         "La opción «Cada palabra aparece ≥ N» permite encontrar expresiones "
         "poco frecuentes formadas únicamente por palabras comunes.<br>"
         "Por ejemplo, si introduce 50, solo se conservarán las expresiones en "
         "las que cada una de sus palabras aparezca al menos 50 veces en todo "
         "el Tanaj. De esta manera, lo excepcional no es que alguna palabra sea "
         "rara, sino la combinación concreta de palabras.<br>"
         "Este tipo de resultado suele ser especialmente útil para formular "
         "buenas preguntas de estudio."),
        ("Comparar por",
         "Este ajuste determina qué considera la aplicación como «la misma "
         "palabra»."
         "<ul>"
         "<li><b>Forma escrita</b> (predeterminada) — compara únicamente las "
         "letras, ignorando las vocales.</li>"
         "<li><b>Con vocales</b> — la comparación es más estricta y tiene en "
         "cuenta también la vocalización.</li>"
         "<li><b>Raíz</b> — todas las formas que pertenecen a una misma raíz se "
         "cuentan como una sola unidad. En este modo la aplicación no busca "
         "formas escritas únicas, sino <i>raíces</i> únicas; encontrar "
         "resultados suele ser mucho más raro y también más difícil.</li>"
         "</ul>"),
        ("Exportar",
         "Puede exportar los resultados de la búsqueda como PDF. El PDF "
         "comienza con una página de resumen que muestra los ajustes "
         "utilizados y los totales correspondientes a cada libro. Después "
         "aparecen los resultados agrupados por capítulo y organizados en "
         "columnas.<br>"
         "De forma opcional, puede incluir el versículo completo debajo de cada "
         "resultado, con la palabra encontrada resaltada en negrita; un índice "
         "alfabético; y una hoja de práctica con las soluciones en una sección "
         "separada.<br>"
         "También puede exportar los resultados en formato HTML o CSV. El "
         "archivo CSV puede abrirse directamente en Excel y también resulta "
         "útil si desea reutilizar los resultados en otro proyecto de "
         "programación o análisis."),
        ("Numeración de versículos",
         "Las ediciones impresas y el manuscrito de Leningrado utilizan una "
         "numeración distinta en algunos capítulos, especialmente en el "
         "Decálogo."
         "<ul>"
         "<li><b>Ediciones impresas</b> — si desea que las referencias "
         "coincidan con ediciones impresas como Koren.</li>"
         "<li><b>Leningrado</b> — si desea seguir la numeración empleada por el "
         "Códice de Leningrado y por la mayoría de los programas "
         "informáticos.</li>"
         "</ul>"
         "Este ajuste modifica únicamente las referencias mostradas. No cambia "
         "las palabras, expresiones ni resultados encontrados."),
        ("La pestaña de raíces",
         "La pestaña <b>Raíces</b> es distinta del ajuste «Comparar por → "
         "Raíz». El ajuste modifica la forma en que se realiza toda la "
         "búsqueda; la pestaña, en cambio, funciona como un diccionario o "
         "herramienta de consulta.<br>"
         "Puede escribir una palabra y ver dónde aparece su raíz en el Tanaj, "
         "sin necesidad de volver a ejecutar la búsqueda principal. Resulta "
         "útil, por ejemplo, para comprobar rápidamente una intuición sobre una "
         "palabra concreta."),
        ("De dónde viene el texto",
         "La aplicación utiliza el texto del Códice de Leningrado (WLC) a "
         "través de Open Scriptures Hebrew Bible. El corpus contiene 39 libros, "
         "23.213 versículos y 305.531 palabras, con vocales y cantilación.<br>"
         "Todo el texto está incluido dentro de la propia aplicación. No es "
         "necesario descargar nada durante el uso y nada de lo que escriba en "
         "la aplicación sale de su ordenador.<br>"
         "El software es libre y se distribuye bajo licencia GPL. El texto del "
         "Tanaj mantiene su licencia CC-BY. Los PDF que genere con la "
         "aplicación son suyos."),
    ],

    # --------------------------------------------------------- Portuguese
    "pt": [
        ("Numa frase",
         "Escreve o programa que está a estudar; a aplicação indica-lhe que "
         "palavras e expressões aparecem nele uma só vez, e produz um PDF para "
         "estudar ou distribuir."),
        ("Três passos",
         "<ul>"
         "<li><b>1.</b> Escreva ou cole o programa na caixa grande em cima à "
         "esquerda — ou escolha um livro e capítulos e prima "
         "<b>Adicionar</b>.</li>"
         "<li><b>2.</b> Prima <b>Encontrar hápax</b>. Alguns segundos, mesmo "
         "para todo o Tanach.</li>"
         "<li><b>3.</b> Prima <b>Guardar PDF…</b>.</li>"
         "</ul>"
         "Todo o resto é opcional."),
        ("Escrever o programa",
         "Escreva-o tal como está impresso na folha oficial: "
         "<code>יהושע: א-יב</code>, <code>שמואל א: א-טו; יז-כ</code>. Letras "
         "hebraicas ou algarismos, e as abreviaturas habituais. Um livro por "
         "linha; um livro inteiro não precisa de qualquer número de capítulo. Os nomes dos livros podem ser escritos em hebraico, inglês, francês, espanhol, português ou russo, com ou sem acentos.<br>"
         "Por baixo da caixa aparece <b>quantos capítulos, versículos e "
         "palavras</b> foram reconhecidos. Se uma linha for ilegível ou o nome "
         "de um livro não for reconhecido, surge um aviso logo abaixo a indicar "
         "a linha em causa: nada é descartado sem lho dizer."),
        ("Único dentro de quê?",
         "A definição mais importante. Uma palavra pode ser única numa passagem "
         "e comum noutra:"
         "<ul>"
         "<li><b>Todo o Tanach</b> — o verdadeiro hápax, uma vez nas 305 531 "
         "palavras.</li>"
         "<li><b>O programa</b> — uma vez no programa de estudo que "
         "escreveu.</li>"
         "<li><b>O seu próprio livro</b> — único dentro de um livro. Ou seja, a "
         "palavra pode aparecer várias vezes no programa, mas se for única num "
         "dos livros será mostrada. Isto permite responder a perguntas do tipo: "
         "“Onde neste livro aparece esta palavra?”.</li>"
         "<li><b>Uma secção</b> — único dentro de uma secção do Tanach: Torá, "
         "Nevi'im, Nevi'im Rishonim, Nevi'im Acharonim, Trei Asar, "
         "Ketuvim…</li>"
         "<li><b>Um intervalo que escreve</b> — único dentro desse intervalo, "
         "escrito como o programa, por exemplo <code>ישעיהו א-לט</code>.</li>"
         "</ul>"),
        ("…o livro inteiro ou só a minha parte?",
         "A caixa por baixo do menu “Único dentro de” decide se os capítulos "
         "que não listou no programa são contados.<br>"
         "Exemplo: programa <code>ישעיהו א-לט</code>. <b>Desmarcada</b>, a "
         "palavra tem de ocorrer uma vez nos 66 capítulos — uma que volta no "
         "capítulo 50 é rejeitada ainda que não a esteja a estudar. "
         "<b>Marcada</b>, só contam os capítulos 1-39 e essa palavra é "
         "mostrada.<br>"
         "Em ambos os casos, <b>cada resultado é um versículo do seu "
         "programa</b>. Esta definição apenas retira resultados; nunca o envia "
         "para outro lado."),
        ("Duas vezes, três vezes — não só os hápax",
         "<b>Aparece no máximo</b> decide o que é suficientemente raro. Com 1 "
         "obtém os hápax verdadeiros: palavras e expressões que ocorrem "
         "exatamente uma vez. Com 2 obtém também as que ocorrem exatamente "
         "duas vezes, com 3 três vezes, e assim por diante.<br>"
         "As contagens junto de cada entrada indicam quantas ocorrências há, "
         "pelo que se vê num relance se uma palavra ocorre uma ou duas vezes. "
         "Serão dadas todas as referências necessárias.<br>"
         "A opção <b>apenas expressões mínimas</b> segue o mesmo limiar: com 2, "
         "uma expressão só é mantida se as suas partes mais curtas ocorrerem "
         "mais de duas vezes."),
        ("Expressões, não só palavras",
         "Marque os comprimentos 1 a 5: a aplicação procura tanto uma palavra "
         "isolada como uma sequência de duas, três, quatro ou cinco palavras "
         "consecutivas.<br>"
         "Deixe <b>apenas expressões mínimas</b> ligado. Sem isso quase toda a "
         "expressão longa é trivialmente única: se uma palavra já é única, "
         "também o é qualquer expressão que a contenha. A opção mantém apenas "
         "as expressões únicas cujas partes mais curtas <i>não</i> o são.<br>"
         "<b>Cada palavra ocorre ≥ N</b> mantém apenas as expressões cujas "
         "palavras são <i>todas</i> frequentes: com 50, cada palavra da "
         "expressão ocorre pelo menos 50 vezes no Tanach. O surpreendente passa "
         "a ser a expressão e não o vocabulário — muitas vezes as melhores "
         "perguntas."),
        ("Comparar por",
         "O que conta como «a mesma palavra»:"
         "<ul>"
         "<li><b>Forma escrita</b> (predefinição) — só letras, sem vogais.</li>"
         "<li><b>Com vogais</b> — mais estrito.</li>"
         "<li><b>Raiz</b> — todas as formas de uma mesma raiz contam como uma "
         "só palavra. Procura portanto <i>raízes</i> únicas e não formas: muito "
         "mais raro e muito mais difícil.</li>"
         "</ul>"),
        ("Exportar",
         "Pode exportar os resultados da sua pesquisa como PDF. O PDF abre com "
         "uma página inicial que recorda as suas definições e os totais por "
         "livro, e depois os resultados agrupados por capítulo em colunas. "
         "Opcional: o <b>versículo completo</b> sob cada entrada com a palavra "
         "a negrito, um <b>índice alfabético</b> e uma <b>folha de "
         "exercícios</b> com soluções à parte.<br>"
         "Há também <b>HTML</b> e <b>CSV</b>; o CSV abre no Excel e presta-se a "
         "outros usos, por exemplo se quiser reutilizar os resultados noutro "
         "projeto de programação."),
        ("Numeração dos versículos",
         "As edições impressas e o manuscrito de Leninegrado numeram alguns "
         "capítulos de forma diferente — sobretudo o Decálogo. Escolha "
         "<b>Edições impressas</b> para seguir um Koren, ou <b>Leninegrado</b> "
         "para seguir a maioria dos programas. Muda apenas as referências, "
         "nunca os resultados."),
        ("O separador de raízes",
         "Não confundir com a definição “Comparar por → Raiz”, que diz respeito "
         "à própria pesquisa. Este separador é um dicionário: escreve uma "
         "palavra e mostra-lhe onde essa raiz aparece, sem relançar a pesquisa. "
         "Prático para confirmar uma intuição sobre uma palavra concreta."),
        ("De onde vem o texto",
         "O Códice de Leninegrado (WLC), via Open Scriptures Hebrew Bible — 39 "
         "livros, 23 213 versículos, 305 531 palavras, com vogais e "
         "cantilação. O texto está incluído na aplicação; nada é transferido e "
         "nada do que escreve sai do seu computador.<br>"
         "Software livre sob licença GPL; o texto do Tanach mantém a sua "
         "licença CC-BY. Os PDF que produzir pertencem-lhe."),
    ],

    # ------------------------------------------------------------ Russian
    "ru": [
        ("В одном предложении",
         "Вы вводите материал, который учите; программа показывает, какие слова "
         "и выражения встречаются в нём только один раз, и выдаёт PDF для "
         "занятий или раздачи."),
        ("Три шага",
         "<ul>"
         "<li><b>1.</b> Введите или вставьте материал в большое поле слева "
         "вверху — или выберите книгу и главы и нажмите <b>Добавить</b>.</li>"
         "<li><b>2.</b> Нажмите <b>Найти гапаксы</b>. Несколько секунд, даже "
         "для всего Танаха.</li>"
         "<li><b>3.</b> Нажмите <b>Сохранить PDF…</b>.</li>"
         "</ul>"
         "Всё остальное — по желанию."),
        ("Как записать материал",
         "Записывайте так, как напечатано на официальном листе: "
         "<code>יהושע: א-יב</code>, <code>שמואל א: א-טו; יז-כ</code>. Подходят "
         "и еврейские буквы, и цифры, и обычные сокращения. По одной книге в "
         "строке; для целой книги номера глав не нужны вовсе. Названия книг можно писать на иврите, английском, французском, испанском, португальском или русском, с диакритикой или без.<br>"
         "Под полем показано, <b>сколько глав, стихов и слов</b> распознано. "
         "Если строка не читается или название книги не распознано, прямо под "
         "полем появляется предупреждение с указанием этой строки: ничего не "
         "отбрасывается без уведомления."),
        ("Уникально внутри чего?",
         "Самая важная настройка. Слово может быть уникальным в одном отрывке и "
         "обычным в другом:"
         "<ul>"
         "<li><b>Весь Танах</b> — настоящий гапакс, один раз на все 305 531 "
         "слово.</li>"
         "<li><b>Материал</b> — один раз в том материале, который вы "
         "ввели.</li>"
         "<li><b>Своя книга</b> — уникально внутри книги. То есть слово может "
         "встречаться в материале несколько раз, но если оно уникально в одной "
         "из книг, оно будет показано. Это позволяет отвечать на вопросы вида: "
         "«Где в такой-то книге встречается такое-то слово?».</li>"
         "<li><b>Раздел</b> — уникально внутри раздела Танаха: Тора, Невиим, "
         "Невиим Ришоним, Невиим Ахароним, Трей Асар, Ктувим…</li>"
         "<li><b>Указанный вами диапазон</b> — уникально внутри этого "
         "диапазона, записанного как материал, например "
         "<code>ישעיהו א-לט</code>.</li>"
         "</ul>"),
        ("…вся книга или только моя часть?",
         "Флажок под меню «Уникально внутри» решает, считаются ли главы, "
         "которые вы не указали в материале.<br>"
         "Пример: материал <code>ישעיהו א-לט</code>. <b>Снят</b> — слово должно "
         "встречаться один раз во всех 66 главах, и слово, повторяющееся в "
         "главе 50, отбрасывается, хотя вы её не учите. <b>Установлен</b> — "
         "считаются только главы 1-39, и это слово показывается.<br>"
         "В обоих случаях <b>каждый результат — стих внутри вашего "
         "материала</b>. Настройка только убирает результаты и никогда не "
         "отправляет вас в другое место."),
        ("Дважды, трижды — не только гапаксы",
         "<b>Встречается не более</b> решает, что считать достаточно редким. "
         "При 1 вы получаете настоящие гапаксы: слова и выражения, "
         "встречающиеся ровно один раз. При 2 — также те, что встречаются "
         "ровно дважды, при 3 — трижды, и так далее.<br>"
         "Числа рядом с каждой записью показывают, сколько всего вхождений, "
         "так что сразу видно, встречается слово один раз или два. Все "
         "необходимые ссылки будут указаны.<br>"
         "Настройка <b>только минимальные выражения</b> использует тот же "
         "порог: при 2 выражение сохраняется, только если его более короткие "
         "части встречаются более двух раз."),
        ("Выражения, а не только слова",
         "Отметьте длины от 1 до 5: программа ищет и отдельное слово, и цепочку "
         "из двух, трёх, четырёх или пяти подряд идущих слов.<br>"
         "Оставьте <b>только минимальные выражения</b> включённым. Без этого "
         "почти любое длинное выражение уникально тривиально: если слово уже "
         "уникально, уникально и любое выражение с ним. Настройка оставляет "
         "только те выражения, чьи более короткие части <i>не</i> "
         "уникальны.<br>"
         "<b>Каждое слово встречается ≥ N</b> оставляет только выражения, все "
         "слова которых частотны: при 50 каждое слово выражения встречается в "
         "Танахе не менее 50 раз. Тогда удивительно само выражение, а не его "
         "лексика — часто это лучшие вопросы."),
        ("Сравнивать по",
         "Что считается «тем же словом»:"
         "<ul>"
         "<li><b>Написание</b> (по умолчанию) — только буквы, без "
         "огласовок.</li>"
         "<li><b>С огласовками</b> — строже.</li>"
         "<li><b>Корень</b> — все формы одного корня считаются одним словом. "
         "Ищутся, таким образом, уникальные <i>корни</i>, а не формы: гораздо "
         "реже и гораздо труднее.</li>"
         "</ul>"),
        ("Экспорт",
         "Результаты поиска можно выгрузить в PDF. PDF открывается титульной "
         "страницей с вашими настройками и итогами по книгам, затем идут "
         "результаты, сгруппированные по главам в колонках. По желанию: "
         "<b>полный стих</b> под каждой записью с выделенным словом, "
         "<b>алфавитный указатель</b> и <b>лист для тренировки</b> с "
         "отдельными ответами.<br>"
         "Есть также <b>HTML</b> и <b>CSV</b>; CSV открывается в Excel и "
         "подходит для других задач, например если вы захотите использовать "
         "результаты в другом программном проекте."),
        ("Нумерация стихов",
         "Печатные издания и Ленинградский кодекс нумеруют несколько глав "
         "по-разному — прежде всего Десятисловие. Выберите <b>печатные "
         "издания</b>, чтобы совпадало с изданием Корен, или "
         "<b>Ленинградский</b>, чтобы совпадало с большинством программ. "
         "Меняются только ссылки, но не результаты."),
        ("Вкладка поиска корней",
         "Не путать с настройкой «Сравнивать по → Корень», которая касается "
         "самого поиска. Эта вкладка — словарь: вводите слово, и она "
         "показывает, где встречается его корень, не перезапуская поиск. "
         "Удобно проверить догадку об одном конкретном слове."),
        ("Откуда взят текст",
         "Ленинградский кодекс (WLC) через проект Open Scriptures Hebrew Bible "
         "— 39 книг, 23 213 стихов, 305 531 слово, с огласовками и "
         "кантилляцией. Текст входит в состав программы; ничего не "
         "скачивается и ничего из введённого вами не покидает компьютер.<br>"
         "Свободная программа под лицензией GPL; текст Танаха остаётся под "
         "своей лицензией CC-BY. Созданные вами PDF принадлежат вам."),
    ],
}


def guide(lang: str) -> list[tuple[str, str]]:
    return GUIDE.get(lang) or GUIDE["en"]
