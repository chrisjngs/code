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
import sys
import shutil
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
def write_log_file(asset=None, mode=None):
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
        sys.exit("Must provide a mode to work with the log file.")

    # If the user didn't provide an asset to check in/out, do it on the current asset.
    if not asset:
        # Get the current asset and store it as the variable asset
        asset = cmds.file(query=True, location=True)
        # If the file isn't saved, escape the check in/out process.
        if asset == "untitled":
            sys.exit("You must save the file before a check in/out can occur.")
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

def check_asset_path(asset=None):
    """
    This function gets the current asset filepath.
    :return:
    """
    if not asset:
        filepath = cmds.file(query=True, location=True)
        return filepath
    else:
        if os.path.isfile(asset):
            filepath = asset
            return filepath
        else:
            errorMessage = ("Error in check_asset_path.\nThe provided file does not "
                            "exist, you must provide a filepath ending with a file."
                            "\nExpected a filepath got: '%s'")%asset
            cmds.error(errorMessage)

def parse_file_path(path=None):
    """
    This function takes a filepath and breaks it into small bite sized pieces that can
    the be used to recreate the path, one folder at a time.

    :param path: The filepath that will be parsed through.
    :type: str, filepath

    :return:
    """
    if not path:
        errorMessage = ("Error in parse_file_path. \nYou must provide a filepath to parse"
                        " through.\nExpected a filepath got: '%s'")%path
        sys.exit(errorMessage)
    splitPath = path.split("\\")
    for entry in splitPath:
        if entry.contains:
            print entry

def write_json(asset=None):
    """
    This function creates a Json file that stores the folder structure of each asset
    that is being checked in/out. This json file will be created by looking at the current
    asset directory and working upward to the project name folder.

    example:
    The live folder structure is projectName>assets>assetName>model>MAYA>mayafile.ma

    :param asset: A passed asset filepath. ex. A:/Chris/_CurrentProjects/moonshop/assets/
    testAsset/model/MAYA/testAsset.ma
    :type: str filepath

    :return: json file
    """
    if not asset:
        cmds.warning("No file was specified, using the current filepath instead.")
        asset = get_asset()

def read_json():
    """
    This function reads the json file that is created in get_asset_folders() and uses it
    to recreate the server folder structure locally or the local folder structure on the
    server.
    :return:
    """

def create_folder(path=None):
    """
    This function creates a folder at the given location.
    :return:
    """
    if not path:
        sys.exit("Error in create_folder. \nNo filepath provided. "
                 "You must provide a directory path to create the folder at.")
    if not os.path.isdir(path):
        newDir = os.makedirs(path)
        return newDir

def copy_files(source=None, destination=None):
    """
    This function moves file(s) from one location to another.

    :param source: The file that should be moved.
    :type: str, filepath

    :param destination: The location the source file should be moved to.
    :type: str, directory

    :return:
    """

    # Converts the provided filepaths to a readable format with the correct slashes.
    destination = readable_filepath(destination)
    source = readable_filepath(source)

    # Checking to make sure a source file was passed.
    if not source:
        sys.exit("You need to specify a file to copy.")
    # Checking to make sure the source variable is a file.
    if not os.path.isfile(source):
        sys.exit("You need to specify a file to copy, not a directory.")
    # Checking to make sure a destination directory was passed.
    if not destination:
        sys.exit("You need to specify where to copy the file to.")
    # Checking to make sure the destination variable is a directory.
    if not os.path.isdir(destination):
        sys.exit("You need to specify a directory to copy the file to.")
    # If the destination variable is a file, then get its directory.
    if os.path.isfile(destination):
        destination = os.path.dirname(destination)

    # Copy the specified file to the destination directory.
    shutil.copy(source, destination)

def readable_filepath(path=None):
    """
    This function converts the slashes in a filepath to be readable by any OS.

    :param path: The filepath to convert.
    :type: str, filepath

    :return final_path: The final converted file_path
    :type: str
    """

    if not path:
        errorMessage = "Error in readable_filepath. No filepath was provided, \nexpected" \
                       "filepath, got: %s"%path
        sys.exit(errorMessage)
    final_path = path.replace("\\", "\\\\")
    return final_path

def check_version(source=None, destination=None):
    """
    This function compairs the version of the local file with that of the server file and
    returns whichever one is newest.

    :param source: The file that is being compaired
    :type: str, filepath

    :param destination: The file that should be compaired to.
    :type: str, filepath
    :return:
    """
    if not source:
        sys.exit("You need to specify a file that needs to be compaired.")
    if not destination:
        sys.exit("You need to specify a file to compair against.")