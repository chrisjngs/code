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

:see_also:
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
#import personal_pipeline.common.json_management as jm
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

    def build_path(self, project=None, asset=None):
        """
        This function builds a folder path for the given project, asset, discipline, and
        software.
        """

        if not project:
            print("No project specified")
            return
        if not asset:
            print("No asset specified")
            return
        temp_base = "c://Users//chris//code//personal_pipeline//new_project"
        final_path = "%s//%s//assets//%s//"%(temp_base, project, asset)
        disciplines = ["Model","Surface", "Rig"]
        mod_soft = ["MAYA","ZBRUSH","EXPORTS"]
        surf_soft = ["SUB_PAINT", "SUB_DESIGN", "MAYA", "PHOTOSHOP", "TEXTURES"]
        rig_soft = ["MAYA", "EXPORTS"]
        path_list = []

        for disc in disciplines:
            if disc == "Model":
                for soft in mod_soft:
                    path_list.append("%s%s//%s"%(final_path,disc,soft))
            elif disc == "Surface":
                for soft in surf_soft:
                    path_list.append("%s%s//%s" % (final_path, disc, soft))
            elif disc == "Rig":
                for soft in rig_soft:
                    path_list.append("%s%s//%s" % (final_path, disc, soft))

        for path in path_list:
            print path
                #print path_list



        return

    def build_notes(self, filepath=None, note=None):
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

        if os.path.exists(filepath):
            print("The file already exists. Updating file....")
            #json.dumps(['foo', {'bar': ('baz', None, 1.0, 2)}])
            new_data = {}
            self.update_json(filepath)


        return

    def write_json(self, filepath=None, data=None):
        """
        This writes data to a json file.
        """
        if not data:
            print ("No data was provided, exiting the write.")
            return

        with open(filepath, "w") as f:
            json.dump(data, f, indent=4)
    def load_json(self, filepath=None):
        """
        Loads the data from an existing .json file.
        """
        with open(filepath, "r") as f:
            existing_data = json.load(f)

        return existing_data

    def update_json(self, filepath=None, new_data=None):
        """
        Updates an existing json file.
        """
        if not new_data:
            print "No new data was provided, exiting the .json update."
            return

        existing_data = self.load_json(filepath)

        # If the data in the existing json is a dict, update with the new information.
        if isinstance(existing_data, dict):
            existing_data.update(new_data)
            self.write_json(filepath, existing_data)
        # If the data in the existing json is a list, append the new information.
        elif isinstance(existing_data, list):
            existing_data.append(new_data)
            self.write_json(filepath, existing_data)

        if not filepath:
            return False

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


note_path = "C://Users//chris//Desktop//version_up//new_folder//asset_notes.json"
bs = BuildStructure()

#bs.build_notes(filepath=note_path)
#bs.update_json(note_path, new_data=False)
bs.build_path(project="Test_Project", asset="TestAsset")