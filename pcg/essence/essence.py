import math

from .drawing_tools import draw
from .collision_shapes import Rect
from .text_image import TextImage
from ..core.window_console import WindowConsole


__all__ = ['Essence', 'GroupEssence', 'collision']


class Essence:
    def __init__(self, instance):
        if not hasattr(instance, 'rect') or not hasattr(instance, 'image'):
            raise AttributeError(f'{instance.__class__.__name__} не имеет атрибутов rect или image.')
        elif not isinstance(instance.rect, Rect) or not isinstance(instance.image, TextImage):
            raise TypeError("image должен быть экземпляром класса TextImage, а rect должен быть экземпляром класса Rect.")


class GroupEssence:
    def __init__(self):
        self.groups = set()

    def get_list(self):
        return list(self.groups)

    def add(self, essence: Essence):
        if not issubclass(essence.__class__, Essence):
            raise TypeError(f'Объект {essence.__class__.__name__} должен наследоваться от класса Essence.')
        self.groups.add(essence)

    def remove(self, essence: Essence):
        self.groups.remove(essence)

    def pop(self, value: int):
        self.groups.pop(value)

    def blit(self, console: WindowConsole):
        for group in self.groups:
            draw.blit(console, group.image, group.rect)

    def update(self):
        for group in set(self.groups):
            if 'update' in group.__dir__():
                group.update()

    def __len__(self):
        return len(self.groups)

    def __iter__(self):
        self._enumeration = 0
        return self
    
    def __next__(self):
        if self._enumeration < len(self.groups):
            essence = list(self.groups)[self._enumeration]
            self._enumeration += 1
            return essence
        else:
            raise StopIteration

class collision:
    @staticmethod
    def collision_rect(rect_1: Rect|Essence, rect_2: Rect|Essence):
        if not isinstance(rect_1, Rect) or not isinstance(rect_2, Rect):
            if not isinstance(rect_1, Essence) or not isinstance(rect_2, Essence):
                raise TypeError("rect_1 и rect_2 должны быть экземплярами класса Rect или класса, который наследуется от класса Essence.")
        if isinstance(rect_1, Essence) and isinstance(rect_2, Essence):
            rect_1 = rect_1.rect
            rect_2 = rect_2.rect
        
        x1 = max(rect_1.x_cor, rect_2.x_cor)
        y1 = max(rect_1.y_cor, rect_2.y_cor)
        x2 = min(rect_1.right, rect_2.right)
        y2 = min(rect_1.bottom, rect_2.bottom)

        if x2 < x1 or y2 < y1:
            return False
        return True

    @staticmethod
    def collision_essence_group(essence_1: Rect|Essence, group: GroupEssence, essence_2_delete: bool=False):
        if not isinstance(group, GroupEssence):
            raise TypeError('group должен быть экземпляром класса GroupEssence.')
        for essence_2 in group:
            if collision.collision_rect(essence_1, essence_2):
                if essence_2_delete:
                    group.remove(essence_2)
                return True
        return False
            
    @staticmethod
    def collision_groups(group_1: GroupEssence, group_2: GroupEssence, 
                        essence_1_delete: bool = False, essence_2_delete: bool=False):
        if not isinstance(group_1, GroupEssence) or not isinstance(group_2, GroupEssence):
            raise TypeError('group_1 и group_2 должны быть экземплярами класса GroupEssence.')
        for essence_1 in group_1:
            for essence_2 in group_2:
                if collision.collision_rect(essence_1, essence_2):
                    if essence_1_delete:
                        group_1.remove(essence_1)
                    if essence_2_delete:
                        group_2.remove(essence_2)
                    return True
        return False

    def collision_rect_circle_BETA(rect: Rect|Essence, circle: Rect|Essence):
        if not isinstance(rect, Rect) or not isinstance(circle, Rect):
            if not isinstance(rect, Essence) or not isinstance(circle, Essence):
                raise TypeError("rect и circle должны быть экземплярами класса Rect, либо экземплярами класса, который наследуется от класса Essence.")
        if isinstance(rect, Essence) and isinstance(circle, Essence):
            rect = rect.rect
            circle = circle.rect

        circle_r = circle.right-circle.x_center

        distance_x = abs(circle.x_center - rect.x_cor - rect.size_x / 2)
        distance_y = abs(circle.y_center - rect.y_cor - rect.size_y / 2)

        if distance_x > rect.size_x / 2 + circle_r or distance_y > rect.size_y / 2 + circle_r:
            return False

        if distance_x <= rect.size_x / 2 or distance_y <= rect.size_y / 2:
            return True

        corner_distance_sq = (distance_x - rect.size_x / 2) ** 2 + (distance_y - rect.size_y / 2) ** 2

        if corner_distance_sq <= circle_r ** 2:
            return True
        return False

    def collision_circle_BETA(circle_1: Rect|Essence, circle_2: Rect|Essence):
        if not isinstance(circle_1, Rect) or not isinstance(circle_2, Rect):
            if not isinstance(circle_1, Essence) or not isinstance(circle_2, Essence):
                raise TypeError("circle_1 и circle_2 должны быть экземплярами класса Rect, либо экземплярами класса, который наследуется от класса Essence.")
        if isinstance(circle_1, Essence) and isinstance(circle_2, Essence):
            circle_1 = circle_1.rect
            circle_2 = circle_2.rect

        circle_1_radius = circle_1.right-circle_1.x_center
        circle_2_radius = circle_2.right-circle_2.x_center

        distance_x = circle_2.x_cor - circle_1.x_cor
        distance_y = circle_2.y_cor - circle_1.y_cor

        distance = math.sqrt(distance_x**2 + distance_y**2)

        radius_sum = circle_1_radius + circle_2_radius

        if distance <= radius_sum:
            return True
        return False