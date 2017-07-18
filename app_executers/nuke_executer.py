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
import argparse
import subprocess
import time
import os
os.environ[ "NUKE_INTERACTIVE" ] = "1"

# Modules That You Wrote

#----------------------------------------------------------------------------------------#
#--------------------------------------------------------------------------- FUNCTIONS --#
def main(args):
    """
    :param args:
    :return:
    """
    # Assign the needed variables
    for arg in args:
        if 'file' in arg:
            file_path = args['file']
        elif 'end_frame' in arg:
            end_frame = args['end_frame']
        elif 'start_frame' in arg:
            start_frame = args['start_frame']
        elif 'discipline' in arg:
            discipline = args['discipline']
        elif 'image' in arg:
            image_path = args['image']
    import nuke
    ren_nuke = LaunchNuke()
    ren_nuke.comp_images(file_path, image_path, discipline, start_frame, end_frame)

#----------------------------------------------------------------------------------------#
#----------------------------------------------------------------------------- CLASSES --#

class LaunchNuke(object):
    """
    This class hold the logic to launch nuke.
    """

    def __init__(self, ren_file=None, str_frm=None, end_frm=None, discipline=None):
        """
        :param ren_file: The file to render
        :type: str

        :param str_frm: The start frame.
        :type: int

        :param end_frm: The end frame.
        :type: int

        :param discipline: The discipline of the file.
        :type: str
        :return:
        """
        self.ren_file = ren_file
        self.start_frame = str_frm
        self.end_frame = end_frm
        self.discipline = discipline

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

    def comp_images(self, file_path=None, image_path=None, discipline=None, start_frame=1, end_frame=24):
        """
        This function sends the command to comp images into a .mov file.
        :param image_path: The path to the images being comped
        :type: str

        :param discipline: The discipline of the render.
        :type: str

        :param start_frame: The frame the render will start at.
        :type: int

        :param end_frame: The frame the render will end at.
        :type: int
        :return:
        """
        # This is mimicking the variables that would be passed in.
        nuke_path = "C:/Program Files/Nuke10.0v2/Nuke10.0.exe"
        date = time.strftime("%d-%m-%Y")
        #mov_name = '%s_%s_%s.mov'%(image_path.rpartition('/')[0], self.discipline, date)
        mov_name = 'raw_wood_%s_%s.mov'%(discipline, date)
        #mov_path = 'C:/Users/cmj140030/Desktop/turntable_test/turntable/%s' %mov_name
        mov_path = '%s/%s' %(file_path.replace("\\","/"), mov_name)

        final_path = image_path.replace("\\","/")

        # This is the read node.
        read = nuke.nodes.Read(file = final_path)
        read["first"].setValue(int(start_frame))
        read["last"].setValue(int(end_frame))

        # This is the write node.
        write = nuke.nodes.Write(file = mov_path)
        write['channels'].setValue('rgba')
        write['colorspace'].setValue('sRGB')
        write['file_type'].setValue('mov')

        # This connects the write node to the read.
        nuke.Node.setInput(write, 0, read)

        # start a background render of nuke.
        frame_range = '%i-%i'%(start_frame, end_frame)
        nuke.executeBackgroundNuke(nuke_path,
                                   [write],
                                   nuke.FrameRanges(frame_range),
                                   ['main'],{})

if __name__ == '__main__':
    """
    This is what is run when you call the module directly.
    """
    parser = argparse.ArgumentParser()
    parser.add_argument("-f", "--file", required = False)
    parser.add_argument("-i", "--image", required=False)
    parser.add_argument("-stf", "--start_frame", type=int, required=False)
    parser.add_argument("-enf", "--end_frame", type=int, required=False)
    parser.add_argument("-disp", "--discipline", required=False)
    args = vars(parser.parse_args())

    main(args)
