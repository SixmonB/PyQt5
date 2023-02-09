# -*- coding: utf-8 -*-
import sys
from PyQt5 import QtCore,QtWidgets

from scene import Scene
from window import MainWindow

print(QtCore.QT_VERSION_STR)
app=QtWidgets.QApplication(sys.argv)
scene=Scene()
position=500,500
dimension=600,400
main=MainWindow(scene)
main.show()
sys.exit(app.exec_())

#asd
