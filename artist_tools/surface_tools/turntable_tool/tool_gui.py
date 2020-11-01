#!/usr/bin/env python
#SETMODE 777

#----------------------------------------------------------------------------------------#
#------------------------------------------------------------------------------ HEADER --#

"""
:author:
    Chris Jennings

:synopsis:
    This module contains the code for the GUI.

:description:
    This module creates the GUI for the turntable tool. Using PySide, this creates a main
    window that the user can interact with and set the file path, start and end frames,
    whether or not to render a wireframe, and the files discipline. If the discipline is
    set to surface, the user can select the quality of the render that will take place.

:applications:
    Maya.

:see_also:
    n/a.

"""

#----------------------------------------------------------------------------------------#
#----------------------------------------------------------------------------- IMPORTS --#

# Built-in and Third Party
try:
    from PyQt4 import QtCore, QtGui
except ImportError:
    from PySide import QtCore, QtGui
    from maya import OpenMayaUI as omui
    from shiboken import wrapInstance

# Modules That You Wrote
import artist_tools.surface_tools.turntable_tool.tool_logic as tl

#----------------------------------------------------------------------------------------#
#--------------------------------------------------------------------------- FUNCTIONS --#
def get_maya_window():
    """
    This gets a pointer to the Maya window.

    :return: A pointer to the Maya window.
    :type: pointer
    """
    maya_main_window_ptr = omui.MQtUtil.mainWindow()
    return wrapInstance(long(maya_main_window_ptr), QtGui.QWidget)

#----------------------------------------------------------------------------------------#
#----------------------------------------------------------------------------- CLASSES --#

class ToolGUI(QtGui.QDialog):
    """
    A GUI that has some labels.
    """
    def __init__(self):
        QtGui.QDialog.__init__(self, parent=get_maya_window())
        self.setting_dropdown = None
        self.save_loc         = None
        self.start_frm_le     = None
        self.end_frm_le       = None
        self.rad_grp          = None
        self.ren_cb           = None
        self.start_frm        = None
        self.end_frm          = None
        self.wireframe        = None

    def init_gui(self):
        """
        Sets up how the GUI looks and shows it to the user.
        """
        # This is the main layout.
        main_layout = QtGui.QVBoxLayout(self)

        # This is the start button.
        start_btn = QtGui.QPushButton('Start Turntable')
        start_btn.clicked.connect(self.init_turn)

        # This is the file browser button.
        brw_btn = QtGui.QPushButton('Browse')
        brw_btn.clicked.connect(self.select_dir)

        # This is the render settings drop down.
        self.setting_dropdown = QtGui.QComboBox()
        self.setting_dropdown.addItems(['Low','Medium','High','Show','Custom'])

        # These are the line edits.
        self.save_loc = QtGui.QLineEdit()
        self.start_frm_le = QtGui.QLineEdit()
        self.end_frm_le = QtGui.QLineEdit()

        # This is the checkbox for rendering wireframe.
        self.ren_cb = QtGui.QCheckBox('Wireframe')

        # This is the radio btn group.
        self.rad_grp = QtGui.QButtonGroup()
        rd_01 = QtGui.QRadioButton('Surface')
        rd_02 = QtGui.QRadioButton('Model')
        rd_01.setObjectName('surface')
        rd_02.setObjectName('model')
        self.rad_grp.addButton(rd_01)
        self.rad_grp.addButton(rd_02)

        discipline = tl.discipline_check()
        if discipline == 'surface':
            rd_01.toggle()
        else:
            rd_02.toggle()

        # These are labels.
        loc_lbl = QtGui.QLabel('Location:')
        start_frm_lbl = QtGui.QLabel('Start Frame:')
        end_frm_lbl = QtGui.QLabel('End Frame:')

        # These are the different layout variables
        h_box_01 = QtGui.QHBoxLayout()
        h_box_02 = QtGui.QHBoxLayout()
        h_box_03 = QtGui.QHBoxLayout()

        v_box_01 = QtGui.QVBoxLayout()

        # This adds the widgets to the layouts.
        v_box_01.addWidget(rd_01)
        v_box_01.addWidget(rd_02)

        h_box_01.addLayout(v_box_01)
        h_box_01.addWidget(self.ren_cb)
        h_box_01.addWidget(self.setting_dropdown)

        h_box_02.addWidget(loc_lbl)
        h_box_02.addWidget(self.save_loc)
        h_box_02.addWidget(brw_btn)

        h_box_03.addWidget(start_btn)
        h_box_03.addWidget(start_frm_lbl)
        h_box_03.addWidget(self.start_frm_le)
        h_box_03.addWidget(end_frm_lbl)
        h_box_03.addWidget(self.end_frm_le)

        # This adds the layouts to the window
        main_layout.addLayout(h_box_01)
        main_layout.addLayout(h_box_02)
        main_layout.addLayout(h_box_03)

        # This is the main window.
        self.setGeometry(300, 300, 250, 150)
        self.setWindowTitle('Turntable Tool')
        self.show()

    def arg_check(self):
        """
        This function checks that everything the user passed in is valid and sets default
        values if not.
        :return:
        """
        # If the user didn't input a value for the start frame, start at frame 1.
        if not self.start_frm_le.text():
            self.start_frm = '1'
            self.start_frm_le.setText('1')

        # If the user didn't input a value for the end frame, end at frame 24
        if not self.end_frm_le.text():
            self.end_frm = '24'
            self.end_frm_le.setText('24')
            
        # If the user set the start or end time to something other than a digit.
        sf = str(self.start_frm)
        ef = str(self.end_frm)

        if not sf.isdigit() or not ef.isdigit():
            print "The start and end frames must be whole numbers."
            return None

        # If wireframe checkbox is checked, toggle wireframe.
        if self.ren_cb.isChecked():
            self.wireframe = True
        elif not self.ren_cb.isChecked():
            self.wireframe = False

        return True

    def select_dir(self):
        """
        This function creates a file browser for the user to select the directory they
        want the tool to look at.
        """
        dir_loc = QtGui.QFileDialog.getExistingDirectory()
        self.update_dir(dir_loc)

    def update_dir(self, new_dir):
        """
        This function will update the file location field.
        :param new_dir: The new directory that the user selected.
        :type: str
        """
        self.save_loc.setText(new_dir)

    def init_turn(self):
        """
        This function instantiates the tool logic Turntable class with the values given by
        the user.
        :return:
        """
        sender = self.sender()
        cur_settings = self.setting_dropdown.currentText()

        if sender:
            cur_disp = self.rad_grp.checkedButton()
            self.start_frm = self.start_frm_le.text()
            self.end_frm = self.end_frm_le.text()
            file_path = self.save_loc.text()
            if self.arg_check():

                wireframe = self.wireframe
                # Instantiate the tool logic with the selected values.
                start_turn = tl.Turntable(cur_disp.objectName(),
                                          self.start_frm,
                                          self.end_frm,
                                          file_path,
                                          wireframe)

                # If discipline is surface, set render settings.
                if cur_disp.objectName() == 'surface':
                    set_turn = tl.RenderTurntable()
                    set_turn.set_render_settings(cur_settings,self.start_frm,self.end_frm)

                start_turn.launch_tool()
