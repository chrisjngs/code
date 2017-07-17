#!/usr/bin/env python
#SETMODE 777

#----------------------------------------------------------------------------------------#
#------------------------------------------------------------------------------ HEADER --#

"""
:author:
    Chris Jennings

:synopsis:
    This module runs the code for rendering a sequence of frames in maya without using a
    batch render process.

:description:
    A detailed description of what this module does.

:applications:
    Maya

:see_also:
    nuke_executer.py

"""

#----------------------------------------------------------------------------------------#
#----------------------------------------------------------------------------- IMPORTS --#

# Built-in and Third Party
import maya.cmds as cmds
import maya.mel as mel
import time
# Modules That You Wrote

#----------------------------------------------------------------------------------------#
#--------------------------------------------------------------------------- FUNCTIONS --#

def render_frames(str_frame=None, end_frame=None, destination=None, img_type=None):
    """
    This function renders a specified frame range and saves the images to a user defined
    location.
    :param str_frame: The first frame to start rendering.
    :type: int

    :param end_frame: The last frame to render.
    :type: int

    :param destination: Where the rendered images should be placed.
    :type str

    :param img_type: The file extension of the rendered images.
    :type int
    :return:
    """
    if not str_frame:
        print "Please specify the start frame"
        return None
    if not end_frame:
        print "Please specify the end frame"
        return None
    if not destination:
        temp_loc = "temp file location"
        print "No destination specified, placing rendered images in temp location.\n\r" \
              "%s"%temp_loc
    if not img_type:
        print "No image type was specified, rendering images as .png"
        img_type = 32
    # Gets the file name to be used for naming the rendered images.
    file_name = cmds.file(query=1, expandName=1)
    scene_name = file_name.rpartition('/')[2]

    # While the str_frame is less than the end_frame, set the current frame to str_frame
    # get the render window and render the current frame and place the image in the
    # specified location, then increment the str_frame up and repeat until it is equal to
    # the end_frame
    while str_frame <= end_frame:
        cmds.currentTime(str_frame)
        print "rendering frame %s" %str_frame
        mel.eval('renderWindowRender redoPreviousRender renderView')
        editor = 'renderView'
        cmds.setAttr("defaultRenderGlobals.imageFormat", img_type)
        cmds.renderWindowEditor(editor, e=True,
                                writeImage="%s/%s_%s"%
                                           (destination,
                                            scene_name.rpartition('.')[0],
                                            str_frame))
        str_frame += 1
current_time = time.strftime("%Y\%m\%d %H:%M:%S")
print "The render was completed at %s" %current_time
#----------------------------------------------------------------------------------------#
#----------------------------------------------------------------------------- CLASSES --#

