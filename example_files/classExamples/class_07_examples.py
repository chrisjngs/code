# Using PySide in Maya.
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


class Example(QtGui.QDialog):
    """
    A GUI that has some labels.
    """
    def __init__(self):
        QtGui.QDialog.__init__(self, parent=get_maya_window())

    def init_gui(self):
        """
        Sets up how the GUI looks and shows it to the user.
        """
        label_one = QtGui.QLabel('First', self)
        label_one.move(20, 20)
        label_two = QtGui.QLabel('Second', self)
        label_two.move(40, 40)
        label_three = QtGui.QLabel('Third', self)
        label_three.move(60, 60)
        self.setGeometry(300, 300, 250, 150)
        self.setWindowTitle('Hello World')
        img_icon = 'C:/Users/<user_name>/code/so_much_win.png'
        self.setWindowIcon(QtGui.QIcon(img_icon))
        self.show()

example_gui = Example()
example_gui.init_gui()


class ButtonGUI(QtGui.QDialog):
    """
    This class has some buttons.
    """
    def __init__(self):
        QtGui.QDialog.__init__(self, parent=get_maya_window())

    def init_gui(self):
        """
        Sets up how the GUI looks and shows it to the user.
        """
        first_btn = QtGui.QPushButton('Erase the harddrive', self)
        first_btn.clicked.connect(self.first_btn_clicked)
        first_btn.move(20, 20)
        first_btn.setFixedHeight(25)
        first_btn.setFixedWidth(120)

        first_btn.setToolTip('This is a QPushButton')

        second_btn = QtGui.QPushButton('Order Chipotle', self)
        second_btn.clicked.connect(self.second_btn_clicked)
        second_btn.move(20, 50)
        second_btn.setFixedHeight(25)
        second_btn.setFixedWidth(120)

        self.setToolTip('This is a QDialog')
        self.setGeometry(300, 300, 250, 150)
        self.setWindowTitle('Button GUI')
        img_icon = 'C:/Users/<user_name>/code/so_much_win.png'
        self.setWindowIcon(QtGui.QIcon(img_icon))
        self.show()

    def first_btn_clicked(self):
        """
        Registers that a button was clicked.
        """
        print 'Yep, the button was clicked'

    def second_btn_clicked(self):
        """
        Registers that a button was clicked.
        """
        print 'Yep, the other button was clicked'

button_gui = ButtonGUI()
button_gui.init_gui()


class ComboBoxGUI(QtGui.QDialog):
    """
    This class has a line edit and a combo box.
    """
    def __init__(self):
        QtGui.QDialog.__init__(self, parent=get_maya_window())
        self.some_cb = None
        self.some_le = None
        self.le_text = None

    def init_gui(self):
        """
        Sets up how the GUI looks and shows it to the user.
        """
        self.some_le = QtGui.QLineEdit(self)
        self.some_le.move(20, 0)

        self.some_cb = QtGui.QComboBox(self)
        self.some_cb.addItems(['Pie Five', 'Chipotle', 'Torchies'])
        self.some_cb.move(20, 20)

        second_btn = QtGui.QPushButton('Get selection', self)
        second_btn.clicked.connect(self.second_btn_clicked)
        second_btn.move(20, 50)
        second_btn.setFixedHeight(25)
        second_btn.setFixedWidth(120)

        self.setToolTip('This is a QDialog')
        self.setGeometry(300, 300, 250, 150)
        self.setWindowTitle('Combo Box GUI')
        img_icon = 'C:/Users/<user_name>/code/so_much_win.png'
        self.setWindowIcon(QtGui.QIcon(img_icon))
        self.show()

    def second_btn_clicked(self):
        """
        Registers that a button was clicked.
        """
        print "The current combo box text is %s" % self.some_cb.currentText()
        self.set_le_value()

    def set_le_value(self):
        """
        Sets the value of line edit.
        """
        self.le_text = self.some_le.text()

cb_gui = ComboBoxGUI()
cb_gui.init_gui()
print cb_gui.le_text


class CheckboxAndRadio(QtGui.QDialog):
    """
    This class has a check box and some radio buttons.
    """
    def __init__(self):
        QtGui.QDialog.__init__(self, parent=get_maya_window())
        self.some_cb   = None
        self.rad_grp   = None
        self.rad_value = None

    def init_gui(self):
        """
        Sets up how the GUI looks and shows it to the user.
        """
        self.some_cb = QtGui.QCheckBox('Some Checkbox', self)
        self.some_cb.move(20, 20)

        self.rad_grp = QtGui.QButtonGroup(self)
        rd_01        = QtGui.QRadioButton('01', self)
        rd_02        = QtGui.QRadioButton('02', self)
        rd_01.move(20, 40)
        rd_02.move(60, 40)
        rd_01.setObjectName('01')
        rd_02.setObjectName('02')
        rd_01.toggled.connect(self.radio_toggled)
        rd_02.toggled.connect(self.radio_toggled)
        self.rad_grp.addButton(rd_01)
        self.rad_grp.addButton(rd_02)

        second_btn = QtGui.QPushButton('Checkbox Value', self)
        second_btn.clicked.connect(self.second_btn_clicked)
        second_btn.move(20, 65)
        second_btn.setFixedHeight(25)
        second_btn.setFixedWidth(120)

        self.setToolTip('This is a QDialog')
        self.setGeometry(300, 300, 250, 150)
        self.setWindowTitle('Combo Box GUI')
        img_icon = 'C:/Users/<user_name>/code/so_much_win.png'
        self.setWindowIcon(QtGui.QIcon(img_icon))
        self.show()

    def radio_toggled(self):
        """
        Lets us know a radio button was toggled.
        """
        sender = self.sender()
        if sender:
            print "The value is %s" % str(sender.objectName())

    def second_btn_clicked(self):
        """
        Registers that a button was clicked.
        """
        print "The checkbox is set to %s" % self.some_cb.checkState()

cbr_gui = CheckboxAndRadio()
cbr_gui.init_gui()

