
import maya.cmds as cmds
from PySide import QtCore, QtGui
import shiboken
import maya.OpenMayaUI as apiUI

def get_maya_window():
    """
    Get the main Maya window as a QtGui.QMainWindow instance
    @return: QtGui.QMainWindow instance of the top level Maya windows
    """
    ptr = apiUI.MQtUtil.mainWindow()
    if ptr is not None:
        return shiboken.wrapInstance(long(ptr), QtGui.QWidget)

class RenamingGUI(QtGui.QDialog):
    def __init__(self):
        QtGui.QDialog.__init__(self, parent=get_maya_window())
        self.list_view = None
        self.item_name = None

    def init_gui(self):
        """
        Draws the GUI and displays it to the user.
        """
        # Choose a layout.
        main_vb = QtGui.QVBoxLayout(self)

        # Add a list or tree view.
        self.list_view = QtGui.QListWidget()

        # Add the buttons.
        load_btn   = QtGui.QPushButton('Load Selected')
        cancel_btn = QtGui.QPushButton('Cancel')
        load_btn.clicked.connect(self.update_list_view)
        cancel_btn.clicked.connect(self.close)

        # Connect the list/tree view with a method appropriate for user interaction.
        self.list_view.currentItemChanged['QListWidgetItem*', 'QListWidgetItem*'].connect(self.set_current_name)
        self.list_view.itemChanged['QListWidgetItem*'].connect(self.change_name)

        # Add the widgets to the layout.
        btn_hb = QtGui.QHBoxLayout()
        btn_hb.addWidget(load_btn)
        btn_hb.addWidget(cancel_btn)
        main_vb.addWidget(self.list_view)
        main_vb.addLayout(btn_hb)

        # Show the GUI.
        self.setGeometry(300, 300, 450, 300)
        self.setWindowTitle('Hello World')
        img_icon = 'C:/Users/caj150430/code/so_much_win.png'
        self.setWindowIcon(QtGui.QIcon(img_icon))
        self.show()

    def update_list_view(self):
        """
        Redraws the list view when the user clicks the 'load selected' button.
        """
        # Clear the list/tree view.
        self.list_view.clear()

        # Find all the selected things in Maya.
        selected = cmds.ls(selection=True)

        # For each of the selected things, create a widget item.
        for thing in selected:
            item = QtGui.QListWidgetItem(thing)
            item.setFlags(item.flags() | QtCore.Qt.ItemIsEditable)
            self.list_view.addItem(item)
            # Set the flags on the widget item so it is editable.

    def set_current_name(self, item):
        """
        Gets the name of the text the user selected.
        """
        # Store the text of whatever the user selected.
        if item:
            self.item_name = str(item.text())
        else:
            self.item_name = ''

    def change_name(self, item):
        """
        Using the new name, it changes the name in the GUI and on the Maya object.
        """
        # Get the new name.
        new_name = str(item.text())
        if not new_name or not self.item_name:
            return None

        # See if the name was actually changed.
        if new_name == self.item_name:
            return None

        # If it was, change the name in the list/tree view and in Maya.
        if not new_name:
            item.setText(self.item_name)
        self.item_name = cmds.rename(self.item_name, new_name)
        item.setText(self.item_name)

rn_gui = RenamingGUI()
rn_gui.init_gui()
