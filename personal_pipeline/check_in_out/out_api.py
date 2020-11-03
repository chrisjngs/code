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

    def check_out(self):
        """
        This is the function that will start the check out process.
        :return:
        """

        outFile = ca.check_asset_path()



        if ca.check_asset_path():

            print "The asset was provided."