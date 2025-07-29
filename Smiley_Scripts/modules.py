import maya.cmds as mc
from pathlib import Path
import json
import os

# Module/functions library for all the plugin modules

# maya modules dependent functions
def move_to_origin(mesh) -> None:
    mc.move(0,0,0, mesh, rotatePivotRelative = True)

def place_mesh_back(values, mesh) -> None:
    mc.move(values[0],
            values[1],
            values[2], mesh, absolute=True)
    
def del_non_deform_history(mesh_sl:list) -> None:
    for obj in mesh_sl:
        if mc.nodeType(obj) != 'joint':
            # deletes the non-derformer history of the selected mesh
            # mc.bakePartialHistory(obj, prePostDeformers=True)
            print(obj)

# data handling related functions

def save_data(path:str, file_name:str, data) -> None:
    '''Saves data into a json file: must include a path to store data.'''
    if not file_name.endswith('.json'):
        file_name+='.json'

    with open(os.path.join(path, file_name), 'w') as file:
        json.dump(data, file, indent=4, sort_keys=True)

def load_data(path:str, file_name:str) -> dict:
    '''Loads the a path data (dictionary) from a json file.'''
    with open(os.path.join(path, file_name), 'r') as file:
        stored_data = json.load(file)

    return stored_data

# Directory related functions
def get_documents_folder() -> str:
    '''Finds the documents path inside the user's home directory.'''

    documents_path = os.path.join(str(Path.home()), 'Documents')
    return documents_path

def verify_path_exists(file_path: str) -> bool:
    '''Checks if a path or file path exists.'''

    if os.path.exists(file_path):
        return True
    
    else:
        return False
    

