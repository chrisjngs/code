
# Imports to use PySide
try:
    from PyQt4 import QtCore, QtGui
except ImportError:
    from PySide import QtCore, QtGui
    from maya import OpenMayaUI as omui
    from shiboken import wrapInstance

def get_maya_window():
    """
    This gets a pointer to the Maya window.

    :return: A pointer to the Maya window.
    :type: pointer
    """
    maya_main_window_ptr = omui.MQtUtil.mainWindow()
    return wrapInstance(long(maya_main_window_ptr), QtGui.QWidget)

# Reviewing what we covered in the last class.
class Practice(QtGui.QDialog):
    def __init__(self):
        QtGui.QDialog.__init__(self, parent=get_maya_window())

    def init_gui(self):
        label_one = QtGui.QLabel('First', self)
        label_one.move(20, 20)
        btn_one   = QtGui.QPushButton('Erase the harddrive', self)
        btn_one.move(20, 50)
        some_cb = QtGui.QComboBox(self)
        some_cb.addItems(['Pie Five', 'Chipotle', 'Torchies'])
        some_cb.move(20, 80)
        some_chbx= QtGui.QCheckBox('Some Checkbox', self)
        some_chbx.move(20, 110)

        # Set up how the window looks.
        self.setGeometry(300, 300, 250, 150)
        self.setWindowTitle('Hello World')
        img_icon = 'C:/Users/caj150430/code/so_much_win.png'
        self.setWindowIcon(QtGui.QIcon(img_icon))
        self.show()

practice_gui = Practice()
practice_gui.init_gui()

# Using VBox and HBox layouts.
class Layouts(QtGui.QDialog):
    def __init__(self):
        QtGui.QDialog.__init__(self, parent=get_maya_window())


    def init_gui(self):
        # Make a layout to use.
        main_vb = QtGui.QVBoxLayout(self)

        # Make some random buttons.
        btn_01 = QtGui.QPushButton('01')
        btn_02 = QtGui.QPushButton('02')
        btn_03 = QtGui.QPushButton('03')
        btn_04 = QtGui.QPushButton('04')
        btn_05 = QtGui.QPushButton('05')
        btn_06 = QtGui.QPushButton('06')
        btn_07 = QtGui.QPushButton('07')
        btn_08 = QtGui.QPushButton('08')
        btn_09 = QtGui.QPushButton('09')

        # Make a column.
        v_box_01 = QtGui.QVBoxLayout()
        v_box_01.addWidget(btn_07)
        v_box_01.addWidget(btn_08)
        v_box_01.addWidget(btn_09)

        # Make a row.
        h_box_01 = QtGui.QHBoxLayout()
        h_box_01.addWidget(btn_01)
        h_box_01.addWidget(btn_03)
        h_box_01.addLayout(v_box_01)

        # Make another row.
        h_box_02 = QtGui.QHBoxLayout()
        h_box_02.addWidget(btn_04)
        h_box_02.addWidget(btn_05)

        # Make another row.
        h_box_03 = QtGui.QHBoxLayout()
        h_box_03.addWidget(btn_06)

        # Add the layouts to the main layout.
        #main_vb.addLayout(h_box_02)
        main_vb.addLayout(h_box_01)
        main_vb.addLayout(h_box_03)

        # Set up how the window looks.
        self.setGeometry(300, 300, 450, 300)
        self.setWindowTitle('Hello World')
        img_icon = 'C:/Users/caj150430/code/so_much_win.png'
        self.setWindowIcon(QtGui.QIcon(img_icon))
        self.show()

layout_gui = Layouts()
layout_gui.init_gui()


# Using a grid layout.
class GridLayout(QtGui.QDialog):
    def __init__(self):
        QtGui.QDialog.__init__(self, parent=get_maya_window())

    def init_gui(self):
        # Make a layout to use.
        main_gl = QtGui.QGridLayout(self)

        # Make some random buttons.
        btn_01 = QtGui.QPushButton('01')
        btn_02 = QtGui.QPushButton('02')
        btn_03 = QtGui.QPushButton('03')
        btn_04 = QtGui.QPushButton('04')
        btn_05 = QtGui.QPushButton('05')
        btn_06 = QtGui.QPushButton('06')
        btn_07 = QtGui.QPushButton('07')
        btn_08 = QtGui.QPushButton('08')
        btn_09 = QtGui.QPushButton('09')

        # Track the rows.
        gr = 0

        # Add some buttons to the grid layout.
        main_gl.addWidget(btn_01, gr, 0)
        main_gl.addWidget(btn_02, gr, 1)
        main_gl.addWidget(btn_03, gr, 2)
        gr += 1
        main_gl.addWidget(btn_04, gr, 1)
        main_gl.addWidget(btn_05, gr, 2)
        gr += 1
        main_gl.addWidget(btn_06, gr, 0, 2, 2)

        # Set up how the window looks.
        self.setGeometry(300, 300, 450, 300)
        self.setWindowTitle('Hello World')
        img_icon = 'C:/Users/caj150430/code/so_much_win.png'
        self.setWindowIcon(QtGui.QIcon(img_icon))
        self.show()

gl_gui = GridLayout()
gl_gui.init_gui()

# Making a GUI that allows the user to select a character.
class ImagesAndLabels(QtGui.QDialog):
    def __init__(self):
        QtGui.QDialog.__init__(self, parent=get_maya_window())

    def init_gui(self):
        # Make a layout to use.
        main_vb = QtGui.QVBoxLayout(self)

        # Load up the images and store them in a way Qt understands them.
        # Then create something to hold the image and a label.
        char_01_img = QtGui.QPixmap('C:/Users/caj150430/code/imgs/Ryu.jpg')
        char_01_btn = QtGui.QPushButton()
        char_01_btn.setIcon(char_01_img)
        char_02_img = QtGui.QPixmap('C:/Users/caj150430/code/imgs/akuma.jpg')
        char_02_btn = QtGui.QPushButton()
        char_02_btn.setIcon(char_02_img)
        char_03_img = QtGui.QPixmap('C:/Users/caj150430/code/imgs/blanka.jpg')
        char_03_btn = QtGui.QPushButton()
        char_03_btn.setIcon(char_03_img)
        char_04_img = QtGui.QPixmap('C:/Users/caj150430/code/imgs/dhalsim.jpg')
        char_04_btn = QtGui.QPushButton()
        char_04_btn.setIcon(char_04_img)

        char_01_lbl = QtGui.QLabel('Ryu')
        char_02_lbl = QtGui.QLabel('Akuma')
        char_03_lbl = QtGui.QLabel('Blanka')
        char_04_lbl = QtGui.QLabel('Dhalsim')

        hb_layout = QtGui.QHBoxLayout()
        hb_layout.addWidget(char_01_btn)
        hb_layout.addWidget(char_02_btn)
        hb_layout.addWidget(char_03_btn)
        hb_layout.addWidget(char_04_btn)
        hb_layout_02 = QtGui.QHBoxLayout()
        hb_layout_02.addWidget(char_01_lbl)
        hb_layout_02.addWidget(char_02_lbl)
        hb_layout_02.addWidget(char_03_lbl)
        hb_layout_02.addWidget(char_04_lbl)

        main_vb.addLayout(hb_layout)
        main_vb.addLayout(hb_layout_02)
        main_vb.addStretch(1)
        # Set up how the window looks.
        self.setGeometry(300, 300, 450, 300)
        self.setWindowTitle('Hello World')
        img_icon = 'C:/Users/caj150430/code/so_much_win.png'
        self.setWindowIcon(QtGui.QIcon(img_icon))
        self.show()

images_gui = ImagesAndLabels()
images_gui.init_gui()

