import sys
import threading

from PyQt5.QtWidgets import QApplication

from print_image import PrintImage
from simple_app import SimpleApp


class Core:
    def __init__(self):
        self.print_image = PrintImage()
        self.app = QApplication(sys.argv)
        self.window = SimpleApp(self.print_image)

        self.print_image.set_file(120, 30, '', '')


core = Core()

def func_print_image():
    while True:
        if core.print_image.image_str:
            core.print_image.print()

if __name__ == '__main__':
    threading.Thread(target=func_print_image).start()
    sys.exit(core.app.exec_())