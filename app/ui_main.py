import os
from PySide6.QtWidgets import *
from PySide6.QtCore import Qt
from .worker import Worker
from .settings import load_settings, save_settings
from .constants import PRESET_QUALITY
from .compressor import find_ghostscript

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.cfg = load_settings()
        self.setWindowTitle("PDF Compressor")
        self.resize(520, 420)
        self.init_ui()
        
    def apply_preset(self, name):
        p = PRESET_QUALITY[name]
        self.dpi.setValue(p["dpi"])
        self.jpeg.setValue(p["jpeg"])
        
    def init_ui(self):
        L = QVBoxLayout()

        self.input_lbl = QLabel("No input selected")
        L.addWidget(self.input_lbl)

        b_in = QPushButton("Select PDF")
        b_in.clicked.connect(self.sel_input)
        L.addWidget(b_in)

        self.out_edit = QLineEdit()
        L.addWidget(self.out_edit)

        b_out = QPushButton("Select Output")
        b_out.clicked.connect(self.sel_output)
        L.addWidget(b_out)

        self.quality_preset = QComboBox()
        self.quality_preset.addItems(PRESET_QUALITY.keys())
        L.addWidget(self.quality_preset)
        self.dpi = QSpinBox()
        self.dpi.setRange(50, 600)
        self.dpi.setValue(150)
        self.dpi.setSuffix(" DPI")
        L.addWidget(self.dpi)

        self.jpeg = QSpinBox()
        self.jpeg.setRange(30, 100)
        self.jpeg.setValue(70)
        self.jpeg.setSuffix(" JPEG")
        L.addWidget(self.jpeg)
        
        self.progress = QProgressBar()
        L.addWidget(self.progress)

        self.log = QTextEdit()
        self.log.setReadOnly(True)
        L.addWidget(self.log)
        
        self.progress = QProgressBar()
        self.progress.setMaximum(100)
        self.progress.setValue(0)
        L.addWidget(self.progress)
        
        self.status_label = QLabel("Idle")
        L.addWidget(self.status_label)
        
        row = QHBoxLayout()
        self.btn_start = QPushButton("Start")
        self.btn_cancel = QPushButton("Cancel")
        row.addWidget(self.btn_start)
        row.addWidget(self.btn_cancel)
        L.addLayout(row)

        self.btn_start.clicked.connect(self.start)
        self.btn_cancel.clicked.connect(self.cancel)
        
        self.setLayout(L)

    def log_msg(self, m):
        self.log.append(m)
    def update_percent(self, value):
        self.progress.setValue(value)
    def sel_input(self):
        f, _ = QFileDialog.getOpenFileName(self, "", "", "PDF (*.pdf)")
        if f:
            self.input = f
            self.input_lbl.setText(f)

    def sel_output(self):
        f, _ = QFileDialog.getSaveFileName(self, "", "", "PDF (*.pdf)")
        if f:
            self.out_edit.setText(f)

    def start(self):
        self.progress.setValue(0)
        if not hasattr(self, "input"):
            QMessageBox.warning(self, "Error", "Select input PDF")
            return

        if not os.path.exists(self.input):
            QMessageBox.critical(self, "Error", "Input file missing")
            return

        out = self.out_edit.text()
        if not out:
            QMessageBox.warning(self, "Error", "Select output path")
            return

        gs = self.cfg["ghostscript_path"] or find_ghostscript()
        if not gs:
            QMessageBox.critical(self, "Error", "Ghostscript not found")
            return

        self.btn_start.setEnabled(False)

        self.worker = Worker(
            gs,
            self.input,
            out,
            self.dpi.value(),
            self.jpeg.value()
        )
        self.quality_preset.currentTextChanged.connect(self.apply_preset)
        self.worker.progress.connect(self.log_msg)
        self.worker.percent.connect(self.update_percent)  # ✅ REQUIRED
        self.worker.done.connect(self.done)
        self.progress.setValue(0)
        self.status_label.setText(
            f"DPI: {self.dpi.value()} | JPEG: {self.jpeg.value()}"
        )
        self.status_label.setText("Starting...")
        self.worker.start()

    def cancel(self):
        if hasattr(self, "worker"):
            self.worker.cancel()

    def done(self, ok, size):
        self.btn_start.setEnabled(True)
        if ok:
            QMessageBox.information(self, "Done", f"{size:.2f} MB")
        else:
            QMessageBox.warning(self, "Stopped", "Failed or cancelled")