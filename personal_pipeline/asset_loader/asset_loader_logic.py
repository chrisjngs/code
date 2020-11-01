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

# Modules That You Wrote

#----------------------------------------------------------------------------------------#
#--------------------------------------------------------------------------- FUNCTIONS --#

#----------------------------------------------------------------------------------------#
#----------------------------------------------------------------------------- CLASSES --#

class AssetLoad(object):

    def __init__(self):
        """

        """

    def load_asset(self, path = None,
                   project = None,
                   asset = None,
                   discipline = None,
                   version = None):
        """
        This function loads a given maya file. The function can either load an exact maya
        file that is given through the path variable, or can be modular by given parts of
        a file path.

        :param path: An exact path to a maya file to load.
        :type: str

        :param project: The project that the asset belongs too.
        :type: str

        :param asset: The asset to load.
        :type: str

        :param discipline: The desired discipline of the asset.
        :type: str

        :param version: The version of the asset to load.
        :type: str

        :return:
        """
        print "\n\n\n\n\n\n\n\n\n\n\n\n"
        initialPath = "A:\\Chris\\_CurrentProject"


        if not path:
            if not version or int(version) == 0:
                #print "loading asset at:\n%s\\%s\\Assets\\%s\\%s\\MAYA\\%s.ma"%\
                      #(initialPath, project, asset, discipline, asset)
                assetPath = "%s\\%s\\Assets\\%s\\%s\\MAYA\\%s.ma"%\
                            (initialPath, project, asset, discipline, asset)

            else:
                #print "loading asset version at:\n" \
                  #"%s\\%s\\Assets\\%s\\%s\\MAYA\\versions\\%s_%s.ma"%\
                      #(initialPath, project, asset, discipline, asset, version)

                assetPath = "%s\\%s\\Assets\\%s\\%s\\MAYA\\versions\\%s_%s.ma"%\
                            (initialPath, project, asset, discipline, asset, version)

        else:
            #print "Loading asset at given path:\n%s"%path
            assetPath = path

        #print "\n\n\n\nOpening file at %s"% assetPath
        cmds.file(assetPath, open = True, force = True)
