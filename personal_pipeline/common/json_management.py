#!/usr/bin/env python
# SETMODE 777

# ----------------------------------------------------------------------------------------#
# ------------------------------------------------------------------------------ HEADER --#

"""
:author:
    Chris Narro

:synopsis:
    A one line summary of what this module does.

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
import json
import os

# Modules That You Wrote

# ----------------------------------------------------------------------------------------#
# --------------------------------------------------------------------------- FUNCTIONS --#
def write_json(filepath=None, data=None):
    """
    This writes data to a json file.
    """
    if not data:
        print("No data was provided, exiting the write.")
        return

    with open(filepath, "w") as f:
        json.dump(data, f, indent=4)

def load_json(filepath=None):
    """
    Loads the data from an existing .json file.
    """
    with open(filepath, "r") as f:
        existing_data = json.load(f)

    return existing_data

def append_json(filepath=None, new_data=None):
    """
    Updates an existing json file.
    """
    if not filepath:
        return False

    if not new_data:
        print("No new data was provided, exiting the .json update.")
        return

    existing_data = load_json(filepath)

    if not isinstance(existing_data, list):
        existing_data = []  # Create a list if the data is not a list

    if isinstance(new_data, list):  # Check if the new data is also a list
        existing_data.extend(new_data)  # Use extend to add multiple items from list
    else:
        existing_data.append(new_data)  # Append the new data to the list
    write_json(filepath, existing_data)

def update_json(filepath=None, key=None, new_value=None, note=None):
    """
    Updates a value in an existing json file.
    :param filepath: The filepath of the json file.
    :param key: The key that needs its value changed.
    :param new_value: The new value that will be assigned.
    :param note: The note that the key belongs to.
    :return:
    """

    if not os.path.exists(filepath):
        print("The provided filepath does not exist. Exiting the .json update.")
        return False
    if not new_value and not new_value == False:
        print("No new value was provided, exiting the .json update.")
        return
    if not key:
        print("No key was given to update. Exiting the .json update.")
        return

    existing_data = load_json(filepath)
    indexes = len(existing_data)
    count = 0
    try:
        if existing_data["first_note"]:
            print (existing_data[key])
            existing_data[key] = new_value
            write_json(filepath, existing_data)
            return
    except:
        count = 0
        while count < indexes:
            # compare the note in the listed dict to the one passed. If it matches modify
            # the desired key
            print("here %s"%count)
            print existing_data["note"]
            #print existing_data[count]["note"]
            if existing_data[count]["note"] == note:
                print ("check")
                existing_data[count][key] = new_value
                write_json(filepath, existing_data)
                return
            count = count+1

        print("No note was found to match the provided one. Check that your note exists and "
              "then try again.")
        return

# ----------------------------------------------------------------------------------------#
# ----------------------------------------------------------------------------- CLASSES --#
