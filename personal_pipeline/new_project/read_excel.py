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
    This Module will read through a given excel file and store its data in a list for
    access later.

:applications:
    Any applications that are required to run this script, i.e. Maya.

:see_also:
    Any other code that you have written that this module is similar to.

"""

#----------------------------------------------------------------------------------------#
#----------------------------------------------------------------------------- IMPORTS --#

# Built-in and Third Party

# Modules That You Wrote

#----------------------------------------------------------------------------------------#
#--------------------------------------------------------------------------- FUNCTIONS --#

#----------------------------------------------------------------------------------------#
#----------------------------------------------------------------------------- CLASSES --#

def start(filePath=None, column=0, exclude=0 ):
    '''
    This function calls the other functions and should be called to start the script.
    :return:
    '''

    # These checks are to make sure the correct information is being checked.
    if not filePath:
        print "You must provide a path to a excel file on disk to start."
        return
    if not column:
        column = 0
    if not exclude:
        exclude = 0

    # If the file path exists and is an excel file, then start storing the data in it.
    if validPath(filePath):
        storeData(filePath, column, exclude)



def validPath(filePath=None):
    '''
    This function checks to make sure the given file path is an excel file that exists.
    :return:
    '''

    path=filePath

    if path.endswith('xlsx'):
        # Testing line, delete later
        print "The filepath is valid"
        return True
    else:
        print "The given file path is not a valid excel file."
        return False



def storeData(excel=None, column=0, exclude=0):
    '''
    This function stores the data from the given column in a provided excel document into
    a list.
    :return:
    '''
    excelData = []


# The following lines are for testing and should be removed before final

start('D://Personal//Projects//WIP//_CurrentProject//MoonShop//Asset_List.xlsx')
start('D://Personal//Projects//WIP//_CurrentProject//MoonShop//Asset_List.txt')