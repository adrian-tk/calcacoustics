from kivy.uix.textinput import TextInput
from kivy.uix.button import Button

import re

class FloatInput(TextInput):
    kname=""
    pat=re.compile('[^0-9]')
    def insert_text(self, substring, from_undo=False):
        pat=self.pat
        if '.' in self.text:
            s = re.sub(pat, "", substring)
        else:
            s = '.'.join(
                    re.sub(pat, "", s)
                    for s in substring.split('.', 1)
                    )
        return super().insert_text(s, from_undo=from_undo)

class DescButton(Button):
    def __init__(self, btnsize=30, **kwargs):
        super().__init__(**kwargs)
        self.text = 'V'
        self.size_hint = (None, None)
        self.size = (btnsize, btnsize)
