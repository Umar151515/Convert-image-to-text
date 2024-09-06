__all__ = ['Rect']


class Coordinates:
    def __set_name__(self, owner, name):
        self.name = '_' + name
 
    def __get__(self, instance, owner):
        return getattr(instance, self.name)
 
    def __set__(self, instance, value):
        if self.name in ('_x_cor', '_y_cor', '_x_center', '_y_center', '_right', '_bottom'):
            if not isinstance(value, (int, float)):
                raise TypeError(f'{self.name} должен быть целым или дробным значением.')
            if self.name == '_right':
                instance.x_cor = value + 1 - instance.size_x
            elif self.name == '_bottom':
                instance.y_cor = value + 1 - instance.size_y
            elif self.name == '_x_center':
                instance.x_cor = (2*value - instance.size_x)/2
            elif self.name == '_y_center':
                instance.y_cor = (2*value - instance.size_y)/2
        elif self.name in ('_top_left', '_top_right', '_bottom_left', '_bottom_right', '_top_center', 
                        '_bottom_center', '_right_center', '_left_center', '_center'):
            if not isinstance(value, tuple) or len(value) != 2:
                raise TypeError(f'{self.name} должен быть кортежем с двумя целыми или дробными значениями.')
            elif not (isinstance(value[0], (int, float)) or isinstance(value[1], (int, float))):
                raise TypeError(f'у {self.name} не целые или дробные значение.')
            right = value[0] + 1 - instance.size_x
            bottom = value[1] + 1 - instance.size_y
            x_center = (2*value[0] - instance.size_x)/2
            y_center = (2*value[1] - instance.size_y)/2
            if self.name == '_top_left':
                instance.x_cor = value[0]
                instance.y_cor = value[1]
            elif self.name == '_top_right':
                instance.x_cor = right
                instance.y_cor = value[1]
            elif self.name == '_bottom_left':
                instance.x_cor = value[0]
                instance.y_cor = bottom
            elif self.name == '_bottom_right':
                instance.x_cor = right
                instance.y_cor = bottom
            elif self.name == '_top_center':
                instance.x_cor = x_center
                instance.y_cor = value[1]
            elif self.name == '_bottom_center':
                instance.x_cor = x_center
                instance.y_cor = bottom
            elif self.name == '_right_center':
                instance.x_cor = right
                instance.y_cor = y_center
            elif self.name == '_left_center':
                instance.x_cor = value[0]
                instance.y_cor = y_center
            elif self.name == '_center':
                instance.x_cor = x_center
                instance.y_cor = y_center
        setattr(instance, self.name, value)
        instance.views_location()


class Rect:
    x_cor = Coordinates()
    y_cor = Coordinates()
    x_center = Coordinates()
    y_center = Coordinates()
    right = Coordinates()
    bottom = Coordinates()
    top_left = Coordinates()
    top_right = Coordinates()
    bottom_left = Coordinates()
    bottom_right = Coordinates()
    top_center = Coordinates()
    bottom_center = Coordinates()
    right_center = Coordinates()
    left_center = Coordinates()
    center = Coordinates()

    def __init__(self, x_cor: int|float, y_cor: int|float, text_image: str=None, size_x: int=None, size_y: int=None):
        self._coordinate_check(x_cor)
        self._coordinate_check(y_cor)
        if not(text_image is None):
            from .text_image import TextImage
            if not isinstance(text_image, TextImage):
                raise TypeError('text_image должен быть экземпляром класса TextImage.')
            self.text_image = text_image
            self.size_x = text_image.size_x
            self.size_y = text_image.size_y
        elif not(size_x is None) and not(size_y is None):
            if not isinstance(size_x, int) or not isinstance(size_y, int) or size_x < 0 or size_y < 0:
                raise TypeError('Размер долен быть целым и не отрицательным значением.')
            self.size_x = size_x
            self.size_y = size_y
        else:
            raise TypeError('Не было передано ни text_image, ни width, height.')
        self._x_cor = x_cor
        self._y_cor = y_cor
        self.views_location()

    def views_location(self, new_x_cor: int|float = None, new_y_cor: int|float = None):
        if not new_x_cor is None:
            self._x_cor = new_x_cor
        if not new_y_cor is None:
            self._y_cor = new_y_cor
        self._right = self.x_cor - 1 + self.size_x
        self._bottom = self.y_cor - 1 + self.size_y
        self._x_center = (self.x_cor+self.right+1) / 2
        self._y_center = (self.y_cor+self.bottom+1) / 2
        self._top_left = (self.x_cor, self.y_cor)
        self._top_right = (self.right, self.y_cor)
        self._bottom_left = (self.x_cor, self.bottom)
        self._bottom_right = (self.right, self.bottom)
        self._top_center = (self.x_center, self.y_cor)
        self._bottom_center = (self.x_center, self.bottom)
        self._right_center = (self.right, self.y_center)
        self._left_center = (self.x_cor, self.y_center)
        self._center = (self.x_center, self.y_center)
        
    @property
    def size(self):
        return self.size_x, self.size_y

    @classmethod
    def _coordinate_check(cls, value):
        if not isinstance(value, (int, float)):
            raise TypeError('Координаты должы быть целым числом или дробным.')

