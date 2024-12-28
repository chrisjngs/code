#!/usr/bin/env python
#SETMODE 777

#----------------------------------------------------------------------------------------#
#------------------------------------------------------------------------------ HEADER --#

"""
:author:
    Chris Narro

:synopsis:
    Creates a gui for the import of published assets

:description:
    A detailed description of what this module does.

:applications:
    Maya

:see_also:
    Any other code that you have written that this module is similar to.

"""

#----------------------------------------------------------------------------------------#
#----------------------------------------------------------------------------- IMPORTS --#

# Built-in and Third Party
from PySide2 import QtGui, QtWidgets, QtCore
from maya import OpenMayaUI as omui
from shiboken2 import wrapInstance
import os

# Modules That You Wrote
import personal_pipeline.publish_asset.export as exp
#reload(exp)

#----------------------------------------------------------------------------------------#
#--------------------------------------------------------------------------- FUNCTIONS --#
def get_maya_window():
    """
    Gets a pointer to the Maya window.
    """
    maya_main_window_ptr = omui.MQtUtil.mainWindow()
    return wrapInstance(long(maya_main_window_ptr), QtWidgets.QWidget)

#----------------------------------------------------------------------------------------#
#----------------------------------------------------------------------------- CLASSES --#
class AssetLoader(QtWidgets.QDialog):
    """
    This makes a layout
    """

    def __init__(self):
        QtWidgets.QDialog.__init__(self, parent=get_maya_window())
        self.type_obj = None
        self.type_abc = None
        self.type_ass = None
        self.type_fbx = None
        self.overwrite = None

    def init_gui(self):
        """
        This method builds and displays the GUI
        """
        # Make a layout.
        main_vb = QtWidgets.QVBoxLayout(self)

        #Create a button to publish with the indicated settings
        btn_import = QtWidgets.QPushButton('Publish Asset')
        btn_import.setAccessibleName("Publish")

        # Make a divider line.
        line = QtWidgets.QFrame()
        line.setFrameStyle(line.HLine)

        #Create 4 different radial buttons to determine what type of file will be exported
        pub_type = QtWidgets.QGroupBox()
        self.type_obj = QtWidgets.QRadioButton("obj")
        self.type_fbx = QtWidgets.QRadioButton("fbx")
        # Commented out the option for ABC since logic function doesn't work
        #self.type_abc = QtWidgets.QRadioButton("abc")
        self.type_ass = QtWidgets.QRadioButton("ass")

        self.smooth = QtWidgets.QCheckBox("smooth")
        self.overwrite = QtWidgets.QCheckBox("Overwrite")

        # Add radio buttons to the group box
        pub_type_layout = QtWidgets.QHBoxLayout(pub_type)
        pub_type_layout.addWidget(self.type_obj)
        pub_type_layout.addWidget(self.type_fbx)
        # Commented out the option for ABC since logic function doesn't work
        #pub_type_layout.addWidget(self.type_abc)
        pub_type_layout.addWidget(self.type_ass)



        # Connect the button to the function to publish with indicated settings
        btn_import.clicked.connect(self.run_tool)

        vbox_01 = QtWidgets.QVBoxLayout()

        vbox_01.addWidget(pub_type)
        vbox_01.addWidget(line)

        hbox_01 = QtWidgets.QHBoxLayout()

        hbox_01.addWidget(self.smooth)
        hbox_01.addWidget(self.overwrite)
        hbox_01.addWidget(btn_import)

        vbox_01.addLayout(hbox_01)
        main_vb.addLayout(vbox_01)

        self.setFixedSize(400, 200)
        self.setWindowTitle("Asset Loader")
        self.show()

    def run_tool(self):
        """
        Passes the values to the export logic to publish the selected asset
        :return:
        """
        publish = exp.Export()

        smoothing = False
        versioning = True

        if self.smooth.isChecked():
            smoothing = True

        if self.overwrite.isChecked():
            versioning = False

        if self.type_obj.isChecked():
            publish.publish(obj=True)
        elif self.type_fbx.isChecked():
            publish.publish(fbx=True)
        # Commented out the option for ABC since logic function doesn't work
        #elif self.type_abc.isChecked():
            #publish.publish(abc=True)
        elif self.type_ass.isChecked():
            publish.publish(smooth=smoothing, version=versioning, ai=True)
        else:
            print "No file type indicated, select one of the options before publishing"
