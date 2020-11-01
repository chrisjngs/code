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

def component_transfer(source=None, targets=None):
    """
    This function transfers UVs from a source object to a list of objects
    :param source: The object with the UVs to transfer from.
    :type: string
    :param targets: All of the objects that you want to have updated UVs transferred to.
    :type: list
    :return:
    """

    if not source:
        print "Please specify the source object, the one with the UVs."
        return None
    if not targets:
        print "Please select at least one object to have UVs transferred to."
        return None

    for target in targets:
        UVs = cmds.transferAttributes(source, target, transferUVs=2, sampleSpace=4)
        cmds.delete(target, constructionHistory=True)

    print "The operation was completed."

#----------------------------------------------------------------------------------------#
#----------------------------------------------------------------------------- CLASSES --#

