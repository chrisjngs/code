#!/usr/bin/env python
#SETMODE 777

#----------------------------------------------------------------------------------------#
#------------------------------------------------------------------------------ HEADER --#

"""
:author:
    Chris Jennings

:synopsis:
    A one line summary of what this module does.

:description:
    A detailed description of what this module does.

:applications:
    Any applications that are required to run this script, i.e. Maya.

:see_also:
    Any other code that you have written that this module is similar to.

"""

#----------------------------------------------------------------------------------------#
#----------------------------------------------------------------------------- IMPORTS --#

# Built-in and Third Party
import maya.cmds as cmds
import maya.mel as mel
# Modules That You Wrote
import personal_pipeline.version_up.version_up as vu

#----------------------------------------------------------------------------------------#
#--------------------------------------------------------------------------- FUNCTIONS --#

#----------------------------------------------------------------------------------------#
#----------------------------------------------------------------------------- CLASSES --#

cvu = vu.VersionControl()

class Assetize(object):

    def __init__(self):
        """

        """
        self.objectsDict = {}

    def move_object(self, objs=None, location=None):
        """

        :param objs: The objects that will be moved.
        :type: list

        :param location: The position the objs will be moved to.
        :type: tuple
        :return:
        """
        # If nothing was passed, then get the current selection.
        if not objs:
            objs = cmds.ls(sl=1)

        # If no location was specified, then move the selection to the origin.
        if not location:
            cmds.move(0,0,0, objs, worldSpace=True)

        # Else, move the objects to the desired location in world space.
        else:
            location = self.objectsDict
            cmds.move(location[objs][0],
                      location[objs][1],
                      location[objs][2],
                      objs,
                      worldSpace=True)

    def get_asset_location(self, objs=None):
        """
        This function gets the current asset location.

        :param objs: The shapes in maya to get the location of.
        :type: list
        :return:
        """
        # Get the location for each indicated object in world space.
        for obj in objs:
            cmds.makeIdentity(apply=True, translate=True)
            mel.eval('performBakeCustomToolPivot 0')
            self.objectsDict[obj] = cmds.xform(obj,
                                               q=1,
                                               translation=True,
                                               worldSpace=True)

    def adjust_pivot(self, objs=None):
        """
        This function moves the pivot of the selected group or object to the center of
        the lowest Y value. aka, the bottom center of the bounding box.

        :param objs: A list of objects that needs their pivot(s) adjusted.
        :type: list
        """
        if not objs:
            objs = cmds.ls(sl=1)

        for obj in objs:
            boundingBox = cmds.xform(obj, boundingBox=True, query=True, worldSpace=True)
            Xval = (boundingBox[3] + boundingBox[0]) / 2
            Yval = boundingBox[1]
            Zval = (boundingBox[5] + boundingBox[2]) / 2

            cmds.xform(obj, pivots=(Xval, Yval, Zval), ws=True)

    def assetize(self, obj=None, project_directory=None):
        """

        :param obj: The objects that will be assetized.
        :type: list

        :param project_directory: The directory path for the assetization.
        :type: str

        :return:
        """
        # If there is a project path that should be used, then use it.
        if project_directory:
            assetPath = project_directory

        # Else, find the current Maya file and start to work backwards from there.
        else:
            assetPath = cvu.get_maya_file()

        # Split the specified filepath into a list and loop through it until you get down
        # to the asset directory.
        
        assetList = assetPath.split("/")
        for asset in assetList:
            # If the last index of the list is the assets folder, then try the one below
            # it.
            if not assetList[-1] == "Assets":
                assetList.pop()
                assetPath = cvu.get_directory(assetPath)
            # Else, put the current asset to be split out, into their own file path.
            else:
                finalPath = "%s//%s//model//MAYA//%s.ma"%(assetPath, obj, obj)
                # Selecting the asset so that the file export selection works on just the
                # specified asset. If you remove this then all asset initially selected
                # will be put into the same Maya file.
                cmds.select(obj)
                cmds.file(finalPath, type="mayaAscii", exportSelected=True)
                cvu.remove_student_warning(finalPath)
                print "the group '%s' as been assetized to:\n%s"%(obj, finalPath)

    def start(self):
        """
        Call this function to assetize the selected groups into the project's folder
        structure. Select groups with corrisponding assets in the project and then call
        this function.
        :return:
        """
        # Get the currently selected groups and their current location in the scene.
        selection = cmds.ls(sl=1)
        self.adjust_pivot(selection)
        self.get_asset_location(selection)
        # For each selected group, move it to the origin and then split it out into it's
        # own Maya scene.
        for sel in selection:
            self.move_object(sel)
            self.assetize(sel)


        print "\n\nAssets exported to individual files," \
              " moving them back to their original locations\n\n"

        # After all selected groups are assetized, move them back to their original places
        for sel in selection:
            self.move_object(sel, self.objectsDict[sel])

        # Re-select the full starting assets.
        cmds.select(selection)



