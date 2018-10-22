from __future__ import unicode_literals
import sys
import os
import math
import matplotlib
from PyQt5.QtWidgets import QPushButton, QLineEdit, QLabel, QMessageBox

matplotlib.use('Qt5Agg')
from PyQt5 import QtCore, QtWidgets

from numpy import arange, sin, pi
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

progname = os.path.basename(sys.argv[0])
progversion = "0.1"


class Grid():
    def __init__(self):
        self.Y = []
        self.X = []

    def solve(self, f, xa, ya, xb, n):
        pass


class Euler(Grid):
    def solve(self, f, xa, ya, xb, n):
        self.X = []
        self.Y = []
        h = (xb - xa) / float(n)
        x = xa + 0
        y = ya + 0

        for i in range(n):
            self.X.append(x)
            self.Y.append(y)
            y += h * f(x, y)
            x += h

        self.X.append(xb)
        self.Y.append(y)


class Solver():
    def __init__(self):
        self.euler = Euler()
        self.f = lambda x, y: y ** 2 * math.exp(x) - 2 * y;
        self.x0 = 1
        self.y0 = 1
        self.X = 1.45867514538708
        self.N = 1000

        # vertical asymptote in  x = 1.458675145387081


class SuperCanvas(FigureCanvas):

    def __init__(self, parent=None, width=5, height=4, dpi=100):
        fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = fig.add_subplot(111)

        self.compute_initial_figure()

        FigureCanvas.__init__(self, fig)
        self.setParent(parent)

        FigureCanvas.setSizePolicy(self,
                                   QtWidgets.QSizePolicy.Expanding,
                                   QtWidgets.QSizePolicy.Expanding)
        FigureCanvas.updateGeometry(self)

    def compute_initial_figure(self):
        pass


class MyDynamicMplCanvas(SuperCanvas):

    def __init__(self, *args, **kwargs):

        SuperCanvas.__init__(self, *args, **kwargs)

        self.plot_button = QPushButton('plot', self)
        self.plot_button.clicked.connect(self.update_figure)
        self.plot_button.resize(100, 30)
        self.plot_button.move(0, 0)

        self.solver = Solver()

        # textbox for x0
        self.input_x0 = QLineEdit('1', self)
        self.input_x0.resize(70, 25)
        self.l1 = QLabel("x0", self)
        self.input_x0.move(0, 40)
        self.l1.move(70, 40)

        # textbox for y0
        self.input_y0 = QLineEdit('1', self)
        self.input_y0.move(0, 65)
        self.input_y0.resize(70, 25)
        self.l1 = QLabel("y0", self)
        self.l1.move(70, 65)

        # textbox for X
        self.input_X = QLineEdit('1.45867514538708', self)
        self.input_X.move(0, 90)
        self.input_X.resize(70, 25)
        self.l1 = QLabel("X", self)
        self.l1.move(70, 90)

        # textbox for N
        self.input_N = QLineEdit('1000', self)
        self.input_N.move(0, 115)
        self.input_N.resize(70, 25)
        self.l1 = QLabel("N", self)
        self.l1.move(70, 115)

    def compute_initial_figure(self):
        self.axes.plot([], [], 'r')

    def update_figure(self):
        self.axes.cla()
        self.confirm_input()

        if float(self.solver.X) > float(1.458675145387081) and float(self.solver.x0) > float(1.458675145387081):
            self.solver.euler.solve(self.solver.f, self.solver.x0, self.solver.y0, self.solver.X, self.solver.N)
            self.axes.plot(self.solver.euler.X, self.solver.euler.Y, 'r')
            self.draw()

        elif float(self.solver.X) < float(1.458675145387081) and float(self.solver.x0) < float(1.458675145387081):
            self.solver.euler.solve(self.solver.f, self.solver.x0, self.solver.y0, self.solver.X, self.solver.N)
            self.axes.plot(self.solver.euler.X, self.solver.euler.Y, 'r')
            self.draw()

        elif self.solver.X > float(1.458675145387081) > self.solver.x0:
            self.solver.euler.solve(self.solver.f, self.solver.x0, self.solver.y0, 1.45867514538708, self.solver.N)
            self.axes.plot(self.solver.euler.X, self.solver.euler.Y, 'r')
            self.solver.euler.solve(self.solver.f, 1.459, -22.908107196089443, self.solver.X, self.solver.N)
            self.axes.plot(self.solver.euler.X, self.solver.euler.Y, 'r')
            self.draw()

    def confirm_input(self):
        self.solver.x0 = float(self.input_x0.text())
        self.solver.y0 = float(self.input_y0.text())
        self.solver.X = float(self.input_X.text())
        self.solver.N = int(self.input_N.text())


class MyWindow(QtWidgets.QMainWindow):
    def __init__(self):
        QtWidgets.QMainWindow.__init__(self)
        self.setAttribute(QtCore.Qt.WA_DeleteOnClose)
        self.setWindowTitle("application main window")

        self.file_menu = QtWidgets.QMenu('&File', self)
        self.file_menu.addAction('&Quit', self.fileQuit,
                                 QtCore.Qt.CTRL + QtCore.Qt.Key_Q)
        self.menuBar().addMenu(self.file_menu)

        self.help_menu = QtWidgets.QMenu('&Help', self)
        self.menuBar().addSeparator()
        self.menuBar().addMenu(self.help_menu)

        self.help_menu.addAction('&About', self.about)

        self.main_widget = QtWidgets.QWidget(self)

        l = QtWidgets.QVBoxLayout(self.main_widget)
        dc = MyDynamicMplCanvas(self.main_widget, width=8, height=4, dpi=100)
        l.addWidget(dc)

        self.main_widget.setFocus()
        self.setCentralWidget(self.main_widget)

        self.statusBar().showMessage("All hail matplotlib!", 2000)

    def fileQuit(self):
        self.close()

    def closeEvent(self, ce):
        self.fileQuit()

    def about(self):
        QtWidgets.QMessageBox.about(self, "About", 'hi')


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    window = MyWindow()
    window.setWindowTitle("oop")
    window.resize(1200, 700)
    window.show()
    sys.exit(app.exec_())
