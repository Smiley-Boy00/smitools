import maya.cmds as mc
import os
# import package dependent modules
import library.modules as md
import library.shapes as shp
import library.ctrlSaver as svr
import shapeUE as ueUI

# CHANGE plugin info from Smiley_Dev to Smiley_Tools for public release
plugin_path = mc.pluginInfo("Smiley_Tools.py", query = True, path = True)
scripts_dir = os.path.join(os.path.dirname(plugin_path), 'Smiley_Scripts')
DATA_PATH = os.path.join(scripts_dir, 'library', 'data')
IMGS = os.path.join(scripts_dir, 'library', 'imgs')

class shapeLibraryUI:
    ''''
    Displays shapes that can be created for building control rigs.
    Can save selected shapes into the library; can create UE control rig shapes.
    '''
    def __init__ (self):
        # set empty variables for functions to query class data
        # name of the shape that will be stored
        self._shapeLabel = None
        # customizable name label for the shape (won't store the name given in the outliner)
        self._new_shapeLabel = None
        # to store the saving shape settings
        self._saveSettingsSHP = None
        # list to add and delete new shape icons into the scroll ui
        self._customShapeList = []
        self._mainWindowID = 'SHAPELIBRARY'
        windowTitle = 'Flexible Shapes Library'
        size = (400,450)

        if mc.window(self._mainWindowID, exists=True):
            mc.deleteUI(self._mainWindowID, window=True)      

        self._windowDisplay = mc.window(self._mainWindowID, title=windowTitle, widthHeight=size, sizeable=True)
        # create & display settings
        self._mainLayout = mc.formLayout(parent=self._windowDisplay)
        top_col = mc.columnLayout(adjustableColumn=False, rowSpacing=10)

        self._shape_frame = mc.frameLayout(borderVisible=True, labelVisible=False, width=560, height=400, generalSpacing=20)
        shape_scroll = mc.scrollLayout(parent=self._shape_frame, horizontalScrollBarThickness=0)
        # place every selectable shape icon UI starting from the default circle and square 
        self._shape_gridLayout = mc.gridLayout(numberOfColumns=4, cellWidthHeight=[135,150], parent=shape_scroll)

        self._shape_collection = mc.iconTextRadioCollection('shapeCollection')

        self._circleShape = mc.iconTextRadioButton(image1=os.path.join(IMGS, 'Circle.jpg'), label='circle', style='iconAndTextVertical', onc=self.set_circle_shape, 
                                                   collection=self._shape_collection, parent=self._shape_gridLayout)
        self._squareShape = mc.iconTextRadioButton(image1=os.path.join(IMGS, 'Square.jpg'), label='square', style='iconAndTextVertical', onc=self.set_square_shape, 
                                                   collection=self._shape_collection, parent=self._shape_gridLayout)
        self.update_shapes_ui()
        mc.setParent('..')
        mc.setParent('..')
        mc.setParent('..')
        mc.setParent('..')
        mc.setParent('..')

        bottom_col = mc.columnLayout(adjustableColumn=True, rowSpacing=10)

        mc.button(label='Save a Selected Shape', command=self.save_shape_ui)

        # shape name input
        self._name_textField = mc.textFieldGrp(label='Name:', placeholderText='Name your controller shape', columnWidth=[2,250])

        self._scaleValue = mc.intSliderGrp(label='Scale:', columnWidth=[(1,50), (2,80)], field=True, fieldMinValue=1, fieldMaxValue=1000, minValue=1, maxValue=10, value=1)

        mc.rowColumnLayout(numberOfColumns=4,
                           columnWidth=[(1, 195), (2, 80), (3, 65), (4, 80)],
                           columnAttach=[(1, 'right', 1.5), (2, 'left', 1.5), (3, 'right', 1.5), (4, 'left', 1.5)],
                           columnAlign=[(1, 'right'), (2, 'left'), (3, 'right'), (4, 'left')])

        # create & display settings
        # prefix and suffix input & checker
        self._prefix_check = mc.checkBox(label='Prefix:', value=False, onc=self.prefix_on, ofc=self.prefix_off)
        self._prefix_textField = mc.textFieldGrp(text='M_', columnWidth=[(1,50), (2,80)], enable=False) 

        self._suffix_check = mc.checkBox(label='Suffix:', value=True, onc=self.suffix_on, ofc=self.suffix_off)
        self._suffix_textField = mc.textFieldGrp(text='_CTRL', columnWidth=[(1,50), (2,80)], enable=True)
        mc.setParent('..')
        
        mc.frameLayout(labelVisible=False)
        mc.rowColumnLayout(numberOfColumns=2, columnWidth=[(1, 90), (2, 150)], columnAttach=(1, 'right', 10))
        
        self._colorTab = mc.optionMenu(changeCommand=self.swap_colorUI)
        mc.menuItem(label='Index')
        mc.menuItem(label='RBG/HSV')
        mc.setParent('..') # back to color_frame

        # color selection (Can be selected by index palette or with RGB/HSV values)
        mc.columnLayout(adjustableColumn=True)
        self._framePalette=mc.frameLayout(labelVisible=0, height=160, visible=True)

        # create color index (rgb) list
        colors = []
        excluded = [0,1,2,3,5,14,16,19]
        for i in range(0, 32):
            if i not in excluded:
                colour = mc.colorIndex(i, query=True)
                colors.append(colour)
        # create palettePort with maya's override colors
        # make grid of 8 columns and 3 rows to display color palette
        self._colorPalette=mc.palettePort(dim=(8, 3), topDown=True, height=100, width=50, visible=True)
        for i, colour in enumerate(colors):
            mc.palettePort(self._colorPalette, edit=True, rgbValue=(i, colour[0], colour[1], colour[2]))
        
        # create alternative color selection option UI
        self._colorRGBWidget = mc.colorInputWidgetGrp(label='Value:', rgb=(1, 1, 0), columnWidth=[(1,45), (2,150)], visible=False)
        mc.setParent('..')
        mc.setParent('..')
        mc.setParent('..')
        mc.setParent('..')

        # create button to open ueShape UI module
        createUE_button = mc.button(label='Create UE Shape', command=self.load_ue_shape)

        # create button for the main tool functionality
        create_button = mc.button(label='Create Shapes', command=self.create_shapes)

        # align the display's layout
        
        mc.formLayout(self._mainLayout, edit=True, attachForm=[(top_col,'right', 10), (top_col, 'left', 10), (top_col, 'top', 10),
                                                               (bottom_col,'right', 10), (bottom_col, 'left', 10), (bottom_col, 'top', 10),
                                                               (create_button, 'right', 5), (create_button, 'left', 5), (create_button, 'bottom', 5),
                                                               (createUE_button, 'right', 5), (createUE_button, 'left', 5), (createUE_button, 'bottom', 5),],
                                                               attachControl=[(bottom_col, 'top', 5, top_col),
                                                                              (bottom_col, 'bottom', 5, createUE_button),
                                                                              (createUE_button, 'bottom', 8, create_button)])
        
        mc.showWindow()

    def update_shapes_ui(self, *args):
        '''
        Restarts the shape frame icon library (container) inside the main UI window.
        '''
        shapeData = md.load_data(DATA_PATH, 'shapesCV_Data.json')

        for i in self._customShapeList:
            mc.deleteUI(i, control=True)
        self._customShapeList.clear()

        # create a list that loops through the label names for each shape found in the JSON
        custom_shapeLabels = [label for label in shapeData.keys() if label not in ('circle', 'square')]

        for shapeLabel in custom_shapeLabels:

            customShape = mc.iconTextRadioButton(image1=os.path.join(IMGS, f'{shapeLabel}.jpg'), label=shapeLabel, style='iconAndTextVertical', onc=self.set_custom_shape, 
                                                 collection=self._shape_collection, parent=self._shape_gridLayout)
            self.popup_menu(shapeLabel, customShape)
            self._customShapeList.append(customShape)
  
    def popup_menu(self, shapeLabel, parentUI):
        ''' 
        Creates a popup menu (right mouse click) to rename and update thumbnail for each icon.
        '''
        popMenu = mc.popupMenu(numberOfItems=3,parent=parentUI)
        mc.menuItem(label='Rename Shape Label', command=lambda arg: self.rename_label_ui(shapeLabel, parentUI))
        # mc.menuItem(label='option2')
        # mc.menuItem(label='option3')

    def rename_label_ui(self, shapeLabel:str, button:str):
        '''
        Creates UI window to rename a icon label. 
        '''
        windowID = 'RENAMESHAPE'
        windowTitle = 'Flexible Shapes Library'
        size = (300,250)

        if mc.window(windowID, exists=True):
            mc.deleteUI(windowID, window=True)  

        windowUI = mc.window(windowID, title=windowTitle, widthHeight=size, sizeable=True)

        layoutUI = mc.formLayout(parent=windowUI)

        # build function window UI
        top_col = mc.columnLayout(adjustableColumn=True, rowSpacing=10)
        mc.text(label='Rename Shape', align='center')

        rename_shapeLabel = mc.textFieldGrp(label='Name:', placeholderText='Rename your shape for the library')

        mc.setParent('..')

        saveSHP_button = mc.button(label='Rename Shape', command=lambda arg: self.rename_label(shapeLabel, rename_shapeLabel, button))

        # align the button at the bottom of the window
        mc.formLayout(layoutUI, edit=True, attachForm=[(top_col, 'right', 5), (top_col, 'left', 5), (top_col, 'top', 5),
                                                       (saveSHP_button, 'right', 5), (saveSHP_button, 'left', 5), (saveSHP_button, 'bottom', 5),],
                                                                attachControl=[(top_col, 'bottom', 5, saveSHP_button),])

        mc.showWindow()

    def rename_label(self, shapeLabel:str, renameField:str, button:str):
        ''''
        Changes the key (shape label) variable name for a shape stored in the JSON data.
        '''
        # get shapeData dictionary and get the key variables
        # store the values (data) of obtained key variable
        shapeData = md.load_data(DATA_PATH, 'shapesCV_Data.json')
        for shape in shapeData.keys():
            if shape==shapeLabel:
                print(f'Rename {shapeLabel}')
                cvData = shapeData.get(shapeLabel)

        newName = mc.textFieldGrp(renameField, query=True, text=True)
        if newName:
            print(cvData)
            print(newName)
            # update dictionary with new key variable that contains the same (previously obtained) data
            shapeData.update({newName:cvData})
            # remove the obtained/called key from dictionary
            shapeData.pop(shapeLabel)
            # remove icon button UI info from the shape library
            self._customShapeList.remove(button)
            # rename shape image thumbnail
            os.rename(os.path.join(IMGS, f'{shapeLabel}.jpg'), os.path.join(IMGS, f'{newName}.jpg'))
            # overwrite updated dictionary data on top of old JSON data
            md.save_data(DATA_PATH, 'shapesCV_Data.json', shapeData)
            # update icon button UI with new given name 
            updatedButton = mc.iconTextRadioButton(button, edit=True, image1=os.path.join(IMGS, f'{shapeLabel}.jpg'), label=shapeLabel)
            # add newly updated icon button UI info to shape library
            self._customShapeList.append(updatedButton)
            print(self._customShapeList)
            # update shape library frame UI
            self.update_shapes_ui()
        else:
            mc.warning('No name given to rename shape.')
            
    def save_shape_ui(self, *args):
        windowID = 'SAVESHAPE'
        windowTitle = 'Flexible Shapes Library'
        size = (400,250)

        if mc.window(windowID, exists=True):
            mc.deleteUI(windowID, window=True)  

        windowUI = mc.window(windowID, title=windowTitle, widthHeight=size, sizeable=True)

        layoutUI = mc.formLayout(parent=windowUI)

        top_col = mc.columnLayout(adjustableColumn=True, rowSpacing=10)
        mc.text(label='Set Save Settings:', align='center')

        self._new_shapeLabel = mc.textFieldGrp(label='Set Shape Name:', placeholderText='Name the shape to store in the library')

        self._saveSettingsSHP = mc.checkBoxGrp(label='Save Settings:', numberOfCheckBoxes=2, columnWidth=[(1, 140), (2, 140)],
                                               label1='Use Active Camera', value1=True,
                                               label2='Use Current Background', value2=False)
        mc.setParent('..')

        saveSHP_button = mc.button(label='Save Selected Shape', command=self.save_shape)

        # align the button at the bottom of the window
        mc.formLayout(layoutUI, edit=True, attachForm=[(top_col, 'right', 5), (top_col, 'left', 5), (top_col, 'top', 5),
                                                       (saveSHP_button, 'right', 5), (saveSHP_button, 'left', 5), (saveSHP_button, 'bottom', 5),],
                                                                attachControl=[(top_col, 'bottom', 5, saveSHP_button),])

        mc.showWindow()

    def save_shape(self, *args):

        custom_shapeLabel = mc.textFieldGrp(self._new_shapeLabel, query=True, text=True)

        activeCam = mc.checkBoxGrp(self._saveSettingsSHP, query=True, value1=True)
        currentBG = mc.checkBoxGrp(self._saveSettingsSHP, query=True, value2=True)

        svr.save_selected_shape(DATA_PATH, IMGS, customLabel=custom_shapeLabel, activeCamera=activeCam, currentBG=currentBG)
        self.update_shapes_ui()

    def load_ue_shape(self, *args):
        ueUI.unrealShapeUI(windowUI=self._mainWindowID)

    def set_circle_shape(self, *args):
        self._shapeLabel = mc.iconTextRadioButton(self._circleShape, query=True, label=True)

    def set_square_shape(self, *args):
        self._shapeLabel = mc.iconTextRadioButton(self._squareShape, query=True, label=True)

    def set_custom_shape(self, *args):
        selected_shape = mc.iconTextRadioCollection(self._shape_collection, query=True, select=True)

        self._shapeLabel = mc.iconTextRadioButton(selected_shape, query=True, label=True)
        
    def create_shapes(self, *args):
        if not self._shapeLabel:
            mc.warning('Select a shape to create.')
            return
        
        shapeData = md.load_data(DATA_PATH, 'shapesCV_Data.json')

        # query the input settings for creation
        shapeName = mc.textFieldGrp(self._name_textField, query=True, text=True)
        if not shapeName:
            mc.warning('Name your shape before creating.')
            return
        full_shapeName = shapeName

        prefixOn = mc.textFieldGrp(self._prefix_textField, query=True, enable=True)
        if prefixOn:
            prefix = mc.textFieldGrp(self._prefix_textField, query=True, text=True)
            full_shapeName = prefix+shapeName

        suffixOn = mc.textFieldGrp(self._suffix_textField, query=True, enable=True)
        if suffixOn: 
            suffix = mc.textFieldGrp(self._suffix_textField, query=True, text=True)
            full_shapeName += suffix

        scaleVal = mc.intSliderGrp(self._scaleValue, query=True, value=True)

        colorTab = mc.optionMenu(self._colorTab, query=True, value=True)
        if colorTab=='RBG/HSV':
            shapeColor = mc.colorInputWidgetGrp(self._colorRGBWidget, query=True, rgb=True)
            
        else:
            shapeColor = mc.palettePort(self._colorPalette, query=True, rgb=True) 


        if self._shapeLabel == 'circle':
            shp.circleShape(name=full_shapeName, scaleValue=scaleVal,typeOverride=shapeColor)

        elif self._shapeLabel == 'square':
            shp.squareShape(shapeData, shapeLabel=self._shapeLabel, scaleValue=scaleVal, name=full_shapeName, typeOverride=shapeColor)

        else:
            shp.customShape(shapeData, shapeLabel=self._shapeLabel, scaleValue=scaleVal, name=full_shapeName, typeOverride=shapeColor)

        shapeName = mc.textFieldGrp(self._name_textField, edit=True, text='')
        
    def prefix_on(self, *args):
        mc.textFieldGrp(self._prefix_textField, edit=True, enable=True)

    def prefix_off(self, *args):
        mc.textFieldGrp(self._prefix_textField, edit=True, enable=False)

    def suffix_on(self, *args):
        mc.textFieldGrp(self._suffix_textField, edit=True, enable=True)

    def suffix_off(self, *args):
        mc.textFieldGrp(self._suffix_textField, edit=True, enable=False)
        
    def swap_colorUI(self, *args):
        colorTab = mc.optionMenu(self._colorTab, query=True, value=True)
        if colorTab=='RBG/HSV':
            mc.palettePort(self._colorPalette, edit=True, visible=False)
            mc.colorInputWidgetGrp(self._colorRGBWidget, edit=True, visible=True)

        else:
            mc.palettePort(self._colorPalette, edit=True, visible=True)
            mc.colorInputWidgetGrp(self._colorRGBWidget, edit=True, visible=False)

            
