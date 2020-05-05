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
        "Прямоугольники 4*n вершин" : __viewer.paint_quads,
        "Текстурирование" : __viewer.paint_texture
    }
    __curr_draw = "Прямоугольники 4*n вершин"

    def __init__(self, parent=None):
        super().__init__(parent)
        self.__grid = QtWidgets.QGridLayout(self)
        self.__setup_main_widget()

    def __setup_main_widget(self):
        self.__glWidget.render.connect(self.__viewer.paint_quads)
        self.__grid.addWidget(self.__glWidget, 0, 0, 5, 4)

        self.__slider.sliderReleased.connect(self.__connect_value_changed)
        self.__grid.addWidget(self.__slider, 6, 0)

        button = QtWidgets.QPushButton()
        button.setText("Open Tomogram")
        button.clicked.connect(self.__connect_open_tomogram)
        self.__grid.addWidget(button, 0, 5)

        button = QtWidgets.QPushButton()
        button.setText("Start render")
        button.clicked.connect(self.__start_render)
        self.__grid.addWidget(button, 2, 5)

        draw_list = QtWidgets.QComboBox()
        draw_list.addItems(self.__draws.keys())
        draw_list.activated[str].connect(self.__connect_chande_draw)
        self.__grid.addWidget(draw_list, 1, 5)

    def __connect_chande_draw(self, draw_name: str):
        self.__glWidget.render.disconnect(self.__draws[self.__curr_draw])
        self.__curr_draw = draw_name
        self.__glWidget.render.connect(self.__draws[self.__curr_draw])

    def __connect_value_changed(self):
        value = self.__slider.value()
        self.__viewer.set_layer(value)
        self.__start_render()

    def __connect_open_tomogram(self):
        tomogram_path = QtWidgets.QFileDialog.getOpenFileName(self, "Open Tomogram", ".")[0]
        if not tomogram_path: return
        tomogram = self.__reader.Read(tomogram_path)
        self.__slider.setRange(0, tomogram.shape[2])
        self.__slider.setValue(0)
        self.__viewer.set_tomogram(tomogram)
        w, h = self.__glWidget.size().width(), self.__glWidget.size().height()
        self.__viewer.setup_view(w, h)
    
    def __start_render(self):
        self.__glWidget.update()
