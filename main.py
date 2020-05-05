import sys

from PyQt5 import QtWidgets

def main():
    app = QtWidgets.QApplication(sys.argv)

    from src.main_widget import GUI 
    gui = QtWidgets.QMainWindow()
    gui.resize(1280, 720)
    gui.setWindowTitle("Computer Graphics. Laboratory Work 2.")
    gui.setCentralWidget(GUI())
    gui.show()

    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
