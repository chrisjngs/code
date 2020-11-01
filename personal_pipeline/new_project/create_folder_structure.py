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
import inspect
# Modules That You Wrote

#----------------------------------------------------------------------------------------#
#--------------------------------------------------------------------------- FUNCTIONS --#
def createFolderStructure(path=None):
    '''
    This function creates the folder structure for each asset.

    :param path: takes a folder path to create the asset folders in. This folder path
    should already be in the project directory. ex. c://myProject/assets/
    :type: str


    '''

    projectPath = path
    assetList = readAssetList(path)

    modelFolders = ["//MAYA", "//ZBRUSH", "//EXPORTS"]
    surfaceFolders = ["//MAYA", "//SUBSTANCE", "//TEXTURES"]

    for asset in assetList:

        #print "creating folder for %s"%asset

        dailiesFolder = projectPath + "//" + asset + "//dailies"
        os.makedirs(dailiesFolder)

        for folder in modelFolders:
            curFolder = projectPath + "//" + asset + "//model" + folder
            os.makedirs(curFolder)

        for folder in surfaceFolders:
            curFolder = projectPath + "//" + asset + "//surface" + folder
            os.makedirs(curFolder)


def readAssetList(path=None):
    """
    This function reads the information from a json or text file to compile a list of
    assets.

    :param path: A path to a json or text file on disk to read.
    :type: str

    :return: list
    :type: list
    """

    listLocation = path + "\\assetList.txt"
    assetList = []
    with open(listLocation, 'r') as file:
        assetList = file.read().replace('\n','')
    # This recasts the list to have each asset be it's own index.
    assetList = assetList.split("\r")

    return assetList

def start(path=None):
    """
    This function is the starting function that calls the other functions.
    :return:
    """
    # If the user didn't pass a directory path, use the python file location.
    if not path:
        path = os.path.abspath(__file__)
        dir_path = os.path.dirname(path)
        createFolderStructure(dir_path)
    else:
        createFolderStructure(path)
#----------------------------------------------------------------------------------------#
#----------------------------------------------------------------------------- CLASSES --#

