#!/usr/bin/env python
# SETMODE 777

# ----------------------------------------------------------------------------------------#
# ------------------------------------------------------------------------------ HEADER --#

"""
:author:
    Chris Narro

:synopsis:
    This script makes and applies the bend and twist deformers to an object.
    It's assumend that the object is a hair card.

:description:
    A detailed description of what this module does.

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

# ----------------------------------------------------------------------------------------#
# --------------------------------------------------------------------------- FUNCTIONS --#

# ----------------------------------------------------------------------------------------#
# ----------------------------------------------------------------------------- CLASSES --#
class HairCardSetup(object):

    def __init__(self):
        """

        """
        self.shape_dict = {}
        self.pivot_dict = {}
        self.twist_handle = None
        self.bend_handles = []
        self.orig_cards = []
        self.new_card = None

    def get_sel(self):
        """
        Gets the current selection and adds them to a dictionary under the key
        'cards'
        """
        self.orig_cards = cmds.ls(sl=1)
        self.shape_dict["cards"] = []
        # Build a dictionary for selected self.orig_cards that holds their name and
        # pivot information.
        for card in self.orig_cards:
            self.pivot_dict ={
                "card":str(card),
                "translation": self.get_pivot(shape=card, trans=True),
                "rotation": self.get_pivot(shape=card, rot=True)
            }
            self.shape_dict["cards"].append(self.pivot_dict)

    def get_pivot(self, shape=None, trans=False, rot=False):
        """
        Gets the world position of a pivot for a given shape.
        """
        if shape:
            if trans:
                pivot_trans = cmds.xform(shape, query=True, worldSpace=True,
                                         translation=True)
                return pivot_trans
            elif rot:
                pivot_rot = cmds.xform(shape, query=True, objectSpace=True,
                                       rotation=True)
                return pivot_rot
            else:
                print ("You must indicate what pivot information you want. Call again with"
                       "either the 'trans' or 'rot' variables set to True")
        if not shape:
            print ("There was no shape given to get a pivot of. Call the function again "
                   "but pass'shape'")


    def setup_card(self, update=False, del_old=None):
        """
        Calls twist_mod() and bend_mod() to apply them to the currently selected card.
        """
        self.get_sel()

        if update:
            count = 0
            for x in self.shape_dict["cards"]:
                # I'm using count so that the original card isn't counted as an old card.
                if count > 0:
                    self.new_card = self.dup_card(base_card=self.orig_cards[0])
                    if not x["card"] == str(self.orig_cards[0]):
                        #print(new_card)
                        self.twist_mod(shape=self.new_card[0])
                        self.bend_mod(shape=self.new_card[0])
                        self.update_card(new=self.new_card[0], old=x["card"])
                        self.move_card(new=self.new_card[0], target=x["card"])
                        if del_old:
                            self.delete_card(x["card"])
                else:
                    count = count+1
        else:
            #For every shape that was selected, create a twist and bend modifier.
            #print(self.shape_dict)
            for x in self.shape_dict["cards"]:
                self.twist_mod(shape = x["card"])
                self.bend_mod(shape = x["card"])
            #print self.shape_dict["cards"][0]["card"]

            cmds.select(self.orig_cards)

    def dup_card(self, base_card=None):
        """
        :param base_card:
        :return:
        """
        return cmds.duplicate(base_card)

    def delete_card(self, card=None):
        """

        :param card:
        :return:
        """
        cmds.delete(card)

    def move_card(self, new=None, target=None):
        """

        :param new:
        :param target:
        :return:
        """
        #print("Moving %s to %s"%(new, target))
        count = 0
        list_len = len(self.shape_dict["cards"])
        while count < list_len:
            if self.shape_dict["cards"][count]["card"]==target:
                trans_x = self.shape_dict["cards"][count]["translation"][0]
                trans_y = self.shape_dict["cards"][count]["translation"][1]
                trans_z = self.shape_dict["cards"][count]["translation"][2]

                rot_x = self.shape_dict["cards"][count]["rotation"][0]
                rot_y = self.shape_dict["cards"][count]["rotation"][1]
                rot_z = self.shape_dict["cards"][count]["rotation"][2]

                break
            else:
                count = count + 1
        cmds.move(trans_x, trans_y, trans_z, new)
        cmds.rotate(rot_x,rot_y,rot_z, new)

    def update_card(self, new=None, old=None):
        """

        :param old:
        :param new:
        :return:
        """
        cmds.select(old)
        old_card = cmds.ls(sl=1)
        #print(self.bend_handles)

        # check if the attr exists and then set values if it does
        if cmds.attributeQuery("Twist_Tip", node=old_card[0], exists=True):
            twist = cmds.getAttr(old_card[0], ".Twist_Tip")
            cmds.setAttr("%s.Twist_Tip" % new, float(twist))

        # check if the attr exists and then set values if it does
        if cmds.attributeQuery("Twist_Root", node=old_card[0], exists=True):
            twist = cmds.getAttr(old_card[0], ".Twist_Root")
            cmds.setAttr("%s.Twist_Root" % new, float(twist))

        # check if the attr exists and then set values if it does
        if cmds.attributeQuery("Bend_UpDown", node=old_card[0], exists=True):
            # Get the incoming connections from the old card to find the bend deformer
            history_nodes = cmds.listHistory(old_card)

            # check each connection for the bendHandleShape
            for node in history_nodes:
                if node == "%sup_down_bendHandleShape"%old_card[0]:
                    # Check to make sure the shape has the lowBound attr
                    if cmds.attributeQuery("lowBound", node=node, exists=True):
                        # Try to get the value of the lowBound and store it in low
                        try:
                            cmds.select(node)
                            low = cmds.getAttr(node, ".lowBound")
                            break
                        except:
                            print("no .lowBound attr was found on %s"%node)
            # First select the old card to get its attribute.
            cmds.select(old_card[0])
            Bend_UpDown = cmds.getAttr(old_card[0], ".Bend_UpDown")
            # Then set the attributes on the new card and deformer
            cmds.setAttr("%s.lowBound"%self.bend_handles[0][1], low)
            cmds.setAttr("%s.Bend_UpDown" % str(new), float(Bend_UpDown))

        # check if the attr exists and then set values if it does
        if cmds.attributeQuery("Bend_LeftRight", node=old_card[0], exists=True):
            #print(self.bend_handles[1])
            history_nodes = cmds.listHistory(old_card)
            for node in history_nodes:
                if node == "%sleft_right_bendHandleShape"%old_card[0]:
                    # Check to make sure the shape has the lowBound attr
                    if cmds.attributeQuery("lowBound", node=node, exists=True):
                        # Try to get the value of the lowBound and store it in low
                        try:
                            cmds.select(node)
                            low = cmds.getAttr(node, ".lowBound")
                            break
                        except:
                            print("no .lowBound attr was found on %s"%node)

            cmds.select(old_card[0])
            cmds.setAttr("%s.lowBound" % self.bend_handles[1][1], low)
            Bend_LeftRight = cmds.getAttr(old_card[0], ".Bend_LeftRight")
            cmds.setAttr("%s.Bend_LeftRight" % str(new), float(Bend_LeftRight))

    def twist_mod(self, shape=None):
        """
        Creates a twist modifier on the given shape. Expects the shape of a hair card.
        """
        cmds.select(shape)
        self.twist_handle = cmds.nonLinear(type="twist", name="%s_twist" % shape,
                                           autoParent=True)

        # Check if the 'Twist' attribute exists on the shape node
        if not cmds.attributeQuery("Twist_Tip", node=shape, exists=True):
            self.create_attr(name="Twist_Tip", shape=shape)

        if not cmds.attributeQuery("Twist_Root", node=shape, exists=True):
            self.create_attr(name="Twist_Root", shape=shape)

        self.connect_attr("%s.Twist_Tip"%shape, "%s.startAngle"%self.twist_handle[1])
        self.connect_attr("%s.Twist_Root"%shape, "%s.endAngle"%self.twist_handle[1])
        cmds.hide(self.twist_handle[1])

    def bend_mod(self, shape=None):
        """
        Creates a bend modifier on the given shape. Expects the shape of a hair card
        with the pivot located at it's base.
        """
        cmds.select(shape)
        bend_handle_UD = cmds.nonLinear(type="bend", name="%sup-down_bend" % shape,
                                             autoParent=True)
        cmds.select(shape)
        bend_handle_LR = cmds.nonLinear(type="bend", name="%sleft-right_bend" % shape,
                                          autoParent=True)
        # Check to see if there is already a bend attribute created for the shape.
        # If there isn't, create one.
        if not cmds.attributeQuery("Bend_UpDown", node=shape, exists=True):
            #print ("no existing attribute on shape")
            self.create_attr(name="Bend_UpDown", shape=shape)
        if not cmds.attributeQuery("Bend_LeftRight", node=shape, exists=True):
            #print ("no existing attribute on shape")
            self.create_attr(name="Bend_LeftRight", shape=shape)

        count = 0
        list_len = len(self.shape_dict["cards"])
        while count < list_len:

            #if self.shape_dict["cards"][count]["card"]==shape or (shape==self.new_card[
            # 0]):
            if self.shape_dict["cards"][count]["card"] == shape or (
                    self.new_card and self.new_card[0] == shape):

                trans_x = self.shape_dict["cards"][count]["translation"][0]
                trans_y = self.shape_dict["cards"][count]["translation"][1]
                trans_z = self.shape_dict["cards"][count]["translation"][2]

                # Move and rotate the up_down bend handle
                cmds.move(trans_x, trans_y, trans_z, bend_handle_UD)
                cmds.setAttr("%s.ry" % bend_handle_UD[1], 90)
                cmds.setAttr("%s.lowBound" % bend_handle_UD[0], -2)
                cmds.setAttr("%s.highBound" % bend_handle_UD[0], 0)

                # More the left_right bend handle
                cmds.move( trans_x, trans_y, trans_z, bend_handle_LR)
                cmds.setAttr("%s.lowBound"%bend_handle_LR[0], -2)
                cmds.setAttr("%s.highBound" % bend_handle_LR[0], 0)

                self.connect_attr("%s.Bend_UpDown" % shape,
                                  "%s.curvature" % bend_handle_UD[1])

                self.connect_attr("%s.Bend_LeftRight"%shape,
                                  "%s.curvature"%bend_handle_LR[1])

                self.bend_handles.append(bend_handle_UD)
                self.bend_handles.append(bend_handle_LR)
                cmds.hide(bend_handle_UD)
                cmds.hide(bend_handle_LR)
                break
            else:
                count = count + 1

    def create_attr(self, name=None, shape=None):
        """
        This creates an attribute on a given shape.
        """
        cmds.select(shape)
        if name == "Bend_UpDown":
            cmds.addAttr(longName=name, defaultValue=0, minValue=-180, maxValue=180,
                         keyable=True)

        if name == "Bend_LeftRight":
            cmds.addAttr(longName=name, defaultValue=0, minValue=-180, maxValue=180,
                         keyable=True)

        if name == "Twist_Tip":
            cmds.addAttr(longName=name, keyable=True)

        if name == "Twist_Root":
            cmds.addAttr(longName=name, keyable=True)

    def connect_attr(self, orig_attr=None, target_attr=None):
        """
        This connects two different attributes, one from a deformer and the other to
        a custom attribute on a shape.
        """
        if orig_attr and target_attr:
            cmds.connectAttr(orig_attr, target_attr)
        else:
            print ("You must pass two different attributes to connect together")
