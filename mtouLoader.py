# import modules
# this script will only run inside of Unreal's environment
from pathlib import Path
import unreal
import json
import os

def printTest():
    print('MtouLoader module')

class MtouLoader:
    '''
    Class to obtain and store the directory of the currently running UE Project.
    '''
    def __init__(self) -> None:
        # get the path directory of the currently running unreal engine project
        self._project_dir = unreal.Paths.project_dir()
        # get the absolute path of the UE path directory
        self._full_path = os.path.abspath(self._project_dir)
        # save the absolute path into a dictionary
        self._ue_dict = {'Current Project' : self._full_path.replace('\\', '/')}

    def save_path_to_json(self, home_path: str) -> None:
        '''Handles the storing of the UE path data (JSON) in a fixed directory.'''

        # create a fixed directory in the user's documents folder
        stored_data_dir = os.path.join(home_path,'UE','Info')
        # check if the path exists, if it doesn't exists create it
        if not os.path.exists(stored_data_dir):
            os.makedirs(stored_data_dir)
        # print the currently running UE project to view it in the output log inside Unreal
        print(self._ue_dict)
        directory = os.path.join(f'{stored_data_dir}', 'ue_path.json')
        # save the UE path dictionary data into a JSON in the specified directory
        with open(os.path.join(directory), 'w') as file:
            json.dump(self._ue_dict, file, indent=4, sort_keys=True)
        print(f'Project Path Directory stored in: {directory}')

    def get_documents_folder(self) -> str:
        '''Finds the user's home directory & documents folder where UE path dictornary will be stored.'''

        documents_path = os.path.join(str(Path.home()), 'Documents')
        return documents_path
    
def run_mtouLoader():
    ue_loader = MtouLoader()
    doc_folder = ue_loader.get_documents_folder()
    ue_loader.save_path_to_json(doc_folder)

printTest()
run_mtouLoader()



