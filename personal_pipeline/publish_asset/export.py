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
import os
import shutil
import pymel.core as pm

# Modules That You Wrote

#----------------------------------------------------------------------------------------#
#--------------------------------------------------------------------------- FUNCTIONS --#

#----------------------------------------------------------------------------------------#
#----------------------------------------------------------------------------- CLASSES --#

class Export(object):

    def __init__(self):
        """

        """
        self.curVersion = None
        self.assetPath = None
        self.publishShapes = None
        self.curAsset = None
        self.fileDirectory =None
        self.exportedFile = None
        self.version = True

    def create_folder(self, dirpath=None):
        """
        This function creates a folder structure at the specific path.
        :param dirpath:
        :return:
        """
        folder = dirpath
        # Checks to make sure the given path is a file.
        isFile = folder.split("/")
        # If the given path is a file, get the folder it's in.
        if "." in isFile[-1]:
            folder = os.path.dirname(dirpath)

        # If the folder does not exist, then make it.
        if not os.path.isdir(folder):
            os.makedirs(folder)
        return True

    def export_obj(self, assetPath=None):
        """
        This function exports the selected shapes as a .obj file
        :return:
        """
        # Sets the filepath based on the passed file path and asset name.
        self.exportedFile = "%s//EXPORTS//Published//%s.obj"%(assetPath, self.curAsset)

        if self.create_folder(self.exportedFile):
            if self.version_export(self.exportedFile, "obj"):
                exportedFile = cmds.file(self.exportedFile, pr=1, typ="OBJexport", es=1, force=True,
                            op="groups=0; ptgroups=0; materials=0; smoothing=1; normals=1")

        print "\n.obj published to:\n%s"%self.exportedFile
        return self.exportedFile

    def export_alembic(self, assetPath = None):
        """
        This function exports the selected shapes as a .abc file
        :return:
        """
        selectedObject = cmds.ls(sl=1)
        start = str(0)
        end = str(0)
        root = "-root Base"#%selectedObject
        print root
        self.exportedFile = "%s//EXPORTS//Published//%s.abc" % (assetPath, self.curAsset)
        print self.exportedFile

        command = "-frameRange " + start + " " + end + " -uvWrite -worldSpace " + root + " -file " + self.exportedFile
        print "\n\n\n%s\n\n\n"%command
        cmds.AbcExport(j=command)

        return self.exportedFile

    def export_fbx(self, assetPath = None):
        """
        This function exports the selected shapes as a .fbx file
        :return:
        """
        # Sets the filepath based on the passed file path and asset name.
        self.exportedFile = "%s//EXPORTS//Published//%s.fbx" % (assetPath, self.curAsset)

        # If the fbxmaya plugin is not loaded, then load it.
        if not cmds.pluginInfo("fbxmaya", query=True, loaded=True):
            pm.loadPlugin("fbxmaya")

        if self.create_folder(self.exportedFile):
            if self.version_export(self.exportedFile, "fbx"):
                exportedFile = pm.mel.FBXExport(f=self.exportedFile)

        print "\n.fbx published to:\n%s"%self.exportedFile
        return self.exportedFile

    def export_arnold(self, assetPath = None):
        """
        This function exports the selected shapes as a .ai file
        :return:
        """
        # Exports the selected shapes to a aiStandIn file
        self.exportedFile = "%s//EXPORTS//Published//%s.ass"%(assetPath, self.curAsset)
        #cmds.arnoldExportAss(filename=self.exportedFile, selected=True)
        #cmds.arnoldExportAss(filename="C:/Users/chris/Desktop/OfflineWork/testFolder/zzTestAsset_Scripted.ass",
        #    selected=True)
        if self.create_folder(self.exportedFile):
            if self.version:
                if self.version_export(self.exportedFile, "ass"):
                    cmds.arnoldExportAss(filename=self.exportedFile, selected=True)
            else:
                cmds.arnoldExportAss(filename=self.exportedFile, selected=True)


        #print ".ai exporter doesn't work yet, try again another time. 08-10-20"
        return self.exportedFile

    def get_asset(self):
        """
        This function gets the publish path for the active asset.

        :return cur_file: The file path of the current maya file
        :type: str
        """
        tempList = []
        cur_file = cmds.file(query=True, location=True)

        # Takes the current file path and splits it out by directory
        self.curAsset = cur_file.split("/")
        # Takes the last entry in the list which is the maya file.
        self.curAsset = self.curAsset.pop()
        # Splits the file extension off of the asset
        tempList = self.curAsset.split(".")
        # Re-assigns the curAsset to the first index, which is just the asset name without
        # a file extension.
        self.curAsset = tempList[0]

        return str(cur_file)

    def render_smooth(self, selection = None):
        """

        :param selection: The shapes that will get smoothed at rendertime in Arnold
        :type: list

        :return:
        """

        if not selection:
            selection = self.publishShapes

        for item in selection:
            shape = cmds.listRelatives(item, s=True)

            if cmds.getAttr("%s.aiSubdivType" % shape[0]) == 1:
                pass
            else:
                cmds.setAttr("%s.aiSubdivType" % shape[0], 1)
                cmds.setAttr("%s.aiSubdivIterations" % shape[0], 2)

    def version_export(self, assetPath=None, extension=None):
        """
        This function versions the published export by duplicating the old publish into
        a versions folder before exporting a new version.

        :return:
        """
        # Checks to see if there is a version of the publish already exported.
        if os.path.isfile(assetPath):
            # If there is a version folder, check the versions inside it.
            assetPath = self.get_directory(assetPath)
            versionFolder = assetPath+"//versions"
            # If there is a versions folder, find the biggest version inside it
            if not os.path.isdir(versionFolder):
                self.create_folder(assetPath + "//versions")
                self.curVersion = 000

            versions_list = os.listdir(versionFolder)
            versions = []
            # If there is nothing in the versions folder, then set the version to 000
            if not versions_list:
                self.curVersion = 000
            # else find the biggest version of the publish and store it in
            # self.curVersion
            else:
                for file in versions_list:
                    remove_ext = file.replace(".", "_")
                    split_version = remove_ext.split("_")
                    for item in split_version:
                        if item.isdigit():
                            versions.append(item)
                if versions:
                    self.curVersion = max(versions)

            # Copy the published export to the versions folder and rename it.
            shutil.copy(self.exportedFile, versionFolder)
            # store the old version of the publish
            oldVersion = "%s//%s.%s"%(versionFolder,
                                      self.curAsset,
                                      extension)

            # Changes the version attribute to string then sets it to be three digits.
            version = str(self.curVersion)
            turn_to_int = int(version) + 1
            version = str(turn_to_int)
            formated_version = version.rjust(3, "0")

            # Store the path to the new publish version
            newVersion = "%s//%s_%s.%s"%(versionFolder,
                                      self.curAsset,
                                      formated_version,
                                      extension)

            # Rename the new publish to have the correct version suffix.
            os.rename(oldVersion, newVersion)
        else:
            self.curVersion = 000

        return True

    def get_directory(self, path=None):
        """
        This function gets the directory of the provided path.

        :param path: The path to a file that you want to get the directory.
        :type: str

        :return: file_directory
        :type:str
        """

        #print "\nThe initial path is:\n%s"%path

        dirPath = os.path.abspath(os.path.join(path, os.pardir))
        dirPath = dirPath.replace("\\", "//")

        return dirPath

    def publish(self, smooth=False, version=True, asset=None, obj=False, abc=False, fbx=False, ai=False):
        """
        This is the starting function that calls the other functions.

        :param smooth: Flag if the published shapes should get smoothed at rendertime in Arnold
        :type: bool

        :param version: Flag if the puplish should version up
        :type: bool

        :param asset: A provided asset to publish outside of the given Maya file.
        :type: str

        :param obj: Boolean argument to export out a .obj file
        :type: bool

        :param abc: Boolean argument to export out a .abc file
        :type: bool

        :param fbx: Boolean argument to export out a .fbx file
        :type: bool

        :param ai: Boolean argument to export out a .ai file
        :type: bool

        :return:
        """
        print "\n\n\n\n\n\n\n\n\n\n\n"
        originalSelection = cmds.ls(sl=1)
        self.assetPath = self.get_asset()
        # check to see if publish should overwrite
        if not version:
            self.version = version
        #print "get_asset ends with:\n%s\n" %self.get_asset()
        self.fileDirectory = self.get_directory(self.assetPath)
        self.fileDirectory = self.get_directory(self.fileDirectory)

        if not asset:
            self.publishShapes = cmds.ls(sl=1)
            if not self.publishShapes:
                #print "Nothing was selected, publishing the asset's parent node."
                cmds.select(self.curAsset)
                self.publishShapes = cmds.ls(sl=1)
        else:
            print "Publishing the given asset through batch"

        if smooth:
            self.render_smooth(selection=self.publishShapes)

        if obj:
            self.export_obj(self.fileDirectory)
        if abc:
            self.export_alembic(self.fileDirectory)
        if fbx:
            self.export_fbx(self.fileDirectory)
        if ai:
            self.export_arnold(self.fileDirectory)

        print "\nFile(s) exported to %s//EXPORTS//Published"%self.fileDirectory
        cmds.select(originalSelection)
