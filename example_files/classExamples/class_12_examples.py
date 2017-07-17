
try:
    from PyQt4 import QtCore, QtGui
except ImportError:
    from PySide import QtCore, QtGui
    from maya import OpenMayaUI as omui
    from shiboken import wrapInstance
import maya.cmds as cmds

def get_maya_window():
    """
    This gets a pointer to the Maya window.

    :return: A pointer to the Maya window.
    :type: pointer
    """
    maya_main_window_ptr = omui.MQtUtil.mainWindow()
    return wrapInstance(long(maya_main_window_ptr), QtGui.QWidget)


class WriteGUI(QtGui.QDialog):
    def __init__(self):
        QtGui.QDialog.__init__(self, parent=get_maya_window())

    def init_gui(self):
        # Make a layout to use.
        main_vb = QtGui.QVBoxLayout(self)

        # Make some random buttons.
        btn_01 = QtGui.QPushButton('Write It')
        btn_01.clicked.connect(self.write_file)

        # Add the layouts to the main layout.
        main_vb.addWidget(btn_01)

        # Set up how the window looks.
        self.setGeometry(300, 300, 450, 300)
        self.setWindowTitle('Writer GUI')
        img_icon = 'C:/Users/caj150430/code/so_much_win.png'
        self.setWindowIcon(QtGui.QIcon(img_icon))
        self.show()

    def write_file(self):
        """
        This method will write out translation, rotation, and scale values.
        """
        # Get the user selection.
        sel = cmds.ls(selection=True)
        if not sel:
            return None
        obj_name = sel[0]

        # Get the attributes.
        obj_tx = cmds.getAttr(obj_name + '.tx')
        obj_ty = cmds.getAttr(obj_name + '.ty')
        obj_tz = cmds.getAttr(obj_name + '.tz')

        # Write it all to a file.
        text_file = 'C:/Users/caj150430/code/translation_values.txt'
        file_hdl  = open(text_file, 'w')
        file_hdl.write('tx: ' + str(obj_tx) + "\r\n")
        file_hdl.write('ty: ' + str(obj_ty) + "\r\n")
        file_hdl.write('tz: ' + str(obj_tz) + "\r\n")
        file_hdl.close()

write_gui = WriteGUI()
write_gui.init_gui()


# Reading an XML document.
from xml.dom import minidom

xml_doc = minidom.Document()
root    = xml_doc.createElement('root')
xml_doc.appendChild(root)

data_dict = {}
data_dict['render_settings'] = ''
data_dict['ice_cream']       = ''
data_dict['cookies']         = ''

all_keys = data_dict.keys()
for item_key in all_keys:
    print "The item key is %s" % item_key
    xml_item = xml_doc.createElement(item_key)
    root.appendChild(xml_item)

xml_str  = xml_doc.toprettyxml(indent='    ')
xml_file = 'C:/Users/caj150430/code/test_xml.xml'
with open(xml_file, 'w') as fh:
    fh.write(xml_str)


class Autovivification(dict):
    """
    This is a Python implementation of Perl's autovivification feature.
    """
    def __getitem__(self, item):
        try:
            return dict.__getitem__(self, item)
        except KeyError:
            value = self[item] = type(self)()
            return value


data_dict = {}
data_dict['root'] = {'render_settings' : {'something' : ''}}
data_dict['root']['ice_cream']       = ''
data_dict['root']['cookies']         = ''
data_dict.keys()

auto_dict = Autovivification()
auto_dict['root']['render_settings']['something'] = ''
auto_dict.keys()

if auto_dict['blah']:
    print 'it does'


auto_dict = Autovivification()
auto_dict['monday']['butterscotch']         = '10'
auto_dict['tuesday']['pancakes']            = '20'
auto_dict['wednesday']['loss_of_innocence'] = '30'

xml_doc = minidom.Document()
root    = xml_doc.createElement('root')
xml_doc.appendChild(root)

for day in auto_dict.keys():
    print "The day is %s" % day
    xml_day = xml_doc.createElement(day)
    root.appendChild(xml_day)
    for thing in auto_dict[day].keys():
        value     = auto_dict[day][thing]
        print "  The thing is %s, and its value is %s" % (thing, value)
        xml_thing = xml_doc.createElement(thing)
        xml_thing.setAttribute('value', value)
        xml_day.appendChild(xml_thing)

xml_str  = xml_doc.toprettyxml(indent='    ')
xml_file = 'C:/Users/caj150430/code/test_xml.xml'
with open(xml_file, 'w') as fh:
    fh.write(xml_str)


class WriteXMLGUI(QtGui.QDialog):
    def __init__(self):
        QtGui.QDialog.__init__(self, parent=get_maya_window())

    def init_gui(self):
        # Make a layout to use.
        main_vb = QtGui.QVBoxLayout(self)

        # Make some random buttons.
        btn_01 = QtGui.QPushButton('Write It')
        btn_01.clicked.connect(self.write_file)

        # Add the layouts to the main layout.
        main_vb.addWidget(btn_01)

        # Set up how the window looks.
        self.setGeometry(300, 300, 450, 300)
        self.setWindowTitle('XML Writer GUI')
        img_icon = 'C:/Users/caj150430/code/so_much_win.png'
        self.setWindowIcon(QtGui.QIcon(img_icon))
        self.show()

    def write_file(self):
        """
        This method will write out translation, rotation, and scale values.
        """
        # Get the user selection.
        sel = cmds.ls(selection=True)
        if not sel:
            return None
        obj_name = sel[0]

        # Get the attributes.
        obj_tx = cmds.getAttr(obj_name + '.tx')
        obj_ty = cmds.getAttr(obj_name + '.ty')
        obj_tz = cmds.getAttr(obj_name + '.tz')

        # Create an XML document.
        xml_doc = minidom.Document()
        root    = xml_doc.createElement('root')
        xml_doc.appendChild(root)

        # Create all the entries.
        xml_tx = xml_doc.createElement('tx')
        xml_tx.setAttribute('value', str(obj_tx))
        root.appendChild(xml_tx)
        xml_ty = xml_doc.createElement('ty')
        xml_ty.setAttribute('value', str(obj_ty))
        root.appendChild(xml_ty)
        xml_tz = xml_doc.createElement('tz')
        xml_tz.setAttribute('value', str(obj_tz))
        root.appendChild(xml_tz)

        # Write it all to a file.
        xml_str  = xml_doc.toprettyxml(indent='    ')
        xml_file = 'C:/Users/caj150430/code/translation_values.xml'
        with open(xml_file, 'w') as fh:
            fh.write(xml_str)

write_gui = WriteXMLGUI()
write_gui.init_gui()


import xml.etree.ElementTree as et

xml_dict = Autovivification()
xml_file = 'C:/Users/caj150430/code/test_xml.xml'
xml_fh   = et.parse(xml_file)
root     = xml_fh.getroot()

root_children = root.getchildren()
for root_child in root_children:
    print "The root child tag is '%s'" % (root_child.tag)
    # Get the children of each of these items.
    day_children = root_child.getchildren()

    # Iterate over those, if they exist.
    if not day_children:
        continue
    for day_child in day_children:
        print "  The day child tag is '%s'" % (day_child.tag)
        print "    And the attribute value is '%s'" % (day_child.attrib['value'])
        # Get the value field.
        value = day_child.attrib['value']
        xml_dict[root_child.tag][day_child.tag] = value
        pass
    # Store everything you found in a dictionary.

auto_dict = Autovivification()
auto_dict['monday']['butterscotch']         = '10'
auto_dict['tuesday']['pancakes']            = '20'
auto_dict['wednesday']['loss_of_innocence'] = '30'

dir(root_child)
root_child.tag
root_child.attrib['value']
root_child.keys()

