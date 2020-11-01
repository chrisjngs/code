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
from datetime import datetime

# Modules That You Wrote


#----------------------------------------------------------------------------------------#
#--------------------------------------------------------------------------- FUNCTIONS --#

#----------------------------------------------------------------------------------------#
#----------------------------------------------------------------------------- CLASSES --#
# The log file should look like this:
# Status -- ComputerName -- UserName -- Date/Time
# out -- Sally5 -- Chris -- 10/28/2020/12:43PM
# in -- Sally5 -- Chris -- 10/28/2020/6:53PM
# store the values into dictionaries as keys and values
# lodDict = [status:in], [Computer:Sally5], [User:Chris], [Date:10/28/2020/6:53PM]
def log_file(asset=None, mode=None):
    """
    This function reads and writes the text file to log which file is checked in\out.

    :param asset: a filepath to a given asset file to check-in/out.
    :type: str
    :param mode: Either read or write the text file, expects either a 'w+' or 'r' flag
    :type: str
    :return:

    """
    # If the user didn't provide a mode to view the log in, prompt for them to pass one.
    if not mode:
        print "must provide a mode to work with the log file."
        return False

    # If the user didn't provide an asset to check in/out, do it on the current asset.
    if not asset:
        # Get the current asset and store it as the variable asset
        asset = cmds.file(query=True, location=True)
        # If the file isn't saved, escape the check in/out process.
        if asset == "untitled":
            print "You must save the file before a check in/out can occur."
            return False
        print asset
    
    # Check to see if the log file exists
    asset_dir = os.path.dirname(asset)
    log = asset_dir+"\\status_log.txt"
    status = {}
    if os.path.exists(log):
        print "The asset has a log file."

        if mode == "r":
            #read the file to find if the file is checked out/in
            #store the last line of the txt file in a variable named "status"
            print "Hello."

        elif mode == "w+":
            # Write in the log file
            # Get the status of the check-in/out
            status = mode
            # Get the Computer name
            computer_name = os.environ["COMPUTERNAME"]

            # Get the Username
            userpath = os.path.expanduser("~")
            tmp_path = userpath.split("\\")
            user_name = tmp_path[-1]

            # Get the date and time
            time = datetime.now()

            line = "%s -- %s -- %s -- %s" %(status, computer_name, user_name, time)
            print line


    else:
        # Create the log file and write it as if it was a check out.
        return status[status]

    """
    if status == "in":
        return "in"
    elif status == "out":
        return "out"
    """
def date():
    """
    This function gets the date and time and returns it as a readible string.
    :return:
    """


def move_files():
    """
    This function moves file(s) to and from the server.
    :return:
    """

def store_struct():
    """
    This function creates a Json file that stores the folder structure of each asset
    that is being checked in.out. This json file will be created by looking at the current
    asset

    example:
    The live folder structure is projectName>assets>assetName>model>MAYA>mayafile.ma

    :return:
    """