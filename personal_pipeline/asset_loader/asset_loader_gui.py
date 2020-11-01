#!/usr/bin/env python
#SETMODE 777

#----------------------------------------------------------------------------------------#
#------------------------------------------------------------------------------ HEADER --#

"""
:author:
    Chris Jennings

:synopsis:
    A one line summary of what this module does.

:description:
    A detailed description of what this module does.

:applications:
    Any applications that are required to run this script, i.e. Maya.

:see_also:
    Any other code that you have written that this module is similar to.

"""

#----------------------------------------------------------------------------------------#
#----------------------------------------------------------------------------- IMPORTS --#

# Built-in and Third Party
from PySide2 import QtGui, QtWidgets, QtCore
from maya import OpenMayaUI as omui
from shiboken2 import wrapInstance
import os

# Modules That You Wrote
import personal_pipeline.asset_loader.asset_loader_logic as all

#----------------------------------------------------------------------------------------#
#--------------------------------------------------------------------------- FUNCTIONS --#
def get_maya_window():
    """
    Gets a pointer to the Maya window.
    """
    maya_main_window_ptr = omui.MQtUtil.mainWindow()
    return wrapInstance(long(maya_main_window_ptr), QtWidgets.QWidget)
#----------------------------------------------------------------------------------------#
#----------------------------------------------------------------------------- CLASSES --#
class AssetLoader(QtWidgets.QDialog):
    """
    This makes a layout
    """

    def __init__(self):
        QtWidgets.QDialog.__init__(self, parent=get_maya_window())
        self.le_01 = None
        self.asset_image = "C:/Users/Chris/code/artist_tools/model_tools/asset_loader/missing_thumbnail.png"
        self.cb_disp = None
        self.cb_asset = None
        self.cb_ver = None
        self.pix_map = None
        self.all_dict = {}
        self.projects_dict = {}
        self.asset_dict = {}
        self.disciplines_dict = {}
        self.files_dict = {}

    def init_gui(self):
        """
        This method builds and displays the GUI
        """
        # Make a layout.
        main_vb = QtWidgets.QVBoxLayout(self)

        # Make some buttons.
        btn_import = QtWidgets.QPushButton('Import Asset')
        btn_import.setAccessibleName("Import")
        btn_load = QtWidgets.QPushButton('Load Asset')
        btn_load.setAccessibleName("Load")

        # Make a divider line.
        line = QtWidgets.QFrame()
        line.setFrameStyle(line.HLine)

        # Make some Label.
        label_01 = QtWidgets.QLabel("Select Asset")
        label_02 = QtWidgets.QLabel("Select Discipline")
        label_03 = QtWidgets.QLabel("Select Version")

        # Make some Combo Boxes.
        self.cb_asset = QtWidgets.QComboBox()
        self.cb_disp = QtWidgets.QComboBox()
        self.cb_ver = QtWidgets.QComboBox()

        # Add options to the ComboBoxes
        # This line is temp for testing
        # Swap the hard coded list with a dynamic version that I get from os.listdir()

        self.get_project_struct()

        valid_disp = ["Model", "Surface", "Rig"]
        for disp in valid_disp:
            self.cb_disp.addItem(disp)

        # This line is temp for testing
        # Swap the hard coded list with a dynamic version that I get from os.listdir()
        versions = ["Active", "001", "002", "003"]
        for ver in versions:
            self.cb_ver.addItem(ver)

        self.cb_asset.addItems(self.find_assets())

        # Create a label to attach the image to
        self.asset_image_label = QtWidgets.QLabel()

        # Load in the image that gets attached
        self.pix_map = QtGui.QPixmap(self.asset_image)
        self.pix_map = self.pix_map.scaledToHeight(250)
        self.asset_image_label.setAlignment(QtCore.Qt.AlignCenter)

        # self.pix_map = self.pix_map.scaled(350, 350, QtCore.Qt.KeepAspectRatio)

        self.asset_image_label.setPixmap(self.pix_map)

        # Connects the buttons to commands.
        btn_import.clicked.connect(self.run_tool)
        btn_load.clicked.connect(self.run_tool)

        self.cb_asset.currentIndexChanged.connect(self.update_thumbnail)

        # Add some rows
        vbox_01 = QtWidgets.QVBoxLayout()

        # Add widgets to the layouts
        vbox_01.addWidget(self.asset_image_label)
        vbox_01.addWidget(line)
        vbox_01.addWidget(label_01)
        vbox_01.addWidget(self.cb_asset)
        vbox_01.addWidget(label_02)
        vbox_01.addWidget(self.cb_disp)
        vbox_01.addWidget(label_03)
        vbox_01.addWidget(self.cb_ver)
        vbox_01.addWidget(btn_import)
        vbox_01.addWidget(btn_load)

        # Add stuff to the main layout.
        main_vb.addLayout(vbox_01)

        # Set the Window size, title, and creates it.
        # self.setGeometry(300, 300, 350, 150)
        self.setFixedSize(400, 500)
        self.setWindowTitle("Asset Loader")
        self.show()

    def update_thumbnail(self):
        """
        This function updates the assets thumbnail on the GUI.
        """

        # Update the thumbnail file path.
        asset = self.cb_asset.currentText()
        # This needs to be changed to be modular, piecing together a file path given by
        # the gui.
        self.asset_image = "C:/Users/Chris/Box/Thesis/Production/Assets/%s/Thumbnails/%s_thumbnail.jpg" % (
        asset, asset)

        # Update the pixmap based on the new file path.
        self.pix_map = QtGui.QPixmap(self.asset_image)
        self.pix_map = self.pix_map.scaledToHeight(250)
        self.asset_image_label.setAlignment(QtCore.Qt.AlignCenter)

        # self.pix_map = self.pix_map.scaled(350, 350, QtCore.Qt.KeepAspectRatio)

        self.asset_image_label.setPixmap(self.pix_map)

    def update_assets(self):
        """
        This function updates the asset list when the project is changed.
        :return:
        """


    def version_update(self):
        """
        This function updates the version list when the asset changes.
        :return:
        """


    def find_assets(self, file_path=None):
        """
        This function searches through the filepath provided to search for assets.
        Once it finds the assets it returns then in a list.
        """

        self.assets = ["WarChief", "WarChief_Young", "OrcWeapon_A"]
        return self.assets

    def run_tool(self):
        """
        This function sends the data over to the logic module.
        """

        sender = self.sender()
        print "%sing the %s of %s, version %s" % (
        sender.accessibleName(), self.cb_disp.currentText(), self.cb_asset.currentText(),
        self.cb_ver.currentText())

        self.load_asset(self.cb_asset.currentText(), self.cb_disp.currentText(),
                        self.cb_ver.currentText())

    def load_asset(self, asset=None, discipline=None, version=None):
        """
        This function will be moved to the Logic class, it is only here for testing purposes.

        This function pieces together a filepath and then loads a Maya file.
        """
        if asset and discipline and version:
            if version == "Active":
                file_path = "C:/Users/Chris/Box/Thesis/Production/Assets/%s/%s/MAYA/%s.ma" % (
                asset, discipline, asset)

            else:
                file_path = "C:/Users/Chris/Box/Thesis/Production/Assets/%s/%s/MAYA/versioins/%s_%s.ma" % (
                asset, discipline, asset, version)

            print file_path

    def get_project_struct(self, base=None, proj=None):

        if not base:
            base = "A:\\Chris\\_CurrentProject"
        projects = []

        if not proj:
            projects = os.listdir(base)
        else:
            projects.append(proj)

        # Read through all of the projects to find their assets.
        for project in projects:
            # print "\n\n\n+++++++++++++++++++++++++++++++\n\n\n"
            project_path = "%s\\%s\\Assets" % (base, project)
            assets = os.listdir(project_path)

            # Add each project as a key in the projects_dict dictionary with an empty value.
            self.projects_dict.setdefault("projects", {})[project] = {}

            # Read through all of the assets in the project to find their disciplines
            for asset in assets:
                asset_path = "%s\\%s\\Assets\\%s" % (base, project, asset)
                if os.path.isdir(asset_path):
                    disciplines = os.listdir(asset_path)

                # Removes any invalid disciplines from the list.
                if "dailies" in disciplines:
                    disciplines_no_dailies = disciplines.remove("dailies")

                # Add each asset as a key in the asset_dict dictionary with an empty value.
                self.asset_dict[asset] = {}

                # Read through all of the disciplines to find their files
                for discipline in disciplines:
                    file_path = "%s\\%s\\Assets\\%s\\%s\\MAYA" % (
                    base, project, asset, discipline)
                    if os.path.isdir(file_path):
                        files = os.listdir(file_path)
                    all_asset_files = []

                    # If there are no files in the discipline, then prompt to create a new Maya file
                    #if not files:
                        #print "The asset '%s' in '%s' doesn't have any files in %s" \
                              #" discipline. Press to create a new asset" % (
                        #asset, project, discipline)

                    # Read through the list to find all of the files.
                    for file in files:
                        # If the file is a maya file, add it to all_asset_files list.
                        # else if it is a versions folder, find all of the maya version files
                        if file.endswith(".ma"):
                            all_asset_files.append(file)
                        elif file == "versions" and os.path.isdir(
                                "%s\\%s\\Assets\\%s\\%s\\MAYA\\%s" % (
                                base, project, asset, discipline, file)):
                            versions_folder = "%s\\%s\\Assets\\%s\\%s\\MAYA\\%s" % (
                            base, project, asset, discipline, file)
                            versions = os.listdir(versions_folder)
                            for version in versions:
                                if version.endswith(".ma"):
                                    all_asset_files.append(version)

                        self.disciplines_dict[discipline] = all_asset_files
                        self.asset_dict[asset] = self.disciplines_dict
                        self.projects_dict[project] = self.asset_dict



