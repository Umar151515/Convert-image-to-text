import json

import pyperclip
from PyQt5.QtWidgets import (QWidget, QLabel, QLineEdit,
    QVBoxLayout, QHBoxLayout, QListWidget, QPushButton, QSpinBox, QFileDialog)
from PyQt5.QtGui import QPixmap, QMovie
from PyQt5.QtCore import Qt


class SimpleApp(QWidget):
    def __init__(self, print_image):
        super().__init__()

        self.print_image = print_image
        self.file_name = ''

        with open('gradient.json', 'r', encoding='utf-8') as file:
            self.gradients = json.load(file)

        self.gradient = self.gradients[0]

        self.init_ui()

    def init_ui(self):
        self.main_h_layout = QHBoxLayout()
        self.v_layout = QVBoxLayout()
        self.v_layout_2 = QVBoxLayout()
        self.h_layout = QHBoxLayout()

        self.new_file_button = QPushButton('Открыть новый файл')
        self.new_file_button.clicked.connect(self.open_image)
        self.label_image = QLabel()
        self.label_image.setAlignment(Qt.AlignCenter)
        self.line_edit = QLineEdit()
        self.line_edit.setPlaceholderText('Напишите что бы добавить градиент')
        self.add_gradient_button = QPushButton('Добавить градиент')
        self.add_gradient_button.clicked.connect(self.add_gradient)
        self.copy_text_button = QPushButton('Скопировать')
        self.copy_text_button.clicked.connect(self.copy_text)

        self.label = QLabel('Градиент')
        self.label.setAlignment(Qt.AlignCenter)
        self.label_2 = QLabel(self.gradient)
        self.list_widget = QListWidget()
        self.list_widget.itemClicked.connect(self.change_gradient)
        for gradient in self.gradients:
            self.list_widget.addItem(gradient)
        self.remove_gradient_button = QPushButton('Удалить градиент')
        self.remove_gradient_button.clicked.connect(self.remove_gradient)
        self.label_3 = QLabel('Размер экрана')
        self.label_3.setAlignment(Qt.AlignCenter)
        self.print_button = QPushButton('Напечатать')
        self.print_button.clicked.connect(self.print)

        self.spin_box = QSpinBox()
        self.spin_box.setMinimum(5)
        self.spin_box.setMaximum(200)
        self.spin_box.setValue(120)
        self.label_4 = QLabel('X')
        self.spin_box_2 = QSpinBox()
        self.spin_box_2.setMinimum(5)
        self.spin_box_2.setMaximum(100)
        self.spin_box_2.setValue(30)

        self.v_layout.addWidget(self.new_file_button)
        self.v_layout.addWidget(self.label_image)
        self.v_layout.addWidget(self.line_edit)
        self.v_layout.addWidget(self.add_gradient_button)
        self.v_layout.addWidget(self.copy_text_button)

        self.v_layout_2.addWidget(self.label)
        self.v_layout_2.addWidget(self.label_2)
        self.v_layout_2.addWidget(self.list_widget)
        self.v_layout_2.addWidget(self.remove_gradient_button)
        self.v_layout_2.addWidget(self.label_3)
        self.v_layout_2.addLayout(self.h_layout)
        self.v_layout_2.addWidget(self.print_button)

        self.h_layout.addWidget(self.spin_box, 2)
        self.h_layout.addWidget(self.label_4)
        self.h_layout.addWidget(self.spin_box_2, 2)

        self.main_h_layout.addLayout(self.v_layout)
        self.main_h_layout.addLayout(self.v_layout_2)

        self.setLayout(self.main_h_layout)
        
        self.setGeometry(150, 150, 800, 400)
        self.setWindowTitle('Convert image to text')
        self.show()

    def change_gradient(self, item):
        index = self.list_widget.row(item)

        self.gradient = self.gradients[index]
        self.label_2.setText(self.gradient)

    def open_image(self):
        options = QFileDialog.Options()
        options |= QFileDialog.ReadOnly

        self.file_name, _ = QFileDialog.getOpenFileName(self, 'Открыть изображение', '', 'Images (*.png *.xpm *.jpg *.bmp *.gif);;All Files (*)', options=options)

        if self.file_name:
            if self.print_image.is_animated_gif(self.file_name):
                movie = QMovie(self.file_name)
                self.label_image.setMovie(movie)
                movie.start()
            else:
                pixmap = QPixmap(self.file_name)
                scaled_pixmap = pixmap.scaled(self.label_image.size(), Qt.KeepAspectRatio)
                self.label_image.setPixmap(scaled_pixmap)

            self.label_image.setAlignment(Qt.AlignCenter)

    def add_gradient(self):
        self.gradients.append(self.line_edit.text())

        with open('gradient.json', 'w', encoding='utf-8') as json_file:
            json.dump(self.gradients, json_file, ensure_ascii=False)

        self.list_widget.clear()

        for gradient in self.gradients:
            self.list_widget.addItem(gradient)

    def remove_gradient(self):
        if self.gradient in self.gradients:
            self.gradients.remove(self.gradient)
            self.gradient = ''
            self.label_2.setText('')

            with open('gradient.json', 'w', encoding='utf-8') as json_file:
                json.dump(self.gradients, json_file, ensure_ascii=False)

            self.list_widget.clear()

            for gradient in self.gradients:
                self.list_widget.addItem(gradient)

    def copy_text(self):
        if self.print_image.image_str:
            if self.print_image.is_animated_gif(self.file_name):
                pyperclip.copy(self.print_image.images_str)
            else:
                pyperclip.copy(self.print_image.image_str.text)

    def print(self):
        if self.gradient and self.file_name:
            self.print_image.set_file(self.spin_box.value(), self.spin_box_2.value(), 
                    self.gradient, self.file_name)