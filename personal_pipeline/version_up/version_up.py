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
import maya.cmds as cmds
import os
import shutil

# Modules That You Wrote

#----------------------------------------------------------------------------------------#
#--------------------------------------------------------------------------- FUNCTIONS --#






#----------------------------------------------------------------------------------------#
#----------------------------------------------------------------------------- CLASSES --#

class VersionControl():
    """
    This Class holds the logic for versioning up a file
    """
    def __init__(self):
        """

        """
        self.cur_version = None
        self.file_directory = None
        self.folder_path = None

    def get_maya_file(self):
        """
        This function returns the file path of either the current Maya session, or of one
        that is passed in by the user using the path parameter.

        :return cur_file: The file path of the current maya file
        :type: str
        """

        cur_file = cmds.file(query=True, location=True)
        return str(cur_file)

    def check_version_folder(self, path=None):
        """
        This function checks to see if the version folder exists. If it does, it returns
        True.

        :param path: The path to the directory that holds the version folder.
        :type: str

        :return: boolean
        :type: bool
        """

        # Append /versions to the path that was provided.
        version_path = self.get_directory(path) + "\\versions"

        # If the version folder is a directory (if it exists) return True, else False.
        if os.path.isdir(version_path):
            #print "finished with check_version_folder"
            return True
        else:
            self.cur_version=000
            #print "finished with check_version_folder"
            return False

    def check_version(self, path=None):
        """
        This function checks to see if there is a versions folder, and if there is, what the
        highest version number is of a specific Maya file. If there is not a versions folder,
        it creates one and sets the version number to 000.

        :param path: The path to the Maya file that you are trying to get the latest version
        of
        :type: str

        :return cur_version: The current version of the Maya file.
        :type: str
        """
        versions_list = os.listdir(self.file_directory+"\\versions")
        versions = []
        for file in versions_list:
            remove_ext = file.replace(".", "_")
            split_version = remove_ext.split("_")
            for item in split_version:
                if item.isdigit():
                    versions.append(item)
        if versions:
            self.cur_version =  max(versions)
        #print "finished with check_version, version is %s"%self.cur_version
        return

    def create_folder(self, path=None, name=None):
        """
        This function creates a folder at a specified file path.

        :param path: The path that the folder should be created at.
        :type: str

        :param name: The name of the folder being created.
        :type: str

        :return folder_path: The newly created folder path.
        :type: str
        """
        self.folder_path = self.file_directory + name
        os.makedirs(self.folder_path)
        #print "finished with create_folder"
        return self.folder_path

    def save_scene(self, version=None, path=None):
        """
        This function copies the current Maya file to the versions folder and increases its
        version number before saving and overwriting the active Maya session.

        :param version: The current version number.
        :type: str

        :param path: The file path to the current Maya version folder.
        :type: str

        :return:
        """
        scene_name = cmds.file(query=True, sceneName=True)
        # Split the file path and the file into different elements.
        split_file_path = scene_name.split("/")
        removed_file = split_file_path.pop()
        removed_file = removed_file.split(".")
        removed_file = removed_file.pop(-2)

        join_file_path = "\\".join(split_file_path)
        final_file_path = join_file_path+"\\versions"

        # Changes the version attribute to string, and then sets it to be three digits.
        version = str(version)
        turn_to_int = int(version)+1
        version = str(turn_to_int)
        formated_version = version.rjust(3, "0")

        new_version = "%s\%s_%s.ma"%( final_file_path,
                                      removed_file,
                                      formated_version)
        # Copy the current Maya file to the versions folder
        shutil.copy(self.get_maya_file(), new_version)

        # Save the maya file.
        new_save = cmds.file(save=True, type="mayaAscii")
        #self.remove_student_warning(new_save)
        #print "finished with save_scene"

    def get_directory(self, path=None):
        """
        This function gets the directory of the provided path.

        :param path: The path to a file that you want to get the directory.
        :type: str

        :return: file_directory
        :type:str
        """
        self.file_directory = os.path.dirname(path)
        return self.file_directory

    def start(self, path=None):
        """
        This is the caller function. Use this to start the version up process. This
        function will call the necessary functions needed in the proper order to version
        up the file.


        :param path: If the you want to version up a specific file, give the file path to
        the file. Include the actual file in the path, not just the directory it's in.
        :type: str

        :return:
        """
        # If the user provided a file path, use that, else find the current maya file.
        if path:
            file_path = path
        else:
            file_path = self.get_maya_file()

        #print "the file_path is %s"%file_path

        # If there is not a versions folder, create one.
        if not self.check_version_folder(file_path):
            #print "there was no versions folder"
            self.create_folder(file_path, "\\versions")
        # If the current version is not 000, find out what it is.
        if not self.cur_version == "000":
            #print "There was a version folder"
            self.check_version(file_path)
        #print self.cur_version
        self.save_scene(self.cur_version)
        print "File versioned up"

    def remove_student_warning(self, filepath=None):
        """
        This function removes the student licensing line from the specified Maya file.
        :param filepath: The exact filepath to the maya file.
        :type: str
        :return:
        """

        if filepath:
            baseFile = open(filepath)
            splitFile = baseFile.readlines()

            origText = """fileInfo "license" "student";"""
            newText = """//fileInfo "license" "student";"""
            new_file_content = ""

            for line in splitFile:
                stripped_line = line.strip()
                new_line = stripped_line.replace(origText, newText)
                new_file_content += new_line + "\n"

            baseFile.close()

            writing_file = open(filepath, "w")
            writing_file.write(new_file_content)
            writing_file.close()