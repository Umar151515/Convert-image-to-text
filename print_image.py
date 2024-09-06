import imageio
from PIL import Image, ImageEnhance

import pcg


class PrintImage:
    def __init__(self):
        self.width = 120
        self.height = 30

        self.i = 0
        self.images_str = []
        self.strings = []

        self.image_str = ''
        self.fps = pcg.FPS(pcg.FPS.MAX_DESIRED_FPS)
        
        self.console = pcg.WindowConsole(self.width, self.height)

        self.fps = pcg.FPS(0)

    def set_file(self, width, height, ascii_chars, file_name):
        self.width = width
        self.height = height
        self.ascii_chars = ascii_chars
        self.file_name = file_name
        self.fps.desired_fps = pcg.FPS.MAX_DESIRED_FPS
        self.i = 0

        self.console.set_size(width, height)

        if file_name:
            self.set_image_str()
        
    def set_image_str(self):
        self.images_str.clear()
        self.strings.clear()
        pil_image = Image.open(self.file_name)

        if self.is_animated_gif(self.file_name):
            try:
                while True:
                    self.images_str.append(self.get_image_str(pil_image.convert("RGBA")))
                    pil_image.seek(pil_image.tell() + 1)
            except EOFError:
                for i in self.images_str:
                    self.strings.append(i.text)
                self.image_str = self.images_str[0]
                self.fps.desired_fps = self.get_gif_fps(self.file_name)
        else:
            self.image_str = self.get_image_str(pil_image)

    def get_image_str(self, pil_image):
        brightness_values = self.get_brightness(pil_image, (self.console.size_x, self.console.size_y))
        if not self.ascii_chars:
            image_str = pcg.TextImage(self.image_to_str(brightness_values, self.console.size_x, self.console.size_y))
        else:
            image_str = pcg.TextImage(self.image_bg_to_str(brightness_values, self.console.size_x, self.console.size_y))
        return image_str
    
    def get_gif_fps(self, filename):
        gif = Image.open(filename)

        try:
            while True:
                gif.seek(gif.tell() + 1)
        except EOFError:
            pass
        fps = gif.info['duration']
        if fps == 0:
            fps = 100
        fps = 1000 / fps
        return fps

    def get_brightness(self, pil_image, size=None):
        if not size is None:
            pil_image = pil_image.resize(size)

        enhancer = ImageEnhance.Brightness(pil_image)
        image = enhancer.enhance(2)

        if self.ascii_chars:
            image = image.convert('L')

        width, height = image.size

        brightness_values = []

        for y in range(height):
            for x in range(width):
                brightness_values.append([])

                brightness = image.getpixel((x, y))

                brightness_values[y].append(brightness)

        return brightness_values

    def image_bg_to_str(self, brightness_values, width, height):
        scale = (len(self.ascii_chars)-1) / 255

        image_str = ''

        for y in range(height):
            for x in range(width):
                image_str += self.ascii_chars[int(brightness_values[y][x]*scale)]
            image_str += '\n'

        return image_str

    def image_to_str(self, brightness_values, width, height):
        image_str = ''

        for y in range(height):
            for x in range(width):
                color_code = f"\033[38;2;{brightness_values[y][x][0]};{brightness_values[y][x][1]};{brightness_values[y][x][2]}m"
                square_symbol = "█"
                reset_code = "\033[0m"
                image_str += f'{color_code}{square_symbol}{reset_code}'
            image_str += '\n'

        return image_str
    
    def is_animated_gif(self, file_path):
        try:
            reader = imageio.get_reader(file_path)
            return len(reader) > 1
        except Exception as e:
            return False

    def print(self):
        self.console.fill(' ')

        if self.images_str:
            if self.i >= len(self.images_str):
                self.i = 0
            self.image_str = self.images_str[self.i]
            self.i += 1

        self.fps.delay()

        pcg.draw.blit(self.console, self.image_str, (0, 0))
        
        self.console.update()