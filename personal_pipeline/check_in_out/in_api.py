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
import personal_pipeline.check_in_out.common_api as ca

#----------------------------------------------------------------------------------------#
#--------------------------------------------------------------------------- FUNCTIONS --#

#----------------------------------------------------------------------------------------#
#----------------------------------------------------------------------------- CLASSES --#

class CheckIn(object):
    """

    """
    def __init__(self):
        """

        """

    def start(self, asset=None):
        """
        This function starts the check in process.

        :param asset: The asset that will be checked in.
        :type: str, filepath.

        :return:
        """
        if not asset:
            cmds.warning("There was no asset pathed to the check-in tool, using the "
                         "current asset.")
        if ca.check_asset_path(asset):
            print "The asset path was provided."