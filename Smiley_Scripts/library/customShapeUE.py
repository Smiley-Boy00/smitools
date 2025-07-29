import maya.cmds as mc
import maya.mel as mel
import library.modules as md
import importlib

importlib.reload(md)

def ue_temp(shapeSelection):
    
    for each in shapeSelection:
        shapeList=mc.listRelatives(each, shapes=True, type='nurbsCurve')
        if shapeList:
            topShape = f'{each}|{shapeList[0]}'
            if mc.nodeType(topShape)=='nurbsCurve':
                print(topShape)
                tempShape = mc.duplicate(each, name=f'TEMP_{each}')
                md.move_to_origin(tempShape)
                mc.makeIdentity(tempShape, apply=True, translate=True, rotate=True, scale=True )
                mc.select(tempShape)

                # Convert every selected curve into a stroke node
                mel.eval('convertCurvesToStrokes')
                mc.delete(tempShape)

def make_UE_shape(globalScale=1):
    shape_selection = mc.ls(selection=True)
    selection_count = 0

    if shape_selection:
        for each in shape_selection:
            selection_count += 1
            print(each)
            shapeList=mc.listRelatives(each, shapes=True, type='nurbsCurve')
            if shapeList:
                topShape = f'{each}|{shapeList[0]}'
                if mc.nodeType(topShape)=='nurbsCurve':
                    print(topShape)
                    tempShape = mc.duplicate(each, name=f'TEMP_{each}')
                    md.move_to_origin(tempShape)
                    mc.makeIdentity(tempShape, apply=True, translate=True, rotate=True, scale=True )
                    mc.select(tempShape)
                    # Record existing stroke nodes before creation
                    strokes_before = set(mc.ls(type="stroke"))

                    # Convert every selected curve into a stroke node
                    mel.eval('convertCurvesToStrokes')

                    # Find every newly created stroke node
                    strokes_after = set(mc.ls(type="stroke"))
                    strokes_created = list(strokes_after - strokes_before)
                    trnNodes_to_combine = []
                    for strokeShape in strokes_created:
                        strokesTRN=mc.listRelatives(strokeShape, p=True)
                        mc.setAttr(f'{strokeShape}.displayPercent', 45)
                        mc.setAttr(f'{strokeShape}.sampleDensity', 15)
                        for parentNode in strokesTRN:
                            brushNode = mc.listConnections(parentNode + '.brush', source=True, destination=False)[0]
                            # Uncomment for Debugging Only
                            # brushAttrs=mc.listAttr(brushNode)
                            mc.setAttr(f'{brushNode}.color1', 1,1,0)
                            mc.setAttr(f'{brushNode}.globalScale', globalScale)

                            mc.select(parentNode)
                            # record existing transform nodes before creation
                            trnNodes_before = set(mc.ls(type="transform"))
                            mel.eval('doPaintEffectsToPoly(0, 1, 0, 0, 100000)')

                            # find every newly created transform node and it to a list
                            trnNodes_after = set(mc.ls(type="transform"))
                            trnNodes_created = list(trnNodes_after - trnNodes_before)
                            print(trnNodes_created)
                            for trnNode in trnNodes_created:
                                if trnNode.endswith('MeshGroup'):
                                    meshGroup=trnNode
                                    trnNodes_to_combine.append(meshGroup)
                        for trn_nodes in strokesTRN:
                            mc.delete(trn_nodes)
                    print(trnNodes_to_combine)

                    if len(trnNodes_to_combine)>1:
                        joinGrp = mc.group(empty=True, name=f'combinedBrush{selection_count}MeshGroup')
                        for trnMesh in trnNodes_to_combine:
                            mc.parent(trnMesh, joinGrp)
                        mc.select(joinGrp)
                        brushMesh = mc.polyUnite(ch=True, mergeUVSets=True, centerPivot=True, name=f'combinedBrush{selection_count}Main')
                        mc.parent(brushMesh[0], joinGrp)
                        mc.delete(brushMesh, ch=True)
                        mc.select(joinGrp)
                        

                    else:
                        # for trnMesh in trnNodes_to_combine:
                        #     mc.rename(trnMesh, f'combinedBrush{selection_count}MeshGroup')
                        mc.select(trnNodes_to_combine[0])
                        

                    ctrlMeshGrp = mc.ls(selection=True)[0]
                    print(ctrlMeshGrp)
                    ctrlMeshTrn=mc.listRelatives(ctrlMeshGrp)[0]
                    print(ctrlMeshTrn)
                    ctrlMesh=mc.listRelatives(ctrlMeshTrn)[0]
                    print(ctrlMesh)
                    shadingNodes = mc.listConnections(ctrlMesh, type='shadingEngine')
                    mainShader = shadingNodes[0]
                    shadingNodes = set(shadingNodes)
                    for shader in shadingNodes:
                        if shader==mainShader:
                            mc.sets(ctrlMeshTrn, e=True, forceElement=shader)
                            shaderMat = mc.listConnections(shader + '.surfaceShader', source=True)[0]
                            mc.rename(shader, f'{each}_ShaderGroup')
                            mc.rename(shaderMat, f'{each}_Shader')
                        else:
                            unusedShader = shader
                            unusedMat = mc.listConnections(unusedShader + '.surfaceShader', source=True)[0]
                            if mc.objExists(unusedShader):
                                mc.delete(unusedShader)
                            if mc.objExists(unusedMat):
                                mc.delete(unusedMat)

                    # create custom UE node 
                    # parent geo to unrealNode
                    ueParentNode = mc.createNode('unrealNode')
                    mc.parent(ctrlMeshTrn, ueParentNode)        
                    mc.rename(ctrlMeshTrn, f'{each}_GEO')
                    mc.rename(ueParentNode, f'{each}_GRP')
                    mc.delete(ctrlMeshGrp)

                    # clean up temporary transform nodes
                    mc.delete(tempShape)

                    # clear selection
                    mc.select(clear=True)
                    print('Unreal ControlRig Shape built.')                
                else:
                    mc.warning('Selection is not a curveShape!')
            else:
                mc.warning('Selection is not a curveShape!')
    else:
        mc.warning('No selection made.')
        return


