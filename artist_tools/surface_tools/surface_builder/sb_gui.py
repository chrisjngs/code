#!/usr/bin/env python
#SETMODE 777

#----------------------------------------------------------------------------------------#
#------------------------------------------------------------------------------ HEADER --#

"""
:author:
    Chris Jennings

:synopsis:
    This is the GUI for the surface builder tool.

:description:
    A detailed description of what this module does.

:applications:
    Maya.

:see_also:
    artist_tool/surface_tool/turntable_tool/tool_gui

"""

#----------------------------------------------------------------------------------------#
#----------------------------------------------------------------------------- IMPORTS --#

# Built-in and Third Party
try:
    from PyQt4 import QtCore, QtGui
except ImportError:
    from PySide import QtCore, QtGui
    from maya import OpenMayaUI as omui
    from shiboken import wrapInstance
# Modules That You Wrote
import artist_tools.surface_tools.surface_builder.sb_logic as sbl;reload(sbl)

from artist_tools.surface_tools.surface_builder.sb_logic import BuildShader

#----------------------------------------------------------------------------------------#
#--------------------------------------------------------------------------- FUNCTIONS --#
def get_maya_window():
    """
    This gets a pointer to the Maya window.

    :return: A pointer to the Maya window.
    :type: pointer
    """
    maya_main_window_ptr = omui.MQtUtil.mainWindow()
    return wrapInstance(long(maya_main_window_ptr), QtGui.QWidget)
#----------------------------------------------------------------------------------------#
#----------------------------------------------------------------------------- CLASSES --#

class SurfaceGUI(QtGui.QDialog):
    """
    This class creates the gui for the surface builder tool.
    """

    def __init__(self):
        QtGui.QDialog.__init__(self, parent=get_maya_window())
        self.surface_name = None

    def init_gui(self):
        """
        Sets up how the GUI looks and shows it to the user.
        """
        # This is the main layout.
        main_layout = QtGui.QVBoxLayout(self)

        # This is the line edit.
        self.surface_name = QtGui.QLineEdit()

        # These are the buttons.
        btn_01 = QtGui.QPushButton('alTriPlanar')
        btn_01.setObjectName('triplanar')
        btn_01.clicked.connect(self.connect_to_logic)

        btn_02 = QtGui.QPushButton('Edge Wear')
        btn_02.setObjectName('edge')
        btn_02.clicked.connect(self.connect_to_logic)

        btn_03 = QtGui.QPushButton('Dust')
        btn_03.setObjectName('dust')
        btn_03.clicked.connect(self.connect_to_logic)

        btn_04 = QtGui.QPushButton('alSurface')
        btn_04.setObjectName('alSurf')
        btn_04.clicked.connect(self.connect_to_logic)

        # This adds the buttons to the layouts.
        main_layout.addWidget(self.surface_name)
        main_layout.addWidget(btn_04)
        main_layout.addWidget(btn_01)
        main_layout.addWidget(btn_02)
        main_layout.addWidget(btn_03)

        # This is the main window.
        self.setGeometry(300, 300, 150, 150)
        self.setWindowTitle('Surface Builder')
        self.show()

    def connect_to_logic(self):
        """
        This function calls the appropriate function in the logic when a button is clicked
        :return:
        """
        sender = self.sender()
        if not self.surface_name.text():
            surface_name = None
        else:
            surface_name = self.surface_name.text()

        sbl = BuildShader(surface_name)
        if sender.objectName() == 'triplanar':
            sbl.al_triplanar()
        elif sender.objectName() == 'edge':
            sbl.edge_wear()
        elif sender.objectName() == 'dust':
            sbl.create_dust()
        elif sender.objectName() == 'alSurf':
            sbl.create_alsurface()
