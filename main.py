import sys
from PyQt6 import QtWidgets
from pyqtgraph import PlotWidget, plot
import pyqtgraph as pg
import numpy as np

class MainWindow(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('test')
        #self.setGeometry(50, 50, 1500, 1000)
        self.interface()
        self.show()

    def interface(self):
        #quit button
        btn = QtWidgets.QPushButton('Quit', self)
        btn.clicked.connect(self.close_app)

        #plot window
        plot = pg.PlotWidget(self)
        
        #layout
        layout = QtWidgets.QVBoxLayout()
        self.setLayout(layout)
        layout.addWidget(btn)
        layout.addWidget(plot)

    def close_app(self):
        sys.exit('app closed!')


def main():
    app = QtWidgets.QApplication(sys.argv)
    main = MainWindow()
    sys.exit(app.exec())

if __name__ == '__main__':
    main()


