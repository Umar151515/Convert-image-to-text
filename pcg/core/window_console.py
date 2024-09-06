import os
import sys

from ..essence.collision_shapes import Rect


__all__ = ['WindowConsole']


class WindowConsole:
    __instance = None

    def __new__(cls, *args, **kwargs):
        if cls.__instance is None or not cls is WindowConsole:
            cls.__instance = super().__new__(cls)
        
        return cls.__instance
    
    def __del__(self):
        WindowConsole.__instance = None

    def __init__(self, size_x: int, size_y: int):
        self._x_cor = 0
        self._y_cor = 0

        self.set_size(size_x, size_y)

        self.allow_console_resizing = False
        
        self.field = []
        self.fill(' ')

        self.update()

    @property
    def size_x(self):
        return self._size_x

    @size_x.setter
    def size_x(self, value):
        self._size_x = value
        self._coordinate_check(value)
        if type(self).__name__ == 'WindowConsole':
            os.system(f'mode con: cols={value}')

    @property
    def size_y(self):
        return self._size_y

    @size_y.setter
    def size_y(self, value):
        self._size_y = value
        self._coordinate_check(value)
        if type(self).__name__ == 'WindowConsole':
            os.system(f'mode con: lines={value}')

    @property
    def x_cor(self):
        return self._x_cor
    
    @x_cor.setter
    def x_cor(self, value: int | float):
        self._cor_check(value)
        self._x_cor = value
    
    @property
    def y_cor(self):
        return self._y_cor
    
    @y_cor.setter
    def y_cor(self, value: int | float):
        self._cor_check(value)
        self._y_cor = value
    
    @classmethod
    def _coordinate_check(cls, value: int):
        if not isinstance(value, int) or value < 0:
            raise TypeError('Размер консоли долен быть целым и не отрицательным числом.')
        
    def _cor_check(self, value: int | float):
        if not isinstance(value, int) and not isinstance(value, float):
            raise TypeError('cor консоли долен быть числом.')
        
    def hide_cursor(self):
        if sys.platform.startswith('win'):
            sys.stdout.write('\033[?25l')
        else:
            sys.stdout.write('\033[?25l\033[?1c')

    def show_cursor(self):
        if sys.platform.startswith('win'):
            sys.stdout.write('\033[?25h')
        else:
            sys.stdout.write('\033[?25h\033[?8c')
    
    def get_console_size(self):
        size = os.get_terminal_size()
        return size.columns, size.lines

    def set_size(self, x_auxiliary: int, y_auxiliary: int):
        self.size_x = x_auxiliary
        self.size_y = y_auxiliary
        if type(self).__name__ == 'WindowConsole':
            os.system(f'mode con: cols={x_auxiliary} lines={y_auxiliary}')
            self.hide_cursor()

    def update(self):
        self.text = ''

        for texts in self.field:
            self.text += ''.join(texts)

        console_size = self.get_console_size()
        if self.allow_console_resizing:
            if (self.size_x, self.size_y) != console_size:
                self.size_x, self.size_y = console_size
                self.hide_cursor()
        elif not self.allow_console_resizing:
            if (self.size_x, self.size_y) != console_size:
                self.set_size(self.size_x, self.size_y)
            
        print(self.text, sep='', end='')

    def fill(self, symbol: str):
        if len(symbol) != 1:
            raise ValueError("symbol должен содержать ровно один символ")
        self.field.clear()

        for cell in range(self.size_y):
            cells = []
            for row in range(self.size_x):
                cells.append(symbol)
            if cell != self.size_y -1:
                cells.append('\n')
            self.field.append(cells)

    def get_rect(self):
        return Rect(self.x_cor, self.y_cor, size_x=self.size_x, size_y=self.size_y)