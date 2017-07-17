import maya.cmds as cmds
import artist_tools.surface_tools.create_shader.create_ai_standard as casd


def removeShader(*args):
	cmds.hyperShade(a='lambert1')
	return

def pubWindow(*args):

	pubWindow = 'pubWindow'
	containters = cmds.ls(con=1)

	if cmds.window('pubWindow', ex=1):
		cmds.deleteUI('pubWindow')
	cmds.window('pubWindow', t='Select Asset', rtf=1)
	cmds.rowColumnLayout()
	cmds.text('Assets in Scene')
	cmds.textScrollList(a=containters)
	cmds.button('addCon', l='Add to asset')
	cmds.button('newCon', l='Create new asset')#, c=casd.publishShader())
	cmds.setParent(u=1)

	cmds.showWindow('pubWindow')
	return

def clickOff(*args):

	cmds.select(cl=1)

def newShaderName(*args):

	selection = cmds.textScrollList('objects', q=1, si=1)
	cmds.select(selection)
	if selection:
		selection = selection[0]
	newName = cmds.textField('shaderNameField', e=1, tx=selection)
	if cmds.ls(sl=1):
		objName = selection
		return objName
	else:
		defaultName ='select object'
		return defaultName

def curShader(*args):

	shadeSel = cmds.textScrollList('shaders', q=1, si=1)
	cmds.select(shadeSel,add=1)
	selShader = cmds.select(shadeSel)
	if shadeSel:
		shadeSel = shadeSel[0]
	print (shadeSel)

	return selShader

def applyBtn(*args):

	print 'the shader has been assigned'
	cmds.hyperShade(newShaderName, a=curShader)

def removeBtn(*args):

	print 'lambert 1 has been assigned'
	cmds.hyperShade(newShaderName, a='lambert1')


def createGUI():

	objects = cmds.ls(typ='mesh')
	realNames = cmds.listRelatives(objects, p=1)
	shaders = cmds.ls(mat=1)

	mainWindow = 'mainWindow'
	if cmds.window(mainWindow, ex=1):
		cmds.deleteUI(mainWindow)

	windowSize = cmds.window('mainWindow', t='Create Shading Network', rtf=1)
	cmds.rowColumnLayout('mainLayout', nc=4)
	cmds.rowColumnLayout('objectList', cw=[(1,200)])
	cmds.text('List of objects in scene')
	cmds.textScrollList('objects', ams=1, a=realNames, h=400, sc=newShaderName)
	cmds.setParent('mainLayout')

	cmds.rowColumnLayout('applyBtns', nr=15, rh=[(1, 30), (2, 30)])
	cmds.text('\n')
	cmds.text('\n')
	cmds.text('\n')
	cmds.text('\n')
	cmds.text('\n')
	cmds.button('addBtn', l='Apply shader', c=applyBtn, h=30)
	cmds.text('\n')
	cmds.text('\n')
	cmds.text('\n')
	cmds.text('\t')
	cmds.button('subBtn', l='Remove shader', h=30, c=removeShader)
	cmds.setParent(u=1)

	cmds.columnLayout('shaderList', w=200, adj=1)
	cmds.text('List of shaders in scene')
	cmds.textScrollList('shaders', ams=0, a=shaders, h=400, sc=curShader)
	cmds.setParent('mainLayout')

	cmds.columnLayout('mainButtons', adjustableColumn=True)
	cmds.text('\t')
	cmds.button(l='Publish to Asset', c=pubWindow, h=30)
	cmds.text('\t')
	cmds.button(l='Create aiStandard', h=30, c=casd.createAiStandard)
	cmds.text('\t')
	cmds.button(l='Create aiSkin', h=30)
	cmds.setParent('mainButtons')

	cmds.rowColumnLayout('nameFieldsText', nr=1, rh=[(1, 20)])
	cmds.text('Enter the shaders prefix and name')
	cmds.setParent(u=1)
	cmds.rowColumnLayout('nameFields', nr=1, rh=[(1, 20)])
	cmds.textField('prefixField')
	shaderPrefix = cmds.textField('prefixField', e=1, text='mrtl_', w=50)
	cmds.textField('shaderNameField')
	shaderName = cmds.textField('shaderNameField',e=1, text=newShaderName())
	cmds.setParent(u=1)

	#cmds.separator()
	cmds.text('\t')
	cmds.text('aiStandard Map Options')
	cmds.separator()
	cmds.rowColumnLayout('checkBoxes', nc=3)
	cmds.checkBox('diffBox',l='Diffuse')
	cmds.checkBox('specBox', l='Spec')
	cmds.checkBox('fresnalBox', l='Fresnal')
	cmds.checkBox('opacityBox', l='Opacity')
	cmds.checkBox('bumpBox', l='Bump')
	cmds.checkBox('sssBox', l='SSS')
	cmds.checkBox('dispBox', l='Displacement')
	cmds.setParent(u=1)
	cmds.text('\t')
	cmds.text('aiSkin Map Options')
	cmds.separator()
	cmds.rowColumnLayout('skinCheckBox', nc=3)
	cmds.checkBox('shallowBox',l='Shallow')
	cmds.checkBox('midBox',l='Mid')
	cmds.checkBox('deepBox',l='Deep')
	cmds.checkBox('sssBox', l='SSS')
	cmds.checkBox('specBox', l='Spec')
	cmds.checkBox('sheenBox', l='Sheen')
	cmds.checkBox('fresnalBox', l='Fresnal')
	cmds.checkBox('bumpBox', l='Bump')
	cmds.checkBox('dispBox', l='Displacement')
	cmds.showWindow(mainWindow)
	return shaderName

createGUI()
