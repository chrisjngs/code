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
import shutil

# This will be used to offload the more intensive parts of the folder gathering logic
# to an additional thread.
import threading


# Modules That You Wrote
import personal_pipeline.common.json_management as jman
reload(jman)
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
        self.server_path = "////192.168.4.45//projects/Chris"

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

    def propogate_thumbnail(self, path=None,asset_name=None):
        """
        Propogate the temp thumbnail to each new asset that's created.
        :param path: The path to the new asset directory
        :return:
        """

        orig_thumb = ("C://Users//chris//code//personal_pipeline//create_asset"
                      "//new_thumb.jpg")
        new_thumb = "%s_Thumbnail"%asset

        if os.path.isdir(path):
            shutil.copy(orig_thumb, path)


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
            os.makedirs(path)
            #print("created a folder at: %s"%path)

        return

    def build_path(self, project=None, asset=None):
        """
        This function builds the folder paths for the given project and asset.
        """

        if not project:
            print("No project specified")
            return
        if not asset:
            print("No asset specified")
            return
        if not isinstance(asset, str):
            print(type(asset))
            print("The provided asset was not in string format, please provide only one "
                  "asset when calling this function")
            return


        if os.path.isdir(self.server_path):
            base_path = self.server_path
        else:
            base_path = ("C://Users//chris//Desktop//OfflineWork//Projects")

        #temp_base = "c://Users//chris//code//personal_pipeline//new_project"
        #server_base = "////192.168.4.45//projects//Chris//_CurrentProject"
        asset_path = "%s//%s//Assets//Work//%s"%(base_path, project, asset)
        disciplines = ["Model","Surface","Rig","Renders"]
        mod_soft = ["MAYA","ZBRUSH","EXPORTS"]
        surf_soft = ["SUB_PAINT","SUB_DESIGN","MAYA","PHOTOSHOP","TEXTURES"]
        rig_soft = ["MAYA","EXPORTS"]
        path_list = []

        for disc in disciplines:
            if disc == "Model":
                for soft in mod_soft:
                    path_list.append("%s//%s//%s"%(asset_path,disc,soft))
            elif disc == "Surface":
                for soft in surf_soft:
                    path_list.append("%s//%s//%s" % (asset_path, disc, soft))
            elif disc == "Rig":
                for soft in rig_soft:
                    path_list.append("%s//%s//%s" % (asset_path, disc, soft))
            elif disc == "Renders":
                path_list.append(("%s//%s" % (asset_path, disc)))
                path_list.append(("%s//%s//Captures" % (asset_path, disc)))


        return path_list, asset_path
    def build_notes(self, filepath=None, note=None, discipline=None, completed=False):
        """
        This function builds the notes json file for each new asset.
        """

        time = datetime.datetime.now()
        formatted_time = time.strftime("%d-%m-%Y %H:%M:%S")

        # If there isn't already a json file, then create it and fill it in with the
        # starting_data.
        if not os.path.isfile(filepath):
            starting_data = {
                "timestamp": "%s" % formatted_time,
                "discipline": "General",
                "note": "No notes yet. Use the field above to add a note",
                "completed": False,
                "first_note": True
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

    def run_tool(self, project=None, asset=None):
        """
        The tool starts here, checks that everything has been provided and then sends
        the variables out to make sure they are valid before building the path for each
        asset given.
        """

        if not project:
            print ("No project specified! Please specify a project to create the asset "
                   "for.")
            return False
        if not asset:
            print ("No asset specified! Please provide an asset to create.")
            return False

        paths = self.build_path(project=project, asset=asset)
        #print (paths[1])
        for path in paths[0]:
            #print path
            self.create_folder(path=path)

        # Checking that the correct path is passed to the build_notes function
        note_path = paths[1]
        if os.path.isdir(note_path):
            note_path = "%s//%s_Notes.json"%(paths[1], asset)

        self.build_notes(filepath=note_path)
        print asset
        self.propogate_thumbnail(path=paths[1], asset_name=asset)

bs = BuildStructure()
assets = ["DavyJones"]
for asset in assets:
    bs.run_tool(project="DavyJones",asset=asset)
# # bs.build_notes(filepath="C://Users//chris//Desktop//OfflineWork//Projects//TestProject"
# #                         "//Assets//Work//TestAsset//TestAsset_Notes.json",
# #               note="New note.", discipline="Model")
# note_path = ("C://Users//chris//Desktop//OfflineWork//Projects//TestProject//Assets"
#              "//Work//TestAsset//TestAsset_Notes.json")
# note_value = "No notes yet. Use the field above to add a note"
# jman.update_json(filepath=note_path, note=note_value, key="completed", new_value=True)