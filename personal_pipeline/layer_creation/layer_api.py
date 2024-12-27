import maya.cmds as cmds


# Get selection.
selection = cmds.ls(sl=1)

# For every item in the selection, create a layer
for item in selection:
    if not cmds.objExists(item+"_Layer"):
        cmds.createDisplayLayer(name = item +"_Layer", noRecurse=True)
    else:
        layerName = item+"_Layer"
        cmds.editDisplayLayerMembers(layerName, item)