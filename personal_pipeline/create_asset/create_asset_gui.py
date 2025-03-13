#!/usr/bin/env python
#SETMODE 777

#----------------------------------------------------------------------------------------#
#------------------------------------------------------------------------------ HEADER --#

"""
:author:
    Chris Jennings

:synopsis:
    Versions up the active Maya file

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
import personal_pipeline.asset_loader.asset_loader_logic as all

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
