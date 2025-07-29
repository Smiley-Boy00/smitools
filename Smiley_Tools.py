import maya.cmds as mc
import maya.OpenMaya as om
import maya.OpenMayaMPx as ommp
import importlib
import sys
from os import path

uNodeTypeName = 'unrealNode'
node_id = om.MTypeId(0x8765)
uTransformMatrixID = om.MTypeId(0x87015)

plugin_path = mc.pluginInfo("Smiley_Tools.py", query = True, path = True)
plugin_dir = path.dirname(plugin_path)
scripts_dir = path.join(plugin_dir, 'Smiley_Scripts')
imgs = path.join(scripts_dir, 'library', 'imgs')

if scripts_dir not in sys.path:
    sys.path.append(scripts_dir)

import mtouExporter
import shapeLibrary
import shapeUE 


def create_menu():
    if mc.menu('SmileyDevMenu', exists = True):
        mc.deleteUI('SmileyDevMenu', menu = True)

    main_menu = mc.menu('SmileyMenu', label = 'Smiley Tools', parent = 'MayaWindow', tearOff = True)

    mc.menuItem(label='MayaToUnreal', command = run_mtou, parent = main_menu)
    mc.menuItem(label='FlexShape Library', command = run_fls, parent = main_menu)
    ue_menu=mc.menuItem(label='Custom UE Control Rig Shapes', parent=main_menu, subMenu=True, tearOff=True)
    mc.menuItem(label='Make Control Rig Shape', command = run_shapeUE, parent=ue_menu)
    mc.menuItem(label='Export Control Rig Shape', command = run_shapeExport, parent=ue_menu)


def run_mtou(*args):
    importlib.reload(mtouExporter)
    mtouExporter.mtouExporterUI()

def run_fls(*args):
    importlib.reload(shapeLibrary)
    shapeLibrary.shapeLibraryUI()

def run_shapeUE(*args):
    importlib.reload(shapeUE)
    shapeUE.unrealShapeUI()

def run_shapeExport(*args):
    importlib.reload(shapeUE)
    shapeUE.shapeExporterUI()

# build custom transform node (unrealNode)
class component(ommp.MPxTransform):
    def __init__(self):
        ommp.MPxTransform.__init__(self)

def creator():
    return ommp.asMPxPtr(component())

def initializer():
    pass

def initializePlugin(plugin):
    mplugin = ommp.MFnPlugin(plugin, "Smiley", "1.0" , "Any")
    matrix = ommp.MPxTransformationMatrix
    iconPath = path.join(imgs, 'icons', 'out_unrealNode.png') # Your custom icon file
    mplugin.registerTransform(uNodeTypeName, node_id, creator, initializer, matrix, uTransformMatrixID)
    create_menu()

def uninitializePlugin(plugin):
    if mc.menu('SmileyMenu', exists = True):
        mc.deleteUI('SmileyMenu', menu = True)
    mplugin = ommp.MFnPlugin(plugin)
    mplugin.deregisterNode(node_id)

