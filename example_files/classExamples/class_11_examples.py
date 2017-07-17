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


# A custom layout.
class LineEditAndButton(QtGui.QHBoxLayout):
    def __init__(self, obj_name='This will be overwritten'):
        """
        :param obj_name: The name of an object in Maya.
        :type: str
        """
        QtGui.QHBoxLayout.__init__(self)
        self.obj_name = obj_name
        self.some_le  = None

    def init_layout(self):
        """
        This method will create the button and line edit.
        """
        # Create a button.
        some_btn = QtGui.QPushButton('Print')

        # Create a line edit.
        self.some_le = QtGui.QLineEdit(self.obj_name)

        # Connect the button to the 'get_value' method.
        some_btn.clicked.connect(self.get_value)

        # Add the line edit and button to the layout.
        self.addWidget(self.some_le)
        self.addWidget(some_btn)

        # Return the layout.
        return self

    def get_value(self):
        """
        This method will trigger when the button is clicked and it will print the value
        of the line edit.
        """
        # Get the value of the text in the line edit.
        print "The value of the line edit is %s" % self.some_le.text()


class DynamicLayouts(QtGui.QDialog):
    """
    This layout makes line edits and buttons depending on the user selection.
    """
    def __init__(self):
        QtGui.QDialog.__init__(self, parent=get_maya_window())

    def init_gui(self):
        """
        Shows the GUI to the user.
        """
        # Create the main layout.
        main_vb = QtGui.QVBoxLayout(self)

        # Get all the stuff the user selected.
        objs = cmds.ls(selection=True)
        for obj in objs:
            # Create a custom layout using the LineEditAndButton class.
            custom_layout = LineEditAndButton(obj)
            custom_layout.init_layout()
            main_vb.addLayout(custom_layout)

        # Set up how the window looks.
        self.setGeometry(300, 300, 450, 300)
        self.setWindowTitle('Hello World')
        img_icon = 'C:/Users/caj150430/code/so_much_win.png'
        self.setWindowIcon(QtGui.QIcon(img_icon))
        self.show()

dynamic = DynamicLayouts()
dynamic.init_gui()


# Using args and kwargs.
def print_function(obj, item):
    print "Here are the values '%s' and '%s'" % (obj, item)

def print_function(food=None, car=None, *args):
    for value in args:
        print "Here is the value " + str(value)
    print "The value of food is %s" % food
    print "The value of car is %s" % car

print_function('hello', 'goodbye', car='testing')

def create_objs(obj_type=None, obj_scale=None):
    """
    This function creates some objects.

    :param obj_type: The type of object to create, i.e. 'pSphere'.
    :type: str

    :param obj_scale: How much to scale the object.
    :type: float
    """
    # Check the object type.
    new_obj = None
    if obj_type == 'pSphere':
        new_obj = cmds.polySphere()[0]
    if new_obj and obj_scale:
        cmds.scale(obj_scale, new_obj, scaleY=True)

def create_objs(*args):
    """
    This function creates some objects.
    """
    # Check the object type.
    new_obj = None
    if args[0] == 'pSphere':
        new_obj = cmds.polySphere()[0]
    if new_obj and args[1]:
        cmds.scale(args[1], new_obj, scaleY=True)

create_objs('pSphere', 5)

def kwargs_test(*args, **kwargs):
    print "The args are %s" % str(args)
    print "The kwargs are %s" % kwargs

kwargs_test('foo', 'blah', triangle='edges', hedges='trees')

def create_objs(**kwargs):
    """
    This function creates some objects.

    :param obj_type: The type of object to create, i.e. 'pSphere'.
    :type: str

    :param obj_scale: How much to scale the object.
    :type: float
    """
    # Set up some defaults.
    obj_type  = kwargs.setdefault('obj_type', None)
    obj_scale = kwargs.setdefault('obj_scale', None)
    obj_move  = kwargs.setdefault('obj_move', None)

    # Check the object type.
    new_obj = None
    if obj_type == 'pSphere':
        new_obj = cmds.polySphere()[0]
    if new_obj and obj_scale:
        cmds.scale(obj_scale, new_obj, scaleY=True)
    if new_obj and obj_move:
        cmds.move(obj_move, new_obj, moveY=True)

create_objs(obj_type='pSphere', triangle='edges', obj_move=5, hedges='trees')


# Making a GUI that writes data to a text file.
# Write a file to disk.
text_file = 'C:/Users/caj150430/code/my_lyrics.txt'
lyrics    = ["On a warm summer's eve",
             "On a train bound for nowhere",
             "I met up with the gambler",
             "We were both too tired to sleep"]
file_hdl  = open(text_file, 'w')
for lyric in lyrics:
    line = "%s\r\n" % lyric
    file_hdl.write(line)
file_hdl.close()

class WriteGUI(QtGui.QDialog):
    def __init__(self):
        QtGui.QDialog.__init__(self, parent=get_maya_window())

    def init_gui(self):
        # Make a layout to use.
        main_vb = QtGui.QVBoxLayout(self)

        # Make some random buttons.
        btn_01 = QtGui.QPushButton('Write It')
        btn_01.clicked.connect(self.write_file)

        # Add the layouts to the main layout.
        main_vb.addLayout(btn_01)

        # Set up how the window looks.
        self.setGeometry(300, 300, 450, 300)
        self.setWindowTitle('Hello World')
        img_icon = 'C:/Users/caj150430/code/so_much_win.png'
        self.setWindowIcon(QtGui.QIcon(img_icon))
        self.show()

    def write_file(self):
        """
        This method will write out translation, rotation, and scale values.
        """

