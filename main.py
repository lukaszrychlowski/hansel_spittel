import sys
from PyQt6 import QtWidgets
from collections import deque
import random
from pyqtgraph import PlotWidget, plot, QtCore, QtGui
import pyqtgraph as pg
import numpy as np

class MainWindow(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('test')
        self.setGeometry(50, 50, 600, 600)
        pg.setConfigOptions(antialias=True)
        self.interface()
        self.timer = QtCore.QTimer(QtWidgets.QApplication.instance())
        self.timer.timeout.connect(self.update)
        self.timer.start(600)
        self.show()

    def interface(self):
        #plot window
        self.plot = pg.PlotWidget(self)
        self.plot.setBackground('w')
        self.data = self.gen_new_data() 
        self.plot.plot(self.x, self.y, pen=None, symbol='o')
        self.plot.setXRange(0,100,padding=0)
        self.plot.setYRange(0,100, padding=0)
        #quit button
        self.btn = QtWidgets.QPushButton('Quit', self)
        self.btn.clicked.connect(self.close_app)
        
        #layout
        layout = QtWidgets.QGridLayout()
        self.setLayout(layout)
        layout.addWidget(self.plot,0,0)
        layout.addWidget(self.btn,1,0)

    def close_app(self):
        sys.exit('app closed!')
    
    def gen_new_data(self):
        self.x = []
        self.y = []
        for i in range(10):
            self.x.append(random.randint(0,100))
            self.y.append(random.randint(0,100))

    def update(self):
        print('updated')
        self.gen_new_data()
        self.plot.plot(self.x, self.y, pen=None, symbol='o', clear=True)




def main():
    app = QtWidgets.QApplication(sys.argv)
    main = MainWindow()
    sys.exit(app.exec())

if __name__ == '__main__':
    main()


