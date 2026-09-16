"""Chidon HaTanach — hapax finder.  PyQt6 desktop app."""

from __future__ import annotations

import os
import sys
import traceback

from PyQt6.QtCore import QSize, QObject, QSettings, Qt, QThread, pyqtSignal
from PyQt6.QtGui import QIcon, QFont, QTextOption
from PyQt6.QtWidgets import (QApplication, QCheckBox, QComboBox, QDialog,
                             QFileDialog, QFormLayout, QGroupBox, QHBoxLayout,
                             QHeaderView, QLabel, QLineEdit, QMessageBox,
                             QPlainTextEdit, QProgressBar, QPushButton,
                             QRadioButton, QSpinBox, QScrollArea, QSplitter, QTableWidget,
                             QTableWidgetItem, QTabWidget, QTextBrowser,
                             QVBoxLayout, QWidget)

from . import help_text, paths, sections
from . import (BSD, __author__, __license__, __url__, __version__,
               __year__, numbering, report)
from .corpus import (USER_CORPUS_PATH, LEVELS, Corpus, corpus_exists,
                     load_corpus)
from .engine import Options, analyze
from .i18n import LANGUAGES, current_language, is_rtl, set_language, tr
from .syllabus import (SyllabusError, collect_verses, describe,
                       parse_syllabus_full)

HE_FONTS = ("'Taamey Frank CLM','SBL Hebrew','David','Frank Ruehl CLM',"
            "'Times New Roman','Arial Hebrew','Noto Serif Hebrew',FreeSerif,serif")
STYLE_PATH = paths.resource("style.qss")
MAX_ROOT_ROWS = 3000


def app_icon() -> QIcon:
    """The window / taskbar icon, at every size the platform may ask for."""
    icon = QIcon()
    for size in (16, 24, 32, 48, 64, 128, 256, 512, 1024):
        path = paths.resource("icons", f"icon_{size}.png")
        if os.path.exists(path):
            icon.addFile(path, QSize(size, size))
    return icon


def load_stylesheet() -> str:
    try:
        with open(STYLE_PATH, encoding="utf-8") as f:
            return f.read()
    except OSError:
        return ""


class Worker(QObject):
    progress = pyqtSignal(float, str)
    finished = pyqtSignal(object)
    failed = pyqtSignal(str)

    def __init__(self, fn):
        super().__init__()
        self.fn = fn

    def run(self):
        try:
            self.finished.emit(self.fn(lambda f, m: self.progress.emit(f, m)))
        except Exception:
            self.failed.emit(traceback.format_exc())


class HelpDialog(QDialog):
    """A plain-language guide, for people who never open the README."""

    def __init__(self, parent=None, settings=None):
        super().__init__(parent)
        self.settings = settings
        self.setWindowTitle(tr("help.title"))
        self.setMinimumSize(660, 620)
        self.setLayoutDirection(Qt.LayoutDirection.RightToLeft if is_rtl()
                                else Qt.LayoutDirection.LeftToRight)
        lay = QVBoxLayout(self)
        lay.setContentsMargins(0, 0, 0, 0)
        lay.setSpacing(0)

        view = QTextBrowser()
        view.setObjectName("Help")
        view.setOpenExternalLinks(True)
        view.document().setDefaultStyleSheet(
            "h1{font-size:19px;margin:0 0 4px 0;}"
            "h2{font-size:15px;margin:20px 0 4px 0;color:#1f4e79;}"
            "p,li{font-size:13px;line-height:150%;}"
            "code{background:#f0ece3;}"
            "ul{margin-top:2px;}")
        align = "right" if is_rtl() else "left"
        parts = [f'<div align="{align}"><h1>{tr("app.title")}</h1>']
        for head, body in help_text.guide(current_language()):
            parts.append(f"<h2>{head}</h2><p>{body}</p>")
        parts.append("</div>")
        view.setHtml("".join(parts))
        lay.addWidget(view, 1)

        bar = QHBoxLayout()
        bar.setContentsMargins(14, 10, 14, 12)
        self.again = QCheckBox(tr("help.again"))
        if settings is not None:
            self.again.setChecked(
                settings.value("help_at_startup", "no") == "yes")
            self.again.toggled.connect(
                lambda on: (settings.setValue("help_at_startup",
                                              "yes" if on else "no"),
                            settings.sync()))
        bar.addWidget(self.again)
        bar.addStretch(1)
        close = QPushButton(tr("help.close"))
        close.setObjectName("Primary")
        close.clicked.connect(self.accept)
        bar.addWidget(close)
        lay.addLayout(bar)


class AboutDialog(QDialog):
    """Small credits box: what this is, which text it uses, who made it."""

    def __init__(self, parent=None, corpus=None):
        super().__init__(parent)
        self.setWindowTitle(tr("about.button"))
        self.setMinimumWidth(560)
        v = QVBoxLayout(self)
        v.setContentsMargins(20, 18, 20, 16)
        v.setSpacing(10)

        title = QLabel(tr("app.title"))
        title.setObjectName("Heading")
        title.setWordWrap(True)
        bsd = QLabel(BSD)
        bsd.setObjectName("Bsd")
        bsd.setVisible(bool(BSD))
        trow = QHBoxLayout()
        trow.addWidget(title, 1)
        trow.addWidget(bsd, 0, Qt.AlignmentFlag.AlignTop)
        if is_rtl():                       # keep it at the top *right* either way
            trow.insertWidget(0, bsd, 0, Qt.AlignmentFlag.AlignTop)
        v.addLayout(trow)

        sub = QLabel(tr("about.version", v=__version__))
        sub.setObjectName("Status")
        v.addWidget(sub)

        body = QTextBrowser()
        body.setOpenExternalLinks(True)
        body.setMinimumHeight(340)
        stats = ""
        if corpus is not None:
            stats = "<p>" + tr("about.corpus", books=f"{len(corpus.books)}",
                               verses=f"{len(corpus.verses):,}",
                               words=f"{corpus.total_words():,}") + "</p>"
        if __author__:
            who = f"<p>© {__year__} {_esc_html(__author__)}</p>"
        else:
            who = (f"<p style='color:#8a8681'>© {__year__} · "
                   f"{tr('about.noAuthor')}</p>")
        link = (f"<p><a href='{__url__}'>{__url__}</a></p>") if __url__ else ""
        license_line = (f"<p>{tr('about.license', license=__license__)}</p>"
                        if __license__ else "")
        body.setHtml(f"""
            <div style='font-size:10.5pt; color:#27313f'>
              <p>{tr('about.tagline')}</p>
              <p><b>{tr('about.textHeading')}</b><br>{tr('about.textBody')}</p>
              {stats}
              <p><a href='https://github.com/openscriptures/morphhb'>
                 openscriptures/morphhb</a> ·
                 <a href='https://github.com/openscriptures/HebrewLexicon'>
                 openscriptures/HebrewLexicon</a></p>
              {license_line}
              {who}{link}
              <p style='color:#8a8681'>{tr('about.thanks')}</p>
            </div>""")
        v.addWidget(body, 1)

        row = QHBoxLayout()
        row.addStretch(1)
        close = QPushButton(tr("btn.close"))
        close.setObjectName("Primary")
        close.clicked.connect(self.accept)
        row.addWidget(close)
        v.addLayout(row)


def _esc_html(s: str) -> str:
    return (s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;"))


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setObjectName("Root")
        self.resize(1240, 820)
        self.corpus: Corpus | None = None
        self.result = None
        self.syllabus = None
        self.ranges = []
        self.thread = None
        self.worker = None
        self.root_rows: list = []
        self.settings = QSettings("ChidonHapax", "HapaxFinder")
        set_language(self.settings.value("language", "en"))
        numbering.set_scheme(self.settings.value("numbering", numbering.WLC))

        root = QVBoxLayout(self)
        root.setContentsMargins(16, 14, 16, 12)
        root.setSpacing(10)

        # ---- header -----------------------------------------------------
        head = QHBoxLayout()
        self.heading = QLabel()
        self.heading.setObjectName("Heading")
        head.addWidget(self.heading)
        head.addStretch(1)
        self.lang_label = QLabel()
        self.lang_combo = QComboBox()
        for code, name in LANGUAGES:
            self.lang_combo.addItem(name, code)
        self.lang_combo.setCurrentIndex(
            max(0, [c for c, _ in LANGUAGES].index(current_language())))
        self.lang_combo.currentIndexChanged.connect(self.change_language)
        head.addWidget(self.lang_label)
        head.addWidget(self.lang_combo)
        self.help_btn = QPushButton()
        self.help_btn.setObjectName("Help")
        self.help_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.help_btn.clicked.connect(self.show_help)
        head.addWidget(self.help_btn)

        self.about_btn = QPushButton("i")
        self.about_btn.setObjectName("Info")
        self.about_btn.setFixedSize(30, 30)
        self.about_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.about_btn.clicked.connect(self.show_about)
        head.addWidget(self.about_btn)
        self.bsd_label = QLabel(BSD)
        self.bsd_label.setObjectName("Bsd")
        self.bsd_label.setVisible(bool(BSD))
        self.header_layout = head
        head.addWidget(self.bsd_label)
        root.addLayout(head)

        bar = QHBoxLayout()
        self.corpus_label = QLabel()
        self.corpus_label.setObjectName("CorpusLabel")
        self.corpus_btn = QPushButton()
        self.corpus_btn.setObjectName("Accent")
        self.corpus_btn.clicked.connect(self.download_corpus)
        bar.addWidget(self.corpus_label, 1)
        bar.addWidget(self.corpus_btn)
        root.addLayout(bar)

        self.split = split = QSplitter(Qt.Orientation.Horizontal)
        root.addWidget(split, 1)

        # ---- left: syllabus + options -----------------------------------
        left_inner = QWidget()
        lv = QVBoxLayout(left_inner)
        lv.setContentsMargins(0, 0, 6, 0)
        lv.setSpacing(8)

        self.syllabus_box = QGroupBox()
        gv = QVBoxLayout(self.syllabus_box)
        gv.setContentsMargins(12, 14, 12, 10)
        gv.setSpacing(6)
        self.syllabus_edit = QPlainTextEdit()
        self.syllabus_edit.textChanged.connect(self.validate_syllabus)
        gv.addWidget(self.syllabus_edit, 1)

        add = QHBoxLayout()
        self.book_combo = QComboBox()
        self.chapters_edit = QLineEdit()
        self.add_btn = QPushButton()
        self.add_btn.clicked.connect(self.add_book_line)
        add.addWidget(self.book_combo, 2)
        add.addWidget(self.chapters_edit, 2)
        add.addWidget(self.add_btn)
        gv.addLayout(add)

        io_row = QHBoxLayout()
        self.open_btn = QPushButton()
        self.open_btn.clicked.connect(self.open_syllabus)
        self.save_btn = QPushButton()
        self.save_btn.clicked.connect(self.save_syllabus)
        io_row.addWidget(self.open_btn)
        io_row.addWidget(self.save_btn)
        io_row.addStretch(1)
        gv.addLayout(io_row)

        self.syllabus_status = QLabel()
        self.syllabus_status.setObjectName("SyllabusStatus")
        self.syllabus_status.setWordWrap(True)
        gv.addWidget(self.syllabus_status)
        lv.addWidget(self.syllabus_box, 1)

        self.options_box = QGroupBox()
        of = QFormLayout(self.options_box)
        of.setContentsMargins(12, 14, 12, 10)
        of.setSpacing(6)
        self.scope_combo = QComboBox()
        self.scope_combo.setMinimumWidth(300)
        for key in ("tanach", "syllabus", "book", "section", "custom"):
            self.scope_combo.addItem("", key)
        self.scope_combo.currentIndexChanged.connect(self.update_scope_widgets)
        self.scope_label = QLabel()
        of.addRow(self.scope_label, self.scope_combo)

        self.section_combo = QComboBox()
        self.section_combo.setMinimumWidth(300)
        for key in sections.ORDER:
            self.section_combo.addItem(sections.label(key), key)
        self.section_combo.setCurrentIndex(sections.ORDER.index("neviim_rishonim"))
        of.addRow("", self.section_combo)

        self.scope_edit = QLineEdit()
        of.addRow("", self.scope_edit)

        self.scope_part = QCheckBox()
        self.scope_part.setChecked(False)
        of.addRow("", self.scope_part)

        self.level_combo = QComboBox()
        self.level_combo.setMinimumWidth(300)
        for key in LEVELS:
            self.level_combo.addItem("", key)
        self.level_combo.setCurrentIndex(LEVELS.index("consonantal"))
        self.compare_label = QLabel()
        of.addRow(self.compare_label, self.level_combo)

        nrow = QHBoxLayout()
        nrow.setContentsMargins(0, 0, 0, 0)
        self.n_boxes = {}
        for n in range(1, 6):
            cb = QCheckBox(str(n))
            cb.setChecked(True)
            self.n_boxes[n] = cb
            nrow.addWidget(cb)
        nrow.addStretch(1)
        nw = QWidget()
        nw.setLayout(nrow)
        self.lengths_label = QLabel()
        of.addRow(self.lengths_label, nw)

        self.minimal_cb = QCheckBox()
        self.minimal_cb.setChecked(True)
        of.addRow(self.minimal_cb)
        self.cross_cb = QCheckBox()
        of.addRow(self.cross_cb)

        self.freq_spin = QSpinBox()
        self.freq_spin.setRange(1, 500)
        self.freq_spin.setValue(1)
        self.freq_label = QLabel()
        of.addRow(self.freq_label, self.freq_spin)
        lv.addWidget(self.options_box)

        self.report_box = QGroupBox()
        rf = QFormLayout(self.report_box)
        rf.setContentsMargins(12, 14, 12, 10)
        rf.setSpacing(6)
        self.title_edit = QLineEdit()
        self.title_label = QLabel()
        rf.addRow(self.title_label, self.title_edit)
        self.numbering_combo = QComboBox()
        self.numbering_combo.setMinimumWidth(240)
        for key in numbering.SCHEMES:
            self.numbering_combo.addItem("", key)
        self.numbering_combo.currentIndexChanged.connect(self.change_numbering)
        self.numbering_label = QLabel()
        rf.addRow(self.numbering_label, self.numbering_combo)
        self.verses_cb = QCheckBox()
        self.index_cb = QCheckBox()
        self.index_cb.setChecked(True)
        self.practice_cb = QCheckBox()
        self.hebnum_cb = QCheckBox()
        self.hebnum_cb.setChecked(True)
        for w in (self.verses_cb, self.index_cb, self.practice_cb, self.hebnum_cb):
            rf.addRow(w)
        lv.addWidget(self.report_box)
        lv.addStretch(1)          # maximising must not distort the panels

        run_row = QHBoxLayout()
        self.run_btn = QPushButton()
        self.run_btn.setObjectName("Primary")
        self.run_btn.clicked.connect(self.run_analysis)
        self.pdf_btn = QPushButton()
        self.pdf_btn.setObjectName("Accent")
        self.pdf_btn.setEnabled(False)
        self.pdf_btn.clicked.connect(self.save_pdf)
        run_row.addWidget(self.run_btn, 1)
        run_row.addWidget(self.pdf_btn, 1)
        lv.addLayout(run_row)

        other = QHBoxLayout()
        self.html_btn = QPushButton()
        self.html_btn.setEnabled(False)
        self.html_btn.clicked.connect(self.save_html)
        self.csv_btn = QPushButton()
        self.csv_btn.setEnabled(False)
        self.csv_btn.clicked.connect(self.save_csv)
        other.addWidget(self.html_btn)
        other.addWidget(self.csv_btn)
        lv.addLayout(other)

        self.progress = QProgressBar()
        self.progress.setRange(0, 100)
        self.progress.setTextVisible(False)
        lv.addWidget(self.progress)
        self.status = QLabel("")
        self.status.setObjectName("Status")
        self.status.setWordWrap(True)
        lv.addWidget(self.status)
        left = QScrollArea()
        left.setWidget(left_inner)
        left.setWidgetResizable(True)
        left.setFrameShape(QScrollArea.Shape.NoFrame)
        left.setHorizontalScrollBarPolicy(
            Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        split.addWidget(left)

        # ---- right: results + roots -------------------------------------
        right = QWidget()
        rv = QVBoxLayout(right)
        rv.setContentsMargins(6, 0, 0, 0)
        rv.setSpacing(10)
        self.tabs = QTabWidget()
        self.tables = {}
        hf = QFont()
        hf.setPointSize(13)
        for n in range(1, 6):
            t = QTableWidget(0, 5)
            t.verticalHeader().setVisible(False)
            t.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
            t.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
            t.setSelectionMode(QTableWidget.SelectionMode.SingleSelection)
            t.setShowGrid(False)
            t.itemSelectionChanged.connect(self.show_detail)
            t.setFont(hf)
            t.horizontalHeader().setStretchLastSection(False)
            # sensible widths before any results exist, so the header is not
            # cut off on a fresh window
            hh0 = t.horizontalHeader()
            hh0.setSectionResizeMode(0, QHeaderView.ResizeMode.Stretch)
            for col in range(1, 5):
                hh0.setSectionResizeMode(col,
                                         QHeaderView.ResizeMode.ResizeToContents)
            self.tables[n] = t
            self.tabs.addTab(t, "")
        self.roots_tab = self._build_roots_tab()
        self.tabs.addTab(self.roots_tab, "")
        rv.addWidget(self.tabs, 3)

        self.detail = QTextBrowser()
        self.detail.setMinimumHeight(140)
        opt = QTextOption()
        opt.setTextDirection(Qt.LayoutDirection.RightToLeft)
        self.detail.document().setDefaultTextOption(opt)
        rv.addWidget(self.detail, 1)
        split.addWidget(right)
        split.setSizes([470, 770])   # refined in fit_controls_to_font()
        self.setAcceptDrops(True)

        self.numbering_combo.setCurrentIndex(
            numbering.SCHEMES.index(numbering.scheme()))
        self.retranslate()
        self.fit_controls_to_font()
        self.refresh_corpus_state()
        self.validate_syllabus()

    # ------------------------------------------------------- roots tab
    def _build_roots_tab(self) -> QWidget:
        w = QWidget()
        v = QVBoxLayout(w)
        v.setContentsMargins(12, 12, 12, 12)
        v.setSpacing(8)
        row = QHBoxLayout()
        self.root_edit = QLineEdit()
        self.root_edit.returnPressed.connect(self.search_root)
        self.root_btn = QPushButton()
        self.root_btn.setObjectName("Primary")
        self.root_btn.clicked.connect(self.search_root)
        row.addWidget(self.root_edit, 1)
        row.addWidget(self.root_btn)
        v.addLayout(row)
        self.root_scope_cb = QCheckBox()
        v.addWidget(self.root_scope_cb)
        self.root_summary = QLabel()
        self.root_summary.setWordWrap(True)
        v.addWidget(self.root_summary)
        self.root_table = QTableWidget(0, 3)
        self.root_table.verticalHeader().setVisible(False)
        self.root_table.setShowGrid(False)
        self.root_table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        self.root_table.setSelectionBehavior(
            QTableWidget.SelectionBehavior.SelectRows)
        f = QFont()
        f.setPointSize(13)
        self.root_table.setFont(f)
        self.root_table.itemSelectionChanged.connect(self.show_root_detail)
        v.addWidget(self.root_table, 1)
        self.root_hint = QLabel()
        self.root_hint.setObjectName("Status")
        self.root_hint.setWordWrap(True)
        v.addWidget(self.root_hint)
        return w

    def change_numbering(self):
        numbering.set_scheme(self.numbering_combo.currentData())
        self.settings.setValue("numbering", numbering.scheme())
        if self.result is not None:
            self.populate(self.result)
        self.detail.clear()
        if self.root_rows:
            self.search_root()

    def update_scope_widgets(self):
        scope = self.scope_combo.currentData()
        self.section_combo.setVisible(scope == "section")
        self.scope_edit.setVisible(scope == "custom")
        # the syllabus scope is already restricted; the Tanach one must not be
        self.scope_part.setVisible(scope in ("book", "section", "custom"))

    def scope_verse_set(self):
        """Verse indexes for a typed scope range, or None."""
        if self.scope_combo.currentData() != "custom":
            return None
        try:
            parsed = parse_syllabus_full(self.scope_edit.text(), self.corpus,
                                         lenient=True)
        except SyllabusError:
            return set()
        return {v.idx for v in collect_verses(parsed.ranges, self.corpus)}

    def show_help(self):
        HelpDialog(self, self.settings).exec()

    def maybe_show_help(self):
        """Open the guide on first run, or whenever the user asked us to.

        Two separate questions, so two separate settings: whether they have
        ever seen it, and whether they want it every time. Sharing one key
        made ticking "show at startup" good for exactly one more launch.
        """
        seen = self.settings.value("help_seen", "no") == "yes"
        always = self.settings.value("help_at_startup", "no") == "yes"
        # migrate the old single key: show_help=no meant "already seen"
        if self.settings.contains("show_help"):
            if self.settings.value("show_help") == "no":
                seen = True
            self.settings.remove("show_help")
        if seen and not always:
            self.settings.setValue("help_seen", "yes")
            self.settings.sync()
            return
        self.settings.setValue("help_seen", "yes")
        self.settings.sync()
        self.show_help()

    def show_about(self):
        AboutDialog(self, self.corpus).exec()

    # ------------------------------------------------------ translation
    def change_language(self):
        set_language(self.lang_combo.currentData())
        self.settings.setValue("language", current_language())
        QApplication.instance().setLayoutDirection(
            Qt.LayoutDirection.RightToLeft if is_rtl()
            else Qt.LayoutDirection.LeftToRight)
        self.detail.clear()
        self.numbering_combo.setCurrentIndex(
            numbering.SCHEMES.index(numbering.scheme()))
        self.retranslate()
        self.fit_controls_to_font()
        self.refresh_corpus_state()
        self.validate_syllabus()
        if self.result is not None:
            self.populate(self.result)

    def fit_controls_to_font(self):
        """Give inputs and buttons room for the platform's own font.

        The stylesheet can only express padding in pixels, but Segoe UI on
        Windows is appreciably taller than the macOS system font at the same
        point size, so a height that looks right on one platform clips
        descenders on the other. Measuring the font at runtime avoids
        guessing per-platform numbers.
        """
        fm = self.fontMetrics()
        line = fm.height()
        for widget in self.findChildren((QComboBox, QLineEdit, QSpinBox)):
            widget.setMinimumHeight(line + 16)
        for button in self.findChildren(QPushButton):
            if button.objectName() in ("Info", "Help"):
                continue                       # round / pill shaped, sized already
            button.setMinimumHeight(line + 18)
        # floor: four lines, so a short window can still shrink it
        # ceiling: fourteen, so maximising does not stretch it out of shape
        self.syllabus_edit.setMinimumHeight(line * 4)
        self.syllabus_edit.setMaximumHeight(line * 14)

        # a combo must fit its longest entry plus the arrow, or the text is
        # cut off mid-word — "Unique in the whole Tana…"
        for combo in self.findChildren(QComboBox):
            cfm = combo.fontMetrics()
            widest = max((cfm.horizontalAdvance(combo.itemText(i))
                          for i in range(combo.count())), default=0)
            combo.setMinimumWidth(min(widest + 58, 460))

        # and the settings panel must be wide enough for whatever that came to
        left = self.split.widget(0)
        if isinstance(left, QScrollArea) and left.widget() is not None:
            inner = left.widget()
        else:
            inner = left
        if inner is not None:
            want = max(470, inner.sizeHint().width() + 24)
            total = max(self.width(), want + 520)
            self.split.setSizes([want, total - want])

    def retranslate(self):
        self.setWindowTitle(tr("app.title"))
        self.setWindowIcon(app_icon())
        self.heading.setText(tr("app.title"))
        self.lang_label.setText(tr("lang.label"))
        self.about_btn.setToolTip(tr("about.button"))
        self.help_btn.setText("?  " + tr("help.button"))
        self.header_layout.removeWidget(self.bsd_label)
        if is_rtl():
            self.header_layout.insertWidget(0, self.bsd_label)
        else:
            self.header_layout.addWidget(self.bsd_label)
        self.corpus_btn.setText(tr("corpus.download"))
        self.syllabus_box.setTitle(tr("group.syllabus"))
        from .i18n import LANGUAGES, STRINGS
        examples = {v.strip() for v in STRINGS["syllabus.example"].values()}
        current = self.syllabus_edit.toPlainText().strip()
        if not current or current in examples:
            self.syllabus_edit.setPlainText(tr("syllabus.example"))
        self.chapters_edit.setPlaceholderText(tr("ph.chapters"))
        self.add_btn.setText(tr("btn.add"))
        self.open_btn.setText(tr("btn.open"))
        self.save_btn.setText(tr("btn.save"))
        self.options_box.setTitle(tr("group.unique"))
        self.scope_label.setText(tr("label.scope"))
        self.scope_combo.setToolTip(tr("tip.scope"))
        for i in range(self.scope_combo.count()):
            self.scope_combo.setItemText(i, tr(f"scope.{self.scope_combo.itemData(i)}"))
        self.scope_edit.setPlaceholderText(tr("ph.scopeCustom"))
        self.scope_part.setText(tr("opt.scopeInSyllabus"))
        self.scope_part.setToolTip(tr("tip.scopeInSyllabus"))
        self.update_scope_widgets()
        self.compare_label.setText(tr("label.compareBy"))
        for i, key in enumerate(LEVELS):
            self.level_combo.setItemText(i, tr(f"level.{key}"))
        self.lengths_label.setText(tr("label.lengths"))
        self.minimal_cb.setText(tr("opt.minimal"))
        self.minimal_cb.setToolTip(tr("tip.minimal"))
        self.cross_cb.setText(tr("opt.cross"))
        self.freq_label.setText(tr("label.freq"))
        self.freq_spin.setToolTip(tr("tip.freq"))
        self.report_box.setTitle(tr("group.report"))
        self.title_label.setText(tr("label.title"))
        self.numbering_label.setText(tr("label.numbering"))
        for i, key in enumerate(numbering.SCHEMES):
            self.numbering_combo.setItemText(i, tr(f"numbering.{key}"))
        self.numbering_combo.setToolTip(tr("tip.numbering"))
        self.title_edit.setPlaceholderText(tr("ph.title"))
        self.verses_cb.setText(tr("opt.verses"))
        self.index_cb.setText(tr("opt.index"))
        self.practice_cb.setText(tr("opt.practice"))
        self.hebnum_cb.setText(tr("opt.hebnum"))
        self.run_btn.setText(tr("btn.run"))
        self.pdf_btn.setText(tr("btn.pdf"))
        self.html_btn.setText(tr("btn.html"))
        self.csv_btn.setText(tr("btn.csv"))
        heads = [tr("col.phrase"), tr("col.place"), tr("col.root"),
                 tr("col.tanach"), tr("col.syllabus")]
        for n, t in self.tables.items():
            t.setHorizontalHeaderLabels(heads)
            if self.result is None:
                self.tabs.setTabText(n - 1, tr("tab.words", n=n))
        self.tabs.setTabText(5, tr("tab.roots"))
        self.root_edit.setPlaceholderText(tr("roots.ph"))
        self.root_btn.setText(tr("roots.search"))
        self.root_scope_cb.setText(tr("roots.onlySyllabus"))
        self.root_table.setHorizontalHeaderLabels(
            [tr("col.place"), tr("col.phrase"), ""])
        self.root_hint.setText(tr("roots.hint"))

    # ------------------------------------------------------------ corpus
    def refresh_corpus_state(self):
        if self.corpus is not None:
            self.corpus_label.setText(tr(
                "corpus.loaded", verses=f"{len(self.corpus.verses):,}",
                words=f"{self.corpus.total_words():,}"))
            self.corpus_btn.setVisible(False)
            if self.book_combo.count() == 0:
                for i, b in enumerate(self.corpus.books):
                    self.book_combo.addItem(f"{b['he']}  ·  {b['en']}", i)
        elif corpus_exists():
            self.corpus_label.setText(tr("corpus.loading"))
            try:
                self.corpus = load_corpus()
            except Exception as e:
                self.corpus_label.setText(str(e))
                return
            self.refresh_corpus_state()
        else:
            self.corpus_label.setText(tr("corpus.missing"))
            self.corpus_btn.setVisible(True)

    def download_corpus(self):
        from .build_corpus import build
        self.corpus_btn.setEnabled(False)

        def job(progress):
            # never the bundle: it is read-only inside an .app or
            # under Program Files
            return build(None, USER_CORPUS_PATH,
                         log=lambda m: progress(0.5, str(m)))

        def done(_):
            self.corpus_btn.setEnabled(True)
            self.refresh_corpus_state()
            self.validate_syllabus()

        self.start_job(job, done, tr("corpus.downloading"))

    # ----------------------------------------------------------- syllabus
    def dragEnterEvent(self, e):
        if e.mimeData().hasUrls():
            e.acceptProposedAction()

    def dropEvent(self, e):
        for url in e.mimeData().urls():
            path = url.toLocalFile()
            if path and os.path.isfile(path):
                try:
                    with open(path, encoding="utf-8") as f:
                        self.syllabus_edit.setPlainText(f.read())
                except OSError:
                    pass
                break

    def add_book_line(self):
        if self.corpus is None or self.book_combo.currentIndex() < 0:
            return
        line = self.corpus.book_he(self.book_combo.currentData())
        ch = self.chapters_edit.text().strip()
        if ch:
            line += " " + ch
        text = self.syllabus_edit.toPlainText().rstrip()
        self.syllabus_edit.setPlainText((text + "\n" + line).strip() + "\n")
        self.chapters_edit.clear()

    def open_syllabus(self):
        path, _ = QFileDialog.getOpenFileName(self, tr("dlg.openSyllabus"), "",
                                              "Text (*.txt);;All files (*)")
        if path:
            with open(path, encoding="utf-8") as f:
                self.syllabus_edit.setPlainText(f.read())

    def save_syllabus(self):
        path, _ = QFileDialog.getSaveFileName(self, tr("dlg.saveSyllabus"),
                                              "syllabus.txt", "Text (*.txt)")
        if path:
            with open(path, "w", encoding="utf-8") as f:
                f.write(self.syllabus_edit.toPlainText())

    def validate_syllabus(self):
        if self.corpus is None:
            self.syllabus_status.setText("")
            return False
        body = "\n".join(l.split("#", 1)[0] for l in
                         self.syllabus_edit.toPlainText().splitlines())
        if not body.strip():          # nothing but comments — say nothing
            self.syllabus, self.ranges = None, []
            self.syllabus_status.setText("")
            return False
        try:
            syl = parse_syllabus_full(self.syllabus_edit.toPlainText(),
                                      self.corpus, lenient=True)
        except SyllabusError as e:
            self.syllabus, self.ranges = None, []
            self.syllabus_status.setText(f"<span style='color:#b3261e'>⚠ {e}</span>")
            return False
        self.syllabus = syl
        self.ranges = syl.ranges
        text = self.syllabus_edit.toPlainText()
        hebrew = any("\u05d0" <= ch <= "\u05ea" for ch in text)
        want = (Qt.LayoutDirection.RightToLeft if (hebrew or is_rtl())
                else Qt.LayoutDirection.LeftToRight)
        if self.syllabus_edit.layoutDirection() != want:
            self.syllabus_edit.setLayoutDirection(want)
        verses = collect_verses(syl.ranges, self.corpus)
        words = sum(len(v.words) for v in verses)
        bits = [f"<span style='color:#2e7d32'>"
                + tr("syl.summary", chapters=f"{syl.n_chapters:,}",
                     verses=f"{len(verses):,}", words=f"{words:,}") + "</span>"]
        if syl.stated_total is not None and syl.stated_total == syl.n_chapters:
            bits.append("<span style='color:#2e7d32'>"
                        + tr("syl.matchesTotal", total=syl.stated_total) + "</span>")
        for w in syl.warnings:
            bits.append(f"<span style='color:#b0743a'>⚠ {w}</span>")
        for e in syl.errors:
            bits.append(f"<span style='color:#b3261e'>⚠ {e}</span>")
        if syl.ignored:
            shown = " / ".join(syl.ignored[:2])
            bits.append("<span style='color:#8a8681'>"
                        + tr("syl.skipped", n=len(syl.ignored), lines=shown)
                        + "</span>")
        self.syllabus_status.setText("<br>".join(bits))
        self.syllabus_status.setToolTip("\n".join(syl.ignored))
        if syl.title and not self.title_edit.text().strip():
            self.title_edit.setPlaceholderText(syl.title)
        return True

    # ----------------------------------------------------------- analysis
    def current_options(self) -> Options:
        include = tuple(n for n, cb in self.n_boxes.items() if cb.isChecked()) or (1,)
        return Options(max_n=max(include),
                       scope=self.scope_combo.currentData(),
                       scope_section=self.section_combo.currentData(),
                       scope_in_syllabus=(self.scope_part.isChecked()
                                          and self.scope_part.isVisible()),
                       level=self.level_combo.currentData(),
                       minimal=self.minimal_cb.isChecked(),
                       cross_verses=self.cross_cb.isChecked(),
                       min_word_freq=self.freq_spin.value(),
                       include_n=include)

    def run_analysis(self):
        if self.corpus is None:
            QMessageBox.information(self, tr("msg.noTextTitle"), tr("msg.noText"))
            return
        if not self.validate_syllabus() or not self.ranges:
            QMessageBox.warning(self, tr("group.syllabus"), tr("msg.fixSyllabus"))
            return
        verses = collect_verses(self.ranges, self.corpus)
        opts = self.current_options()
        scope_verses = self.scope_verse_set()
        if opts.scope == "custom" and not scope_verses:
            QMessageBox.warning(self, tr("label.scope"), tr("err.scopeEmpty"))
            return
        inside = None
        if opts.scope == "section":
            books = sections.book_indexes(self.corpus, opts.scope_section)
            inside = any(v.book in books for v in verses)
            where = sections.label(opts.scope_section)
        elif opts.scope == "custom":
            inside = any(v.idx in scope_verses for v in verses)
            where = self.scope_edit.text().strip()
        if inside is False:
            QMessageBox.warning(self, tr("label.scope"),
                                tr("err.scopeNoOverlap", scope=where))
            return
        if not opts.minimal and opts.max_n >= 3:
            if QMessageBox.question(self, tr("msg.longTitle"), tr("msg.longBody")) \
                    != QMessageBox.StandardButton.Yes:
                return

        corpus = self.corpus
        self.run_btn.setEnabled(False)
        for b in (self.pdf_btn, self.html_btn, self.csv_btn):
            b.setEnabled(False)

        def job(progress):
            return analyze(corpus, verses, opts, progress=progress,
                           scope_verses=scope_verses)

        def done(res):
            self.result = res
            self.run_btn.setEnabled(True)
            for b in (self.pdf_btn, self.html_btn, self.csv_btn):
                b.setEnabled(True)
            self.populate(res)
            self.status.setText(tr("status.found", n=f"{len(res.hits):,}",
                                   s=f"{res.elapsed:.1f}"))

        self.start_job(job, done, tr("status.searching"))

    def start_job(self, job, done, label):
        self.progress.setValue(0)
        self.status.setText(label)
        self.thread = QThread(self)
        self.worker = Worker(job)
        self.worker.moveToThread(self.thread)
        self.thread.started.connect(self.worker.run)
        self.worker.progress.connect(self.on_progress)
        self.worker.failed.connect(self.on_failed)

        def finish(res):
            self.thread.quit()
            self.thread.wait()
            self.progress.setValue(100)
            done(res)

        self.worker.finished.connect(finish)
        self.thread.start()

    def on_progress(self, frac, msg):
        self.progress.setValue(int(frac * 100))
        self.status.setText(msg)

    def on_failed(self, tb):
        self.thread.quit()
        self.thread.wait()
        self.run_btn.setEnabled(True)
        self.corpus_btn.setEnabled(True)
        self.status.setText(tr("msg.wrong"))
        QMessageBox.critical(self, tr("msg.error"), tb[-2000:])

    # ------------------------------------------------------------ results
    def populate(self, res):
        by_root = res.options.level == "root"
        for n, table in self.tables.items():
            hits = res.by_n(n)
            self.tabs.setTabText(n - 1, f"{tr('tab.words', n=n)}  ({len(hits):,})")
            self.tabs.setTabEnabled(n - 1, bool(hits))
            table.setRowCount(0)
            table.setRowCount(len(hits))
            for row, h in enumerate(hits):
                roots = " · ".join(self.corpus.lemma_text(r) for r in h.roots) \
                    if by_root else ""
                cells = [h.text, self.corpus.ref(h.verse), roots,
                         f"{h.tanach_count:,}", f"{h.syllabus_count:,}"]
                for col, txt in enumerate(cells):
                    it = QTableWidgetItem(txt)
                    it.setTextAlignment(
                        Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter
                        if col in (0, 2) else
                        Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)
                    table.setItem(row, col, it)
            table.setColumnHidden(2, not by_root)
            table.resizeColumnsToContents()
            hh = table.horizontalHeader()
            # cap the narrow columns so the phrase column keeps the width
            scale = table.fontMetrics().height() / 16.0
            for col in range(1, 5):
                hh.setSectionResizeMode(col, QHeaderView.ResizeMode.Fixed)
                cap = int((170 if col == 1 else 110) * scale)
                table.setColumnWidth(col, min(table.columnWidth(col) + 8, cap))
            hh.setSectionResizeMode(0, QHeaderView.ResizeMode.Stretch)
        for n in range(1, 6):
            if res.by_n(n):
                self.tabs.setCurrentIndex(n - 1)
                break

    def _verse_html(self, verses, marked, note=""):
        parts = []
        for vv in verses:
            words = []
            for i, w in enumerate(vv.words):
                words.append(f"<b style='color:#b0743a'>{w}</b>"
                             if (vv.idx, i) in marked else w)
                if i < len(vv.words) - 1:
                    words.append("־" if i in vv.maqqef else " ")
            parts.append(f"<p dir='rtl' align='right'>"
                         f"<span style='color:#2f5d92'>{self.corpus.ref(vv)}</span>"
                         f" — {''.join(words)}</p>")
        return (f"<div style='font-family:{HE_FONTS};font-size:14pt'>"
                + "".join(parts) + note + "</div>")

    def show_detail(self):
        if self.result is None:
            return
        n = self.tabs.currentIndex() + 1
        table = self.tables.get(n)
        if table is None:
            return
        rows = {i.row() for i in table.selectedItems()}
        hits = self.result.by_n(n)
        if not rows or min(rows) >= len(hits):
            return
        hit = hits[min(rows)]
        marked = {(vv.idx, i) for vv, i in hit.positions}
        verses = []
        for vv, _ in hit.positions:
            if vv not in verses:
                verses.append(vv)
        extra = ""
        if hit.roots:
            extra = " · ".join(
                f"{self.corpus.lemma_text(r)} ({self.corpus.lemma_gloss(r)})"
                for r in hit.roots if r)
        note = (f"<p dir='ltr' align='left' style='color:#6b7482;font-size:10pt'>"
                f"{tr('col.tanach')}: {hit.tanach_count:,} · "
                f"{tr('col.syllabus')}: {hit.syllabus_count:,}"
                + (f" · {tr('col.root')}: {extra}" if extra else "") + "</p>")
        self.detail.setHtml(self._verse_html(verses, marked, note))

    # -------------------------------------------------------------- roots
    def search_root(self):
        if self.corpus is None:
            QMessageBox.information(self, tr("msg.noTextTitle"), tr("msg.noText"))
            return
        q = self.root_edit.text().strip()
        if not q:
            return
        occ, _ = self.corpus.build_lemma_index()
        lemmas = self.corpus.find_lemmas(q)
        if not lemmas:
            self.root_summary.setText(
                f"<span style='color:#b3261e'>{tr('roots.none', q=q)}</span>")
            self.root_table.setRowCount(0)
            self.root_rows = []
            return

        in_syllabus = ({v.idx for v in collect_verses(self.ranges, self.corpus)}
                       if self.ranges else set())
        only_syllabus = self.root_scope_cb.isChecked() and bool(in_syllabus)

        lines, rows = [], []
        for lemma in lemmas[:6]:
            places = occ.get(lemma, [])
            syll_n = sum(1 for p in places if p[0].idx in in_syllabus)
            inside = [p for p in places
                      if not only_syllabus or p[0].idx in in_syllabus]
            lines.append(tr("roots.summary",
                            lemma=self.corpus.lemma_text(lemma),
                            gloss=self.corpus.lemma_gloss(lemma) or "—",
                            tanach=f"{len(places):,}", syllabus=f"{syll_n:,}"))
            rows.extend((lemma, v, i) for v, i in inside)

        rows.sort(key=lambda r: (r[1].book, r[1].chapter, r[1].verse, r[2]))
        self.root_rows = rows[:MAX_ROOT_ROWS]
        self.root_summary.setText("<br>".join(
            f"<span style='font-family:{HE_FONTS};font-size:12pt'>{ln}</span>"
            for ln in lines))
        self.root_table.setRowCount(0)
        self.root_table.setRowCount(len(self.root_rows))
        for r, (lemma, v, i) in enumerate(self.root_rows):
            ref = QTableWidgetItem(self.corpus.ref(v))
            word = QTableWidgetItem(v.words[i])
            word.setTextAlignment(Qt.AlignmentFlag.AlignRight
                                  | Qt.AlignmentFlag.AlignVCenter)
            ctx = QTableWidgetItem(self.corpus.join_words(
                v, max(0, i - 3), min(len(v.words), i + 4)))
            ctx.setTextAlignment(Qt.AlignmentFlag.AlignRight
                                 | Qt.AlignmentFlag.AlignVCenter)
            self.root_table.setItem(r, 0, ref)
            self.root_table.setItem(r, 1, word)
            self.root_table.setItem(r, 2, ctx)
        self.root_table.resizeColumnsToContents()
        self.root_table.horizontalHeader().setSectionResizeMode(
            2, QHeaderView.ResizeMode.Stretch)

    def show_root_detail(self):
        rows = {i.row() for i in self.root_table.selectedItems()}
        if not rows or min(rows) >= len(self.root_rows):
            return
        lemma, v, i = self.root_rows[min(rows)]
        note = (f"<p dir='ltr' align='left' style='color:#6b7482;font-size:10pt'>"
                f"{tr('col.root')}: {self.corpus.lemma_text(lemma)} "
                f"({self.corpus.lemma_gloss(lemma)})</p>")
        self.detail.setHtml(self._verse_html([v], {(v.idx, i)}, note))

    # ------------------------------------------------------------ exports
    def _html(self) -> str:
        return report.build_html(
            self.corpus, self.result, describe(self.ranges, self.corpus),
            title=(self.title_edit.text().strip()
                   or (self.syllabus.title if self.syllabus else "")),
            n_chapters=self.syllabus.n_chapters if self.syllabus else 0,
            show_verses=self.verses_cb.isChecked(),
            alphabetical_index=self.index_cb.isChecked(),
            practice_sheet=self.practice_cb.isChecked(),
            hebrew_refs=self.hebnum_cb.isChecked())

    def save_pdf(self):
        path, _ = QFileDialog.getSaveFileName(self, tr("dlg.savePdf"),
                                              "hapax.pdf", "PDF (*.pdf)")
        if not path:
            return
        self.status.setText(tr("status.writing"))
        QApplication.processEvents()
        try:
            report.export_pdf(self._html(), path,
                              self.title_edit.text().strip() or "Hapax")
        except Exception as e:
            QMessageBox.critical(self, tr("msg.error"), str(e))
            return
        self.status.setText(tr("status.saved", name=os.path.basename(path)))

    def save_html(self):
        path, _ = QFileDialog.getSaveFileName(self, tr("btn.html"), "hapax.html",
                                              "HTML (*.html)")
        if path:
            report.export_html(self._html(), path)
            self.status.setText(tr("status.saved", name=os.path.basename(path)))

    def save_csv(self):
        path, _ = QFileDialog.getSaveFileName(self, tr("btn.csv"), "hapax.csv",
                                              "CSV (*.csv)")
        if path:
            report.export_csv(self.corpus, self.result, path)
            self.status.setText(tr("status.saved", name=os.path.basename(path)))


def main():
    app = QApplication(sys.argv)
    app.setApplicationName("Chidon Hapax Finder")
    app.setWindowIcon(app_icon())
    app.setStyleSheet(load_stylesheet())
    w = MainWindow()
    screen = app.primaryScreen()
    if screen is not None:
        # leave room for the taskbar / dock: availableGeometry excludes it
        avail = screen.availableGeometry()
        w.resize(min(1280, int(avail.width() * 0.94)),
                 min(940, int(avail.height() * 0.92)))
        w.move(avail.center() - w.rect().center())
    if is_rtl():
        app.setLayoutDirection(Qt.LayoutDirection.RightToLeft)
    w.show()
    w.maybe_show_help()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
