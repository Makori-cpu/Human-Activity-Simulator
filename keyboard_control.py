
class KeyboardController:

    def __init__(self, entry):
        self.entry = entry

    def type_text(self, text):
        self.entry.insert("end", text)

    def clear_text(self):
        self.entry.delete(0, "end")
