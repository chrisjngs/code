#!/usr/bin/env python
# SETMODE 777

# ----------------------------------------------------------------------------------------#
# ------------------------------------------------------------------------------ HEADER --#

"""
:author:
    Chris Narro

:synopsis:
    A one line summary of what this module does.

:description:
    This should create a file browser to select the file that should be loaded into a newly
    created arnold stand-in. After the file is selected, the full filepath should be
    assigned to the stand-in. Once assigned, the stand-in should be set to shaded and then
    have the transform name changed to the file name minus the extension. For instance,
    the file path is c://path/to/file/scroll.ass, then the transform for the new
    stand-in should be scroll_001.


    After everything is created, I would like to get rid of the file browser from this
    and move it to the gui file. I would also like to have the gui load all of the files
    in a project as thumbnails for easy browsing.
    Look at personal_pipeline/asset_loader/asset_loader_gui.py for how the gui could look.

:applications:
    Any applications that are required to run this script, i.e. Maya.

:see_also:
    Any other code that you have written that this module is similar to.

"""

# ----------------------------------------------------------------------------------------#
# ----------------------------------------------------------------------------- IMPORTS --#

# Built-in and Third Party
import maya.cmds as cmds

# Modules That You Wrote

# ----------------------------------------------------------------------------------------#
# --------------------------------------------------------------------------- FUNCTIONS --#

# ----------------------------------------------------------------------------------------#
# ----------------------------------------------------------------------------- CLASSES --#

class SetDress(object):
    """


    """

    def __init__(self):
        """

        """

    def create_standin(self):
        """
        This creates a blank arnold stand-in
        :return:
        """

    def load_asset(self):
        """
        This takes a filepath and assigns it into the newly created arnold stand-in.
        :return:
        """

    def run_tool(self):
        """
        This runs the tool
        :return:
        """


