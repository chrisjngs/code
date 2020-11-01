#!/usr/bin/env python
#SETMODE 777

#----------------------------------------------------------------------------------------#
#------------------------------------------------------------------------------ HEADER --#

"""
:author:
    Chris Jennings

:synopsis:
    This holds the logic for building elements of a shader.

:description:
    A detailed description of what this module does.

:applications:
    Maya.

:see_also:
    n/a.

"""

#----------------------------------------------------------------------------------------#
#----------------------------------------------------------------------------- IMPORTS --#

# Built-in and Third Party
import maya.cmds as cmds

# Modules That You Wrote

#----------------------------------------------------------------------------------------#
#--------------------------------------------------------------------------- FUNCTIONS --#

#----------------------------------------------------------------------------------------#
#----------------------------------------------------------------------------- CLASSES --#

class BuildShader(object):
    """
    This class holds the logic for building various parts of shaders.
    """

    def __init__(self, surface_name=None):
        """
        :param surface_name: The name of the shader.
        :type: str
        """
        self.surface_name = surface_name

    def check_name(self):
        """
        This function checks to make sure the user passed in a name. If they didn't it
        assigns a default one.
        :return:
        """
        if not self.surface_name:
            self.surface_name = 'noName'
            return self.surface_name
        else:
            return True

    def al_triplanar(self):
        """
        This function creates an alTriPlanar node graph.
        :return:
        """
        self.check_name()
        # Creates the nodes
        file_node = cmds.createNode('file')
        triplanar = cmds.createNode('alTriplanar')
        file_remap = cmds.createNode('alRemapFloat', name = '%s_ALR'%self.surface_name)

        # Connects the nodes together.
        cmds.connectAttr("%s.fileTextureName" % file_node, "%s.texture" % triplanar)
        cmds.connectAttr("%s.outColorR" % triplanar, "%s.input" % file_remap)

    def edge_wear(self):
        """
        This function creates the nodes needed for edge wear.
        :return:
        """
        self.check_name()
        # Creates the nodes
        edge_wear = cmds.createNode('alCurvature')
        edge_wear_mask = cmds.createNode('alGaborNoise')
        wear_comp = cmds.createNode('alCombineFloat')
        wear_remap = cmds.createNode('alRemapFloat')

        # Connects the nodes together.
        cmds.connectAttr("%s.outColorR" % edge_wear, "%s.input2" % wear_comp)
        cmds.connectAttr("%s.outValue" % wear_comp, "%s.input" % wear_remap)
        cmds.connectAttr("%s.outColorR" % edge_wear_mask, "%s.input1" % wear_comp)

    def create_dust(self):
        """
        This function creates the nodes for creating procedural dust.
        :return:
        """
        self.check_name()
        # Creates the nodes
        dust_node = cmds.createNode('alInputVector', name='dust_%s_AIV'%self.surface_name)
        remap = cmds.createNode('alRemapFloat', name='dust_%s_ARF'%self.surface_name)
        noise = cmds.createNode('alGaborNoise', name='dust_mask_AGN')
        dust_comp = cmds.createNode('alCombineFloat', name='dust_ACF')
        dust_remap = cmds.createNode('alRemapFloat', name='dust_intensity_ARF')

        # Connects the nodes together.
        cmds.connectAttr("%s.outValueY" % dust_node, "%s.input" % remap)
        cmds.connectAttr("%s.outValue" % remap, "%s.input2" % dust_comp)
        cmds.connectAttr("%s.outColorR" % noise, "%s.input1" % dust_comp)
        cmds.connectAttr("%s.outValue" % dust_comp, "%s.input" % dust_remap)

        # Sets some default values
        cmds.setAttr("%s.input" % dust_node, 2)
        cmds.setAttr("%s.space" % noise, 1)
        cmds.setAttr("%s.RMPcontrast" % noise, 0.35)

    def create_alsurface(self):
        """
        This function creates an alSurface shader.
        :return:
        """
        self.check_name()
        # Creates the nodes.
        shader = cmds.createNode('alSurface', name = "%s_M"%self.surface_name)
        disp   = cmds.createNode('displacementShader', name='disp_%s_M'%self.surface_name)
        sg     = cmds.createNode('shadingEngine', name = '%s_SG'%self.surface_name)
        diff   = cmds.createNode('alLayerColor', name = 'diff_%s_ALC'%self.surface_name)
        spec   = cmds.createNode('alLayerFloat', name='spec_%s_ALC' % self.surface_name)
        rough  = cmds.createNode('alLayerFloat', name='rough_%s_ALC' % self.surface_name)
        d_alf  = cmds.createNode('alLayerFloat', name='disp_%s_ALC' % self.surface_name)

        # Connects the nodes together.
        cmds.connectAttr("%s.outColor"%shader, "%s.aiSurfaceShader"%sg)
        cmds.connectAttr("%s.displacement" % disp, "%s.displacementShader" % sg)
        cmds.connectAttr("%s.outColor"%diff, "%s.diffuseColor"%shader)
        cmds.connectAttr("%s.outValue" % spec, "%s.specular1Strength" % shader)
        cmds.connectAttr("%s.outValue" % rough, "%s.specular1Roughness" % shader)
        cmds.connectAttr("%s.outValue" % d_alf, "%s.displacement" % disp)

        # Sets some default values.
        cmds.setAttr("%s.layer1"%spec, 1)
        cmds.setAttr("%s.layer1a"%spec, 1)
        cmds.setAttr("%s.layer1" % rough, 0.3)
        cmds.setAttr("%s.layer1a"%rough, 1)
        cmds.setAttr("%s.layer1"%diff, 0.5,0.5,0.5, type='double3')
        cmds.setAttr("%s.layer1a"%diff, 1)

















