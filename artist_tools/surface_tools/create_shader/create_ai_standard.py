#!/usr/bin/env python
# SETMODE 777

# ----------------------------------------------------------------------------------------#
# ------------------------------------------------------------------------------ HEADER --#

"""
:author:
    Chris Narro

:synopsis:
    Creates a gui for the shader creation tool.

:description:
    This script runs the logic for the GUI for the shader network creation tool.

:applications:
    Any applications that are required to run this script, i.e. Maya.

:see_also:
    Any other code that you have written that this module is similar to.

"""

# ----------------------------------------------------------------------------------------#
# ----------------------------------------------------------------------------- IMPORTS --#

# Built-in and Third Party
import maya.cmds as cmds

# Modules That You Wrote
#import personal_pipeline.common_api as common
# ----------------------------------------------------------------------------------------#
# --------------------------------------------------------------------------- FUNCTIONS --#


# ----------------------------------------------------------------------------------------#
# ----------------------------------------------------------------------------- CLASSES --#

class CreateShader(object):
	"""

	"""
	def __init__(self):
		"""

		"""
		self.newShader=None
		self.newShaderEngine=None

	def diffuse_texture(self, shadename=None):
		texture = cmds.shadingNode('file', name="%s_diffuse_tex" % shadename, asTexture=True,
								   isColorManaged=True)
		aiColor = cmds.shadingNode("aiColorCorrect",
								   name="%s_diffuse_colorCorrect" % shadename, asTexture=True)
		cmds.connectAttr("%s.outColor" % texture, "%s.input" % aiColor)
		cmds.connectAttr("%s.outColor" % aiColor, "%s.baseColor" % self.newShader)


	def rough_texture(self, shadename=None):
		texture = cmds.shadingNode('file', name="%s_rough_tex" % shadename, asTexture=True,
								   isColorManaged=True)
		aiColor = cmds.shadingNode("aiColorCorrect", name="%s_rough_colorCorrect" % shadename,
								   asTexture=True)
		luminance = cmds.shadingNode("luminance", name="%s_rough_luminance" % shadename,
									 asUtility=True)
		cmds.connectAttr("%s.outColor" % texture, "%s.input" % aiColor)
		cmds.connectAttr("%s.outColor" % aiColor, "%s.value" % luminance)
		cmds.connectAttr("%s.outValue" % luminance, "%s.specularRoughness" % self.newShader)


	def bump_texture(self, shadename=None):
		texture = cmds.shadingNode('file', name="%s_bump_tex" % shadename, asTexture=True,
								   isColorManaged=True)
		bump2d = cmds.shadingNode('bump2d', name="%s_b2d" % shadename, asUtility=True)
		cmds.connectAttr("%s.outAlpha" % texture, "%s.bumpValue" % bump2d)
		cmds.connectAttr("%s.outNormal" % bump2d, "%s.normalCamera" % self.newShader)


	def opacity_texture(self, shadename=None):
		texture = cmds.shadingNode('file', name="%s_opacity_tex" % shadename, asTexture=True,
								   isColorManaged=True)
		cmds.connectAttr("%s.outColor" % texture, "%s.opacity" % self.newShader)


	def sss_texture(self, shadename=None):
		texture = cmds.shadingNode('file', name="%s_SSS_tex" % shadename, asTexture=True,
								   isColorManaged=True)
		aiColor = cmds.shadingNode("aiColorCorrect", name="%s_SSS_colorCorrect" % shadename,
								   asTexture=True)
		cmds.connectAttr("%s.outColor" % texture, "%s.input" % aiColor)
		cmds.connectAttr("%s.outColor" % aiColor, "%s.subsurfaceColor" % self.newShader)



	def normal_texture(self, shadename=None):
		texture = cmds.shadingNode('file', name="%s_normal_tex" % shadename, asTexture=True,
								   isColorManaged=True)
		bump2d = cmds.shadingNode('bump2d', name="%s_b2d" % shadename, asUtility=True)
		cmds.connectAttr("%s.outAlpha" % texture, "%s.bumpValue" % bump2d)
		cmds.connectAttr("%s.outNormal" % bump2d, "%s.normalCamera" % self.newShader)
		cmds.setAttr("%s.bumpInterp" % bump2d, 1)


	def displace_texture(self, shadename=None):
		texture = cmds.shadingNode('file', name="%s_disp_tex" % shadename, asTexture=True,
								   isColorManaged=True)
		bump2d = cmds.shadingNode('bump2d', name="%s_b2d" % shadename, asUtility=True)
		cmds.connectAttr("%s.outAlpha" % texture, "%s.bumpValue" % bump2d)
		cmds.connectAttr("%s.outNormal" % bump2d, "%s.normalCamera" % self.newShader)


	def create_shader(self, shadename=None):
		if not shadename:
			shadename = "aiStandardSurface"

		self.newShader = cmds.shadingNode("aiStandardSurface", name="%s_MTL"%shadename,
										 asShader=True)
		#self.newShaderEngine = cmds.shadingNode("shadingEngine", name="%s_sg" % shadename,
										  #asUtility=True)
		#cmds.connectAttr("%s.outColor" % self.newShader, "%s.surfaceShader" %
						 #self.newShaderEngine)

		return self.newShader

