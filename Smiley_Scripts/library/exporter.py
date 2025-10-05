import maya.cmds as mc
import maya.mel as mel
import library.modules as md
import os

def make_dir_if_none_exists(dir_path):
    if dir_path:
        if not os.path.exists(dir_path):
            os.makedirs(dir_path)
    else:
        raise ValueError('No path set for directory.')
    
class fbx:
    def __init__(self):

        self.export_path = None
        self._file_name = None
        
        self._fbx_ver_dict = {"FBX 2020": "FBX202000", "FBX 2019": "FBX201900",
                             "FBX 2018": "FBX201800", "FBX 2016/2017": "FBX201600",
                             "FBX 2014/2015": "FBX201400", "FBX 2013": "FBX201300",
                             "FBX 2012": "FBX201200", "FBX 2011": "FBX201100",
                             "FBX 2010": "FBX201000", "FBX 2009": "FBX200900"}

        # empty dictionary to store every mesh with their translation values 
        self._obj_placement = {}

    def get_fbx_versions(self) -> dict:
        return self._fbx_ver_dict

    def set_file_name(self, file_name: str):
        self._file_name = file_name

    def set_UE_project_path(self, ue_path:str, folder_name='MayaImports'):
        # create a path inside the UE's project contents folder where the mesh will be exported to
        self.export_path = os.path.join(ue_path, 'Content', folder_name)

        make_dir_if_none_exists(self.export_path)
        
    def move_sel_to_origin(self, obj_selection):
        for obj in obj_selection:
            # store every obj with their translation values 
            self._obj_placement[obj] = mc.xform(obj, worldSpace=True, query=True, translation=True)
            # place the obj at the world origin [worldSpace=0,0,0]
            md.move_to_origin(obj)

    def place_sel_to_original_pos(self, obj_selection):
        for obj in obj_selection:
            md.place_mesh_back(self._obj_placement[obj], obj)
    
    def export_smoothing_groups(self, active: bool=False):
        mel_value = (str(active)).lower()
        mel.eval('FBXExportSmoothingGroups -v {}'.format(mel_value))

    def export_smooth_mesh(self, active: bool=False):
        mel_value = (str(active)).lower()
        mel.eval('FBXExportSmoothMesh -v {}'.format(mel_value))

    def export_tangents_binormals(self, active: bool=False):
        mel_value = (str(active)).lower()
        mel.eval('FBXExportTangents -v {}'.format(mel_value))

    def export_skinWeights(self, active: bool=False):
        mel_value = (str(active)).lower()
        mel.eval('FBXExportSkins -v {}'.format(mel_value))

    def export_blendShapes(self, active: bool=False):
        mel_value = (str(active)).lower()
        mel.eval('FBXExportShapes -v {}'.format(mel_value))

    def export_embedded_textures(self, active: bool=False):
        mel_value = (str(active)).lower()
        mel.eval('FBXExportEmbeddedTextures -v {}'.format(mel_value))

    def triangulate(self, active: bool=False):
        mel_value = (str(active)).lower()
        mel.eval('FBXExportTriangulate -v {}'.format(mel_value))

    def file_type(self, active: bool=False):
        mel_value = (str(active)).lower()
        mel.eval('FBXExportInAscii -v {}'.format(mel_value))

    def up_axis(self, value: bool=False):
        if value:
            mel.eval('FBXExportUpAxis y')
        else:
            mel.eval('FBXExportUpAxis z')
    
    def file_version(self, version: str="FBX 2018"):
        if version not in self._fbx_ver_dict.keys():
            raise ValueError(f'FBX version [{version}] not found or non-existent')
        
        for fbx, export_value in self._fbx_ver_dict.items():
            if fbx == version:
                print(f'Exported: {fbx} - {export_value}')
                mel.eval('FBXExportFileVersion -v {}'.format(export_value))

    def export(self):
        if not self._file_name:
            self._file_name = 'mayaExport.fbx'

        # if the user didn't add '.fbx' at the end of the file name, add it
        if not self._file_name.endswith('.fbx'):
            self._file_name += ".fbx"

        if not self.export_path:
            self.export_path = md.get_documents_folder()

        export_file = os.path.join(self.export_path, self._file_name)

        #'-f' stands for "File" & '-s' for "Selected"; the command exports the selected mesh into a .fbx file
        mel.eval('FBXExport -f "{}" -s'.format(export_file.replace('\\', '/')))