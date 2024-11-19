import sys
from PySide6 import QtWidgets
from Interface.interface import InterfaceLoader 
from TextToBrail.texttobrail import TextToBrailLoader  
from TexttoSpeech.texttospeech import TextToSpeechLoader

class AppManager:
    def __init__(self):
        self.app = QtWidgets.QApplication.instance() or QtWidgets.QApplication(sys.argv)
        self.main_window = InterfaceLoader(self)
        self.text_to_braille_window = TextToBrailLoader(self)
        self.text_to_speech_window= TextToSpeechLoader(self)

    def show_main_window(self):
        self.text_to_braille_window.ui.hide()
        self.main_window.show()

    def show_text_to_braille(self):
        self.main_window.ui.hide()
        self.text_to_braille_window.show()

    def show_text_to_speech(self):
        self.main_window.ui.hide()
        self.text_to_speech_window.show()

def runapp():
    app_manager = AppManager()
    app_manager.show_main_window()
    sys.exit(app_manager.app.exec())

if __name__ == "__main__":
    runapp()
