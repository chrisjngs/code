if

dir()
len()
type()

import maya.cmds as cmds
from xml.dom import minidom

class Autovivification(dict):
    def __getitem__(self, item):
        try:
            return dict.__getitem__(self, item)
        except KeyError:
            value = self[item] = type(self)()
            return value

xml_doc = minidom.Document()
root = xml_doc.createElement('root')
xml_doc.appendChild(root)


arnold_settings = cmds.listAttr('defaultArnoldRenderOptions', hasData=True)
global_settings = cmds.listAttr('defaultRenderGlobals', hasData=True)

res_settings = cmds.listAttr('defaultResolution', hasData=True)

render_dict =Autovivification()
# Low render settings
render_dict['Low']['defaultArnoldRenderOptions'] = arnold_settings
render_dict['Low']['defaultRenderGlobals']       = global_settings
render_dict['Low']['defaultResolution']          = res_settings
# Medium render settings
render_dict['Medium']['defaultArnoldRenderOptions'] = arnold_settings
render_dict['Medium']['defaultRenderGlobals']       = global_settings
render_dict['Medium']['defaultResolution']          = res_settings
# High render settings
render_dict['High']['defaultArnoldRenderOptions'] = arnold_settings
render_dict['High']['defaultRenderGlobals']       = global_settings
render_dict['High']['defaultResolution']          = res_settings
# Show render settings
render_dict['Show']['defaultArnoldRenderOptions'] = arnold_settings
render_dict['Show']['defaultRenderGlobals']       = global_settings
render_dict['Show']['defaultResolution']          = res_settings

render_settings = render_dict.keys()
# The actual code to run.
for setting in render_dict:
    # Adds the setting name to the xml, example: low
    setting_entry = xml_doc.createElement(setting)
    root.appendChild(setting_entry)
    setting_makes = render_dict[setting].keys()
    for key in setting_makes:
        # Adds the setting to the xml, example: defaultArnoldRenderOptions
        setting_entry_make = xml_doc.createElement(key)
        setting_name       = render_dict[setting][key]
        setting_entry.appendChild(setting_entry_make)
               
        for key_value in setting_name:
            # Adds the attr to the xml and sets its value, example: AASamples = 2
            key_value_entry = xml_doc.createElement(key_value)
            attr_name       = render_dict[setting][key]
            setting_entry_make.appendChild(key_value_entry)
            cur_value = cmds.getAttr("%s.%s" %(key, key_value))
            key_value_entry.setAttribute('value', str(cur_value))

xml_str = xml_doc.toprettyxml(indent='    ')

file_location = 'C:/Users/chris/code/temp/test_render_file.xml'

with open(file_location, 'w') as fh:
    fh.write(xml_str)

'''
# The logic for how to layer the information
render_settings = render_dict.keys()
for setting in render_dict:
    # Setting is the current setting level, example: low
    setting_makes = render_dict[setting].keys()
    for key in setting_makes:
        # key is the first part of the attr, example:defaultArnoldRenderOptions.
        attr_settings = render_dict[setting][key]
        #print '\nThe current key is %s' % key
        for key_value in attr_settings:
            # key_value is the second part of the attr, example:.AASamples.
            # value is what the attr is set to, example: 2
            value = cmds.getAttr("%s.%s" %(key, key_value))
            #print "The value for %s in %s is %s" %(key_value, key, value)
            # prints "The value for AASamples in defaultArnoldRenderOptions is 2".
'''   