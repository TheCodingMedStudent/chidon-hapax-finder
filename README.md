# Chidon HaTanach — Hapax Finder

Finds every word and every short phrase that occurs **only once**, for whatever
syllabus (חומר הבחינה) you give it, and prints the whole list with references
as a PDF.

That's the classic Chidon question — *"היכן מופיעה המילה הזאת?"* — and until now
the only way to prepare for it was to already know the text by heart.

---

## Install

Python 3.10 or newer.

```bash
pip install PyQt6
python run.py
```

That's the only dependency. The Tanach text is bundled
(`chidon_hapax/data/tanach.json.gz`, 1.5 MB), so it works offline from the first
launch. If that file ever goes missing the app shows a **Download the Tanach
text** button that fetches and rebuilds it (≈20 MB, once).

---

## Paste the syllabus exactly as it's published

The parser reads the format official syllabi are printed in — headings,
bracketed chapter counts, `סך הכל` lines and all. Paste it, or open the `.txt`:

```
חומר חידון התנ׳׳ך העולמי תשפ׳׳ז
בראשית (50)
שמות: א-כד, לב-לד (27)
במדבר: י-יז, כ-כז, לא-לד (20)
סך הכל: 113
זכריה א-ד; יא-יד(8)
איוב: א-ה, ח, יא, לב, מב(9)
דברי הימים ב: יא-טז, יט-כא(9)
סך הכל כל החומר: 449 פרקים
```

Handled: Hebrew or English book names, gematria or digits, `:` after the book
name, comma and `;` separated ranges on one line, verse-level ranges
(`שמואל א טז:א-יז:נח`, `מלכים ב יח:יג-כ`), abbreviations (`שמו"א`, `דהי"ב`),
`#` comments. Headings and anything unrecognisable are skipped and listed, so
nothing disappears silently.

### It checks the syllabus against itself

The number in brackets is compared with the chapters actually selected, and
each `סך הכל` with the lines above it. On the תשפ״ז sheet above that check
reports:

```
✓ 448 chapters · 11,521 verses · 169,833 words
⚠ line 43 (“דברי הימים א: כח-כט”): the syllabus says 3 chapters, this selects 2
⚠ line 45: “סך הכל: 87” — the lines above it select 86 chapters
⚠ line 46: “סך הכל כל החומר: 449 פרקים” — the whole syllabus parses to 448
```

Which is correct: כח-כט is two chapters, not three, so that one printed line
and every total downstream of it are off by one. Worth resolving with whoever
published it before you study from it — the missing chapter is probably כז or ל.

---

## Languages and appearance

The interface is available in **English, עברית, Français, Español, Português
and Русский** — pick one from the top-right corner; it applies instantly, is
remembered between sessions, and in Hebrew the whole window mirrors to
right-to-left. Everything is translated, including the parser's own complaints
about your syllabus and the labels inside the PDF. The biblical text itself is
of course always Hebrew.

Add a seventh language by adding a code to `LANGUAGES` and one line per entry
in `chidon_hapax/i18n.py`; anything you leave out falls back to English.

The **i** button beside the language picker opens an About box with the
version, the text and lexicon credits, the licence and the copyright line.
Put your own name in `__author__` at the top of `chidon_hapax/__init__.py` and
it appears there; the same file holds the version, licence, an optional project
URL, and `BSD`, the בס״ד printed at the top right of the window, the About box
and the PDF cover (set it to `""` to leave it out).

The look comes from `chidon_hapax/style.qss` — edit that file to restyle the
app without touching any Python.

---

## Roots (שורשים)

Two features, both built on the Strong's lemma that the Open Scriptures text
carries for every word (98% coverage; the rest falls back to the written form).

**Compare by → Root / dictionary word.** Two words count as "the same" when
they share a dictionary entry, so a hapax means *the root itself* occurs only
once in the Tanach. On the תשפ״ז syllabus that turns 9,990 written-form hapaxes
into **1,240 truly unique words** — גֹּפֶר, בְּזֵעַת, פִּישׁוֹן, יוּבָל — a far more
studiable list, and closer to what the Chidon means by מילה יחידאית. The Root
column in the results and the detail pane show the dictionary form and its
gloss.

**The Root search tab.** Type a word as it appears (ויאמר), a dictionary form,
a bare root (שפט) or a Strong's number (8199), and get every occurrence with
its reference and surrounding words. A checkbox limits the list to the
syllabus. Searching שפט finds both שָׁפַט "judge" (202 occurrences, 111 in this
syllabus) and the name שָׁפָט (8 / 5), listed separately.

---

### The whole Tanach in one tick

A **Whole Tanach** checkbox under the syllabus box fills it with all 39 books —
929 chapters, 23,213 verses — without typing anything. Unticking restores
whatever you had before, so it costs nothing to try.

Searching everything is heavier than a normal syllabus but still quick: single
words take about 3 seconds, all five phrase lengths about 6, peaking around
340 MB. Every word in the Tanach that occurs exactly once: 20,480 of them.

## Unique **within what?** — five answers

The single most useful setting. A word can be unique in one span of text and
ordinary in another, and each of those is a real Chidon question.

* **The whole Tanach** (default) — the true hapax legomenon: once in all
  305,531 words, and that once is inside your syllabus.
* **The syllabus** — once in your material, though it may be common elsewhere.
* **Its own book** — once in the book it appears in. With a syllabus spanning
  several books you get a separate answer per book in one pass: יונה yields its
  305 book-unique words, עמוס its 803, side by side.
* **A section of the Tanach** — תורה, נביאים, נביאים ראשונים, נביאים אחרונים,
  תרי עשר, כתובים, ספרי אמ״ת, חמש מגילות.
* **A range you type** — same syntax as the syllabus, e.g. `ישעיהו א-לט`, so
  "unique in First Isaiah" or "unique in Sefer Shmuel" is one line of typing.

### …the whole book, or only my part of it?

Under the scope box sits a checkbox: **"…but only the part of it that is in my
syllabus."** It decides whether chapters you did not list are counted.

Say your syllabus is ישעיהו א-לט and the scope is "its own book":

* **Unchecked** — a word must occur once in all 66 chapters. Chapters 40-66 are
  counted even though you are not studying them, so a word appearing in both
  chapter 5 and chapter 50 is rejected. Stricter: 2,883 words.
* **Checked** — only chapters 1-39 are counted. That same word is now reported,
  because within your material it does occur just once. 3,311 words.

Either way **every result is a verse inside your syllabus.** The scope only ever
removes results; it never sends you to a chapter you are not studying.

The checkbox matters most with several books: it is the only way to ask for
"unique within my part of Yeshayahu" and "unique within my part of Yirmiyahu"
separately in one run. It is hidden for the whole-Tanach scope (which must not
be restricted) and for the syllabus scope (which already is).

Everything else still applies: phrase lengths 1–5, the minimal rule, the
frequency floor and root comparison all work in every scope. A two-word phrase
occurring once in Nevi'im Rishonim is found the same way as one occurring once
in the whole Tanach.

The results table keeps showing the Tanach-wide count alongside, so you can see
at a glance that a word unique in its section appears, say, twenty times
elsewhere.

---

## Why phrases need the "minimal" rule

Almost every 5-word window in the Tanach is unique. A naive list of unique
5-grams would return nearly your whole syllabus and tell you nothing.

So the app reports only **minimal** unique phrases: unique **and neither of its
two shorter sub-phrases is already unique**. It's the shortest window at that
spot that pins the location down — drop a word from either end and it stops
identifying. That's exactly what a question can be built on.

---

## The other knob that matters

**"In phrases, each word occurs ≥ N"** drops phrases that are only unique
because they happen to contain a rare word. Set it to 50 and what's left are
phrases built entirely from ordinary words whose *combination* occurs once.
Single words are never filtered by it (a hapax occurs once by definition).

Measured on the full תשפ״ז syllabus (449 chapters, 169,833 words, 2.1 seconds):

| floor | 1 word | 2 words | 3 words | 4 words | 5 words |
|---|---|---|---|---|---|
| 1 (off) | 9,990 | 63,347 | 16,841 | 2,051 | 316 |
| 50 | 9,990 | 11,268 | 8,349 | 1,138 | 143 |
| 200 | 9,990 | 2,182 | 2,937 | 479 | 57 |

63,347 two-word phrases is the honest answer and a useless PDF. A practical
study pack for a syllabus this size: single words on their own (214 pages,
three columns), and phrases of 4–5 words with the floor at 50 (101 pages).
Both are included here as samples, along with a root-level list.

---

## Options in full

| Option | What it does |
|---|---|
| Unique within | Whole Tanach, the syllabus, its own book, a named section, or a range you type. |
| …only my part of it | Whether chapters outside your syllabus are counted. |
| Compare by | **Root** (dictionary word), **Consonants only** (default — ignores nikkud), **+ nikkud**, or **+ te'amim**. Stricter comparison ⇒ more things count as unique. |
| Phrase lengths 1–5 | Tick what you want. Each length is a section in the PDF and a tab in the app. |
| Minimal phrases only | The rule above. Leave it on; the app warns you if you switch it off. |
| Across a verse boundary | Lets a phrase run from the end of one verse into the next. Off by default. |
| Print the full verse | The whole pasuk under each entry with the hapax in bold. Switches the layout to one entry per line, so roughly triples the page count. |
| Alphabetical index | Appendix of every single-word hapax sorted א→ת with its reference. **This is the one to study from**: read the word, try to recall the place. |
| Practice sheet | Numbered phrases with a blank for the reference, answer key on later pages. |
| Hebrew letters | פרק:פסוק as gematria (default) or digits. |
| Verse numbers | **Leningrad Codex** (default, matching the bundled text) or **printed editions** (Koren, Mamre). See below. |

---

## Verse numbering — why your printed Tanach may disagree

The bundled text is the Westminster Leningrad Codex, which numbers the
Decalogue by *ta'am tachton*: לֹא תִּרְצָח, לֹא תִּנְאָף and לֹא תִּגְנֹב each get
their own verse. Printed Hebrew Bibles use *ta'am elyon*, which puts them
together, so from the middle of Exodus 20 and Deuteronomy 5 their numbers run
lower. Two other places differ as well.

**Exactly four chapters are affected. Every other chapter of all 39 books is
identical in both schemes**, so this changes references only — never which
words are hapaxes.

| | Leningrad (default) | Printed editions |
|---|---|---|
| לֹא תִרְצָח | Exodus 20:13 | Exodus 20:12 |
| לֹא תַחְמֹד | Exodus 20:17 | Exodus 20:13 |
| end of Exodus 20 | 20:26 | 20:22 |
| לֹא תִרְצָח | Deuteronomy 5:17 | Deuteronomy 5:16 |
| end of Deuteronomy 5 | 5:33 | 5:29 |
| וַיְהִי אַחֲרֵי הַמַּגֵּפָה | Numbers 25:19 | Numbers 26:1 |
| end of Joshua 21 | 21:45 | 21:43 |

Joshua 21:36-37 (the Levitical cities of Reuben) are a special case: they are
in the Leningrad Codex but absent from most printed editions — Radak writes
that he never saw these two verses in any accurate old manuscript. In printed
mode they are marked with an asterisk, and the rest of the chapter runs two
verses lower.

Switch with **Verse numbers** in the Report box. The choice is remembered, it
applies to the results table and the PDF alike, and the PDF cover records which
scheme it used.

---

## In the app

Type or paste the syllabus on the left; the line underneath turns green with
the chapter/verse/word count, amber for count mismatches, red for a range it
can't read (*"יהושע has 24 chapters"*). There's a book picker if you'd rather
click. Press **Find hapaxes**, browse the results in the tabs on the right —
clicking a row shows the full verse with the phrase highlighted — then
**Save PDF**, or export HTML or CSV.

---

## The PDF

Produced by Qt itself, so Hebrew shaping, nikkud placement and RTL layout are
correct with no extra library. Cover page with the syllabus and every setting
used, totals per length and per book, then one section per length grouped by
book and chapter, then the optional index and practice sheet. Single words
print three to a row and two-word phrases two to a row, filled right-to-left.
Page numbers in the footer.

---

## Files

```
run.py                        launcher
chidon_hapax/
    app.py                    the PyQt6 window
    engine.py                 the hapax / minimal-phrase engine
    corpus.py                 loading, Hebrew normalisation, gematria
    syllabus.py               syllabus parser + count checking
    numbering.py              the two verse-numbering schemes
    sections.py               the canonical divisions of the Tanach
    paths.py                  file locations, source or frozen bundle
    help_text.py              the in-app guide, six languages
    icons/                    app icon, .ico and .icns included
    report.py                 HTML document, PDF/CSV export
    i18n.py                   the six interface languages
    style.qss                 the theme — edit to restyle
    build_corpus.py           downloads and rebuilds the text file
    data/tanach.json.gz       the bundled Tanach + lemmas + lexicon
examples/
    chidon_5787.txt           the full תשפ״ז syllabus
    yehoshua.txt, neviim_rishonim.txt
```

## Text

Open Scriptures Hebrew Bible — a morphologically tagged Westminster Leningrad
Codex, CC-BY 4.0, <https://github.com/openscriptures/morphhb>. 39 books, 23,213
verses, 305,531 words. Words joined by maqqef are counted separately, as the
Chidon does. Where there's a ketiv/qere the qere (the reading) is used; the
ketiv is kept in the data. Rebuild any time with
`python -m chidon_hapax.build_corpus`.

Roots come from the same project's Strong's lemma tagging, with the Hebrew
dictionary forms and glosses taken from the Open Scriptures
[HebrewLexicon](https://github.com/openscriptures/HebrewLexicon) (Strong's,
public domain), bundled into the same file.

Counts were verified against brute-force recounts: אשר 4,837 · הארץ 935 ·
בראשית 5. Just over half of all consonantal word-forms in the Tanach (20,480 of
39,527) occur exactly once.

## Installing it — and the warnings you will see

The apps are not signed with a paid developer certificate, so both operating
systems warn about them. Nothing is wrong: the warnings say *"we cannot verify
who made this"*, not *"this is dangerous"*. The steps below are what to tell
anyone you pass it to.

### macOS

Open the `.dmg` and drag **Hapax Finder** to Applications. The first time you
open it you get:

> **"Hapax Finder" Not Opened**
> Apple could not verify "Hapax Finder" is free of malware that may harm your
> Mac or compromise your privacy.

with a single **Done** button and no visible way forward. This stops most
people, so it is worth spelling out:

1. Click **Done**.
2.  → **System Settings** → **Privacy & Security**.
3. Scroll down. A line has appeared: *"Hapax Finder" was blocked to protect
   your Mac*, with an **Open Anyway** button beside it.
4. Click **Open Anyway** and authenticate.
5. Click **Open Anyway** once more in the dialog that follows.

That is only needed once; afterwards it opens normally.

**The order matters.** The Open Anyway button appears only *after* you have
tried to open the app and been refused, and it disappears again after about an
hour. Approving it in advance is not possible. On macOS Sequoia and later, the
old trick of right-clicking the app and choosing Open no longer works either.

### Windows

Download the `.zip` and **extract it before running anything**. Windows itself
warns about this:

> **This application may depend on other compressed files in this folder.**
> For the application to run properly, it is recommended that you first extract
> all files.

Click **Extract all**. The warning is correct — the program is a folder of
files, not a single executable, and running it from inside the zip will fail.

Then open the extracted folder and run **Hapax Finder.exe**. You may then meet
SmartScreen, in one of two blue dialogs. Which one depends on whether the
machine can reach Microsoft's reputation service, and some people will see
neither, because SmartScreen can be switched off.

**"Windows protected your PC"** — the usual one, on a machine with a working
connection. The only obvious buttons are *Don't run* and *Close*; the way
forward hides behind the small **More info** link. Click that, then
**Run anyway**.

**"SmartScreen can't be reached right now"** — when the machine is offline or
behind a restrictive network:

> Check your Internet connection. Microsoft Defender SmartScreen is unreachable
> and can't help you decide if this app is ok to run.
> Publisher: Unknown Publisher · File Type: .exe · App: Hapax Finder.exe

This one offers **Run** and **Don't Run** directly. Click **Run**.

"Unknown Publisher" is simply the absence of a paid code-signing certificate,
not a judgement about the program.

An antivirus may also flag it. This is a false positive, and a common one: a
Python program packaged this way looks structurally similar to some malware, in
that a launcher unpacks and runs bundled code. Nothing is downloaded, nothing is
installed, and the whole source is in this repository for anyone who wants to
check.

### Why not just sign it?

Signing costs $99 a year for an Apple Developer ID, plus notarisation for every
release, and a separate certificate for Windows. For a program given free to
friends that is hard to justify. The trade is real though: unsigned software
asks the people you give it to to trust you personally rather than trust a
certificate.

## Building the apps

The program runs from source with `python run.py` on any platform with Python
3.10+ and PyQt6. What follows produces the standalone `.exe` and `.app`.

```
pip install pyinstaller
pyinstaller chidon_hapax.spec
```

That produces `dist/Hapax Finder/` on Windows and `dist/Hapax Finder.app` on
macOS. Check the result without a screen:

```
"dist/Hapax Finder/Hapax Finder" --selftest                       # Windows
"dist/Hapax Finder.app/Contents/MacOS/Hapax Finder" --selftest    # macOS
```

It loads the bundled corpus, runs a known analysis (Jonah must yield exactly 49
hapaxes) and checks every packaged resource, then prints `SELFTEST PASSED`. If a
data file failed to reach the bundle, this catches it.

**You cannot cross-compile.** A Windows `.exe` must be built on Windows and a
macOS `.app` on macOS, and the architecture matters too: a build made on an
Apple-silicon Mac, including inside an ARM Windows virtual machine, will not run
on an ordinary Intel/AMD Windows PC.

### macOS: two builds, not one universal app

`PyQt6-Qt6` — the Qt libraries themselves, and most of the bundle's weight — is
published as separate `x86_64` and `arm64` wheels, with no `universal2` wheel.
PyInstaller cannot fuse a universal app out of single-architecture libraries, so
**`target_arch="universal2"` will fail.** Build once per architecture:

| Mac | runner in CI |
| --- | --- |
| Apple silicon (M1 and later, 2020+) | `macos-14` |
| Intel (2019 and earlier) | `macos-15-intel` |

An Intel build does run on Apple silicon through Rosetta 2, so a single Intel
build would cover every Mac — but users without Rosetta get an install prompt at
first launch. Publishing both and labelling them clearly is kinder.

### Choices made in the spec

* `--onedir`, not `--onefile`. A single-file executable unpacks itself to a
  temporary folder on every launch: slower to start, and the behaviour most
  antivirus heuristics treat as suspicious.
* No UPX compression, for the same reason.
* Qt's WebEngine, QML, Quick and Multimedia are excluded; none are used, and
  they account for most of the weight otherwise.
* `version_info.txt` fills in Windows' Properties → Details. An executable with
  no publisher information looks *more* suspicious to SmartScreen, not less.

## Publishing

[`PUBLISHING.md`](PUBLISHING.md) walks through putting this on GitHub and
producing the three downloads, written for someone who has not used git before.

`.github/workflows/build.yml` builds all three on GitHub's machines — Windows
x64, macOS Apple Silicon, macOS Intel — and each build must pass `--selftest`
*inside the packaged app* before it can be published. Pushing a tag beginning
with `v` creates a draft release with the files attached.

## The built-in guide

People who run the packaged app never see this README, so the program carries
its own guide: an eleven-section walkthrough in all six interface languages,
reached from **How it works** in the header. It opens by itself on first run;
the checkbox at the bottom of it controls whether it opens every time, and the
button brings it back whenever you want it.

## Which corpus gets used

The Tanach text ships inside the program. The **Download Tanach text** button
rebuilds it from the Open Scriptures source into your own data folder
(`%APPDATA%\ChidonHapaxFinder` on Windows, `~/Library/Application
Support/ChidonHapaxFinder` on macOS) — never into the program folder, which is
read-only inside a `.app` or under Program Files.

When both exist, the program picks between them by the corpus's format version:

* Bundled version **newer** than yours → the bundled one wins, so a corpus fix
  shipped in an update reaches people who rebuilt once, instead of staying
  invisible on their machine forever.
* Same version → **yours** wins. You rebuilt deliberately, and that stands.
* Your file unreadable or truncated → the bundled one, silently.

`CORPUS_FORMAT_VERSION` in `corpus.py` is the single place that number lives;
`build_corpus.py` stamps it into every corpus it writes. Bump it whenever you
change how the corpus is generated.

## Licence

Copyright (C) 2026 Daniel Mechoulan.

This program is free software under the **GNU General Public License, version 3
or later**. You may use it, study it, share it and change it. The one condition
that matters: if you distribute it, or anything built from it, you must do so
under the GPL as well and make the source available. That keeps it free for
everyone downstream — nobody can take this, close it, and sell it.

The full text is in [`LICENSE`](LICENSE).

The GPL is also required here rather than merely chosen: the program is built on
PyQt6, which is itself GPL-3.0, so any binary containing it has to be.

### The Hebrew text is licensed separately

The bundled Tanach is the Westminster Leningrad Codex as published by the
[Open Scriptures Hebrew Bible](https://github.com/openscriptures/morphhb)
project, under **CC-BY 4.0**, and it stays under those terms — the GPL does not
and cannot apply to it. Root and gloss data come from
[HebrewLexicon](https://github.com/openscriptures/HebrewLexicon) (Strong's,
public domain).

As CC-BY requires: *the text has been modified.* The OSIS XML was parsed into a
compressed JSON corpus, with qere readings preferred, maqqef-joined words
counted separately, and a Strong's lemma attached to each word. The text itself
was not altered.

### What you produce is yours

The PDFs, HTML and CSV files this program generates belong to you. The GPL
covers the program, not its output, so you may share study sheets with anyone,
in any way, including for money.

## Known limits

* Peak memory ≈ 225 MB on the largest runs; a full-syllabus search takes about
  two seconds.
* By default, matching is on word forms as written, so וַיֹּאמֶר and אָמַר are
  different words — the right behaviour for the Chidon, which asks about the
  word as it appears. Switch **Compare by** to Root when you want the other
  behaviour.
* The frequency floor and the "minimal" rule are the two things to reach for
  when a report comes out too long.
