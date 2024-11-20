from PySide6 import QtWidgets, QtCore
from PySide6.QtUiTools import QUiLoader

loader = QUiLoader()

class InterfaceLoader(QtCore.QObject):
    def __init__(self, app_manager):
        super().__init__()
        self.app_manager = app_manager
        self.ui = loader.load("./Interface/interface.ui", None)
        self.ui.setWindowTitle("Automated Braille Conversion Tool - Modern UI")

        self.ui.texttobraillebut.clicked.connect(self.texttobraille)
        self.ui.texttospeechbutt.clicked.connect(self.texttospeech)

        self.apply_styles()

    def show(self):
        self.ui.show()

    def texttobraille(self):
        self.ui.hide()
        self.app_manager.show_text_to_braille()

    def texttospeech(self):
        self.ui.hide()
        self.app_manager.show_text_to_speech()

    def pdftobraille(self):
        self.ui.hide()
        self.app_manager.show_pdf_to_braille()

    def apply_styles(self):
        self.ui.setStyleSheet("""
            QMainWindow {
                background-image: url('./assets/bg.png');  
                background-repeat: no-repeat;
                background-position: center;
            }
            QPushButton {
                background-color: rgba(255, 255, 255, 0.1);
                border-radius: 15px;
                margin: 10px;
                color: #ffffff;
            }
            QPushButton:hover {
                background-color: rgba(255, 255, 255, 0.2);
            }
            QPushButton:pressed {
                background-color: rgba(255, 255, 255, 0.3);
            }
        """)

