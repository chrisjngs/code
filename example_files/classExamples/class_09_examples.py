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

class ImagesAndLabels(QtGui.QDialog):
    def __init__(self):
        QtGui.QDialog.__init__(self, parent=get_maya_window())
        self.player_le = None

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

        # Give the buttons a name and connect a click even.
        char_01_btn.setObjectName('ryu')
        char_02_btn.setObjectName('akuma')
        char_03_btn.setObjectName('blanka')
        char_04_btn.setObjectName('dhalsim')
        char_01_btn.clicked.connect(self.change_player)
        char_02_btn.clicked.connect(self.change_player)
        char_03_btn.clicked.connect(self.change_player)
        char_04_btn.clicked.connect(self.change_player)

        # Add some labels.
        char_01_lbl = QtGui.QLabel('Ryu')
        char_02_lbl = QtGui.QLabel('Akuma')
        char_03_lbl = QtGui.QLabel('Blanka')
        char_04_lbl = QtGui.QLabel('Dhalsim')

        # Add this stuff to an hbox layout.
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

        # Add a player field and a line edit.
        hb_player_data = QtGui.QHBoxLayout()
        player_lbl     = QtGui.QLabel('Player: ')
        self.player_le = QtGui.QLineEdit('')
        hb_player_data.addWidget(player_lbl)
        hb_player_data.addWidget(self.player_le)
        main_vb.addLayout(hb_layout)
        main_vb.addLayout(hb_layout_02)
        main_vb.addLayout(hb_player_data)
        main_vb.addStretch(1)

        # Set up how the window looks.
        self.setGeometry(300, 300, 450, 300)
        self.setWindowTitle('Hello World')
        img_icon = 'C:/Users/caj150430/code/so_much_win.png'
        self.setWindowIcon(QtGui.QIcon(img_icon))
        self.show()

    def change_player(self):
        """
        Lets us know a radio button was toggled.
        """
        sender = self.sender()
        if sender:
            print "The value is %s" % str(sender.objectName())
            sender_text = str(sender.objectName())
            self.player_le.setText(sender_text)

images_gui = ImagesAndLabels()
images_gui.init_gui()


class ListViewGUI(QtGui.QDialog):
    def __init__(self):
        QtGui.QDialog.__init__(self, parent=get_maya_window())
        self.list_view = None

    def init_gui(self):
        # Make a layout to use.
        main_vb = QtGui.QVBoxLayout(self)

        # Add a list view.
        self.list_view  = QtGui.QListWidget()
        some_items = ['ice cream', 'pizza', 'bubble tea']
        self.add_lv_items(some_items)
        self.list_view.currentItemChanged['QListWidgetItem*', 'QListWidgetItem*'].connect(self.lv_item_clicked)
        self.list_view.setMinimumWidth(200)
        self.list_view.setMinimumHeight(150)

        # Add some buttons.
        vb_layout = QtGui.QVBoxLayout()
        btn_01    = QtGui.QPushButton('Sure')
        btn_02    = QtGui.QPushButton('Why Not')
        btn_01.setStyleSheet('background-color: firebrick')
        btn_02.setStyleSheet('background-color: salmon')
        btn_01.clicked.connect(self.cycle_through_lv)
        vb_layout.addWidget(btn_01)
        vb_layout.addWidget(btn_02)

        main_vb.addWidget(self.list_view)
        main_vb.addLayout(vb_layout)

        # Set up how the window looks.
        self.setGeometry(300, 300, 450, 300)
        self.setWindowTitle('Hello World')
        img_icon = 'C:/Users/caj150430/code/so_much_win.png'
        self.setWindowIcon(QtGui.QIcon(img_icon))
        self.show()

    def cycle_through_lv(self):
        """
        """
        # Put code here.
        # Check out the 'count' attribute of the list view widget.
        print "Here are the items in the list view:"
        for i in range(self.list_view.count()):
            widget_item = self.list_view.item(i)
            print "  %s" % widget_item.text()

    def lv_item_clicked(self, item):
        """
        """
        if item:
            print str(item.text())

    def add_lv_items(self, items):
        """
        """
        if items:
            self.list_view.clear()
            for item in items:
                widget_item = QtGui.QListWidgetItem(item)
                self.list_view.addItem(widget_item)

list_gui = ListViewGUI()
list_gui.init_gui()


# Add this to your class.
    def move_items_up(self, items):
        """
        """
        cmds.move(5, items, moveY=True)

