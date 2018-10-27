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
        x = xa
        prevy = ya
        y = 0
        for i in range(n):
            y = prevy + h * f(x, prevy)
            x = x + h
            prevy = y
            self.X.append(x)
            self.Y.append(y)

        self.X.append(x)
        self.Y.append(y)


class ImprovedEuler(Grid):
    def solve(self, f, xa, ya, xb, n):
        self.X = []
        self.Y = []
        h = (xb - xa) / float(n)
        x = xa + 0
        y = ya + 0

        for i in range(n):
            self.X.append(x)
            self.Y.append(y)
            y += h / 2 * (f(x, y) + f(x + h, y + h * f(x, y)))
            x += h

        self.X.append(xb)
        self.Y.append(y)


class RungeKutta(Grid):
    def solve(self, f, xa, ya, xb, n):
        self.X = []
        self.Y = []
        h = (xb - xa) / float(n)
        x = xa + 0
        y = ya + 0

        for i in range(n):
            self.X.append(x)
            self.Y.append(y)
            k1i = f(x, y)
            k2i = f(x + h / 2, y + (h / 2) * k1i)
            k3i = f(x + h / 2, y + (h / 2) * k2i)
            k4i = f(x + h, y + h * k3i)
            y += (h / 6) * (k1i + 2 * k2i + 2 * k3i + k4i)
            x += h

        self.X.append(xb)
        self.Y.append(y)


class Exact(Grid):
    def solve(self, f, xa, ya, xb, n, c):
        #in exact solution we need to know c (it is computed in MyDynamicCanvas.confirm_input)
        sol = lambda x, c: 1 / (math.exp(2 * x) * (math.exp(-x) + c))
        x = xa + 0
        y = ya + 0
        h = (xb - xa) / float(n)
        self.X = []
        self.Y = []
        for i in range(n):
            self.X.append(x)
            self.Y.append(y)
            x += h
            y = sol(x, c)
        self.X.append(x)
        self.Y.append(y)


class Solver():
    def __init__(self):
        # arrays of errors for euler, Improved and runge kutta
        self.dE = []
        self.dI = []
        self.dR = []
        # and arrays of total errors
        self.totaldE = []
        self.totaldI = []
        self.totaldR = []

        self.exact = Exact()
        self.euler = Euler()
        self.improved_euler = ImprovedEuler()
        self.runge_kutta = RungeKutta()

        self.f = lambda x, y: y ** 2 * math.exp(x) - 2 * y
        self.x0 = 1
        self.y0 = 1
        self.X = 1.45867514538708
        self.N = 1000
        self.c = -0.23254415793482963
        self.N1 = 20
        self.N2 = 50


class SuperCanvas(FigureCanvas):

    def __init__(self, parent=None, width=5, height=4, dpi=200):
        fig = Figure(figsize=(width, height), dpi=dpi)

        self.axes = fig.add_subplot(221)
        self.axes.set_title('approximations')
        self.axes.set_ylabel('y')
        self.axes.set_xlabel('x')
        self.error_axes = fig.add_subplot(222)
        self.error_axes.set_title('errors')
        self.error_axes.set_ylabel('e')
        self.error_axes.set_xlabel('x')
        self.error_analyze = fig.add_subplot(223)
        self.error_analyze.set_title('analyze')
        self.error_analyze.set_xlabel('N')
        self.error_analyze.set_ylabel('e')

        self.compute_initial_figure()

        FigureCanvas.__init__(self, fig)
        self.setParent(parent)

        FigureCanvas.setSizePolicy(self, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        FigureCanvas.updateGeometry(self)

    def compute_initial_figure(self):
        pass

    def plot_error(self):
        pass


class MyDynamicMplCanvas(SuperCanvas):

    def __init__(self, *args, **kwargs):
        SuperCanvas.__init__(self, *args, **kwargs)

        self.lab = QLabel("red - euler, blue - improved euler, yellow - runge-kutt, black - exact", self)
        self.lab.move(110, 0)

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
        self.input_X = QLineEdit('1.45', self)
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

        self.button_analyze = QPushButton('analyze', self)
        self.button_analyze.clicked.connect(self.plot_error_analyze)
        self.button_analyze.resize(100, 30)
        self.button_analyze.move(0, 150)

        self.input_N1 = QLineEdit('20', self)
        self.input_N1.resize(70, 25)
        self.input_N1.move(0, 180)
        self.label_N1 = QLabel('N1', self)
        self.label_N1.move(70, 180)

        self.input_N2 = QLineEdit('50', self)
        self.input_N2.resize(70, 25)
        self.input_N2.move(0, 205)
        self.label_N2 = QLabel('N2', self)
        self.label_N2.move(70, 205)

    def compute_initial_figure(self):
        self.axes.plot([], [], 'r')

    def update_figure(self):
        self.axes.cla()
        self.confirm_input()

        self.axes.set_title('approximations')
        self.axes.set_ylabel('y')
        self.axes.set_xlabel('x')

        self.solver.euler.solve(self.solver.f, self.solver.x0, self.solver.y0, self.solver.X, self.solver.N)
        self.solver.improved_euler.solve(self.solver.f, self.solver.x0, self.solver.y0, self.solver.X, self.solver.N)
        self.solver.runge_kutta.solve(self.solver.f, self.solver.x0, self.solver.y0, self.solver.X, self.solver.N)
        self.solver.exact.solve(self.solver.f, self.solver.x0, self.solver.y0, self.solver.X, self.solver.N,
                                self.solver.c)

        self.axes.plot(self.solver.runge_kutta.X, self.solver.runge_kutta.Y, 'y')
        self.axes.plot(self.solver.euler.X, self.solver.euler.Y, 'r')
        self.axes.plot(self.solver.improved_euler.X, self.solver.improved_euler.Y, 'b')
        self.axes.plot(self.solver.exact.X, self.solver.exact.Y, 'black')

        # errors
        self.plot_error()

        self.draw()

    def plot_error(self):
        self.error_axes.cla()

        self.error_axes.set_title('errors')
        self.error_axes.set_ylabel('e')
        self.error_axes.set_xlabel('x')

        self.solver.dE = [abs(float(float(self.solver.exact.Y[i]) - float(self.solver.euler.Y[i]))) for i in
                          range(len(self.solver.euler.Y))]
        self.solver.dI = [abs(float(float(self.solver.exact.Y[i]) - float(self.solver.improved_euler.Y[i]))) for i in
                          range(len(self.solver.euler.Y))]
        self.solver.dR = [abs(float(float(self.solver.exact.Y[i]) - float(self.solver.runge_kutta.Y[i]))) for i in
                          range(len(self.solver.euler.Y))]

        self.error_axes.plot(self.solver.euler.X, self.solver.dE, 'r')
        self.error_axes.plot(self.solver.euler.X, self.solver.dI, 'b')
        self.error_axes.plot(self.solver.euler.X, self.solver.dR, 'y')

    def plot_error_analyze(self):

        self.solver.totaldE = []
        self.solver.totaldI = []
        self.solver.totaldR = []

        self.error_analyze.cla()

        self.solver.N1 = int(self.input_N1.text())
        self.solver.N2 = int(self.input_N2.text())

        self.error_analyze.set_title('analyze')
        self.error_analyze.set_xlabel('N')
        self.error_analyze.set_ylabel('e')

        currentN = self.solver.N1

        for i in range(self.solver.N1, self.solver.N2):
            self.solver.euler.solve(self.solver.f, self.solver.x0, self.solver.y0, self.solver.X, currentN)
            self.solver.improved_euler.solve(self.solver.f, self.solver.x0, self.solver.y0, self.solver.X, currentN)
            self.solver.runge_kutta.solve(self.solver.f, self.solver.x0, self.solver.y0, self.solver.X, currentN)
            self.solver.exact.solve(self.solver.f, self.solver.x0, self.solver.y0, self.solver.X, currentN,
                                    self.solver.c)

            self.solver.dE = [abs(float(float(self.solver.exact.Y[i]) - float(self.solver.euler.Y[i]))) for i in
                              range(len(self.solver.euler.Y))]

            self.solver.dI = [abs(float(float(self.solver.exact.Y[i]) - float(self.solver.improved_euler.Y[i]))) for i
                              in range(len(self.solver.euler.Y))]
            self.solver.dR = [abs(float(float(self.solver.exact.Y[i]) - float(self.solver.runge_kutta.Y[i]))) for i in
                              range(len(self.solver.euler.Y))]

            self.solver.totaldE.append(max(self.solver.dE))
            self.solver.totaldI.append(max(self.solver.dI))
            self.solver.totaldR.append(max(self.solver.dR))

            currentN += 1

        self.error_analyze.plot([i for i in range(self.solver.N1, self.solver.N2)], self.solver.totaldE, 'r')
        self.error_analyze.plot([i for i in range(self.solver.N1, self.solver.N2)], self.solver.totaldI, 'b')
        self.error_analyze.plot([i for i in range(self.solver.N1, self.solver.N2)], self.solver.totaldR, 'y')

        self.draw()

    def confirm_input(self):
        self.solver.x0 = float(self.input_x0.text())
        self.solver.y0 = float(self.input_y0.text())
        self.solver.X = float(self.input_X.text())
        self.solver.N = int(self.input_N.text())

        # function c = f(x,y)
        self.lamdac = lambda x, y: 1 / (y * math.exp(2 * x)) - math.exp(-x)

        self.solver.c = float(self.lamdac(self.solver.x0, self.solver.y0))


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

    def fileQuit(self):
        self.close()

    def closeEvent(self, ce):
        self.fileQuit()

    def about(self):
        QtWidgets.QMessageBox.about(self, "About", 'When you want to build approximation' '\n'
                                                   'first of all find asymptotes if there are any.''\n'
                                                   'Build approximation only on the segment before asymptote''\n'
                                                   'and on the segment after it''\n'
                                                   'Ensure that between x0 and X no asymptotes')


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    window = MyWindow()
    window.setWindowTitle('differential equations programming assignment')
    window.resize(1500, 1000)
    window.show()
    sys.exit(app.exec_())
