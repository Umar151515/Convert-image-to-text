import math

from .text_image import TextImage
from .collision_shapes import Rect
from ..core.window_console import WindowConsole


__all__ = ['draw']


class draw:
    @staticmethod
    def blit(console: WindowConsole, text_image: TextImage, cors: Rect|tuple[int|float, int|float]):
        if not isinstance(text_image, TextImage) and not isinstance(text_image, WindowConsole):
            raise TypeError('text_image должен быть экземпляром класса TextImage.')
        if isinstance(cors, Rect):
            x_cor = cors.x_cor
            y_cor = cors.y_cor
        elif isinstance(cors, tuple):
            if len(cors) != 2 or not isinstance(cors[0], (int, float)) or not isinstance(cors[1], (int, float)):
                raise TypeError('Кортеж должен принимать 2 целые или дробнные значение (x_cor, y_cor).')
            x_cor = cors[0]
            y_cor = cors[1]
        else:
            raise AttributeError('Не было передано ни объекта Rect, ни кортежа с координатами.')
        if not isinstance(console, WindowConsole):
            raise TypeError('Объект console должен быть объектом класса WindowConsole.')

        cursor_x = int(x_cor - console.x_cor)
        cursor_y = int(y_cor - console.y_cor)

        for image in text_image.image_shares:
            for row in image:
                if cursor_x <= console.size_x-1 and cursor_x >= 0 and\
                    cursor_y <= console.size_y-1 and cursor_y >= 0 and row != ' ':

                    console.field[cursor_y][cursor_x] = row
                cursor_x += 1
            cursor_y += 1
            cursor_x = int(x_cor - console.x_cor)

    @staticmethod
    def draw_rectangle(width: int, height: int, fill: str, width_side: int=None, height_side: int=None):
        if len(fill) != 1:
            raise ValueError("fill должен содержать ровно один символ")
        if not isinstance(width, int) or width < 0 or not isinstance(height, int) or height < 0:
            raise TypeError('Размер width, height долен быть целым и не отрицательным числом.')
        if width_side is None:
            width_side = width
        if height_side is None:
            height_side = height
        if not isinstance(width_side, int) or width_side < 0 or\
              not isinstance(height_side, int) or height_side < 0:
            raise TypeError('width_side, height_side долен быть целым и не отрицательным числом.')
        
        rectangle = ""
        for y in range(height):
            row = ""
            for x in range(width):
                if x < width_side or x >= width - width_side or y < height_side or y >= height - height_side:
                    row += fill
                else:
                    row += " "
            rectangle += row + "\n"
        
        return TextImage(rectangle)

    @staticmethod
    def draw_circle(radius: int, fill: str, width: int=None):
        if len(fill) != 1:
            raise ValueError("fill должен содержать ровно один символ")
        if not isinstance(radius, int) or radius < 0:
            raise TypeError('radius быть целым и не отрицательным числом.')
        if not isinstance(width, int) or width < 0:
            if not width is None:
                raise TypeError('width долен быть целым и не отрицательным числом.')
        if width is None:
            width = radius
        
        circle = ""
        for y in range(-radius, radius+1):
            row = ""
            for x in range(-radius, radius+1):
                dist = math.sqrt(x**2 + y**2)
                if dist <= radius and dist >= radius - width:
                    row += fill
                else:
                    row += " "
            circle += row + "\n"
        
        return TextImage(circle)