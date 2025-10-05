import maya.cmds as mc
import os
import sys
# import package dependent modules
import library.modules as md
from library import exporter


class mtouExporterUI():
    '''
    Class that creates the Maya to Unreal Exporter window and runs the module script.
    Needs a UE 'Current Project' directory to export.
    '''
    def __init__(self) -> None:

        self.window_ID = "EXPORTER"
        self.title = "Maya to Unreal Exporter"
        self.size = (500, 500)

        if mc.window(self.window_ID, exists=True):
            mc.deleteUI(self.window_ID, window=True)

        self.windowDisplay = mc.window(self.window_ID, title=self.title, widthHeight=self.size, sizeable=True)

        self.main_layout = mc.formLayout(parent=self.windowDisplay)

        self._fbx = exporter.fbx()

        # locate the user's home\Documents absolute path and
        # get the user's UE path directory data 
        # The data, for now, will be found under: C:\Users\[user]\Documents\UE\Info
        # get the ue_path.json file path directory
        self._folder_path = os.path.join(md.get_documents_folder(), 'UE', 'Info')
        self.filePath = os.path.join(f'{self._folder_path}', 'ue_path.json')

        # check if a UE project has been loaded
        # get the currently loaded UE Project path directory
        self.fileExists = md.verify_path_exists(self.filePath)
        
        self.exportType_tab = mc.optionMenu(label='Export:', changeCommand=self.change_export_type)
        mc.menuItem(label="FBX")
        mc.menuItem(label="OBJ")
        
        mc.formLayout(self.main_layout, edit=True, attachForm = [(self.exportType_tab, 'left', 5), (self.exportType_tab, 'top', 10)],)

        self.exportType = "FBX"

        self.filename_field = mc.textFieldGrp(label='File Name:', placeholderText = 'Name your .fbx file')
        self.foldername_field = mc.textFieldGrp(label='Folder Name:', placeholderText = 'Name the Contents Folder', text = 'MayaImports')

        # empty dictionary to store and connect every check box object to its function
        self._checkerObjDict = {}
        self._checkerObjList = []
        self._tabObjDict = {}
        self._tabObjList = []
        self._separators = []

        # create dictionary for all the available FBX Maya export versions with their mel command line
        self._fbx_versions = self._fbx.get_fbx_versions()
        
        # build Maya Export Option Settings frame
        self.maya_frame = mc.frameLayout(label = 'Maya Export Settings', collapsable = True,
                                    backgroundColor=(0.25,0.46,0.88),
                                    highlightColor=(0.25,0.46,0.88), 
                                    parent=self.main_layout)

        self._maya_column = mc.columnLayout(adjustableColumn = True, parent=self.maya_frame)
        self._maya_checkRow = mc.rowLayout(numberOfColumns=4, generalSpacing=25, 
                                    adjustableColumn=2, columnAlign=(4, 'right'),
                                    parent=self._maya_column)

        self._leftMaya_column = mc.columnLayout(adjustableColumn=True, parent=self._maya_checkRow)
        self._centerLeftMaya_column = mc.columnLayout(adjustableColumn=True, parent=self._maya_checkRow)
        self._centerRightMaya_column = mc.columnLayout(adjustableColumn=True, parent=self._maya_checkRow)
        self._rightMaya_column = mc.columnLayout(adjustableColumn=True, parent=self._maya_checkRow)

        self.fbx_ui_settings()

        self.check_current_button = mc.button(label='Current UE Project', command=self.print_UE_project, parent=self.main_layout)
        self.export_button = mc.button(label='Export To Unreal', command=self._do_FBX_export, parent=self.main_layout)

        # align and place the layout's widgets in the display window
            
        mc.formLayout(self.main_layout, edit=True, attachForm = [(self.maya_frame, 'left', 5), (self.maya_frame, 'right', 5),
                                                                (self.exportType_tab, 'left', 5), (self.exportType_tab, 'top', 10)],
                                                                attachControl = [(self.filename_field, 'top', 10, self.exportType_tab),
                                                                                 (self.foldername_field, 'top', 10, self.filename_field),
                                                                                 (self.maya_frame, 'top', 10, self.foldername_field),])
        
        mc.formLayout(self.main_layout, edit=True, attachForm = [(self.export_button, 'left', 5), (self.export_button, 'right', 5),
                                                                (self.export_button, 'bottom', 5),
                                                                (self.check_current_button, 'left', 5), (self.check_current_button, 'right', 5),
                                                                (self.check_current_button, 'bottom', 5)],
                                                                attachControl = [(self.check_current_button, 'bottom', 8, self.export_button)])

        
        mc.showWindow()

    def fbx_ui_settings(self) -> None:
        # store the check box flags/values for every check box object that will be instantiated in the UI
        mayaFBX_checkBoxes = [
            {'label': 'Smoothing Groups', 'value': True, 'function': 'smooth_groups', 'position': 'left'},
            {'label': 'Smooth Mesh', 'value': False, 'function': 'smooth_mesh', 'position': 'left'},
            {'label': 'Tangents and Binormals', 'value': True, 'function': 'tangents', 'position': 'centerLeft'},
            {'label': 'Triangulate', 'value': False, 'function': 'triangulate', 'position': 'centerLeft'},
            {'label': 'Move to Origin', 'value': True, 'function': 'move_to_origin', 'position': 'centerRight'},
            {'label': 'Embed Textures', 'value': True, 'function': 'embed_media', 'position': 'centerRight'},
            {'label': 'Skinning', 'value': True, 'function': 'skins', 'position': 'right'},
            {'label': 'Blend Shapes', 'value': True, 'function': 'blnd_shapes', 'position': 'right'},
        ]


        # build all the checkers found in _maya_checkBoxes and position them in their corresponding column
        for index, checker in enumerate(mayaFBX_checkBoxes):
            if checker['position'] == 'left':
                parentUI = self._leftMaya_column
            elif checker['position'] == 'centerLeft':
                parentUI = self._centerLeftMaya_column
            elif checker['position'] == 'centerRight':
                parentUI = self._centerRightMaya_column
            elif checker['position'] == 'right':
                parentUI = self._rightMaya_column
            else:
                parentUI = self._leftMaya_column # default to left

            # create the check box object
            chk_obj = mc.checkBox(label = checker['label'],
                                parent=parentUI,
                                value = checker['value'])
            
            # add vertical spacer after every checker column except the last one
            if index < len(mayaFBX_checkBoxes)-1:
                separator_checkers = mc.separator(style='none', parent=parentUI, height=5)
                self._separators.append(separator_checkers)

            # connect the check box object to its function
            self._checkerObjDict[checker['function']] = chk_obj
            self._checkerObjList.append(chk_obj)

        lower_separator = mc.separator(style='none', height=10, parent=self._maya_column)
        self._separators.append(lower_separator)

        # build all the tab menus export settings
        exportAxis_tab = mc.optionMenu(label='Up Axis:', parent=self._maya_column)
        mc.menuItem(label="Y-Up")
        mc.menuItem(label="Z-Up")
        self._tabObjDict['axis'] = exportAxis_tab
        self._tabObjList.append(exportAxis_tab)

        fbxFileType_Tab = mc.optionMenu(label='FBX File Type:', parent=self._maya_column)
        mc.menuItem(label="Binary")
        mc.menuItem(label="Ascii")
        self._tabObjDict['fileType'] = fbxFileType_Tab
        self._tabObjList.append(fbxFileType_Tab)

        version_tab = mc.optionMenu(label='FBX Version:', parent=self._maya_column)
        for fbxKey in self._fbx_versions.keys():
            mc.menuItem(label=fbxKey)
        self._tabObjDict['version'] = version_tab
        self._tabObjList.append(version_tab)

    def obj_ui_settings(self) -> None:
        # store the check box flags/values for every check box object that will be instantiated in the UI
        mayaFBX_checkBoxes = [
            {'label': 'Move to Origin', 'value': True, 'function': 'move_to_origin', 'position': 'left'},
            {'label': 'Groups', 'value': True, 'function': 'groups', 'position': 'centerLeft'},
            {'label': 'Point Groups', 'value': True, 'function': 'ptgroups', 'position': 'centerLeft'},
            {'label': 'Materials', 'value': True, 'function': 'materials', 'position': 'centerRight'},
            {'label': 'Smoothing', 'value': True, 'function': 'smoothing', 'position': 'right'},
            {'label': 'Normals', 'value': True, 'function': 'normals', 'position': 'right'},
        ]


        # build all the checkers found in _maya_checkBoxes and position them in their corresponding column
        for index, checker in enumerate(mayaFBX_checkBoxes):
            if checker['position'] == 'left':
                parentUI = self._leftMaya_column
            elif checker['position'] == 'centerLeft':
                parentUI = self._centerLeftMaya_column
            elif checker['position'] == 'centerRight':
                parentUI = self._centerRightMaya_column
            elif checker['position'] == 'right':
                parentUI = self._rightMaya_column
            else:
                parentUI = self._leftMaya_column # default to left

            # create the check box object
            chk_obj = mc.checkBox(label = checker['label'],
                                parent=parentUI,
                                value = checker['value'])
            
            # add vertical spacer after every checker column except the last one
            if index < len(mayaFBX_checkBoxes)-1:
                separator_checkers = mc.separator(style='none', parent=parentUI, height=5)
                self._separators.append(separator_checkers)

            # connect the check box object to its function
            self._checkerObjDict[checker['function']] = chk_obj
            self._checkerObjList.append(chk_obj)

    def change_export_type(self, *args) -> None:
        export_type = mc.optionMenu(self.exportType_tab, query=True, value=True)
        if export_type=='OBJ':
            mc.textFieldGrp(self.filename_field, edit=True, placeholderText='Name your .obj file')
            self._clear_ui_panels()
            
            self.obj_ui_settings()
            
            mc.button(self.export_button, edit=True, command=self._do_OBJ_export)
        
        elif export_type=='FBX':
            mc.textFieldGrp(self.filename_field, edit=True, placeholderText='Name your .fbx file')
            self._clear_ui_panels()

            self._checkerObjList.clear()
            self._tabObjList.clear()
            self._separators.clear()

            self.fbx_ui_settings()
            
            mc.button(self.export_button, edit=True, command=self._do_FBX_export)

    def _clear_ui_panels(self) -> None:
        for checkers in self._checkerObjList:
            mc.deleteUI(checkers)
        for separators in self._separators:
            mc.deleteUI(separators)
        for tabs in self._tabObjList:
            mc.deleteUI(tabs)
            
        self._checkerObjList.clear()
        self._tabObjList.clear()
        self._separators.clear()

    def print_UE_project(self, *args) -> None:
        if not self.fileExists:
            mc.warning('No UE project has been loaded.')
            return
        
        if self.fileExists:
            ue_path=md.load_data(self._folder_path, 'ue_path.json')
            ue_proj=ue_path.get("Current Project")
            # print and write path to script editor and command line log
            sys.stdout.write(f"Current UE Project: {ue_proj}\n")

    def _get_checkbox_state(self, name) -> bool:
        '''Returns the query of a check box object based on the object function's name as long as it exists.'''
        return mc.checkBox(self._checkerObjDict[name], query=True, value=True)

    def _do_FBX_export(self, *args) -> None:
        '''Handles the fbx the FBX export procedure. Checks that there's no user input error before exporting.'''

        # get and store check box object query state 
        smooth_grps = self._get_checkbox_state('smooth_groups')
        smooth_mesh = self._get_checkbox_state('smooth_mesh')
        tangents = self._get_checkbox_state('tangents')
        triangulate = self._get_checkbox_state('triangulate')
        move_mesh = self._get_checkbox_state('move_to_origin')
        embed_tex = self._get_checkbox_state('embed_media')
        blnd_shapes = self._get_checkbox_state('blnd_shapes')
        skins = self._get_checkbox_state('skins')

        #creates a list of the selected mesh/es
        mesh_selection = mc.ls(selection = True)

        if not self.fileExists:
            mc.warning('No UE project has been loaded for export!')
            return

        if not mesh_selection:
            mc.warning("Please select a mesh to export.")
            return
        
        # query the user's file & folder name
        mesh_file = mc.textFieldGrp(self.filename_field, query=True, text=True)
        folder_name = mc.textFieldGrp(self.foldername_field, query=True, text=True)

        if not mesh_file:
            mc.warning('Please name for your file for export.')
            return


        ue_dict = md.load_data(self._folder_path, 'ue_path.json')
        ue_project_path = ue_dict.get('Current Project')

        if folder_name:
            # create a path inside the UE's project contents folder where the mesh will be exported to
            self._fbx.set_UE_project_path(ue_project_path, folder_name)
        else:
            mc.warning('Please provide a folder name to export.')
            return

        self._fbx.set_file_name(mesh_file)

        if move_mesh:
            self._fbx.move_sel_to_origin(mesh_selection)

        # do value/settings evaluations before exporting mesh into file
        # evaluate if the mesh's file will be exported with Smoothing Groups information in the file
        if smooth_grps:
            self._fbx.export_smoothing_groups(True)
        else:
            self._fbx.export_smoothing_groups()

        # evaluate if the mesh will be Subdivided once exported
        if smooth_mesh:
            self._fbx.export_smooth_mesh(True)
        else:
            self._fbx.export_smooth_mesh()

        # evaluate if the mesh's file will contain Tangents & Binormals information data in the file
        if tangents:
            self._fbx.export_tangents_binormals(True)
        else:
            self._fbx.export_tangents_binormals()

        # evaluate if the mesh will be Triangulated before importing into the Game Engine
        if triangulate:
            self._fbx.triangulate(True)
        else:
            self._fbx.triangulate()

        # evaluate if the mesh will be exported it's Skin deformation data
        if skins:
            self._fbx.export_skinWeights(True)
        else:
            self._fbx.export_skinWeights()

        # evaluate if the mesh's file will contain geometry Blend Shapes from the current scene
        if blnd_shapes:
            self._fbx.export_blendShapes(True)
        else:
            self._fbx.export_blendShapes()

        # evaluate if the mesh's file will be exported with Embedded media/textures
        if embed_tex:
            self._fbx.export_embedded_textures(True)
        else:
            self._fbx.export_embedded_textures()

        # evaluate with what axis the mesh will be exported in (Y-Up or Z-Up)
        axisValue = mc.optionMenu(self._tabObjDict['axis'], query=True, value=True)
        if axisValue == 'Y-Up':
            self._fbx.up_axis(True)
        else:
            self._fbx.up_axis()

        # evaluate if the FBX will be exported as Ascii or Binary
        fbxFileType=mc.optionMenu(self._tabObjDict['fileType'], query=True, value=True)
        if fbxFileType == "Ascii":
            self._fbx.file_type(True)
        else:
            self._fbx.file_type()

        # evaluate which FBX version will the mesh be exported in    
        fbxVersion = mc.optionMenu(self._tabObjDict['version'], query=True, value=True)
        print(fbxVersion)
        for fbxKey in self._fbx_versions.keys():
            if fbxKey == fbxVersion:
                self._fbx.file_version(fbxKey)

        self._fbx.export()
        
        self._fbx.place_sel_to_original_pos(mesh_selection)

        # closes the window after the program executes successfully
        mc.deleteUI(self.windowDisplay, window=True)

    def _do_OBJ_export(self, *args) -> None:
        if not self.fileExists:
            mc.warning('No UE project has been loaded for export!')
            return

        move_mesh = self._get_checkbox_state('move_to_origin')
        obj_groups = self._get_checkbox_state('groups')
        obj_ptgroups = self._get_checkbox_state('ptgroups')
        obj_materials = self._get_checkbox_state('materials')
        obj_smoothing = self._get_checkbox_state('smoothing')
        obj_normals = self._get_checkbox_state('normals')

        #creates a list of the selected mesh/es
        mesh_selection = mc.ls(selection = True)

        if not mesh_selection:
            mc.warning("Please select a mesh to export.")
            return
        
        # query the user's file & folder name
        mesh_file = mc.textFieldGrp(self.filename_field, query=True, text=True)
        folder_name = mc.textFieldGrp(self.foldername_field, query=True, text=True)

        if not mesh_file:
            mc.warning('Please name for your file for export.')
            return
        if not mesh_file.endswith('.obj'):
            mesh_file += ".obj"
        
        ue_dict = md.load_data(self._folder_path, 'ue_path.json')
        ue_project_path = ue_dict.get('Current Project')

        if folder_name:
        # create a path inside the UE's project contents folder where the mesh will be exported to
            export_path = os.path.join(ue_project_path, 'Content', folder_name)
        else:
            mc.warning('Please provide a folder name to export.')
            return     

        #if the path doesn't exist (os.path.exists) create the path (os.makedirs())
        if not os.path.exists(export_path):
            os.makedirs(export_path)
            
        # if the user didn't add '.obj' at the end of the file name, add it
        export_file = os.path.join(export_path, mesh_file)

        # md.del_non_deform_history(mesh_selection)

        # empty dictionary to store every mesh with their translation values 
        obj_placement = {}

        if move_mesh:
            for mesh in mesh_selection:
                # store every mesh with their translation values 
                obj_placement[mesh] = mc.xform(mesh, worldSpace=True, query=True, translation=True)
                # place the mesh at the world origin [worldSpace=0,0,0]
                md.move_to_origin(mesh)

        mc.select(clear=True)
        tempGRP=mc.group(empty=True, name='temp_GRP')
        for obj in mesh_selection:
            mc.parent(obj, tempGRP)
            mc.rotate(90,0,0, tempGRP)

        # evaluate if the OBJ file will contain group information
        if obj_groups:
            groups=1
        else:
            groups=0
        
        # evaluate if the OBJ file will contain point groups information
        if obj_ptgroups:
            ptgroups=1
        else:
            ptgroups=0

        # evaluate if the OBJ file will contain materials information
        if obj_materials:
            materials=1
        else:
            materials=0

        # evaluate if the OBJ file will contain smoothing groups information
        if obj_smoothing:
            smoothing=1
        else:
            smoothing=0

        # evaluate if the OBJ file will contain normals information
        if obj_normals:
            normals=1
        else:
            normals=0

        # evaluate the user's settings and store them in a tuple for exporting
        export_settings = (f'groups={groups};'
                            f'ptgroups={ptgroups};'
                            f'materials={materials};'
                            f'smoothing={smoothing};'
                            f'normals={normals}')
        
        print(export_settings)
        print(export_file)

        # force export selected mesh to Unreal
        # ignore non-crucial errors
        try:
            mc.file(export_file, force=True, options=export_settings, typ="OBJexport", exportSelected=True)
            print("Export completed")
        except Exception as e:
            print(f"Export completed with warnings: {e}")

        mc.rotate(0,0,0, tempGRP)
        for obj in mesh_selection:
            mc.parent(obj, world=True)
            mc.delete(tempGRP)

        # place the mesh back to the original/starting position
        for mesh in mesh_selection:
            md.place_mesh_back(obj_placement[f'{mesh}'], mesh)

        # closes the window after the program executes successfully
        mc.deleteUI(self.windowDisplay, window=True)
        



        

