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


import maya.cmds as cmds
from xml.dom import minidom

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


class XMLWriter(object):
    """
    This class writes out the information in a dictionary to an XML file.
    """
    def __init__(self, data_dict, xml_file):
        """
        :param data_dict: A dictionary that is two levels deep.
        :type: dict

        :param xml_file: The path where we will be writing an XML file.
        :type: str
        """
        self.data_dict = data_dict
        self.xml_file  = xml_file

    def write_xml(self):
        """
        Creates an XML based on the contents of the dictionary.
        """
        # Let's make sure we have something of value.
        if not self.data_dict:
            print 'The dictionary passed in does not have any values.'
            return None

        # Create an instance of the XML minidom document, and establish a root.
        xml_doc = minidom.Document()
        root    = xml_doc.createElement('root')
        xml_doc.appendChild(root)

        # Step through the levels of the dictionary to see what data we have to write.
        level_one = self.data_dict.keys()
        for key in level_one:
            level_two = self.data_dict[key].keys()
            obj_elem = xml_doc.createElement(key)
            root.appendChild(obj_elem)
            if not level_two:
                continue
            for item in level_two:
                value = self.data_dict[key][item]
                data_elem = xml_doc.createElement(item)
                data_elem.setAttribute('value', value)
                obj_elem.appendChild(data_elem)

        # Write the XML out to disk.
        xml_str = xml_doc.toprettyxml(indent='  ')
        with open(self.xml_file, 'w') as fh:
            fh.write(xml_str)


class MayaXMLWriter(object):
    """
    This class writes out the translation values of all the meshes in Maya.
    """
    def __init__(self, xml_location):
        """
        :param xml_location: The location on disk to write the XML to.
        :type: str
        """
        self.file_path = xml_location
        self.data_dict = Autovivification()
        self.objs      = []

    def get_obj_attrs(self):
        """
        Builds a dictionary that stores object names and translational information.
        """
        # Loop over all the objects.
        for obj in self.objs:
            # Loop over all the attributes we want to store.
            for attr in ['tx', 'ty', 'tz',  'rx', 'ry', 'rz', 'sx', 'sy', 'sz']:
                attr_value = cmds.getAttr(obj + '.' + attr)
                self.data_dict[obj][attr] = str(attr_value)

    def write_xml(self):
        """
        Writes out all the translational values of meshes in Maya to an XML document.
        """
        self.objs = cmds.ls(selection=True)
        # Verify that we have a file path and objects to write out.
        if not self.file_path or not self.objs:
            print 'A file path and a list of objects are required.'
            return None

        # Call get object attributes.
        self.get_obj_attrs()

        # Instantiate the write XML class and have it do all the work of writing out the XML.
        xml_writer = XMLWriter(self.data_dict, self.file_path)
        xml_writer.write_xml()
        return True

maya_writer = MayaXMLWriter('C:/Users/caj150430/code/asm.xml')
maya_writer.write_xml()

xml_dict = maya_writer.data_dict

data_objs = []
for name in xml_dict.keys():
    temp_dict = xml_dict[name]
    temp_dict['name'] = name
    print "The dictionary is %s" % temp_dict
    my_data = MyMayaData(**temp_dict)
    data_objs.append(my_data)

class MyMayaData(object):
    def __init__(self, **kwargs):
        self.name = kwargs.setdefault('name', None)
        self.tx = kwargs.setdefault('tx', None)
        self.ty = kwargs.setdefault('ty', None)
        self.tz = kwargs.setdefault('tz', None)

for data_obj in data_objs:
    print data_obj.tx
    print data_obj.name


class MayaXMLReader(object):
    """
    This class reads in translation values of objects and creates them in Maya.
    """
    def __init__(self, xml_location):
        """
        :param xml_location: The location on disk to write the XML to.
        :type: str
        """
    def validate(self):
        """
        Checks to make sure the XML exists.
        """
    def parse_keys(self):
        """
        Looks at the dictionary that we got back from reading the XML.
        """
    def create_and_set(self, obj_dict):
        """
        For each block in the dictionary, it creates an object, like a 'pSphere', and positions it.
        """
    def read_xml(self):
        """
        Reads in the XML document, stores it in a dictionary, and calls parse_keys.
        """

maya_reader = MayaXMLReader('C:/Users/caj150430/code/asm.xml')
maya_reader.write_xml()

