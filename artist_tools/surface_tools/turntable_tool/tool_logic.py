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
import maya.mel as mel
import math
import os
import xml.etree.ElementTree as et
import tempfile


# Modules That You Wrote


#----------------------------------------------------------------------------------------#
#--------------------------------------------------------------------------- FUNCTIONS --#
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
        print '\nThe file has no set discipline.\n'
        discipline = 'none'
        return discipline

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
    This is the base class, it holds the logic that is needed for both disciplines to work
    """

    def __init__(self, discipline=None, min_frame=1, max_frame=24, file_path=None, wireframe=None):
        """
        :param discipline: The user specified discipline.
        :type: str

        :param min_frame: The frame the turntable will start at.
        :type: int

        :param max_frame: The frame the turntable will end at.
        :type: int

        :param file_path: The location on disk where the files will be saved.
        :type: str

        :param wireframe: If wireframe should be rendered.
        :type: bool
        """
        self.discipline  = discipline
        self.min_frame   = min_frame
        self.max_frame   = max_frame
        self.file_path   = file_path
        self.wireframe   = wireframe
        self.cam_loc     = None
        self.ren_cam     = None
        self.cur_cam     = None
        self.ren_set     = None
        self.cur_project = None

    def error_check(self):
        """
        This helper function checks to make sure the scene is ready to use the tool.
        :return: If any of the checks are not true.
        :type: bool

        :return: If all of the checks pass.
        :type: bool
        """
        save_check = cmds.file(query=1, expandName=1)
        file_name = save_check.rpartition('/')[2]

        # If the scene is called untitled, return None.
        if file_name == "untitled":
            print 'The file cannot be named untitled, please rename the file'
            return None

        # If there is no object selected, return None.
        if not cmds.ls(selection = True):
            print "Please select the object(s) that you want to create a turntable of."
            return None

        # If the user did not specify a file path, file_path is temp folder.
        if not self.file_path:
            temp_path = tempfile.mkdtemp()
            self.file_path = temp_path
        return True

    def launch_tool(self):
        """
        This helper function launches the appropriate class depending on the discipline
        of the turntable.

        :return: If there is no discipline.
        :type: bool
        """
        if self.error_check():
            # If the user didn't specify a discipline.
            if not self.discipline:
                print 'Please select which discipline you want to work with.'
                return None
            else:
                if self.discipline == 'model':
                    inst = PlayblastTurntable(self.discipline,
                                              self.min_frame,
                                              self.max_frame,
                                              self.file_path,
                                              self.wireframe)
                    inst.start_tool()
                elif self.discipline == 'surface':
                    inst = RenderTurntable(self.discipline,
                                           self.min_frame,
                                           self.max_frame,
                                           self.file_path,
                                           self.wireframe)
                    inst.start_tool()
                else:
                    print "The valid disciplines are 'model' or 'surface'."
                    return None

    def start_tool(self):
        """
        This function calls the error check and then instantiates the class that is needed.
        :return:
        """

    def playblast(self, start_frm=1, end_frm=24):
        """
        This function creates a playblast of the turntable

        :param start_frm: The frame the turntable should start at.
        :type: int

        :param end_frm: The frame the turntable should end at.
        :type: int

        :return:
        """

    def confirm_vis(self):
        """
        This function confirms that the object is entirely visible.
        :return:
        """
        # For testing purposes, this will always return True
        result = cmds.confirmDialog(
        title="Confirmation Window",
        message="Can you see the entire object?",
        button=["Yes", "No", "Cancel"],
        defaultButton ="Yes",
        cancelButton="Cancel",
        dismissString="No")

        if result == 'Yes':
            self.playblast(1, 24)
        elif result == 'No':
            cmds.move(5, self.ren_cam, moveZ=True, objectSpace=True, relative=True)
            cmds.refresh(force=True)
            self.confirm_vis()
        else:
            self.clean_up()

    def create_camera(self):
        """
        This function creates the camera for the turntable.
        :return:
        """
        self.cur_cam = cmds.lookThru(query=True)
        obj = cmds.ls(selection=True)

        # Calculates the center of the objects and stores it in xc, yx, zc variables.
        x1, y1, z1, x2, y2, z2 = cmds.exactWorldBoundingBox(obj)
        xc = (x2 + x1) / 2.0
        yc = (y2 + y1) / 2.0
        zc = (z2 + z1) / 2.0
        pos_center = [xc, yc, zc]
        self.cam_loc = cmds.spaceLocator(name="turntableLocator")

        # Moves the locator to the center of the bounding box
        cmds.xform(self.cam_loc,
                   translation=(pos_center[0], pos_center[1], pos_center[2]))

        # Sets the key frames of the turntable
        cmds.setKeyframe(self.cam_loc,
                         time=self.min_frame,
                         value=0,
                         attribute='rotateY',
                         inTangentType='linear',
                         outTangentType='linear')
        cmds.setKeyframe(self.cam_loc,
                         time=self.max_frame,
                         value=360,
                         attribute='rotateY',
                         inTangentType='linear',
                         outTangentType='linear')

        # Sets the initial camera position based on the objects size.
        x = 0
        y = math.fabs(y2)
        z = math.fabs(x1) * 4

        self.ren_cam = cmds.camera(name="turntableCamera", p=(x, y, z))
        cmds.parent(self.ren_cam[0], self.cam_loc)

        aim_con = cmds.aimConstraint(self.cam_loc,
                                     self.ren_cam[0],
                                     aim=(0.0, 0.0, -1.0))
        cmds.delete(aim_con)
        cmds.lookThru(self.ren_cam)
        cmds.hide(self.cam_loc)
        cmds.refresh(force=True)

        self.confirm_vis()

        return self.ren_cam, self.cur_cam, self.cam_loc

    def set_wireframe(self):
        """
        This function enables the wireframe to be shown during the turntable.
        """

    def clean_up(self):
        """
        This function returns the scene to how it was before the tool was run.
        :return:
        """
        cmds.lookThru(self.cur_cam)
        cmds.delete(self.cam_loc)
        active_view = cmds.getPanel(withLabel='Persp View')
        cmds.modelEditor(active_view, edit=True, headsUpDisplay=True)
        cmds.modelEditor(active_view, edit=True, cameras=True)

class PlayblastTurntable(Turntable):
    """
    This class is for the model discipline, it creates a turntable.
    """

    def start_tool(self):
        """
        This function calls the error check and then instantiates the class that is needed.
        :return:
        """
        #print 'The PlayblastTurntable class has been called and the tool has started.'
        if self.error_check():
            self.set_wireframe()
            self.create_camera()

    def set_wireframe(self):
        """
        This function enables the wireframe to be shown during the turntable.
        """
        if self.wireframe:
            active_view = cmds.getPanel(withLabel='Persp View')
            cmds.setAttr("hardwareRenderingGlobals.multiSampleEnable", True)
            cmds.modelEditor(active_view, edit=True, wireframeOnShaded=True)
        else:
            active_view = cmds.getPanel(withLabel='Persp View')
            cmds.modelEditor(active_view, edit=True, wireframeOnShaded=False)
        cmds.modelEditor(active_view, edit=True, headsUpDisplay=False)
        cmds.modelEditor(active_view, edit=True, cameras=False)

    def playblast(self, start_frm=1, end_frm=24):
        """
        This function creates a playblast of the turntable

        :param start_frm: The frame the turntable should start at.
        :type: int

        :param end_frm: The frame the turntable should end at.
        :type: int

        :return:
        """
        file_name = cmds.file(query=1, expandName=1)
        scene_name = file_name.rpartition('/')[2]
        if self.wireframe:
            correct_name = "%s/%s" %(self.file_path, scene_name.rpartition('.')[0]+"_wf.mov")
        else:
            correct_name = "%s/%s" %(self.file_path, scene_name.rpartition('.')[0]+".mov")

        cmds.playblast(startTime=self.min_frame,
                       endTime=(int(self.max_frame)-1),
                       filename=correct_name,
                       format="qt",
                       percent=100,
                       forceOverwrite=True,
                       viewer=False,
                       widthHeight=[1920,1080])
        print "\nThe playblast was created and put in:\n%s\n" %self.file_path
        self.clean_up()

    def clean_up(self):
        """
        This function returns the scene to how it was before the tool was run.
        :return:
        """
        super(PlayblastTurntable, self).clean_up()

class RenderTurntable(Turntable):
    """
    This class is for the model discipline, it creates a turntable.
    """

    def start_tool(self):
        """
        This helper function calls the functions that need to run at the start.
        :return:
        """
        #print 'The RenderTurntable class has been called and the tool has started.'
        if self.wireframe:
            self.set_wireframe()
        self.create_camera()

    def set_wireframe(self):
        """
        This function enables the wireframe to be shown during the turntable.
        """
        # For testing purposes, the wireframe will return True.

        print 'The wireframe has been turned on'

    def playblast(self, start_frm=1, end_frm = 24):
        """
        This function creates a playblast of the turntable

        :param start_frm: The frame the turntable should start at.
        :type: int

        :param end_frm: The frame the turntable should end at.
        :type: int

        :return:
        """
        file_name = cmds.file(query=1, expandName=1)
        scene_name = file_name.rpartition('/')[2]
        correct_name = "%s/%s" %(self.file_path, scene_name.rpartition('.')[0]+"_pb.mov")

        print '\nGenerating preview...\n'
        cmds.playblast(startTime=self.min_frame,
                       endTime=(int(self.max_frame)-1),
                       filename=correct_name,
                       format="qt",
                       percent=100,
                       forceOverwrite=True,
                       viewer=True,
                       widthHeight=[1920/2,1080/2],
                       offScreen=True)
        self.confirm_render()

    def confirm_render(self):
        """
        This function confirms that the playblast is good and the render is ready to start
        :return:
        """
        result = cmds.confirmDialog(
        title="Confirmation Window",
        message="Does the playblast look correct?",
        button=["Yes", "No", "Cancel"],
        defaultButton ="Yes",
        cancelButton="Cancel",
        dismissString="No")

        if result == 'Yes':
            self.render_turntable()
        elif result == 'No':
            cmds.move(5, self.ren_cam, moveZ=True, objectSpace=True, relative=True)
            cmds.refresh(force=True)
            self.playblast()
        else:
            self.clean_up()

    def set_render_settings(self, quality=None, start_frame=1, end_frame=24):
        """
        This function reads through an xml to set the render settings.

        :param quality: The quality of the render settings.
        :type: str

        :param start_frame: The frame to start the render on.
        :type: int

        :param end_frame: The frame to end the render on.
        :type: int

        :return:
        """
        # For testing purposes, this will not change any settings.
        self.ren_set = quality
        if self.ren_set == 'Custom':
            print 'The user has decided to use custom settings.'

        else:
            # Checks the current renderer then changes it to arnold if it isn't already.
            cur_render = cmds.getAttr('defaultRenderGlobals.currentRenderer')
            if not cur_render == 'arnold':
                cmds.setAttr('defaultRenderGlobals.currentRenderer',
                             'arnold',
                             type='string')
            # Gets the file path of the module and then the directory it is in.
            path = os.path.abspath(__file__)
            dir_path = os.path.dirname(path)
            file_location = '%s/render_settings.xml'%dir_path
            if not os.path.isfile(file_location):
                IO.error("The file, %s, does not exist" % file_location)

            xml_fh = et.parse(file_location)
            root = xml_fh.getroot()

            xml_nodes = root.iter(self.ren_set)
            if not xml_nodes:
                print 'I could not find any child nodes'

            xml_dict = Autovivification()
            for xml_node in xml_nodes:
                # Loops through the first indented item, ex: Low
                # print "\nThe tag is %s" % xml_node.tag
                settings = xml_node.getchildren()
                for setting in settings:
                    # setting = defaultArnoldRenderOptions
                    # Loops through the second indented item, ex: defaultArnoldRenderOptions
                    attrs = setting.getchildren()
                    for attr in attrs:
                        # attr = AASamples
                        # reads the third indented item and its value, ex: AASamples = 2
                        value = attr.attrib['value']
                        if str(value).isdigit():
                            cmds.setAttr("%s.%s" % (setting.tag, attr.tag), int(value))
                        elif '.' in value and value.replace('.', '').isdigit():
                            cmds.setAttr("%s.%s" % (setting.tag, attr.tag), float(value))
                        elif '-' in value and value.replace('-', '').isdigit():
                            cmds.setAttr("%s.%s" % (setting.tag, attr.tag), int(value))
                        elif '-' and '.' in str(
                                value):  # and value.replace(('-', '.'), '').isdigit():
                            cmds.setAttr("%s.%s" % (setting.tag, attr.tag), float(value))
                        elif '/' or '$' or '&' in str(value):
                            cmds.setAttr("%s.%s" % (setting.tag, attr.tag), str(value),
                                         type="string")
                        elif str(value) == '':
                            cmds.setAttr("%s.%s" % (setting.tag, attr.tag), '', type="string")
                        else:
                            print 'The value is not valid'
            # sets the persp camera to not render and then the start and end frames.
            cmds.setAttr('perspShape.renderable', 0)
            cmds.setAttr('defaultRenderGlobals.endFrame', end_frame)
            cmds.setAttr('defaultRenderGlobals.startFrame', start_frame)
            print 'Render settings have been set'

    def render_turntable(self):
        """
        This function renders the turntable from Maya.
        :return:
        """

        # Stores the current project and sets a new one to the user specified file path.
        # Then sets the turntable camera to be renderable.
        file_name = cmds.file(query=1, expandName=1)
        scene_name = file_name.rpartition('/')[2]
        correct_name = '%s'%scene_name.rpartition('.')[0]
        cmds.setAttr('defaultRenderGlobals.imageFilePrefix',
                     '%s/%s'%(self.file_path, correct_name),
                     type="string")

        cmds.setAttr('%s.renderable'%self.ren_cam[0], 1)

        # Starts the batch render.
        mel.eval("mayaBatchRender()")
        self.clean_up()

    def clean_up(self):
        """
        This function returns the scene to how it was before the tool was run.
        :return:
        """
        super(RenderTurntable, self).clean_up()
        #mel.eval('setProject "%s"'%self.cur_project)
