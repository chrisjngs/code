
import maya.cmds as cmds

#imports the file at the specified location and adds it to the namespace 'whiteLightRig'
file_path ='C:/Users/Chris/code/artist_tools/surface_tools/light_rig/white_light_rig.ma'
cmds.file(file_path, i=True, namespace='whiteLightRig')
