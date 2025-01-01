#!/usr/bin/env python
#SETMODE 777

#----------------------------------------------------------------------------------------#
#------------------------------------------------------------------------------ HEADER --#

"""
:author:
    Chris Jennings

:synopsis:
    Versions up the active Maya file

:description:
    A detailed description of what this module does.

:applications:
    Maya

see_also:
    Any other code that you have written that this module is similar to.

"""

#----------------------------------------------------------------------------------------#
#----------------------------------------------------------------------------- IMPORTS --#

# Built-in and Third Party
import os
import json
import datetime

# This will be used to offload the more intensive parts of the folder gathering logic
# to an additional thread.
import threading


# Modules That You Wrote
import personal_pipeline.common.json_management as jman
#reload(jman)
#----------------------------------------------------------------------------------------#
#--------------------------------------------------------------------------- FUNCTIONS --#


#----------------------------------------------------------------------------------------#
#----------------------------------------------------------------------------- CLASSES --#

class BuildStructure:
    """
    This class holds the logic to create the folder structure for a given asset.
    The final path structure should look like this:
    //path/to/network/currentProjects/PROJECTNAME/Assets/Work/ASSETNAME/Model/Maya
    """
    def __init__(self):
        """

        """
        self.server_path = "//192.168.1.100"

        self.project_name = None
        self.asset_name = None
        self.discipline = None
        self.software = None

        self.project_path = None
        self.asset_path = None
        self.disc_path = None
        self.soft_path = None

    def get_project(self, proj=None):
        """
        Gets passed a value and then checks that it is a valid project path.
        """

        return

    def get_asset(self, asset=None):
        """
        Gets passed a value and then checks that it is a valid asset path.
        """

        return

    def get_discipline(self, disc=None):
        """
        Gets passed a value and then checks that it is a valid discipline path.
        """

        return

    def get_software(self, soft=None):
        """
        Gets passed a value and then checks that it is a valid software path.
        """

        return

    def create_folder(self, path=None):
        """
        This creates a folder at the provided path.

        :param path: The path that will be created.
        """
        # Check to make sure that a path value was given.
        if not path:
            raise ValueError("The 'create_folder' function didn't receive a valid path.")

        # If the given path isn't an existing directory, then make it.
        if not os.path.isdir(path):
            os.mkdir(path)
            print("created, test")

        return

    def build_path(self):
        """
        This function builds a folder path for the given project, asset, discipline, and
        software.
        """

        return

    def build_notes(self, filepath=None, note=None, discipline=None, completed=False):
        """
        This function builds the notes json file for each new asset.
        """
        time = datetime.datetime.now()
        formatted_time = time.strftime("%d-%m-%Y %H:%M:%S")

        # If there isn't already a json file, then create it and fill it in with the
        # starting_data.
        if not os.path.exists(filepath):
            starting_data = {
                "timestamp": "%s" % formatted_time,
                "discipline": "Model",
                "note": "No notes yet. Use the field above to add a note",
                "completed": False
            }
            with open(filepath, 'w') as f:
                json.dump(starting_data, f, indent=4)

            return

        # If no disciple was specified, assign the note to general.
        if not discipline:
            discipline = "General"

        if not note:
            print("No note was provided, cannot build note file without note to add.")
            return False

        if not isinstance(note, str):
            print("The given note isn't a string, converting to string.")
            note = str(note)

        if os.path.exists(filepath):
            print("The file already exists. Updating file....")
            new_data = {
                "timestamp": "%s" % formatted_time,
                "discipline": discipline,
                "note": note,
                "completed": completed
            }
            jman.append_json(filepath, new_data)
        return

    def update_spreadsheet(self):
        """
        Adds each new asset to the Google Sheet used for asset tracking.
        """

        return

    def run_tool(self, project=None, asset=None, disc=None, software=None):
        """
        The tool starts here, checks that everything has been provided and then sends
        the variables out to make sure they are valid before building the path for each
        asset given.
        """

#bs = BuildStructure()
#bs.build_notes(filepath="Z://code//personal_pipeline//new_project//asset_notes.json",
#               note="New note.", discipline="Model")

jman.update_json(filepath="Z://code//personal_pipeline//new_project//asset_notes.json",
                 note="New note 2.", key="completed", new_value=False)