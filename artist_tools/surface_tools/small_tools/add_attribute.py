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

def add_float_attr(objs=None,attr_name=None,min_range=None,max_range=None,default=None):
    """
    This function adds a float attribute to the selected shapes.

    :param objs: The shapes that the attribute will be added to.
    :type: list

    :param attr_name: The name of the attribute that will be added.
    :type: string

    :param min_range: The minimum range of the attribute.
    :type: float

    :param max_range: The maximum range of the attribute.
    :type: float

    :param default: The default value of the attribute.
    :type: float

    :return:
    """
    if not objs:
        print "Please pass in the object(s) you want the attribute added to."
        return None
    if not attr_name:
        print "Please specify the name of the new attribute."
        return None
    if not min_range:
        min_range=0.0
    if not max_range:
        max_range=1.0
    if not default:
        default=0

    for obj in objs:
        cmds.addAttr(obj,
                     longName=attr_name,
                     attributeType="float",
                     minValue=min_range,
                     maxValue=max_range,
                     defaultValue=default)

def add_int_attr(objs=None, attr_name=None, min_range=None, max_range=None, default=None):
    """
    This function adds a int attribute to the selected shapes.

    :param objs: The shapes that the attribute will be added to.
    :type: list

    :param attr_name: The name of the attribute that will be added.
    :type: string

    :param min_range: The minimum range of the attribute.
    :type: int

    :param max_range: The maximum range of the attribute.
    :type: int

    :param default: The default value of the attribute.
    :type: int

    :return:
    """
    if not objs:
        print "Please pass in the object(s) you want the attribute added to."
        return None
    if not attr_name:
        print "Please specify the name of the new attribute."
        return None
    if not min_range:
        min_range=0
    if not max_range:
        max_range=1
    if not default:
        default=0

    for obj in objs:
        cmds.addAttr(obj,
                     longName=attr_name,
                     attributeType="long",
                     minValue=min_range,
                     maxValue=max_range,
                     defaultValue=default)

def add_string_attr(objs=None, attr_name=None, value=None):
    """
    This function adds a string attribute to the selected shapes.
    :param objs: The shapes that the attribute will be added to.
    :type: list

    :param attr_name: The name of the attribute that will be added.
    :type: string

    :param value: The string value that is being added.
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
        cmds.addAttr(obj,
                     longName=attr_name,
                     dataType="string")
    if value:
        for obj in objs:
            cmds.setAttr("%s.%s" % (obj, attr_name), value, type="string")

def add_bool_attr(objs=None, attr_name=None, value=None):
    """
    This function adds a boolean attribute to the selected shapes.
    :param objs: The shapes that the attribute will be added to.
    :type: list

    :param attr_name: The name of the attribute that will be added.
    :type: string

    :param value: The boolean value that is being added.
    :type: bool
    :return:
    """
    if not objs:
        print "Please pass in the object(s) you want the attribute added to."
        return None
    if not attr_name:
        print "Please specify the name of the new attribute."
        return None

    for obj in objs:
        cmds.addAttr(obj, longName=attr_name, attributeType="bool")

    if value:
        for obj in objs:
            cmds.setAttr("%s.%s"%(obj, attr_name), value)


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

def random_string_attr(objs=None, attr_name=None, value=None):
    """
    This function takes a list of string values and randomly assigns them to the
    specified attribute on the specified object(s)
    :param objs: The object(s) that have the attribute
    :type: list

    :param attr_name: The name of the attribute that is being edited.
    :type: string

    :param value: A list of strings that will be assigned randomly to the attribute
    :type:list of strings
    :return:
    """
    if not objs:
        print "Please pass in the object(s) that has the attribute being edited"
        return None
    if not attr_name:
        print "Please specify the name of the attribute to be edited."
        return None
    if not value:
        print "please supply at least one (1) string that can be assigned."

    for obj in objs:
        ran_value = random.choice(value)
        cmds.setAttr("%s.%s"%(obj, attr_name), str(ran_value), type="string")

#----------------------------------------------------------------------------------------#
#----------------------------------------------------------------------------- CLASSES --#

