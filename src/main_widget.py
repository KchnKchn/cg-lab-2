from PyQt5 import QtWidgets, QtCore

from src.reader import Reader
from src.viewer import Viewer
from src.openglwidget import glWidget

class GUI(QtWidgets.QWidget):

    __reader = Reader()
    __viewer = Viewer()
    __glWidget = glWidget()
    __slider = QtWidgets.QSlider(QtCore.Qt.Horizontal)
    __draws = {
        "Текстурирование" : __viewer.paint_texture,
        "Прямоугольники 2*n + 2 вершин" : __viewer.paint_quadstrip,
        "Прямоугольники 4*n вершин" : __viewer.paint_quads
    }
    __curr_draw = "Текстурирование"

    def __init__(self, parent=None):
        super().__init__(parent)
        self.__grid = QtWidgets.QGridLayout(self)
        self.__setup_main_widget()

    def __setup_main_widget(self):
        self.__glWidget.render.connect(self.__viewer.paint_texture)
        self.__grid.addWidget(self.__glWidget, 0, 0, 10, 2)

        self.__slider.sliderReleased.connect(self.__connect_value_changed)
        self.__grid.addWidget(self.__slider, 11, 0)
        self.__curr_slider = QtWidgets.QLabel()
        self.__curr_slider.setText("0")
        self.__grid.addWidget(self.__curr_slider, 11, 1)

        button = QtWidgets.QPushButton()
        button.setText("Open Tomogram")
        button.clicked.connect(self.__connect_open_tomogram)
        self.__grid.addWidget(button, 12, 0, 1, 2)

        draw_list = QtWidgets.QComboBox()
        draw_list.addItems(self.__draws.keys())
        draw_list.activated[str].connect(self.__connect_chande_draw)
        self.__grid.addWidget(draw_list, 13, 0, 1, 2)

        self.__min_input = QtWidgets.QLineEdit()
        self.__min_input.setText("0")
        self.__grid.addWidget(self.__min_input, 14, 0)
        self.__lenght_input = QtWidgets.QLineEdit()
        self.__lenght_input.setText("2000")
        self.__grid.addWidget(self.__lenght_input, 14, 1)

        button = QtWidgets.QPushButton()
        button.setText("Set transfer parameters")
        button.clicked.connect(self.__connect_transfer_parameters)
        self.__grid.addWidget(button, 15, 0, 1, 2)

        button = QtWidgets.QPushButton()
        button.setText("Start render")
        button.clicked.connect(self.__start_render)
        self.__grid.addWidget(button, 16, 0, 1, 2)

    def __connect_chande_draw(self, draw_name: str):
        self.__glWidget.render.disconnect(self.__draws[self.__curr_draw])
        self.__curr_draw = draw_name
        self.__glWidget.render.connect(self.__draws[self.__curr_draw])

    def __connect_value_changed(self):
        value = self.__slider.value()
        self.__curr_slider.setText(str(value))
        self.__viewer.set_layer(value)
        self.__start_render()

    def __connect_transfer_parameters(self):
        min, lenght = int(self.__min_input.text()), int(self.__lenght_input.text())
        self.__viewer.set_transfer_parameters(min, lenght)

    def __connect_open_tomogram(self):
        tomogram_path = QtWidgets.QFileDialog.getOpenFileName(self, "Open Tomogram", ".")[0]
        if not tomogram_path: return
        shape, tomogram = self.__reader.Read(tomogram_path)
        self.__slider.setRange(0, shape[2]-1)
        self.__slider.setValue(0)
        self.__curr_slider.setText("0")
        w, h = self.__glWidget.size().width(), self.__glWidget.size().height()
        min, lenght = int(self.__min_input.text()), int(self.__lenght_input.text())
        self.__viewer.set_tomogram(shape, tomogram)
        self.__viewer.set_transfer_parameters(min, lenght)
        self.__viewer.setup_view(w, h)
    
    def __start_render(self):
        self.__glWidget.update()
