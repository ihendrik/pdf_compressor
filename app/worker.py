from PySide6.QtCore import QThread, Signal
from .compressor import run_gs_with_progress, size_mb
from .constants import MAX_ITERS, PRESET_QUALITY

class Worker(QThread):
    percent = Signal(int)
    progress = Signal(str)
    done = Signal(bool, float)

    def __init__(self, gs, inp, out, dpi, jpeg):
        super().__init__()
        self.gs = gs
        self.inp = inp
        self.out = out
        self.dpi = dpi
        self.jpeg = jpeg
        self._cancel = False

    def cancel(self):
        self._cancel = True

    def run(self):
        self.progress.emit("Starting compression...")

        ok = run_gs_with_progress(
            self.gs,
            self.inp,
            self.out,
            self.dpi,
            self.jpeg,
            self.percent.emit,
            lambda: self._cancel
        )

        if ok:
            size = size_mb(self.out)
            self.progress.emit(f"Completed: {size:.2f} MB")
        else:
            size = 0
            self.progress.emit("Compression failed or cancelled")

        self.done.emit(ok, size)