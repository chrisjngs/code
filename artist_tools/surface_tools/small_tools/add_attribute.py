#!/usr/bin/env python
#SETMODE 777

#----------------------------------------------------------------------------------------#
#------------------------------------------------------------------------------ HEADER --#

"""
:author:
    Chris Jennings

:synopsis:
    A one line summary of what this module does.

:description:
    A detailed description of what this module does.

:applications:
    Any applications that are required to run this script, i.e. Maya.

:see_also:
    Any other code that you have written that this module is similar to.

"""

#----------------------------------------------------------------------------------------#
#----------------------------------------------------------------------------- IMPORTS --#

# Built-in and Third Party
import maya.cmds as cmds
import random

# Modules That You Wrote

#----------------------------------------------------------------------------------------#
#--------------------------------------------------------------------------- FUNCTIONS --#

def add_float_attr(objs=None, attr_name=None):
    """
    This function adds a float attribute to the selected shapes.

    :param objs: The shapes that the attribute will be added to.
    :type: list

    :param attr_name: The name of the attribute that will be added.
    :type: string

    :return:
    """
    if not objs:
        print "Please pass in the object(s) you want the attribute added to."
        return None
    if not attr_name:
        print "Please specify the name of the new attribute."
        return None

    for obj in objs:
        cmds.addAttr(obj, longName=attr_name, attributeType="float")

def add_int_attr(objs=None, attr_name=None):
    """
    This function adds a int attribute to the selected shapes.

    :param objs: The shapes that the attribute will be added to.
    :type: list

    :param attr_name: The name of the attribute that will be added.
    :type: string

    :return:
    """
    if not objs:
        print "Please pass in the object(s) you want the attribute added to."
        return None
    if not attr_name:
        print "Please specify the name of the new attribute."
        return None

    for obj in objs:
        cmds.addAttr(obj, longName=attr_name, attributeType="long")


def random_float_attr(objs=None, attr_name=None, min_range=None, max_range=None):
    """
    This function assigns a random float value to an attribute.

    :param objs: The object(s) that have the attribute.
    :type: list

    :param attr_name: The name of the attribute that is being edited.
    :type: string

    :param min_range: The minimum value that can be assigned.
    :type: float

    :param max_range: The maximum value that can be assigned.
    :type: float

    :return:
    """
    if not objs:
        print "Please pass in the object(s) that has the attribute being edited"
        return None
    if not attr_name:
        print "Please specify the name of the attribute to be edited."
        return None
    if not min_range:
        print "Please specify the minimum value that can be assigned."
        return None
    if not max_range:
        print "please specify the maximum value that can be assigned."

    for obj in objs:
        value = random.randrange(min_range, max_range)
        cmds.setAttr("%s.%s"%(obj, attr_name), value)

#----------------------------------------------------------------------------------------#
#----------------------------------------------------------------------------- CLASSES --#

