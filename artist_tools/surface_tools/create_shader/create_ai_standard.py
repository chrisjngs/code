import maya.cmds as cmds


object = cmds.ls(selection=True)
objName = object
cmds.select(object)


def testFunc(*args):

	return

def createAiStandard(*args):

	print 'made a shader with '
	curName = cmds.textField('shaderNameField', q=1, tx=1)
	curPrefix = cmds.textField('prefixField', q=1, tx=1)
	finalName = curPrefix+curName
	aiStnd = {}
	shader = cmds.shadingNode('aiStandard', asShader=True, n=finalName)
	shading_group= cmds.sets(r=1,nss=1,em=1, n=finalName.replace(curPrefix, 'SG_'))
	aiStnd[shader] = shader

	#appends the new shader to the shading list
	cmds.textScrollList('shaders', e=1, a=aiStnd[shader])

	p2dAttr = ['.coverage', '.mirrorU', '.mirrorV', '.noiseUV', '.offset', '.uvCoord', '.uvFilterSize', '.repeatUV', '.rotateFrame', '.rotateUV', '.stagger', '.translateFrame', '.vertexCameraOne', '.vertexUvOne', '.vertexUvThree', '.vertexUvTwo', '.wrapU', '.wrapV']
	revAttr = ['.inputs[0].colorB', '.inputs[0].colorR', '.inputs[0].colorG']

	cmds.connectAttr(shader + '.outColor', shading_group + '.surfaceShader')
	p2d1 = cmds.createNode('place2dTexture', n=finalName.replace(curPrefix, 'p2d_') + '_main')
	aiStnd[p2d1] = p2d1

	if cmds.checkBox('diffBox', v=1, q=1):

		print 'a diffuse file'

		#      Creating Nodes      #
		file1 = cmds.createNode('file', n=finalName.replace(curPrefix, 'txt_') + '_diff')

		#      Connecting Nodes      #
		cmds.connectAttr(file1 + '.outColor', shader + '.color')
		for attr in p2dAttr:
			cmds.connectAttr(p2d1 + attr, file1 + attr)

		#      Adding variables to dictionary      #
		aiStnd[file1] = file1

	if cmds.checkBox('specBox', v=1, q=1):

		print 'a spec file'

		#      Creating Nodes      #
		file2 = cmds.createNode('file', n=finalName.replace(curPrefix, 'txt_') + '_spec')
		file3 = cmds.createNode('file', n=finalName.replace(curPrefix, 'txt_') + '_roughness')

		#      Connecting Nodes      #
		cmds.connectAttr(file2 + '.outColor', shader + '.KsColor')
		cmds.connectAttr(file3 + '.outAlpha', shader + '.specularRoughness')
		for attr in p2dAttr:
			cmds.connectAttr(p2d1 + attr, file2 + attr)
			cmds.connectAttr(p2d1 + attr, file3 + attr)

		#      Adding variables to dictionary      #
		aiStnd[file2] = file2
		aiStnd[file3] = file3

	if cmds.checkBox('fresnalBox', v=1, q=1):

		print 'a fresnal file'

		#      Creating Nodes      #
		aiW1 = cmds.createNode('aiWriteFloat', n=finalName.replace(curPrefix, 'aiW_') + '_fresnalControl')
		file4 = cmds.createNode('file', n=finalName.replace(curPrefix, 'txt_') + '_fresnal')
		lay1 = cmds.createNode('layeredTexture', n=finalName.replace(curPrefix, 'lay_') + '_fresnal')
		reV1 = cmds.createNode('remapValue', n=finalName.replace(curPrefix, 'reV_') + '_fresnal')

		#      Connecting Nodes      #
		cmds.connectAttr(aiW1 + '.input', lay1 + '.inputs[1].alpha')
		cmds.connectAttr(file4 + '.outColor', lay1 + '.inputs[1].color')
		cmds.connectAttr(file4 + '.alphaIsLuminance', lay1 + '.inputs[0].alpha')
		cmds.connectAttr(lay1 + '.outAlpha', shader + '.Ksn')
		for attr in revAttr:
			cmds.connectAttr(reV1 + '.outputMax', lay1 + attr)
		for attr in p2dAttr:
			cmds.connectAttr(p2d1 + attr, file4 + attr)

		#      Adding variables to dictionary      #
		aiStnd[aiW1] = aiW1
		aiStnd[file4] = file4
		aiStnd[lay1] = lay1
		aiStnd[reV1] = reV1

	if cmds.checkBox('bumpBox', v=1, q=1):

		print 'a bump file'

		#      Creating Nodes      #

		p2d2 = cmds.createNode('place2dTexture', n=finalName.replace(curPrefix, 'p2d_') + '_tileBump')
		b2d1 = cmds.createNode('bump2d', n=finalName.replace(curPrefix, 'b2d_') + '_master')
		b2d2 = cmds.createNode('bump2d', n=finalName.replace(curPrefix, 'b2d_') + '_slave')
		file5 = cmds.createNode('file', n=finalName.replace(curPrefix, 'txt_') + '_normal')
		file6 = cmds.createNode('file', n=finalName.replace(curPrefix, 'txt_') + '_slaveBump')
		lay2 = cmds.createNode('layeredTexture', n=finalName.replace(curPrefix, 'lay_') + '_slaveBump')

		#      Connecting Nodes      #
		#cmds.connectAttr(aiW1 + '.input', lay2 + '.inputs[1].alpha')
		cmds.connectAttr(b2d1 + '.outNormal', shader + '.normalCamera')
		cmds.connectAttr(b2d2 + '.outNormal', b2d1 + '.normalCamera')
		cmds.connectAttr(file5 + '.outAlpha', b2d1 + '.bumpValue')
		cmds.connectAttr(file6 + '.outColor', lay2 + '.inputs[1].color')
		cmds.connectAttr(lay2 + '.outAlpha', b2d2 + '.bumpValue')
		for attr in p2dAttr:
			cmds.connectAttr(p2d1 + attr, file5 + attr)
			cmds.connectAttr(p2d2 + attr, file6 + attr)

		#      Adding variables to dictionary      #

		aiStnd[b2d1] = b2d1
		aiStnd[b2d2] = b2d2
		aiStnd[file5] = file5
		aiStnd[file6] = file6
		aiStnd[lay2] = lay2
		aiStnd[p2d2] = p2d2


	if cmds.checkBox('opacityBox', v=1, q=1):

		print 'a opacity file'


		#      Creating Nodes      #
		file7 = cmds.createNode('file', n=finalName.replace(curPrefix, 'txt_') + '_opacity')
		lay3 = cmds.createNode('layeredTexture', n=finalName.replace(curPrefix, 'lay_') + '_opacity')

		#      Connecting Nodes      #
		cmds.connectAttr(file7 + '.outColor', lay3 + '.inputs[1].color')
		cmds.connectAttr(file7 + '.alphaIsLuminance', lay3 + '.inputs[0].alpha')
		cmds.connectAttr(lay3 + '.outColor', shader + '.opacity')
		for attr in p2dAttr:
			cmds.connectAttr(p2d1 + attr, file7 + attr)

		#      Adding variables to dictionary      #
		aiStnd[file7] = file7
		aiStnd[lay3] = lay3

	if cmds.checkBox('sssBox', v=1, q=1):

		print 'a sss file'


		#      Creating Nodes      #
		file8 = cmds.createNode('file', n=finalName.replace(curPrefix, 'txt_') + '_sssColor')
		file9 = cmds.createNode('file', n=finalName.replace(curPrefix, 'txt_') + '_sssWeight')
		file10 = cmds.createNode('file', n=finalName.replace(curPrefix, 'txt_') + '_sssRadius')
		lay4 = cmds.createNode('layeredTexture', n=finalName.replace(curPrefix, 'lay_') + '_sssColor')
		lay5 = cmds.createNode('layeredTexture', n=finalName.replace(curPrefix, 'lay_') + '_sssWeight')
		lay6 = cmds.createNode('layeredTexture', n=finalName.replace(curPrefix, 'lay_') + '_sssRadius')
		reV2 = cmds.createNode('remapValue', n=finalName.replace(curPrefix, 'reV_') + '_sssWeight')

		#      Connecting Nodes      #
		cmds.connectAttr(file8 + '.outColor', lay4 + '.inputs[1].color')
		cmds.connectAttr(file8 + '.alphaIsLuminance', lay4 + '.inputs[0].alpha')
		cmds.connectAttr(file9 + '.outColor', lay5 + '.inputs[1].color')
		cmds.connectAttr(file9 + '.alphaIsLuminance', lay5 + '.inputs[0].alpha')
		cmds.connectAttr(file10 + '.outColor', lay6 + '.inputs[1].color')
		cmds.connectAttr(file10 + '.alphaIsLuminance', lay6 + '.inputs[0].alpha')
		cmds.connectAttr(lay4 + '.outColor', shader + '.KsssColor')
		cmds.connectAttr(lay5 + '.outColor', shader + '.sssRadius')
		cmds.connectAttr(lay6 + '.outAlpha', shader + '.Ksss')
		for attr in revAttr:
			cmds.connectAttr(reV2 + '.outputMax', lay5 + attr)
		for attr in p2dAttr:
			cmds.connectAttr(p2d1 + attr, file8 + attr)
			cmds.connectAttr(p2d1 + attr, file9 + attr)
			cmds.connectAttr(p2d1 + attr, file10 + attr)
			
		#      Adding variables to dictionary      #
		aiStnd[file8] = file8
		aiStnd[file9] = file9
		aiStnd[file10] = file10
		aiStnd[lay4] = lay4
		aiStnd[lay5] = lay5
		aiStnd[lay6] = lay6
		aiStnd[reV2] = reV2

	if cmds.checkBox('dispBox', v=1, q=1):

		print 'a displacement node'


		#      Creating Nodes      #
		displacement = cmds.shadingNode('displacementShader', asShader=True, n=finalName.replace(curPrefix, 'disp_'))
		#cmds.hyperShade(object,assign=displacement)
		file11 = cmds.createNode('file', n=finalName.replace(curPrefix, 'txt_') +  '_disp')

		#      Connecting Nodes      #
		cmds.connectAttr(displacement + '.displacement', shading_group + '.displacementShader')
		cmds.connectAttr(file11 + '.outColorR', displacement + '.displacement')
		for attr in p2dAttr:
			cmds.connectAttr(p2d1 + attr, file11 + attr)
		#      Adding variables to dictionary      #
		aiStnd[displacement] = displacement

	return

def publishShader(*args):

	cmds.container(n=t, inc=1, isd=1)

def createAiSkin(*args):

	aiSkn={}
	aiSkin = cmds.shadingNode('aiSkin', asShader=True, n=objName.replace('geo_', 'mrtl_'))
	aiSkn[aiSkin]=aiSkin
	p2dAttr = ['.coverage', '.mirrorU', '.mirrorV', '.noiseUV', '.offset', '.uvCoord', '.uvFilterSize', '.repeatUV', '.rotateFrame', '.rotateUV', '.stagger', '.translateFrame', '.vertexCameraOne', '.vertexUvOne', '.vertexUvThree', '.vertexUvTwo', '.wrapU', '.wrapV']
	
	p2d1 = cmds.createNode('place2dTexture', n=objName.replace('geo_', 'p2d_')+'_main')
	
	return aiSkn
	

	


