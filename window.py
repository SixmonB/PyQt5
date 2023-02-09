# -*- coding: utf-8 -*-
import os,sys
from PyQt5 import QtCore,QtGui,QtWidgets
from numpy import size
from scene import Scene
import json

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self,scene=None,position=(0,0),dimension=(500,300)):
        QtWidgets.QMainWindow.__init__(self)
        self.setWindowTitle("CAI : Editeur v0.1")
        x,y=position
        width,height=dimension
        self.setGeometry(QtCore.QRect(x,y,width,height))
        self.scene=scene
        self.view=None
        position=0,0
        self.create_view(position,dimension)
        self.create_actions()
        self.create_menus()
        self.connect_actions()
        # self.dock=QtWidgets.QDockWidget("Left Right Dock",self)
        # self.dock.setAllowedAreas(QtCore.Qt.LeftDockWidgetArea | QtCore.Qt.RightDockWidgetArea)
        # self.addDockWidget(QtCore.Qt.LeftDockWidgetArea,self.dock)
    def set_scene(self,scene) :
        self.scene=scene
    def get_scene(self) :
        return self.scene
    def set_view(self,view) :
        self.view=view
    def get_view(self) :
        return self.view
    def create_view(self,position,dimension) :
        self.view=QtWidgets.QGraphicsView()
        x,y=position
        width,height=dimension
        if self.scene :
            self.scene.setSceneRect(x,y,width,height)
            # self.scene.setSceneRect(-width/2,-height/2,width/2,height/2)
            self.view.setScene(self.scene)
        else :
            print("MainWindow need  a scene ")
        self.setCentralWidget(self.view)
    def create_actions(self) :
        
        #FILE ACTIONS
        # OPEN
        self.action_file_open=QtWidgets.QAction(QtGui.QIcon('Icons/open.png'),"Open",self)
        self.action_file_open.setShortcut("Ctrl+O")
        self.action_file_open.setStatusTip("Open file")

        # CLEAR SCENE
        self.action_file_clear=QtWidgets.QAction(QtGui.QIcon('Icons/clear.svg'),"Clear", self)
        self.action_file_clear.setShortcut("Ctrl+R") #r for reset
        self.action_file_clear.setStatusTip("Clear scene")

        # SAVE
        self.action_file_save=QtWidgets.QAction(QtGui.QIcon('Icons/save.ico'),"Save", self)
        self.action_file_save.setShortcut("Ctrl+S")
        self.action_file_save.setStatusTip("Save file")

        # SAVE AS
        self.action_file_save_as=QtWidgets.QAction("Save As", self)
        self.action_file_save_as.setShortcut("Ctrl+Shift+S")
        self.action_file_save_as.setStatusTip("Save file as")

        # EXIT
        self.action_file_exit = QtWidgets.QAction(QtGui.QIcon('Icons/exit.svg'), "Exit",self)
        self.action_file_exit.setShortcut("Esc")
        self.action_file_exit.setStatusTip("Exit")

        self.action_file=QtWidgets.QActionGroup(self)
        
        # TOOLS ACTIONS
        # SELECT
        self.action_tools_select=QtWidgets.QAction(QtGui.QIcon('Icons/select.svg'),"Select", self)
        self.action_tools_select.setShortcut("A")
        self.action_tools_select.setCheckable(True)
        self.action_tools_select.setChecked(False)

        # DELETE
        self.action_tools_delete=QtWidgets.QAction(QtGui.QIcon('Icons/delete.svg'),"Delete", self)
        self.action_tools_delete.setShortcut("D")
        self.action_tools_delete.setCheckable(True)
        self.action_tools_delete.setChecked(False)

        # LINE
        self.action_tools_line=QtWidgets.QAction(
            self.tr("&Line"),
            self
        )
        self.action_tools_line.setShortcut("L")
        self.action_tools_line.setCheckable(True)
        self.action_tools_line.setChecked(False)

        # Rectangle
        self.action_tools_rect=QtWidgets.QAction(
            self.tr("&Rect"),
            self
        )
        self.action_tools_rect.setShortcut("R")
        self.action_tools_rect.setCheckable(True)
        self.action_tools_rect.setChecked(True)

        # ellipse
        self.action_tools_ellipse=QtWidgets.QAction(
            self.tr("&Ellipse"),
            self
        )
        self.action_tools_ellipse.setShortcut("E")
        self.action_tools_ellipse.setCheckable(True)
        self.action_tools_ellipse.setChecked(False)

        # polygon
        self.action_tools_polygon=QtWidgets.QAction(
            self.tr("&Polygon"),
            self
        )
        self.action_tools_polygon.setShortcut("P")
        self.action_tools_polygon.setCheckable(True)
        self.action_tools_polygon.setChecked(False)

        # Text
        self.action_tools_text = QtWidgets.QAction(
            self.tr("Text"),
            self
        )
        self.action_tools_text.setShortcut("T")
        self.action_tools_text.setCheckable(True)
        self.action_tools_text.setChecked(False)

        self.action_tools=QtWidgets.QActionGroup(self)

        #CONFIG ACTIONS
        # Style
        self.action_style=QtWidgets.QActionGroup(self)
        self.action_pen=QtWidgets.QActionGroup(self.action_style)
        self.action_brush=QtWidgets.QActionGroup(self.action_style)
        # PEN
        self.action_style_pen_color=QtWidgets.QAction(
            self.tr("&Color"),
            self
        )
        self.action_style_pen_line=QtWidgets.QAction(
            self.tr("&Line"),
            self
        )
        self.action_style_pen_width=QtWidgets.QAction(
            self.tr("&Width"),
            self
        )
        # Brush
        self.action_style_brush_color=QtWidgets.QAction(
            self.tr("&Color"),
            self
        )
        self.action_style_brush_fill=QtWidgets.QAction(
            self.tr("&Fill"),
            self
        )

        # Font
        self.action_style_font=QtWidgets.QAction(
            self.tr("&Font"),
            self
        )

        self.action_help=QtWidgets.QActionGroup(self)
        self.action_help_about_us=QtWidgets.QAction(
            self.tr("&About us"),
            self
        )
        self.action_help_about_qt=QtWidgets.QAction(
            self.tr("&About qt"),
            self
        )
        self.action_help_about_app=QtWidgets.QAction(
            self.tr("&About app"),
            self
        )

        # undo
        self.action_undo=QtWidgets.QAction(QtGui.QIcon('Icons/undo.svg'),"Undo", self)
        self.action_undo.setShortcut("Ctrl+Z")
        # redo
        self.action_redo=QtWidgets.QAction(QtGui.QIcon('Icons/redo.svg'),"Redo", self)
        self.action_redo.setShortcut("Ctrl+Y")

        self.action_file.addAction(self.action_file_save)
        self.action_file.addAction(self.action_file_save_as)
        self.action_file.addAction(self.action_file_exit)
        self.action_file.addAction(self.action_file_clear)
        self.action_file.addAction(self.action_file_open)

        self.action_tools.addAction(self.action_tools_select)
        self.action_tools.addAction(self.action_tools_delete)
        self.action_tools.addAction(self.action_tools_line)
        self.action_tools.addAction(self.action_tools_rect)
        self.action_tools.addAction(self.action_tools_ellipse)
        self.action_tools.addAction(self.action_tools_polygon)
        self.action_tools.addAction(self.action_tools_text)
        self.action_tools.addAction(self.action_undo)
        self.action_tools.addAction(self.action_redo)

    def create_menus(self) :
        # MENU BAR
        menubar = self.menuBar()
        menu_file = menubar.addMenu('&File')
        menu_file.addAction(self.action_file_open)
        menu_file.addAction(self.action_file_save)
        menu_file.addAction(self.action_file_save_as)
        menu_file.addAction(self.action_file_clear)
        menu_file.addAction(self.action_file_exit)
  

        menu_tools = menubar.addMenu('&Tools')
        menu_tools.addAction(self.action_tools_select)
        menu_tools.addAction(self.action_tools_delete)
        menu_tools.addAction(self.action_tools_line)
        menu_tools.addAction(self.action_tools_rect)
        menu_tools.addAction(self.action_tools_ellipse)
        menu_tools.addAction(self.action_tools_polygon)
        menu_tools.addAction(self.action_tools_text)
        menu_tools.addAction(self.action_undo)
        menu_tools.addAction(self.action_redo)

        
        menu_style = menubar.addMenu('&Style')
        menu_pen =  menu_style.addMenu('&Pen')
        menu_pen.addAction(self.action_style_pen_color)
        menu_pen.addAction(self.action_style_pen_line)
        menu_pen.addAction(self.action_style_pen_width)
        menu_brush =  menu_style.addMenu('&Brush')
        menu_brush.addAction(self.action_style_brush_color)
        menu_brush.addAction(self.action_style_brush_fill)
        menu_style.addAction(self.action_style_font)

        menu_help = menubar.addMenu('&Help')
        menu_help.addAction(self.action_help_about_us)
        menu_help.addAction(self.action_help_about_qt)
        menu_help.addAction(self.action_help_about_app)

        toolbar=self.addToolBar("File")
        toolbar.addAction(self.action_file_open)
        toolbar.addAction(self.action_file_save)
        toolbar.addAction(self.action_file_clear)

        toolbar=self.addToolBar("Tools")
        toolbar.addAction(self.action_tools_select)
        toolbar.addAction(self.action_tools_delete)
        toolbar.addAction(self.action_tools_line)
        toolbar.addAction(self.action_tools_rect)
        toolbar.addAction(self.action_undo)
        toolbar.addAction(self.action_redo)


    def mousePressEvent(self, QMouseEvent):
        if (QMouseEvent.button() == QtCore.Qt.MouseButton.RightButton):
            self.RightClickMenu(QMouseEvent)

    def RightClickMenu(self, event):
        context_menu = QtWidgets.QMenu(self)
        # Populating the widget with actions
        context_tools = context_menu.addMenu("Tools")
        context_tools.addAction(self.action_tools_select)
        context_tools.addAction(self.action_tools_line)
        context_tools.addAction(self.action_tools_rect)
        context_tools.addAction(self.action_tools_ellipse)
        context_tools.addAction(self.action_tools_polygon)
        context_tools.addAction(self.action_tools_text)
        context_style = context_menu.addMenu("Style")
        context_pen =  context_style.addMenu('&Pen')
        context_pen.addAction(self.action_style_pen_color)
        context_pen.addAction(self.action_style_pen_line)
        context_pen.addAction(self.action_style_pen_width)
        context_brush =  context_style.addMenu('&Brush')
        context_brush.addAction(self.action_style_brush_color)
        context_brush.addAction(self.action_style_brush_fill)
        context_style.addAction("&Font")
        context_menu.exec_(self.mapToGlobal(event.pos()))

    def connect_actions(self) :
        self.action_file_open.triggered.connect(self.open)
        self.action_file_save.triggered.connect(self.save)
        self.action_file_clear.triggered.connect(self.clear)
        self.action_file_exit.triggered.connect(self.exit)
        self.action_file_save_as.triggered.connect(self.save_image)
    
        self.action_style_pen_color.triggered.connect(self.setPenColor)
        self.action_style_brush_color.triggered.connect(self.setBrushColor)
        self.action_style_pen_width.triggered.connect(self.setPenWidth)
        self.action_style_pen_line.triggered.connect(self.setPenLine)
        self.action_style_brush_fill.triggered.connect(self.setBrushstyle)
        self.action_style_font.triggered.connect(self.setFont)

        self.action_help_about_app.triggered.connect(self.openAboutAppDialog)
        self.action_help_about_qt.triggered.connect(self.openAboutQtDialog)
        self.action_help_about_us.triggered.connect(self.openAboutUsDialog)

        self.action_undo.triggered.connect(self.undo)
        self.action_redo.triggered.connect(self.redo)

        self.action_tools_select.triggered.connect(
            lambda checked,tool="select": self.set_action_tools(checked,tool)
        )
        self.action_tools_delete.triggered.connect(
            lambda checked,tool="delete": self.set_action_tools(checked,tool)
        )
        self.action_tools_line.triggered.connect(
            lambda checked,tool="line": self.set_action_tools(checked,tool)
        )
        self.action_tools_rect.triggered.connect(
            lambda checked,tool="rectangle": self.set_action_tools(checked,tool)
        )
        self.action_tools_ellipse.triggered.connect(
            lambda checked,tool="ellipse": self.set_action_tools(checked,tool)
        )
        self.action_tools_polygon.triggered.connect(
            lambda checked,tool="polygon": self.set_action_tools(checked,tool)
        )
        self.action_tools_text.triggered.connect(
            lambda checked, tool="text": self.set_action_tools(checked,tool)
        )

    def exit(self):
        exit_box = QtWidgets.QMessageBox(QtWidgets.QMessageBox.Question, "Exit", "Are you sure you want to exit?")
        exit_box.addButton(QtWidgets.QMessageBox.Yes)
        exit_box.addButton(QtWidgets.QMessageBox.No)
        exit_box.setDefaultButton(QtWidgets.QMessageBox.No)
        reply = exit_box.exec()
        if(reply==QtWidgets.QMessageBox.Yes):
            self.close()
        exit_box.close()
    

    def clear(self):
        self.scene.clearScene()

    def undo(self):
        self.scene.undo()

    def redo(self):
        self.scene.redo()

    def data_to_items(self, data):
        self.scene.clear()
        print("data",data)
        for d_item in data :
            print("d_item",d_item)
            t = d_item["type"]
            if t == "line":
                x1, y1, x2, y2, color, style, width = d_item["x1"], d_item["y1"], d_item["x2"], d_item["y2"], d_item["color"], d_item["style"], d_item["width"]
                pen = QtGui.QPen()
                pen.setColor(QtGui.QColor(color))
                pen.setWidth(width)
                pen.setStyle(style)
                self.scene.addLine(x1, y1, x2, y2, pen)
            elif t == "rect":
                x, y, w, h, color, brush_color, brush_style  = d_item["x"], d_item["y"], d_item["w"], d_item["h"], d_item["color"], d_item["brush_color"], d_item["brush_style"]
                pen = QtGui.QPen()
                brush = QtGui.QBrush()
                brush.setColor(QtGui.QColor(brush_color))
                brush.setStyle(brush_style)
                pen.setColor(QtGui.QColor(color))
                self.scene.addRect(x,y,w,h, pen, brush)
            elif t == "ellipse":
                x, y, recX, recY, recW, recH, color, width, style, brush_color, brush_style  = d_item["x"], d_item["y"], d_item["recX"], d_item["recY"], d_item["recW"], d_item["recH"], d_item["color"], d_item["width"], d_item["style"], d_item["brush_color"], d_item["brush_style"]
                pen = QtGui.QPen()
                brush = QtGui.QBrush()
                brush.setColor(QtGui.QColor(brush_color))
                brush.setStyle(brush_style)
                pen.setWidth(width)
                pen.setColor(QtGui.QColor(color))
                pen.setStyle(style)
                self.scene.addEllipse(recX,recY,recW,recH, pen, brush).setPos(x,y)
            elif t == "polygon":
                pen = QtGui.QPen()
                brush = QtGui.QBrush()
                x, y, points, color, width, style, brush_color, brush_style = d_item["x"], d_item["y"], d_item["points"], d_item["color"], d_item["width"], d_item["style"], d_item["brush_color"], d_item["brush_style"]
                pen.setColor(QtGui.QColor(color))
                pen.setWidth(width)
                pen.setStyle(style)
                brush.setColor(QtGui.QColor(brush_color))
                brush.setStyle(brush_style)
                self.scene.addPolygon(QtGui.QPolygonF([QtCore.QPoint(int(p[0]), int(p[1])) for p in points]),pen, brush).setPos(x,y)
            elif t == "text":
                font = QtGui.QFont()
                x, y, text, style, family, size = d_item["x"], d_item["y"], d_item["text"], d_item["style"], d_item["family"], d_item["size"]
                font.setStyleName(style)
                font.setPointSize(size)
                font.setFamily(family)
                self.scene.addText(text, font).setPos(x,y)

    def open(self):
        filename = QtWidgets.QFileDialog.getOpenFileName(self,"Open File", os.getcwd())
        #fileopen=QtCore.QFile(filename[0])
        file_to_open = json.load(open(filename[0], "r"))
        self.data_to_items(file_to_open)

    def items_to_data(self):
        # liste de dictionnaires d'items à sauvegarder
        to_save=[]
        for item in self.scene.items():
            if isinstance(item, QtWidgets.QGraphicsLineItem):
                # création d'un dictionnaire pour chaque item
                data = {}
                data["type"] = "line"
                data["x1"] = item.line().x1()
                data["y1"] = item.line().y1()
                data["x2"] = item.line().x2()
                data["y2"] = item.line().y2()
                data["color"] = item.pen().color().name()
                data["style"] = item.pen().style().numerator
                data["width"] = item.pen().width()
                # ajout du dictionnaire dans la liste des dictionnaires d'items
                to_save.append(data)
            # a completer pour chaque item
            elif  isinstance(item, QtWidgets.QGraphicsRectItem):
                data = {}
                data["type"] = "rect"
                data["x"] = item.rect().x()
                data["y"] = item.rect().y()
                data["w"] = item.rect().width()
                data["h"] = item.rect().height()
                data["color"] = item.pen().color().name()
                data["brush_color"] = item.brush().color().name()
                data["brush_style"] = item.brush().style().numerator
                to_save.append(data)
            elif  isinstance(item, QtWidgets.QGraphicsEllipseItem):
                data = {}
                data["type"] = "ellipse"
                data["x"] = item.pos().x()
                data["y"] = item.pos().y()
                data["recX"] = item.rect().x()
                data["recY"] = item.rect().y()
                data["recW"] = item.rect().width()
                data["recH"] = item.rect().height()
                data["color"] = item.pen().color().name()
                data["width"] = item.pen().width()
                data["style"] = item.pen().style()
                data["brush_color"] = item.brush().color().name()
                data["brush_style"] = item.brush().style()
                to_save.append(data)
            elif  isinstance(item, QtWidgets.QGraphicsPolygonItem):
                data = {}
                data["type"] = "polygon"
                data["x"] = item.pos().x()
                data["y"] = item.pos().y()
                data["points"] = [[p.x(), p.y()] for p in item.polygon()]
                data["color"] = item.pen().color().name()
                data["width"] = item.pen().width()
                data["style"] = item.pen().style()
                data["brush_color"] = item.brush().color().name()
                data["brush_style"] = item.brush().style()
                to_save.append(data)
            elif isinstance(item, QtWidgets.QGraphicsSimpleTextItem):
                data = {}
                data["type"] = "text"
                data["x"] = item.pos().x()
                data["y"] = item.pos().y()
                data["text"] = str(item.text())
                data["style"] = item.font().styleName()
                data["family"] = str(item.font().family())
                data["size"] = item.font().pointSize()
                to_save.append(data)
            else :
                pass
        return to_save

    def save(self) :
        filename = QtWidgets.QFileDialog.getSaveFileName(self,"Save File", os.getcwd())
        data=self.items_to_data()
        print(data)
        # file_to_save = open(filename,"wb")
        # pickle.dump(data,file_to_save)
        # file_to_save.close()
        file_to_save = QtCore.QFile(filename[0])
        if file_to_save.open(QtCore.QIODevice.WriteOnly):
            file_to_save.write(json.dumps(data).encode("utf-8"))
            file_to_save.close()

    def save_image(self):
        screen = QtWidgets.QApplication.primaryScreen()
        screenshot = screen.grabWindow( self.winId() )
        files_types = "JPG (*.jpg);;PNG (*.png)"
        filename = QtWidgets.QFileDialog.getSaveFileName(self, 'Save Image', os.getcwd(), files_types)
        screenshot.save(filename[0], 'jpg')

    def setFont(self):
        font, ok = QtWidgets.QFontDialog.getFont(self)
        if ok:
            print("Selected font : ", font.styleName(), font.pointSize(), font.family())
            self.scene.set_font(font.styleName(), font.pointSize(), font.family())
        
    def setPenColor(self):
        color = QtGui.QColor(QtWidgets.QColorDialog.getColor(QtCore.Qt.yellow, self ))
        if( color.isValid() ):
            print("Selected color : ", color.name())
            self.scene.set_pen_color(color)
        else:
            print("color invalid")

    def setBrushColor(self):
        color = QtGui.QColor(QtWidgets.QColorDialog.getColor(QtCore.Qt.yellow, self ))
        if( color.isValid() ):
            print("Selected color : ", color.name())
            self.scene.set_brush_color(color)
        else:
            print("color invalid")

    def setPenWidth(self):
        print(self.scene.pen.width())
        width = QtWidgets.QInputDialog.getInt(
            self, "Width modification",
            "Pen width:", self.scene.pen.width(), 0, 10, 1
        )
        if(width[1]):
            print("Selected width : ", width[0])
            self.scene.set_pen_width(width[0])
    
    def setPenLine(self):

        optionsLabel = ["NoPen", "SolidLine", "DashLine", "DotLine", "DashDotLine", "DashDotDotLine"]
        options = [QtCore.Qt.NoPen, QtCore.Qt.SolidLine, QtCore.Qt.DashLine, QtCore.Qt.DotLine, QtCore.Qt.DashDotLine, QtCore.Qt.DashDotDotLine]

        print("style :", self.scene.pen.style())
        line = QtWidgets.QInputDialog.getItem(
            self,
            "Line modification",
            "Pen line style :",
            optionsLabel,
            self.scene.pen.style(),
            False
        )
        print(line)
        if(line[1]):
            self.scene.set_pen_line(options[optionsLabel.index(line[0])])

    def setBrushstyle(self):

        optionsLabel = [
            "NoBrush",
            "SolidPattern",
            "Dense1Pattern",
            "Dense2Pattern",
            "Dense3Pattern",
            "Dense4Pattern",
            "Dense5Pattern",
            "Dense6Pattern",
            "Dense7Pattern",
            "HorPattern",
            "VerPattern",
            "CrossPattern",
            "BDiagPattern",
            "FDiagPattern",
            "DiagCrossPattern",
            "DashDotDotLine",
            "LinearGradientPattern",
            "ConicalGradientPattern",
            "RadialGradientPattern"
            ]
        options = [
            QtCore.Qt.NoBrush,
            QtCore.Qt.SolidPattern,
            QtCore.Qt.Dense1Pattern,
            QtCore.Qt.Dense2Pattern,
            QtCore.Qt.Dense3Pattern,
            QtCore.Qt.Dense4Pattern,
            QtCore.Qt.Dense5Pattern,
            QtCore.Qt.Dense6Pattern,
            QtCore.Qt.Dense7Pattern,
            QtCore.Qt.HorPattern,
            QtCore.Qt.VerPattern,
            QtCore.Qt.CrossPattern,
            QtCore.Qt.BDiagPattern,
            QtCore.Qt.FDiagPattern,
            QtCore.Qt.DiagCrossPattern,
            QtCore.Qt.DashDotDotLine,
            QtCore.Qt.LinearGradientPattern,
            QtCore.Qt.ConicalGradientPattern,
            QtCore.Qt.RadialGradientPattern]
            

        print("brush style :", self.scene.brush.style())
        line = QtWidgets.QInputDialog.getItem(
            self,
            "Brush modification",
            "Brush line style :",
            optionsLabel,
            self.scene.brush.style(),
            False
        )
        print(line)
        if(line[1]):
            self.scene.set_brush_style(options[optionsLabel.index(line[0])])    


    def set_action_tools(self,checked,tool) :
        print("checked : ",checked)
        print("tool : ",tool)
        self.scene.set_tool(tool)



    def openAboutAppDialog(self):
        dlg = QtWidgets.QMessageBox()
        dlg.setWindowTitle("About App")
        dlg.setText(
            "README\n\n"+
            "Application qui permet de dessiner des formes (lignes, rectangles, ellipses et polygone) avec différents styles tels que la taille/couleur/type de contours et la couleur/type de remplissage\n\n"+
            "Afin de bouger correctement les formes, il existe mode \"selection\"\n"+
            "Pour l'utiliser il faut cliquer sur les formes (le contour vert indique la selection\n"+
            "Pour déplacer les formes, il faut cliquer sur une forme déjà selectionnée, "+
            "rester appuyé et déplacer la souris.\n"+
            "Pour déselectionner les formes, il suffit de cliquer dans une zone sans forme\n")
        dlg.exec()
    
    def openAboutQtDialog(self):
        dlg = QtWidgets.QMessageBox()
        dlg.setText("Version de Qt : " + QtCore.QT_VERSION_STR)
        dlg.setWindowTitle("About Qt")
        dlg.exec()
    
    def openAboutUsDialog(self):
        dlg = QtWidgets.QMessageBox()
        dlg.setWindowTitle("About Us")
        dlg.setText("Valentin Roncoroni - Simon Bruno")
        dlg.exec()
    
    def resizeEvent(self, event):
        print("MainWindow.resizeEvent()")
        print("dx : ",self.size().width()-self.view.size().width())
        print("dy : ",self.size().height()-self.view.size().height())
        print("menubar size : ", self.menuBar().size())

if __name__ == "__main__" :  
    print(QtCore.QT_VERSION_STR)
    app=QtWidgets.QApplication(sys.argv)
    scene=Scene()
    position=500,500
    dimension=600,400
    main=MainWindow(scene,position,dimension)
    main.show()
    sys.exit(app.exec_())

# look at https://www.informit.com/articles/article.aspx?p=1187104&seqNum=3# for undo-redo
