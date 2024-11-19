import fitz
import pyttsx3
from PySide6 import QtCore, QtWidgets
from PySide6.QtUiTools import QUiLoader

loader = QUiLoader()

class TextToSpeechLoader(QtCore.QObject):
    def __init__(self, app_manager=None):
        super().__init__()
        self.app_manager = app_manager

        self.ui = loader.load("./TextToSpeech/texttospeech.ui", None)
        self.ui.setWindowTitle("Text-to-Speech Conversion")

        self.engine = pyttsx3.init()

        self.ui.speak_button.clicked.connect(self.speak_text)
        self.ui.backbutt_2.clicked.connect(self.goback)
        self.ui.open_pdf_button.clicked.connect(self.open_pdf)

        self.apply_styles()

    def show(self):
        self.ui.show()

    def speak_text(self):
        text = self.ui.Inputbox.toPlainText()
        if text:
            try:
                self.engine.say(text)
                self.engine.runAndWait() 
            except Exception as e:
                print(f"Error speaking text: {e}")

    def goback(self):
        if self.app_manager:
            self.ui.hide()
            self.app_manager.show_main_window()
        else:
            print("Error: app_manager is not set.")

    def open_pdf(self):
        file_path, _ = QtWidgets.QFileDialog.getOpenFileName(self.ui, "Open PDF", "", "PDF Files (*.pdf)")
        if file_path:
            self.ui.Inputbox.clear()
            self.extract_text(file_path)

    def extract_text(self, file_path):
        try:
            pdf = fitz.open(file_path)
            extracted_text = ""
            for page_num in range(len(pdf)):
                page = pdf[page_num]
                text = page.get_text()
                extracted_text += f"--- Page {page_num + 1} ---\n{text}\n\n"
            pdf.close()
            self.ui.Inputbox.setPlainText(extracted_text)
        except Exception as e:
            self.ui.Inputbox.setPlainText(f"Error reading PDF: {e}")

    def closeEvent(self, event):
        self.engine.stop()
        event.accept()

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
