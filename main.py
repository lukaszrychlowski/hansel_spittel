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

        #plot window
        plot = pg.PlotWidget(self)
        plot.setBackground('w')
        x = [0,1,2,3,4,5,6,7,8,9]
        y = [0,1,4,9,16,25,36,49,64,81]
        plot.plot(x,y, pen=None, symbol='o')

        #quit button
        btn = QtWidgets.QPushButton('Quit', self)
        btn.clicked.connect(self.close_app)
        
        #layout
        layout = QtWidgets.QVBoxLayout()
        self.setLayout(layout)
        layout.addWidget(plot)
        layout.addWidget(btn)

    def close_app(self):
        sys.exit('app closed!')
    
def main():
    app = QtWidgets.QApplication(sys.argv)
    main = MainWindow()
    sys.exit(app.exec())

if __name__ == '__main__':
    main()


