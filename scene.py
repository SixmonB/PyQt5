#!/usr/bin/python
import sys
import math
from PyQt5 import QtCore,QtGui,QtWidgets

class Scene (QtWidgets.QGraphicsScene) :
    def __init__(self):
        QtWidgets.QGraphicsScene.__init__(self)
        self.begin,self.end=QtCore.QPoint(0,0),QtCore.QPoint(0,0)
        self.tool="rectangle"
        self.pen,self.brush=None,None
        
        self.elasticObject = None

        self.offsets = []
        self.previousOptions = []
        self.selectedItems = []
        self.canMove = False

        self.undoObjects = []
        self.redoObjects = []

        self.qt_polygon_shape = QtGui.QPolygonF()
        self.polygon_peak = []

        self.create()
    def __repr__(self):
        return "<Scene({},{},{})>".format(self.pen,self.brush,self.tool)
    def create(self) :
        self.create_pen()
        line=QtWidgets.QGraphicsLineItem(0,0,100,100)
        line.setPen(self.pen)
        self.addItem(line)
        self.create_brush()
        self.create_font()
        # rect=QtWidgets.QGraphicsRectItem(110,110,100,50)
        # rect.setPen(self.pen)
        # rect.setBrush(self.brush)
        # self.addItem(rect)
        # line=QtWidgets.QGraphicsLineItem(180,180,360,360)
        # line.setPen(self.pen)
        # self.addItem(line)
    def create_pen(self) :
        self.pen=QtGui.QPen()
        self.pen.setColor(QtCore.Qt.red)
    def create_brush(self) :
        self.brush=QtGui.QBrush()
        self.brush.setColor(QtCore.Qt.blue)
        self.brush.setStyle(QtCore.Qt.CrossPattern)
    def create_font(self):
        self.myfont=QtGui.QFont()
    def set_tool(self,tool) :
        print("Scene.set_tool(self,tool)",tool)
        self.tool=tool
    def set_pen_color(self,color) :
        print("Scene.set_pen_color(self,color)",color)
        self.pen.setColor(color)
    def set_pen_width(self,width) :
        print("Scene.set_pen_width(self,width)",width)
        self.pen.setWidth(width)
    def set_pen_line(self, line):
        print("Scene.set_pen_line(self,style)",line)
        self.pen.setStyle(line)
    def set_brush_color(self,color) :
        print("Scene.set_brush_color(self,color)",color)
        self.brush.setColor(color)
    def set_brush_style(self,style) :
        print("Scene.set_brush_style(self,color)",style)
        self.brush.setStyle(style)
    def set_font(self, name, size, family):
        print("Scene.set_font(self,font)", name, size, family)
        self.myfont.setStyleName(name)
        self.myfont.setPointSize(size)
        self.myfont.setFamily(family)

    def clearScene(self):
        msgbox = QtWidgets.QMessageBox(QtWidgets.QMessageBox.Question, "Confirm clear scene", "Are you sure you want to clear the scene ?")
        msgbox.addButton(QtWidgets.QMessageBox.Yes)
        msgbox.addButton(QtWidgets.QMessageBox.No)
        msgbox.setDefaultButton(QtWidgets.QMessageBox.No)
        reply = msgbox.exec()
        if(reply==QtWidgets.QMessageBox.Yes):
            self.offsets = []
            self.previousOptions = []
            self.selectedItems = []
            self.canMove = False
            self.undoObjects = []
            self.redoObjects = []
            self.polygon_peak = []
            for item in self.items():
                self.removeItem(item)
    
    def undo(self):
        if(len(self.undoObjects)>0):
            self.redoObjects.append(self.undoObjects[-1])
            self.removeItem(self.undoObjects[-1])
            self.undoObjects.pop()

    def redo(self):
        if(len(self.redoObjects)>0):
            self.undoObjects.append(self.redoObjects[-1])
            self.addItem(self.redoObjects[-1])
            self.redoObjects.pop()

    # events
    def mousePressEvent(self, event):
        print("Scene.mousePressEvent()")
        print("event.scenePos() : ",event.scenePos())
        print("event.screenPos() : ",event.screenPos())
        self.begin=self.end=event.scenePos()
        if(event.button()==QtCore.Qt.LeftButton):
            if(self.tool == "select"):
                item=self.itemAt(self.begin,QtGui.QTransform())
                if item:
                    if(item in self.selectedItems):
                        self.canMove = True
                        self.offsets = []
                        for selectedItem in self.selectedItems:
                            self.offsets.append(self.begin-selectedItem.pos())   
                    else:
                        self.canMove = False
                        self.previousOptions.append({
                            "color": item.pen().color(),
                            "style": item.pen().style(),
                            "width": item.pen().width()
                            })
                        pen=QtGui.QPen()
                        pen.setColor(QtCore.Qt.green)
                        item.setPen(pen)
                        self.selectedItems.append(item)
                else:
                    self.canMove = False
                    for index in range(len(self.selectedItems)):
                        pen=QtGui.QPen()
                        pen.setColor(self.previousOptions[index]["color"])
                        pen.setStyle(self.previousOptions[index]["style"])
                        pen.setWidth(self.previousOptions[index]["width"])
                        self.selectedItems[index].setPen(pen)
                    self.previousOptions = []
                    self.selectedItems = [] 
    def mouseMoveEvent(self, event):
            print("Scene.mouseMoveEvent()")
            print("event.scenePos() : ",event.scenePos())
            self.end = event.scenePos()
            if(self.elasticObject != None):
                self.removeItem(self.elasticObject)
            if(self.tool == "select"):
                if self.canMove:
                    for index in range(len(self.selectedItems)):
                        self.selectedItems[index].setPos(event.scenePos() - self.offsets[index])
            elif(self.tool == "line"):
                elasticLine=QtWidgets.QGraphicsLineItem(self.begin.x(), self.begin.y(), self.end.x(), self.end.y())
                elasticLine.setPen(self.pen)
                self.elasticObject = elasticLine
                self.addItem(elasticLine)
            elif(self.tool == "rectangle"):
                tempPoint = self.end-self.begin
                topLeftPoint = QtCore.QPointF(0,0)
                topLeftPoint.setX(self.begin.x() if tempPoint.x() >= 0 else self.end.x())
                topLeftPoint.setY(self.begin.y() if tempPoint.y() >= 0 else self.end.y())
                

                elasticRect=QtWidgets.QGraphicsRectItem(
                                    topLeftPoint.x(),topLeftPoint.y(),
                                    abs(self.end.x()-self.begin.x()),
                                    abs(self.end.y()-self.begin.y())
                            )
                elasticRect.setPen(self.pen)
                elasticRect.setBrush(self.brush)
                self.elasticObject = elasticRect
                self.addItem(elasticRect)
            elif(self.tool == "ellipse"):
                elasticEllipse=QtWidgets.QGraphicsEllipseItem(
                                    self.begin.x(),self.begin.y(),
                                    self.end.x()-self.begin.x(),
                                    self.end.y()-self.begin.y()
                            )
                elasticEllipse.setPen(self.pen)
                elasticEllipse.setBrush(self.brush)
                self.elasticObject = elasticEllipse
                self.addItem(elasticEllipse)
    def mouseReleaseEvent(self, event):
        print("-----------------------------------")
        print("Scene.mouseReleaseEvent()")
        print("Scene or View",self)
        print("event.scenePos() : ",event.scenePos())
        print("self.tool : ",self.tool)
        print("self.selectedItems : ",self.selectedItems)
        #print("offsets : ",self.offsets)
        print("Previous Color", self.previousOptions)
        print("items number : ",len(self.items()))
        print("pen : ",self.pen.color())
        self.end = event.scenePos()
        if(self.elasticObject != None):
            self.removeItem(self.elasticObject)
            self.elasticObject = None
        if(event.button()==QtCore.Qt.LeftButton):
            if(self.tool == "select"):
                    if self.canMove:
                        for index in range(len(self.selectedItems)):
                            self.selectedItems[index].setPos(event.scenePos() - self.offsets[index])
            elif(self.tool == "delete"):
                item=self.itemAt(self.begin,QtGui.QTransform())
                if(item):
                    msgbox = QtWidgets.QMessageBox(QtWidgets.QMessageBox.Question, "Confirm delete", "Are you sure you want to delete?")
                    msgbox.addButton(QtWidgets.QMessageBox.Yes)
                    msgbox.addButton(QtWidgets.QMessageBox.No)
                    msgbox.setDefaultButton(QtWidgets.QMessageBox.No)
                    reply = msgbox.exec()
                    if(reply==QtWidgets.QMessageBox.Yes):
                        self.undoObjects.remove(item)
                        self.removeItem(item)

            elif self.tool=="line" :
                line=QtWidgets.QGraphicsLineItem(self.begin.x(), self.begin.y(), self.end.x(), self.end.y())
                line.setPen(self.pen)
                line.setFlags(line.flags() | QtCore.Qt.ItemIsSelectable)
                self.undoObjects.append(line)
                self.addItem(line)
            elif self.tool=="rectangle" :
                tempPoint = self.end-self.begin
                topLeftPoint = QtCore.QPointF(0,0)
                topLeftPoint.setX(self.begin.x() if tempPoint.x() >= 0 else self.end.x())
                topLeftPoint.setY(self.begin.y() if tempPoint.y() >= 0 else self.end.y())
                

                rect=QtWidgets.QGraphicsRectItem(
                                    topLeftPoint.x(),topLeftPoint.y(),
                                    abs(self.end.x()-self.begin.x()),
                                    abs(self.end.y()-self.begin.y())
                            )
                rect.setPen(self.pen)
                rect.setBrush(self.brush)
                rect.setFlags(rect.flags() | QtCore.Qt.ItemIsSelectable)
                self.undoObjects.append(rect)
                self.addItem(rect)
            elif self.tool=="ellipse" :
                ellipse=QtWidgets.QGraphicsEllipseItem(
                                    self.begin.x(),self.begin.y(),
                                    self.end.x()-self.begin.x(),
                                    self.end.y()-self.begin.y()
                            )
                ellipse.setPen(self.pen)
                ellipse.setBrush(self.brush)
                ellipse.setFlags(ellipse.flags() | QtCore.Qt.ItemIsSelectable)
                self.undoObjects.append(ellipse)
                self.addItem(ellipse)
            
            elif self.tool=="polygon" :

                if(self.qt_polygon_shape.isEmpty()):          
                    self.qt_polygon_shape.append(QtCore.QPointF(self.end.x(), self.end.y()))
                    ellipse=QtWidgets.QGraphicsEllipseItem(
                                    self.end.x(),
                                    self.end.y(),
                                    4,
                                    4)
                    ellipse.setPen(self.pen)
                    self.polygon_peak.append(ellipse)
                    self.addItem(ellipse)
                else:
                    distance = math.sqrt((self.end.x()-self.qt_polygon_shape.first().x())**2 + (self.end.y()-self.qt_polygon_shape.first().y())**2)
                    if(distance <= 30):
                        self.qt_polygon_shape.append(QtCore.QPointF(self.qt_polygon_shape.first().x(), self.qt_polygon_shape.first().y()))
                    else:
                        self.qt_polygon_shape.append(QtCore.QPointF(self.end.x(), self.end.y()))
                        ellipse=QtWidgets.QGraphicsEllipseItem(
                                    self.end.x(),self.end.y(),
                                    4,
                                    4)
                        ellipse.setPen(self.pen)
                        self.polygon_peak.append(ellipse)
                        self.addItem(ellipse)
                if(self.qt_polygon_shape.isClosed() and len(self.qt_polygon_shape)>2):
                    for peak in self.polygon_peak:
                        self.removeItem(peak)
                    self.polygon_peak = []
                    polygone=QtWidgets.QGraphicsPolygonItem(self.qt_polygon_shape)
                    polygone.setPen(self.pen)
                    polygone.setBrush(self.brush)
                    polygone.setFlags(polygone.flags() | QtCore.Qt.ItemIsSelectable)
                    self.undoObjects.append(polygone)
                    self.addItem(polygone)
                    self.qt_polygon_shape.clear()
                else :
                    print("nothing to draw !")
            elif self.tool == "text":
                text,ok = QtWidgets.QInputDialog.getText(None,"Text","Enter the text")
                if ok:
                    graphicsText = QtWidgets.QGraphicsSimpleTextItem()
                    graphicsText.setText(text)
                    graphicsText.setPos(self.end)
                    graphicsText.setFont(self.myfont)
                    self.undoObjects.append(graphicsText)
                    self.addItem(graphicsText)
                else :
                    print("Not a valid text!")

    def resizeEvent(self,event):
        print("geometry : ",self.width,self.height)
        print("dy : ",self.size().height()-self.view.size().height())
    
if __name__ == "__main__" :  
    print(QtCore.QT_VERSION_STR)
    app=QtWidgets.QApplication(sys.argv)
    scene=Scene()
    x,y=0,0
    w,h=600,400
    scene.setSceneRect(x,y,w,h)
    scene.create()
    root=QtWidgets.QGraphicsView()
    root.setGeometry(x,y,w,h)
    root.setScene(scene)
    # scene.setSceneRect(x-50,y-50,width,height)
    root.show()
    sys.exit(app.exec_())

