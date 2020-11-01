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
import os
import maya.cmds as cmds
import pymel.core as pm
import maya.mel as mel

# Modules That You Wrote
import personal_pipeline.publish_asset.export as pa

#----------------------------------------------------------------------------------------#
#--------------------------------------------------------------------------- FUNCTIONS --#
pae = pa.Export()

#----------------------------------------------------------------------------------------#
#----------------------------------------------------------------------------- CLASSES --#

class Import(object):

    def __init__(self):
        """

        """
        self.file          = None
        self.curAsset      = None
        self.assetPath     = None
        self.fileDirectory = None
        self.exportedFile  = None

    def import_obj(self, filepath = None):
        """

        :param self:
        :param filepath: The path to the file that should be imported
        :type: str
        :return:
        """
        self.exportedFile = "%s//model//EXPORTS//Published//%s.obj" % (filepath, self.curAsset)
        cmds.file(self.exportedFile, i=True)

        #print self.exportedFile

    def import_fbx(self, filepath=None):
        """

        :param self:
        :param filepath: The path to the file that should be imported
        :type: str
        :return:
        """
        self.exportedFile = "%s//model//EXPORTS//Published//%s.fbx" % (filepath, self.curAsset)

        # If the fbxmaya plugin is not loaded, then load it.
        if not cmds.pluginInfo("fbxmaya", query=True, loaded=True):
            pm.loadPlugin("fbxmaya")


        exportedFile = pm.mel.FBXImport(f=self.exportedFile)

        print self.exportedFile

    def import_alembic(self, filepath=None):
        """
        This function imports a given alembic file in my pipeline.
        :param self:
        :param filepath: The path to the file that should be imported
        :type: str
        :return:
        """
        self.exportedFile = "%s//EXPORTS//Published//%s.abc" % (filepath, self.curAsset)
        cmds.AbcImport(self.exportedFile, mode=open)

    def import_arnold(self, filepath=None):
        """

        :param self:
        :param filepath: The path to the file that should be imported
        :type: str
        :return:
        """
        self.exportedFile = "%s//model//EXPORTS//Published//%s.ai" % (filepath, self.curAsset)
        print self.exportedFile

    def start(self, obj=False, abc=False, fbx=False, ai=False):
        """

        :return:
        """
        if self.curAsset == "unknown":
            print "The current asset is unsaved and unpublished."
            return

        self.assetPath = pae.get_asset()
        self.curAsset = pae.curAsset
        #print "get_asset ends with:\n%s\n" %self.get_asset()
        self.fileDirectory = pae.get_directory(self.assetPath)
        self.fileDirectory = pae.get_directory(self.fileDirectory)
        self.fileDirectory = pae.get_directory(self.fileDirectory)

        if obj:
            self.import_obj(self.fileDirectory)
        if abc:
            self.import_alembic(self.fileDirectory)
        if fbx:
            self.import_fbx(self.fileDirectory)
        if ai:
            self.import_arnold(self.fileDirectory)