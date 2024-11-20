import fitz
import cv2
import pytesseract
from PySide6 import QtCore, QtWidgets
from PySide6.QtUiTools import QUiLoader
from PySide6.QtGui import QTextDocument, QPageSize
from PySide6.QtPrintSupport import QPrintDialog, QPrinter
from PySide6.QtWidgets import QFileDialog
from converters import Convertor

loader = QUiLoader()
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

class TextToBrailLoader(QtCore.QObject):
    def __init__(self, app_manager=None):
        super().__init__()
        self.app_manager = app_manager  
        print(f"TextToBrailLoader initialized with app_manager: {self.app_manager}")

        self.ui = loader.load("./TextToBrail/texttobrail.ui", None)
        self.ui.setWindowTitle("Text to Braille Conversion")
        self.ui.convertbutt.clicked.connect(self.convert)
        self.ui.clipboardbutt.clicked.connect(self.copytoclipboard)
        self.ui.backbutt.clicked.connect(self.goback)  
        self.ui.switchbutt.clicked.connect(self.switch)
        self.ui.openpdfbutt.clicked.connect(self.open_pdf)
        self.ui.printbutt.clicked.connect(self.save_and_print_braille_pdf)
        self.ui.openimgbutt.clicked.connect(self.extract_text_from_image)

        self.languages = {"input_text": "English", "output_text": "Braille"}
        self.update_language_labels()

        self.apply_styles()

    def show(self):
        self.ui.show()

    def convert(self):
        input_text = self.ui.inputbox.toPlainText()
        if self.languages["input_text"] == "English" and self.languages["output_text"] == "Braille":
            output_text = Convertor().text_to_braille_convert(input_text)
        elif self.languages["input_text"] == "Braille" and self.languages["output_text"] == "English":
            output_text = Convertor().braille_to_text_convert(input_text)
        else:
            output_text = "Unsupported language conversion"

        self.ui.outputbox.setPlainText(output_text)
        self.ui.clipboardbutt.setText("❒  Copy") 

    def open_pdf(self):
        file_path, _ = QtWidgets.QFileDialog.getOpenFileName(self.ui, "Open PDF", "", "PDF Files (*.pdf)")
        if file_path:
            self.ui.inputbox.clear()
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
            self.ui.inputbox.setPlainText(extracted_text)
        except Exception as e:
            self.ui.inputbox.setPlainText(f"Error reading PDF: {e}")

    def save_and_print_braille_pdf(self):
        braille_text = self.ui.outputbox.toPlainText()
        if braille_text:
            file_path, _ = QtWidgets.QFileDialog.getSaveFileName(self.ui, "Save Braille as PDF", "", "PDF Files (*.pdf)")
            if file_path:
                document = QTextDocument(braille_text)
                printer = QPrinter()
                printer.setOutputFormat(QPrinter.PdfFormat)
                printer.setOutputFileName(file_path)
                document.print_(printer)

                print_printer = QPrinter()
                print_printer.setPageSize(QPageSize(QPageSize.A4))
                print_printer.setOutputFormat(QPrinter.NativeFormat)

                dialog = QPrintDialog(print_printer, self.ui)
                if dialog.exec() == QPrintDialog.Accepted:
                    document.print_(print_printer)

    def copytoclipboard(self):
        text_to_copy = self.ui.outputbox.toPlainText()
        clipboard = QtWidgets.QApplication.clipboard()
        clipboard.setText(text_to_copy)
        self.ui.clipboardbutt.setText("✔  Copied")

    def goback(self):
        print("goback button pressed")
        if self.app_manager:
            self.ui.hide()
            self.app_manager.show_main_window()  
        else:
            print("Error: app_manager is not set.")

    def extract_text_from_image(self,image_path):
        image_path, _ = QFileDialog.getOpenFileName(None, "Select an Image", "", "Image Files (*.png *.jpg *.jpeg *.bmp)")
        image = cv2.imread(image_path)
        gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        _, thresh_image = cv2.threshold(gray_image, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

        text = pytesseract.image_to_string(thresh_image)
        self.ui.inputbox.setPlainText(text)
    
    def switch(self):
        self.languages["input_text"], self.languages["output_text"] = self.languages["output_text"], self.languages["input_text"]
        self.update_language_labels()
        self.ui.clipboardbutt.setText("❒  Copy") 

    def update_language_labels(self):
        self.ui.Inputlang.setText(self.languages["input_text"])
        self.ui.Outputlang.setText(self.languages["output_text"])

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


