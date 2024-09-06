from .collision_shapes import Rect
from ..core.window_console import WindowConsole


__all__ = ['TextImage', 'Surface']

def colored_string_length(text):
    in_escape = False
    length = 0

    for char in text:
        if char == '\033':
            in_escape = True
        elif in_escape:
            if char == 'm':
                in_escape = False
            continue
        else:
            length += 1

    return length

class TextImage():
    def __init__(self, text: str):
        self.text = text

    @property
    def text(self):
        return self._text
    
    @text.setter
    def text(self, new_text):
        self._check_text(new_text)

        self._text = new_text

        self.image_shares = new_text.split('\n')
        
        self.size_x = colored_string_length(max(self.image_shares, key=colored_string_length))
        self.size_y = len(self.image_shares)

    def _check_text(self, new_text):
        if not isinstance(new_text, str):
            raise TypeError('text должен быть строкой.')
        if not new_text:
            raise TypeError('text не должен быть пустым.')
    
    @property
    def size(self):
        return self.size_x, self.size_y
        
    def get_rect(self):
        return Rect(0, 0, text_image = self)
    

class Surface(WindowConsole, TextImage):
    def __init__(self, size_x: int, size_y: int):
        super().__init__(size_x, size_y)
        self.update()

    def update(self):
        _text = ''

        for texts in self.field:
            _text += ''.join(texts)
        
        self.text = _text