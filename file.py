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
    """A canvas that updates itself every second with a new plot."""

    def __init__(self, *args, **kwargs):
        SuperCanvas.__init__(self, *args, **kwargs)
        button = QPushButton('plot',self)
        button.clicked.connect(self.update_figure2)
        button.move(260,0)
        self.solver = Solver()

        self.button_info = QPushButton('confirm input', self)
        self.button_info.clicked.connect(self.on_click)
        self.button_info.move(350, 0)
        self.x0,self.y0,self.X,self.N = 0,0,0,0


        # textbox for x0
        self.textbox_x0 = QLineEdit('1', self)

        self.textbox_x0.resize(40, 25)
        self.l1 = QLabel("x0", self)
        self.textbox_x0.move(0, 40)
        self.l1.move(40, 40)

        # textbox for y0
        self.textbox_y0 = QLineEdit('1', self)
        self.textbox_y0.move(0, 65)
        self.textbox_y0.resize(40, 25)
        self.l1 = QLabel("y0", self)
        self.l1.move(40, 65)

        # textbox for X
        self.textbox_X = QLineEdit('1.458675145387081', self)
        self.textbox_X.move(0, 90)
        self.textbox_X.resize(40, 25)
        self.l1 = QLabel("X", self)
        self.l1.move(40, 90)

        # textbox for N
        self.textbox_N = QLineEdit('1000', self)
        self.textbox_N.move(0, 115)
        self.textbox_N.resize(40, 25)
        self.l1 = QLabel("N", self)
        self.l1.move(40, 115)
        # timer = QtCore.QTimer(self)
        # timer.timeout.connect(self.update_figure)
        # timer.start(1000)

    def compute_initial_figure(self):
        self.axes.plot([0, 1, 2, 3], [1, 2, 3, 4], 'r')

    def update_figure2(self):
         #Euler method returns 2 tuple of 2 list X and Y
        # X, Y = self.solver.euler.Euler(self.solver.f,self.solver.x0,self.solver.y0,self.solver.X,self.solver.N)[0],\
        #        self.solver.euler.Euler(self.solver.f,self.solver.x0,self.solver.y0,self.solver.X,self.solver.N)[1]
        self.solver.euler.solve(self.solver.f,self.solver.x0,self.solver.y0,self.solver.X,self.solver.N)
        self.axes.cla()
        self.axes.plot(self.solver.euler.X,self.solver.euler.Y,'r')
        self.solver.euler.solve(self.solver.f, 1.459, -22.908107196089443, 10, self.solver.N)
        self.axes.plot(self.solver.euler.X, self.solver.euler.Y, 'r')
        self.draw()

    def on_click(self):
        self.solver.x0 = float(self.textbox_x0.text())
        self.solver.y0 = float(self.textbox_y0.text())
        self.solver.X = float(self.textbox_X.text())
        self.solver.N = int(self.textbox_N.text())

        textboxValue = []
        textboxValue.append(self.textbox_x0.text())
        textboxValue.append(self.textbox_y0.text())
        textboxValue.append(self.textbox_X.text())
        textboxValue.append(self.textbox_N.text())
        QMessageBox.question(self, 'Message', "your input is: " + str(textboxValue), QMessageBox.Ok, QMessageBox.Ok)



class ApplicationWindow(QtWidgets.QMainWindow):
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
        QtWidgets.QMessageBox.about(self, "About",'e^x == math.exp(x)')
class Grid():
    def __init__(self):
        self.Y = [0]
        self.X = [0]
    def solve(self, f,xa, ya, xb, n):
        pass

class Exact(Grid):
    pass

class Euler(Grid):
    def solve(self,f, xa, ya, xb, n):
        X = []
        Y = []
        h = (xb - xa) / float(n)
        x = xa + 0
        y = ya + 0

        for i in range(n):
            X.append(x)
            Y.append(y)
            y += h * f(x, y)
            x += h
        X.append(xb)
        Y.append(y)
        self.X = X.copy()
        self.Y = Y.copy()

class EI(Euler):
    pass

class RK(Euler):
    pass

class Solver():
    def __init__(self):
        self.euler = Euler()
        self.ei = EI()
        self.rk = RK()
        self.exact = Exact()
        #        #f = lambda x, y: y**2*math.exp(x)-2*y;

        self.f = lambda x, y: y**2*math.exp(x)-2*y;

        #asymptote: x = 2 - log(e - 1)
        # dannaya funkciya imeet raztuv v tochke
        # x = 1.4586751453870819.
        #so instead of 1 plot from 1 to 10
        #will be 2 plots from 1 to 1.4586751453870819
        # and from 1.4586751453870819 to 10
        const = 2 - math.log(math.e-1)

        self.x0 = 0
        self.y0 = 0
        self.X = 0
        self.N = 0





qApp = QtWidgets.QApplication(sys.argv)

aw = ApplicationWindow()
aw.setWindowTitle("%s" % progname)
aw.show()
sys.exit(qApp.exec_())
#qApp.exec_()


