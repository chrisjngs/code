
### Writing an xml file ###
import os
import xml.etree.ElementTree as et
import maya.cmds as cmds

class Autovivification(dict):
    def __getitem__(self, item):
        try:
            return dict.__getitem__(self, item)
        except KeyError:
            value = self[item] = type(self)()
            return value




file_location = 'C:/Users/chris/code/temp/test_render_file.xml'

if not os.path.isfile(file_location):
    IO.error("The file, %s, does not exist" % file_location)

xml_fh = et.parse(file_location)
root   = xml_fh.getroot()
# Replace param with user specified setting, example: root.iter(self.render_setting)
xml_nodes = root.iter('Low')
if not xml_nodes:
    print 'I could not find any child nodes'

xml_dict = Autovivification()
for xml_node in xml_nodes:
    # Loops through the first indented item, example: Low
    #print "\nThe tag is %s" % xml_node.tag
    settings = xml_node.getchildren()
    for setting in settings:
        # setting = defaultArnoldRenderOptions
        # Loops through the second indented item, example: defaultArnoldRenderOptions
        attrs = setting.getchildren()
        for attr in attrs:
            # attr = AASamples
            # reads the third idented item and its value, example: AASamples = 2
            value = attr.attrib['value']
            print "%s.%s" %(setting.tag, attr.tag)
            if str(value).isdigit():
                print 'value is an int of %s'%value
                # cmds.setAttr("%s.%s" %(setting.tag, attr.tag), int(value))
            elif '.' in value and value.replace('.', '').isdigit():
                # print 'value is a float of %s'%value
                cmds.setAttr("%s.%s" %(setting.tag, attr.tag), float(value))
            elif '-' in value and value.replace('-', '').isdigit():
                # print 'value is a negative int of %s'%value
                cmds.setAttr("%s.%s" %(setting.tag, attr.tag), int(value))
            elif '-' and '.' in str(value):# and value.replace(('-', '.'), '').isdigit():
                # print 'value is a negative float of %s'%value
                cmds.setAttr("%s.%s" %(setting.tag, attr.tag), float(value))
            elif '/' or '$' or '&' in str(value):
                # print 'value is a string of %s'%value
                cmds.setAttr("%s.%s" %(setting.tag, attr.tag), str(value), type="string")
            elif str(value) == '':
                # print 'value is a bool of None'
                cmds.setAttr("%s.%s" %(setting.tag, attr.tag), '', type="string")
            else:
                print 'The value is not valid'

