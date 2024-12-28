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
    A detailed description of what this module does.

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

class UpdatePublish(object):
    """


    """
    def __init__(self):
        """

        """
        self.selection = None


    def get_selection(self):
        """

        :return:
        """
        self.selection = cmds.ls(selection=True)

        if self.selection:
            return self.selection
        else:
            return False

    def varify_node_type(self, shape=None):
        """

        :return:
        """
        if cmds.nodeType(shape) == "transform":
            shape = cmds.listRelatives(shape, shapes=True)
            shape_type = cmds.nodeType(shape)
            shape == shape_type

        #print cmds.nodeType(shape)
        if cmds.nodeType(shape) == "aiStandIn":
            return "aiStandIn"
        elif cmds.nodeType(shape) == "mesh":
            return "mesh"
        else:
            return False

    def update_publishes(self, shapes=None):
        """

        :return:
        """
        if shapes:
            for shape in shapes:
                if self.varify_node_type(shape) == "aiStandIn":
                    publish_path = cmds.getAttr("%s.dso"%shape)
                    cmds.setAttr("%s.dso" % shape, publish_path, type='string')
                elif self.varify_node_type(shape) == "mesh":
                    print "did another thing"
                    # Store the transforms
                    # Store the material(s) assigned to each shape
                    # Delete the shape from the scene
                    # Import the new publish
                    # Assign the transforms from the old version
                    # Assign the material(s) from the old publish            #update only the selected shapes
                print "Updated the selected publishes."

        else:
            #update all aiStandIns in the scene
            stand_ins = cmds.ls(type="aiStandIn")
            for stand_in in stand_ins:
                publish_path = cmds.getAttr("%s.dso" % stand_in)
                cmds.setAttr("%s.dso" % stand_in, publish_path, type='string')
            #print stand_ins
            print "Updated all aiStandIns in the scene."

    def run_tool(self):
        """

        :return:
        """

        if self.get_selection():
            self.update_publishes(self.selection)
        else:
            self.update_publishes()

        print "Tool finished successfully."