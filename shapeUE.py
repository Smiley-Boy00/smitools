import maya.cmds as mc
import importlib
import sys
import os
# import package dependent modules
import library.modules as md
import library.customShapeUE as shpUE
from library import exporter

# DELETE importlib reloads for public release
importlib.reload(shpUE)

class unrealShapeUI:
    '''
    UI Display for creating control Rig Shapes. Requires a selected curve shape.
    Can call exporter module and load shape into the current UE project.
    '''
    def __init__(self, *args, windowUI=None):
        self._shape_selection = mc.ls(selection=True)
        if self._shape_selection:
            for each in self._shape_selection:
                shapeList=mc.listRelatives(each, shapes=True, type='nurbsCurve')
                if not shapeList:
                    mc.warning('Selection is not a curveShape!')
                    return

        else:
            mc.warning('No selection made.')
            return

        if windowUI:
            mc.deleteUI(windowUI, window=True)

        # create main UI window display
        self._windowID = 'UNREALSHAPE'
        windowTitle = 'UE Control Rig Shape Creator'
        size = (400,350)

        self._strokes_before = set(mc.ls(type="stroke"))
        self._temp_ue_shapes=[]

        if mc.window(self._windowID, exists=True):
            mc.deleteUI(self._windowID, window=True)

        self._windowDisplay = mc.window(self._windowID, title=windowTitle, widthHeight=size, sizeable=True)

        self._mainLayout = mc.formLayout(parent=self._windowDisplay)
        top_col = mc.columnLayout(adjustableColumn=True, rowSpacing=10)

        self._scaleValue = mc.floatSliderGrp(label='globalScale:', columnWidth=[(1,65), (2,80)], field=True, fieldMinValue=0.000, fieldMaxValue=1000.000, 
                                             minValue=1.000, maxValue=10.000, value=15.000, precision=3, 
                                             changeCommand=self.preview_shape, dragCommand=self.preview_shape)
        mc.setParent('..')

        # create button for the main tool functionality
        create_button = mc.button(label='Create UE Shape', command=self.create_ue_shape)
        
        # align UI layout
        mc.formLayout(self._mainLayout, edit=True, attachForm=[(top_col, 'top', 10), (top_col, 'left', 10), (top_col, 'right', 10),
                                                               (create_button, 'bottom', 10), (create_button, 'left', 10), (create_button, 'right', 10)],
                                                               attachControl=[(top_col, 'bottom', 5, create_button)])
        
        shpUE.ue_temp(self._shape_selection)
        self.preview_shape()

        mc.showWindow()

    def create_ue_shape(self, *args):
        scale=mc.floatSliderGrp(self._scaleValue, query=True, value=True)
        mc.select(self._shape_selection)
        shpUE.make_UE_shape(globalScale=scale)
        mc.deleteUI(self._windowID, window=True)

    def preview_shape(self, *args):
        scale=mc.floatSliderGrp(self._scaleValue, query=True, value=True)
    
        attributes=['tx', 'ty', 'tz', 'rx', 'ry', 'rz', 'sx', 'sy', 'sz', 'v']
        # find every newly created stroke node
        strokes_after = set(mc.ls(type="stroke"))
        strokes_created = list(strokes_after - self._strokes_before)
        for strokeShape in strokes_created:
            strokesTRN=mc.listRelatives(strokeShape, p=True)
            mc.setAttr(f'{strokeShape}.displayPercent', 100)
            mc.setAttr(f'{strokeShape}.sampleDensity', 15)
            for parentNode in strokesTRN:
                brushNode = mc.listConnections(parentNode + '.brush', source=True, destination=False)[0]
                self._temp_ue_shapes.append(parentNode)
                # Uncomment for Debugging Only
                # brushAttrs=mc.listAttr(brushNode)
                mc.setAttr(f'{brushNode}.color1', 1,1,0)
                mc.setAttr(f'{brushNode}.globalScale', scale)
            
        for tempShape in self._temp_ue_shapes:
            for attr in attributes:
                mc.setAttr(f'{tempShape}.{attr}', lock=True, keyable=False, channelBox=False)
        mc.select(clear=True)

        mc.window(self._windowID, edit=True, closeCommand=self.del_preview_shape)

    def del_preview_shape(self):
        print('delete temp shape')
        for tempShape in self._temp_ue_shapes:
            if mc.objExists(tempShape):
                mc.delete(tempShape)

class shapeExporterUI:
    '''
    Creates UI and handles export settings for unrealNodes into a loaded Unreal Engine Project.
    '''
    def __init__(self):
        self._window_ID = "SHAPEXPORTER"
        title = "Unreal Shape Exporter"
        size = (300,350)

        self._exportType=True
        # locate the user's home\Documents absolute path and
        # get the user's UE path directory data 
        # The data, for now, will be found under: C:\Users\[user]\Documents\UE\Info
        # get the ue_path.json file path directory
        self._folder_path = os.path.join(md.get_documents_folder(), 'UE', 'Info')
        self.filePath = os.path.join(f'{self._folder_path}', 'ue_path.json')

        # check if a UE project has been loaded
        # get the currently loaded UE Project path directory
        self.fileExists = md.verify_path_exists(self.filePath)

        if mc.window(self._window_ID, exists=True):
            mc.deleteUI(self._window_ID, window=True)

        self._windowDisplay = mc.window(self._window_ID, title=title, widthHeight=size, sizeable=True)

        self._mainLayout = mc.formLayout(parent=self._windowDisplay)
        top_col = mc.columnLayout(adjustableColumn=True, rowSpacing=10)

        mc.text(label='Export Settings:', font='boldLabelFont')
        mc.text(label='NOTE: This tool only exports custom unrealNodes.\nMake sure to have created an unrealNode shape prior to export.')

        self._exportCheck=mc.radioButtonGrp( label='Export:',numberOfRadioButtons=2, labelArray2=['Only Selected', 'All'], select=2,
                                            onCommand1=lambda args: self.query_settings(exportAll=False), 
                                            onCommand2=lambda args: self.query_settings(exportAll=True))
        mc.setParent('..')

        check_current_button = mc.button(label='Current UE Project', command=self.print_UE_project, parent=self._mainLayout)

        # create button for the main tool functionality
        create_button = mc.button(label='Export UE Shapes', command=self.export_shape)

        # align UI layout
        mc.formLayout(self._mainLayout, edit=True, attachForm=[(top_col, 'top', 10), (top_col, 'left', 10), (top_col, 'right', 10),
                                                               (create_button, 'bottom', 10), (create_button, 'left', 10), (create_button, 'right', 10),
                                                               (check_current_button, 'bottom', 10), (check_current_button, 'left', 10), (check_current_button, 'right', 10)],
                                                               attachControl=[(top_col, 'bottom', 5, check_current_button),
                                                                              (check_current_button, 'bottom', 8, create_button)])

        mc.showWindow()

    def query_settings(self, exportAll=True):
        self._exportType=exportAll

    def print_UE_project(self, *args) -> None:
        if self.fileExists:
            ue_path=md.load_data(self._folder_path, 'ue_path.json')
            ue_proj=ue_path.get("Current Project")
            # print and write path to script editor and command line outlog
            sys.stdout.write(f"Current UE Project: {ue_proj}\n")

        else:
            mc.warning('No UE project has been loaded.')
            return

    def export_shape(self, *args):
        if mc.ls(type='unrealNode'):
            fbx=exporter.fbx()
            if self._exportType:
                exportList=mc.ls(type='unrealNode')
                print('Export All')
            else:
                exportList=mc.ls(selection=True, type='unrealNode')
                if not exportList:
                    mc.warning('No UE Shape selected.')
                    return
                print('Export Selected Only')
            fbx.move_sel_to_origin(exportList)
            for ueNode in exportList:
                mc.select(ueNode)
                fileName=ueNode
                if '|' in ueNode:
                    fileName=ueNode.split('|')[1]
                ue_path=md.load_data(self._folder_path, 'ue_path.json')
                fbx.set_file_name(fileName)
                fbx.set_UE_project_path(ue_path['Current Project'], folder_name='ControlRigShapes')
                fbx.export_smoothing_groups(active=True)
                fbx.export_tangents_binormals(active=True)
                fbx.export()
                
            fbx.place_sel_to_original_pos(exportList)
            mc.select(clear=True)
            mc.deleteUI(self._window_ID, window=True)

        else:
            mc.warning('No UE Shape has been created!')
            return