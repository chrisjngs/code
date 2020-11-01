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

# Modules That You Wrote
import personal_pipeline.check_in_out.common_api as ca

#----------------------------------------------------------------------------------------#
#--------------------------------------------------------------------------- FUNCTIONS --#

#----------------------------------------------------------------------------------------#
#----------------------------------------------------------------------------- CLASSES --#

class CheckOut(object):
    """

    """
    def __init__(self):
        """
        
        """
    def start(self):
        """
        This is the function that will start the check out process.
        :return:
        """

    def check_folder_struct(self):
        """
        This function checks the folder structure of the given asset. It should store
        the structure in a dictionary that can be used when creating the local folder
        structure.
        :return:
        """

    def create_folder_struct(self):
        """
        This function creates the folder structure that matches the folder structure for
        the  on selected asset the server.

        For example:

        This function is given a dictionary and stores it in the variable 'servDict'.
        This dictionary holds a list with each asset being checked out.

        servDict = {assetName:[
        :return:
        """