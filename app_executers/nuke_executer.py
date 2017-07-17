#!/usr/bin/env python
#SETMODE 777

#----------------------------------------------------------------------------------------#
#------------------------------------------------------------------------------ HEADER --#

"""
:author:
    Chris Jennings

:synopsis:
    This module holds the logic to launch Nuke and start a render.

:description:
    A detailed description of what this module does.

:applications:
    Nuke.

:see_also:
    N/A

"""

#----------------------------------------------------------------------------------------#
#----------------------------------------------------------------------------- IMPORTS --#

# Built-in and Third Party
import subprocess
# Modules That You Wrote

#----------------------------------------------------------------------------------------#
#--------------------------------------------------------------------------- FUNCTIONS --#

#----------------------------------------------------------------------------------------#
#----------------------------------------------------------------------------- CLASSES --#

class LaunchNuke(object):
    """
    This class hold the logic to launch nuke.
    """

    def __init__(self, ren_file=None):
        """
        :param ren_file: The file to render
        :type: str
        :return:
        """
        self.ren_file = ren_file


    def launch_nuke(self):
        """
        This function launches a new nuke scene.
        :return:
        """
        # Replace with nuke.EXE_PATH()
        if self.ren_file:
            subprocess.call('c:/program files/Nuke10.5v1/Nuke10.5.exe', self.ren_file)
        else:
            subprocess.call('c:/program files/Nuke10.5v1/Nuke10.5.exe')
        return True

    def comp_images(self, image_path=None):
        """
        This function sends the command to comp images into a .mov file.
        :return:
        """
        pass