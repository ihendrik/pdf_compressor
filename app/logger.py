from PySide6.QtCore import QObject, Signal

class UILogger(QObject):
    log = Signal(str)

    def info(self, msg):
        self.log.emit(msg)