try:
    from PyQt4 import QtCore, QtGui
except ImportError:
    from PySide import QtCore, QtGui
    from maya import OpenMayaUI as omui
    from shiboken import wrapInstance
import maya.cmds as cmds

def get_maya_window():
    """
    This gets a pointer to the Maya window.

    :return: A pointer to the Maya window.
    :type: pointer
    """
    maya_main_window_ptr = omui.MQtUtil.mainWindow()
    return wrapInstance(long(maya_main_window_ptr), QtGui.QWidget)


class ShapeMaker(QtGui.QDialog):
    """
    This class creates some default shapes.
    """
    def __init__(self):
        QtGui.QDialog.__init__(self, parent=get_maya_window())

    def init_gui(self):
        main_layout = QtGui.QVBoxLayout(self)
        sphere_btn  = QtGui.QPushButton('Sphere')
        cone_btn    = QtGui.QPushButton('Cone')
        torus_btn   = QtGui.QPushButton('Torus')
        sphere_btn.clicked.connect(self.create_sphere)
        cone_btn.clicked.connect(self.create_cone)
        torus_btn.clicked.connect(self.create_torus)
        main_layout.addWidget(sphere_btn)
        main_layout.addWidget(cone_btn)
        main_layout.addWidget(torus_btn)

        # Set up how the window looks.
        self.setGeometry(300, 300, 450, 300)
        self.setWindowTitle('Hello World')
        img_icon = 'C:/Users/caj150430/code/so_much_win.png'
        self.setWindowIcon(QtGui.QIcon(img_icon))
        self.show()

    @classmethod
    def create_sphere(cls):
        """
        This method creates a default sphere.
        """
        cmds.polySphere()

    @classmethod
    def create_cone(cls):
        """
        This method creates a default cone.
        """
        cmds.polyCone()

    @classmethod
    def create_torus(cls):
        """
        This method creates a default torus.
        """
        cmds.polyTorus()

shape_maker = ShapeMaker()
shape_maker.init_gui()
shape_maker.create_sphere()
shape_maker.create_cone()
shape_maker.create_torus()


class TreeView(QtGui.QDialog):
    """
    This class creates some default shapes.
    """
    def __init__(self):
        QtGui.QDialog.__init__(self, parent=get_maya_window())
        self.tree_view = None
        self.cones     = None
        self.spheres   = None

    def init_gui(self):
        main_layout = QtGui.QVBoxLayout(self)

        self.tree_view  = QtGui.QTreeWidget()
        self.tree_view.setMinimumWidth(200)
        self.tree_view.setMinimumHeight(140)
        self.tree_view.setHeaderLabel('Tree View Widget')
        root            = QtGui.QTreeWidgetItem(self.tree_view, ['Root Level'])
        self.spheres    = QtGui.QTreeWidgetItem(root, ['Spheres'])
        self.cones      = QtGui.QTreeWidgetItem(root, ['Cones'])
        #QtGui.QTreeWidgetItem(sphere_sublevel, ['Sphere1'])
        #QtGui.QTreeWidgetItem(sphere_sublevel, ['Sphere2'])
        #QtGui.QTreeWidgetItem(cone_sublevel, ['Cone1'])

        add_btn = QtGui.QPushButton('Add Stuff')
        add_btn.clicked.connect(self.add_stuff)
        main_layout.addWidget(self.tree_view)
        main_layout.addWidget(add_btn)

        # Make the items expand when they a created.
        root.setExpanded(True)
        self.spheres.setExpanded(True)
        self.cones.setExpanded(True)

        # Set up how the window looks.
        self.setGeometry(300, 300, 450, 300)
        self.setWindowTitle('Hello World')
        img_icon = 'C:/Users/caj150430/code/so_much_win.png'
        self.setWindowIcon(QtGui.QIcon(img_icon))
        self.show()

    def add_stuff(self):
        all_trans = cmds.ls(type='transform')
        for trans in all_trans:
            if 'pSphere' in trans:
                QtGui.QTreeWidgetItem(self.spheres, [trans])
            elif 'pCone' in trans:
                QtGui.QTreeWidgetItem(self.cones, [trans])

shape_maker = TreeView()
shape_maker.init_gui()


class SomeCheckboxes(QtGui.QDialog):
    """
    This class creates some default shapes.
    """
    def __init__(self):
        QtGui.QDialog.__init__(self, parent=get_maya_window())
        self.cb_01 = None
        self.cb_02 = None
        self.cb_03 = None

    def init_gui(self):
        main_layout = QtGui.QVBoxLayout(self)

        # Make some check boxes and a button.
        self.cb_01 = QtGui.QCheckBox('01')
        self.cb_02 = QtGui.QCheckBox('02')
        self.cb_03 = QtGui.QCheckBox('03')
        toggle_btn = QtGui.QPushButton('Toggle')
        toggle_btn.clicked.connect(self.toggle_it)

        # Add them to a layout.
        cb_hb = QtGui.QHBoxLayout()
        cb_hb.addWidget(self.cb_01)
        cb_hb.addWidget(self.cb_02)
        cb_hb.addWidget(self.cb_03)

        # Add it all to the layout.
        main_layout.addLayout(cb_hb)
        main_layout.addWidget(toggle_btn)

        # Set up how the window looks.
        self.setGeometry(300, 300, 450, 300)
        self.setWindowTitle('Hello World')
        img_icon = 'C:/Users/caj150430/code/so_much_win.png'
        self.setWindowIcon(QtGui.QIcon(img_icon))
        self.show()

    def toggle_it(self):
        """
        Toggles the state of all the check boxes to either enable or
        disable user interaction with them.
        """
        for cb in [self.cb_01, self.cb_02, self.cb_03]:
            if cb.isEnabled():
                cb.setDisabled(True)
            else:
                cb.setDisabled(False)

shape_maker = SomeCheckboxes()
shape_maker.init_gui()

# Passing things from one class to another.
class One(object):
    def pass_something(self):
        value = '30'
        two   = Two(value)
        print "The value of two is really %s" % two.value


class Two(object):
    def __init__(self, value):
        print "The value is %s" % value
        self.value = value
one = One()
one.pass_something()

