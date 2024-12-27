#!/usr/bin/env python
# SETMODE 777

# ----------------------------------------------------------------------------------------#
# ------------------------------------------------------------------------------ HEADER --#

"""
:author:
    Chris Narro

:synopsis:
    Creates a gui for the shader creation tool.

:description:
    This script runs the logic for the GUI for the shader network creation tool.

:applications:
    Any applications that are required to run this script, i.e. Maya.

:see_also:
    Any other code that you have written that this module is similar to.

"""

# ----------------------------------------------------------------------------------------#
# ----------------------------------------------------------------------------- IMPORTS --#

# Built-in and Third Party
import maya.cmds as cmds
from PySide2 import QtCore, QtGui, QtWidgets
from PySide2.QtCore import *
from PySide2.QtWidgets import *
from maya import OpenMayaUI as omui
from shiboken2 import wrapInstance
# Modules That You Wrote
import artist_tools.surface_tools.create_shader.create_ai_standard as cai
reload(cai)
# ----------------------------------------------------------------------------------------#
# --------------------------------------------------------------------------- FUNCTIONS --#
def get_maya_window():
    """
    Gets a pointer to the Maya window.
    """
    maya_main_window_ptr = omui.MQtUtil.mainWindow()
    return wrapInstance(long(maya_main_window_ptr), QtWidgets.QWidget)
# ----------------------------------------------------------------------------------------#
# ----------------------------------------------------------------------------- CLASSES --#

class ShaderGUI(QtWidgets.QDialog):
    """

    """

    def __init__(self):
        """

        """
        QtWidgets.QDialog.__init__(self, parent=get_maya_window())
        self.object_list = None
        self.shader_list = None

        #self.model = QStandardItemModel()

        self.create_shader_btn = None
        self.shader_name = None

        self.diff_cb = None
        self.spec_cb = None
        self.metal_cb = None
        self.rough_cb = None
        self.opac_cb = None
        self.bump_cb = None
        self.norm_cb = None
        self.subs_cb = None
        self.disp_cb = None


    def init_gui(self):
        """

        :return:
        """
        # Make a layout.
        main_vb = QtWidgets.QVBoxLayout(self)

        # List portion of the gui
        self.object_list = QtWidgets.QListWidget()
        #self.object_list.setModel(QtGui.QStandardItemModel())
        object_label = QtWidgets.QLabel("Existing Objects")
        reload_btn = QtWidgets.QPushButton("Refresh Object List")
        assign_btn =QtWidgets.QPushButton("Assign Shader")
        self.shader_list = QtWidgets.QListWidget()
        shader_label = QtWidgets.QLabel("Existing Shaders")

        # Add information to lists.
        self.update_obj_list()
        self.update_shader_list()

        # vbox_03 portion of the gui
        self.create_shader_btn = QtWidgets.QPushButton("Create Shader")
        shader_type = QtWidgets.QComboBox()
        shader_type.addItem("aiStandardSurface")
        label_003 = QtWidgets.QLabel("Shader Name")
        self.shader_name = QtWidgets.QLineEdit()
        line = QtWidgets.QFrame()
        line.setFrameStyle(line.HLine)
        grid = QtWidgets.QGridLayout()

        # Texture options
        self.diff_cb = QtWidgets.QCheckBox("Diffuse")
        self.spec_cb = QtWidgets.QCheckBox("Specular")
        self.metal_cb = QtWidgets.QCheckBox("Metal")
        self.rough_cb = QtWidgets.QCheckBox("Rough")
        self.opac_cb = QtWidgets.QCheckBox("Opacity")
        self.bump_cb = QtWidgets.QCheckBox("Bump")
        self.norm_cb = QtWidgets.QCheckBox("Normal")
        self.subs_cb = QtWidgets.QCheckBox("SSS")
        self.disp_cb = QtWidgets.QCheckBox("Disp")

        # Set some default values
        self.diff_cb.setChecked(True)
        self.rough_cb.setChecked(True)
        self.norm_cb.setChecked(True)

        self.shader_name.setPlaceholderText("aiStandardSurface")

        hbox_01 = QtWidgets.QHBoxLayout()
        vbox_01 = QtWidgets.QVBoxLayout()
        vbox_02 = QtWidgets.QVBoxLayout()
        vbox_03 = QtWidgets.QVBoxLayout()

        # Add all the checkboxes
        grid.addWidget(self.diff_cb, 0,0)
        grid.addWidget(self.spec_cb, 0,1)
        grid.addWidget(self.metal_cb, 0,2)

        grid.addWidget(self.rough_cb,1,0)
        grid.addWidget(self.opac_cb,1,1)
        grid.addWidget(self.bump_cb,1,2)

        grid.addWidget(self.norm_cb,2,0)
        grid.addWidget(self.subs_cb,2,1)
        grid.addWidget(self.disp_cb,2,2)

        # Add items to vbox_01
        vbox_01.addWidget(object_label)
        vbox_01.addWidget(reload_btn)
        vbox_01.addWidget(self.object_list)
        vbox_01.addWidget(assign_btn)

        # Add items to vbox_02
        vbox_01.addWidget(shader_label)
        vbox_01.addWidget(self.shader_list)

        # Add items to vbox_03
        vbox_03.addWidget(self.create_shader_btn)
        vbox_03.addWidget(shader_type)
        vbox_03.addWidget(line)
        vbox_03.addWidget(label_003)
        vbox_03.addWidget(self.shader_name)
        #vbox_03.addWidget(line)
        vbox_03.addLayout(grid)

        # Connect buttons to logic.
        self.create_shader_btn.clicked.connect(self.run_create)
        reload_btn.clicked.connect(self.update_obj_list)

        hbox_01.addLayout(vbox_01)
        hbox_01.addLayout(vbox_02)

        hbox_01.addLayout(vbox_03)

        main_vb.addLayout(hbox_01)

        #self.setFixedSize(1400, 800)
        self.setWindowTitle("Shader Network")
        self.show()

    def run_create(self):
        """

        :return:
        """
        #print "create Shader button pressed"
        shader = cai.CreateShader()
        name = self.shader_name.displayText()

        shader.create_shader(shadename=name)

        if self.diff_cb.isChecked():
            shader.diffuse_texture(name)
        #if self.spec_cb_cb.isChecked():
            #shader.specular_texture(name)
        #if self.metal_cb.isChecked():
            #shader.metal_texture(name)
        if self.rough_cb.isChecked():
            shader.rough_texture(name)
        if self.norm_cb.isChecked():
            shader.normal_texture(name)
        if self.opac_cb.isChecked():
            shader.opacity_texture(name)
        if self.subs_cb.isChecked():
            shader.sss_texture(name)
        if self.bump_cb.isChecked():
            shader.bump_texture(name)
        if self.disp_cb.isChecked():
            shader.displace_texture(name)

        self.update_shader_list()

    def update_obj_list(self):
        """

        :return:
        """
        self.object_list.clear()
        objects = cmds.ls(dag=1, g=1)

        for name in objects:
            #print "item '%s' added" % item
            item = QListWidgetItem(name)
            self.object_list.addItem(item)

    def update_shader_list(self):
        """

        :return:
        """
        self.shader_list.clear()
        shaders = cmds.ls(mat=1)

        for name in shaders:
            #print "item '%s' added" % item
            item = QListWidgetItem(name)
            self.shader_list.addItem(item)
