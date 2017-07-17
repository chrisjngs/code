#!/usr/bin/env python
#SETMODE 777

#----------------------------------------------------------------------------------------#
#------------------------------------------------------------------------------ HEADER --#

"""
:author:
    Chris Jennings

:synopsis:
    This creates a turntable of the object(s) selected by the user.

:description:
    The user selects the object that they want to have a turntable of and then runs the
    script. If the object is fully visible then they click the 'yes' button in the prompt.
    If the object isn't fully visible then the user can click the 'no' button and the
    camera will move away from the object and ask the user to confirm they can see the
    object again. Once the user presses the 'yes' button, a playblast will be created with
    the name of the '.mov' file being the name of the Maya scene. The file will be placed
    in the users documents folder, unless specified otherwise.


:to do:

    -add the ability to render a turntable out of maya
    -add the automatic comp of the rendered images with Nuke
    -add an automatic detection of the white light rig and key it appropriately

:applications:
    Maya, Nuke

:see_also:
    N/A

"""
#----------------------------------------------------------------------------------------#
#----------------------------------------------------------------------------- IMPORTS --#

# Built-in and Third Party
import maya.cmds as cmds
import math
import os
import xml.etree.ElementTree as et

# Modules That You Wrote

#----------------------------------------------------------------------------------------#
#--------------------------------------------------------------------------- FUNCTIONS --#
def scene_check():
    """
    This function checks to make sure that the maya scene is saved and has a filename

    :return False: If the scene isn't saved

    :return True: If the scene is saved as something other than 'untitled'

    """
    save_check = cmds.file(query=1, expandName=1)
    file_name = save_check.rpartition('/')[2]
    if file_name == "untitled":
        return False
    return True

def discipline_check():
    """
    This function gets the file path for the current session of maya and returns its
    discipline. Valid disciplines are either 'model' or 'surface', if the file is
    neither, a 'none' discipline will be returned.

    :return 'surface': If the file contains a 'surface' folder.
    :type: str

    :return 'model': If the file contains a 'model' folder.
    :type: str

    :return 'none': If the file doesn't contain either a model or surface folder.
    :type: str
    """

    file_path = cmds.file(query=1, expandName=1)

    if '/surface/' in file_path:
        discipline = 'surface'
        return discipline
    elif '/model/' in file_path:
        discipline = 'model'
        return discipline
    else:
        print '\nThe file has no discipline.\n'
        discipline = 'none'
        return discipline

def launch_tool():
    """
    This helper function launches the appropriate class depending on the discipline of the
    class

    :return: RenderTurntable or PlayblastTurntable
    :type: class
    """

    result = discipline_check()
    if result == 'model':
        inst = PlayblastTurntable()
    elif result == 'surface':
        inst = RenderTurntable()
    else:
        return None
    return inst


#----------------------------------------------------------------------------------------#
#----------------------------------------------------------------------------- CLASSES --#
class Autovivification(dict):
    def __getitem__(self, item):
        try:
            return dict.__getitem__(self, item)
        except KeyError:
            value = self[item] = type(self)()
            return value

class Turntable(object):
    """
    This class creates a turntable of the object(s) selected by the user.
    """

    def __init__(self, start_frm=1, end_frm=24, file_path=None):

        self.count      = 4
        self.cam_loc    = None
        self.ren_cam    = None
        self.cur_cam    = None
        self.discipline = None
        self.start_frm  = start_frm
        self.end_frm    = end_frm

    def start_tool(self, discipline=None):
        """
        This function runs checks of the file before the actual tool is run. If any of the
        checks fail, the tool will not run.

        :param discipline: The discipline of the current maya file
        :type: string
        """
        #if the user didn't pass a discipline in, check the file path for the discipline.
        if not discipline:
            discipline = launch_tool()
            self.discipline = discipline
        else:
            self.discipline = discipline
            print 'the discipline is was set to %s by the user.' %discipline
        #if the scene is saved as a valid name, run the tool
        if scene_check():
            disp = launch_tool()
            self.create_camera()
        else:
            cmds.headsUpMessage("Please save the scene before continuing")
            print "The scene cannot be called 'untitled' please save it as a valid name."

    def cam_move(self, z_val):
        """
        This function moves the newly created camera back along the Z axis

        :param z_val: The value that the camera will move in the z direction
        :type: int
        """

        cmds.move(z_val, self.ren_cam, moveZ=True, objectSpace=True, relative=True)
        cmds.refresh(force=True)

    def confirm_window(self):
        """
        This function creates a confirmation window to make sure that the object is fully
        in view and that the user wanted to run the tool

        :return True: If the user clicks the 'Yes' button
        :return False: If the user clicks the 'No' button
        :return None: If the user clicks the 'Cancel' button
        """

        result = cmds.confirmDialog(
            title="Confirmation Window",
            message="Can you see the entire object?",
            button=["Yes", "No", "Cancel"],
            defaultButton ="Yes",
            cancelButton="Cancel",
            dismissString="No")

        if result == 'Yes':
            self.playblast(self.start_frm, self.end_frm)
        elif result == 'No':
            self.cam_move(5)
            self.confirm_window()
        else:
            self.clean_up()

    def set_key(self, min_frame, max_frame):
        """
        This function sets the keyframes for the start and end of the turntable.

        :param min_frame: The frame that the playblast will start at
        :type: int

        :param max_frame: The frame that the playblast will end at
        :type: int

        """
        cmds.setKeyframe(self.cam_loc,
                         time=min_frame,
                         value=0,
                         attribute='rotateY',
                         inTangentType='linear',
                         outTangentType='linear')
        cmds.setKeyframe(self.cam_loc,
                         time=max_frame,
                         value=360,
                         attribute='rotateY',
                         inTangentType='linear',
                         outTangentType='linear')

    def create_camera(self):
        """
        This function creates a camera and locator and then positions the camera based
        on the bounding box of the selected object. To aim the camera at the center of
        the object we grab the center of the bounding box and then aim constrain to it.

        :return renCam: The name of the camera that is being rendered
        :return curCam: The name of the camera that is active when the tool is run
        :return camLoc: the name of the locator that is created
        """

        self.cur_cam = cmds.lookThru(query=1)
        obj = cmds.ls(selection=True)
        if not obj:
            cmds.headsUpMessage("Please select the object you "
                                "want to make a turntable of")
            print "Please select the object(s) you want to make a turntable of."
            return None

        #calculates the center of the objects and stores it in xc, yx, zc variables.
        x1, y1, z1, x2, y2, z2 = cmds.exactWorldBoundingBox(obj)
        xc = (x2 + x1) / 2.0
        yc = (y2 + y1) / 2.0
        zc = (z2 + z1) / 2.0
        pos_center = [xc, yc, zc]
        self.cam_loc = cmds.spaceLocator(name="turntableLocator")

        #Moves the locator to the center of the bounding box
        cmds.xform(self.cam_loc,
                   translation=(pos_center[0], pos_center[1], pos_center[2]))

        #sets the start and end keyframes#
        self.set_key(1, 24)

        x = 0
        y = math.fabs(y2)
        z = math.fabs(x1)*self.count

        self.ren_cam = cmds.camera(name="turntableCamera", p=(x, y, z))
        cmds.parent(self.ren_cam[0], self.cam_loc)

        aim_con = cmds.aimConstraint(self.cam_loc,
                                     self.ren_cam[0],
                                     aim=(0.0, 0.0, -1.0))
        cmds.delete(aim_con)
        cmds.lookThru(self.ren_cam)
        cmds.hide(self.cam_loc)
        cmds.refresh(force=True)
        self.confirm_window()

        return self.ren_cam, self.cur_cam, self.cam_loc

    def playblast(self, min_frame, max_frame):
        """
        This function is the base function for creating the playblast. If the discipline
        is 'model' then the playblast will be put in the model directory. If the
        discipline is 'surface' then the playblast will be put in the surface directory.

        :param min_frame: The frame that the turntable will start at
        :type: int

        :param max_frame: The frame that the turntable will end at
        :type: int

        :return:
        """

        return

    def clean_up(self):
        """
        This function returns the scene to what it was before the tool was run.
        """
        # Look through the camera that user was originally using and delete the turntable
        # locator
        cmds.lookThru(self.cur_cam)
        cmds.delete(self.cam_loc)

class PlayblastTurntable(Turntable):
    """
    This class holds everything that is needed to create a playblast of the turntable.
    """

    def __init__(self):

        super(PlayblastTurntable, self).__init__()
        self.file_path=''

    def playblast(self, min_frame, max_frame):
        """
        This is a function that will do a playblast of the turntable before the actual
        render to ensure it is correct.

        :param min_frame: The frame that the turntable will start at
        :type: int

        :param max_frame: The frame that the turntable will end at
        :type: int
        """
        if self.discipline == 'model':
            self.file_path = '%USERPROFILE%/desktop/turntable_test/playblast/'

        file_name = cmds.file(query=1, expandName=1)
        scene_name = file_name.rpartition('/')[2]
        correct_name = self.file_path + scene_name.rpartition('.')[0]+".mov"

        cmds.playblast(startTime=min_frame,
                       endTime=(int(max_frame)-1),
                       filename=correct_name,
                       format="qt",
                       percent=100,
                       forceOverwrite=True,
                       viewer=False,
                       widthHeight=[1920,1080])

        print "\nThe playblast was created and put in:\n %s\n" %self.file_path
        self.clean_up()

class RenderTurntable(Turntable):
    """
    This class holds everything that is needed to render the turntable
    """

    def __init__(self):
        """

        """
        super(RenderTurntable, self).__init__()
        self.file_path = ''

    def render_window(self):
        """
        This function creates a confirmation window to make sure that the object is fully
        in view and that the user wants to render the scene

        :return True: If the user clicks the 'Yes' button
        :return False: If the user clicks the 'No' button
        :return None: If the user clicks the 'Cancel' button
        """

        result = cmds.confirmDialog(
            title="Confirm Render",
            message="Was the playblast good to render?",
            button=["Yes", "No", "Cancel"],
            defaultButton ="Yes",
            cancelButton="Cancel",
            dismissString="No")

        if result == 'Yes':
            return True
        elif result == 'No':
            self.cam_move(5)
            self.render_window()
            return False
        else:
            return None

    def playblast(self, min_frame, max_frame):
        """
        This function creates a playblast before the actual render occurs in order to
        confirm that everything is visible.

        :param min_frame: The starting frame
        :type: int
        :param max_frame: The ending frame
        :type: int
        :return:
        """
        if self.discipline == 'surface':
            self.file_path = '%USERPROFILE%/desktop/turntable_test/turntable/'

        file_name = cmds.file(query=1, expandName=1)
        scene_name = file_name.rpartition('/')[2]
        correct_name = self.file_path + scene_name.rpartition('.')[0]+".mov"

        cmds.playblast(startTime=min_frame,
                       endTime=(int(max_frame)-1),
                       filename=correct_name,
                       format="qt",
                       percent=100,
                       forceOverwrite=True,
                       viewer=True,
                       widthHeight=[1920,1080])
        result = self.render_window()
        if result:
            self.render_scene()
        else:
            self.clean_up()

    def render_scene(self):
        """
        This function renders the scene using the same settings as the playblast for start
        and end frames.

        """
        #to keep the scene clean, delete when done
        print 'The scene is rendering'
        self.clean_up()

    def set_render_settings(self, setting=None):
        """
        This function reads an xml file that contains different levels of render settings.
        :param setting: The level of quality of the render settings
        :type: str
        :return:
        """
        file_location = 'C:/Users/cmj140030/code/artist_tools/surface_tools/turntable_tool/render_settings.xml'

        if not os.path.isfile(file_location):
            IO.error("The file, %s, does not exist" % file_location)

        xml_fh = et.parse(file_location)
        root   = xml_fh.getroot()
        xml_nodes = root.iter(setting)
        if not xml_nodes:
            print 'I could not find any child nodes'

        for xml_node in xml_nodes:
            # Loops through the first indented item, example: Low
            settings = xml_node.getchildren()
            for set in settings:
                # setting = defaultArnoldRenderOptions
                attrs = set.getchildren()
                for attr in attrs:
                    # attr = AASamples
                    val = attr.attrib['value']
                    if str(val).isdigit():
                        cmds.setAttr("%s.%s" % (set.tag,attr.tag),int(val))
                    elif '.' in val and val.replace('.', '').isdigit():
                        cmds.setAttr("%s.%s" % (set.tag,attr.tag),float(val))
                    elif '-' in val and val.replace('-', '').isdigit():
                        cmds.setAttr("%s.%s" % (set.tag,attr.tag),int(val))
                    elif '-' and '.' in str(val):
                        cmds.setAttr("%s.%s" % (set.tag,attr.tag),float(val))
                    elif '/' or '$' or '&' in str(val):
                        cmds.setAttr("%s.%s" % (set.tag,attr.tag),str(val),type="string")
                    elif str(val) == '':
                        cmds.setAttr("%s.%s" % (set.tag,attr.tag),'',type="string")
                    else:
                        print 'The value is not valid'


