braille_dict = {
    "a": "⠁", "b": "⠃", "c": "⠉", "d": "⠙", "e": "⠑", "f": "⠋", "g": "⠛", "h": "⠓", "i": "⠊", "j": "⠚",
    "k": "⠅", "l": "⠇", "m": "⠍", "n": "⠝", "o": "⠕", "p": "⠏", "q": "⠟", "r": "⠗", "s": "⠎", "t": "⠞",
    "u": "⠥", "v": "⠧", "w": "⠺", "x": "⠭", "y": "⠽", "z": "⠵",

    "1": "⠼⠁", "2": "⠼⠃", "3": "⠼⠉", "4": "⠼⠙", "5": "⠼⠑", "6": "⠼⠋", "7": "⠼⠛", "8": "⠼⠓", "9": "⠼⠊", "0": "⠼⠚",

    ".": "⠲", ",": "⠂", ";": "⠆", ":": "⠒", "!": "⠖", "?": "⠦", "'": "⠄", "-": "⠤", "(": "⠶", ")": "⠶",
    "/": "⠌", "@": "⠈⠁", "+": "⠖", "=": "⠶", "*": "⠔", "<": "⠦", ">": "⠴",

    "CAPITAL": "⠠", 
    "NUMERIC": "⠼"  
}

reverse_braille_dict = {v: k for k, v in braille_dict.items()}

class Convertor:
    def __init__(self):
        self.braille = ""
        self.text = ""

    def text_to_braille_convert(self, text):
        self.braille = ""  
        for char in text:
            if char == " ":
                self.braille += " "
            elif char == "\n":
                self.braille += "\n"
            elif char.isupper():
                self.braille += braille_dict["CAPITAL"]
                self.braille += braille_dict.get(char.lower(), "")
            elif char.isdigit():
                self.braille += braille_dict["NUMERIC"]
                self.braille += braille_dict.get(char, "")
            else:
                self.braille += braille_dict.get(char, "")
        return self.braille

    def braille_to_text_convert(self, braille):
        self.text = "" 
        is_caps = False
        is_numeric = False
        buffer = ""

        for symbol in braille:
            if symbol == " ":
                self.text += buffer + " "
                buffer = ""
                is_numeric = False
            elif symbol == "\n":
                self.text += buffer + "\n"
                buffer = ""
                is_numeric = False
            elif symbol == braille_dict["CAPITAL"]:
                is_caps = True
            elif symbol == braille_dict["NUMERIC"]:
                is_numeric = True
            else:
                character = reverse_braille_dict.get(symbol, "")
                if character:
                    if is_numeric:
                        buffer += character
                        if not buffer.isdigit():
                            self.text += buffer
                            buffer = ""
                            is_numeric = False
                    else:
                        if is_caps:
                            character = character.upper()
                            is_caps = False 
                        self.text += buffer + character
                        buffer = ""

        if buffer:
            self.text += buffer
        return self.text

