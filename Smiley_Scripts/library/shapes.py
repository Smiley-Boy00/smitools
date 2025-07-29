import maya.cmds as mc

def circleShape(name='crnode', scaleValue=1, typeOverride=None):
    '''
    typeOverride args: [float, float, float]
    '''
    # create curve circle
    crv = mc.circle( nr=(0, 1, 0), c=(0, 0, 0), r=1.0 , n=name)[0]
    # delete history
    mc.delete(crv,ch=True)

    if scaleValue <= 0: 
        mc.xform(crv, scale=[1,1,1])
    else:
        mc.xform(crv, scale=[scaleValue, scaleValue, scaleValue])
    
    mc.setAttr(f"{crv}.overrideEnabled", True)

    if typeOverride:
        # enable and set color RGB override
        print(typeOverride[0])
        print(typeOverride[1])
        print(typeOverride[2])
        mc.setAttr(f"{crv}.overrideRGBColors", True)
        mc.setAttr(f"{crv}.overrideColorRGB", typeOverride[0], typeOverride[1], typeOverride[2])
    else:
        # enable and set default (blue) color Index override
        mc.setAttr(f"{crv}.overrideColor", 6)
        
def squareShape(shapeData:dict, shapeLabel='squareShape', scaleValue=1, name='crnode', typeOverride=None):
    '''
    typeOverride args: [float, float, float]
    '''
    # create empty group to place every shape node
    crv = mc.group(em=True, n=name)

    # gather the shape dictionary data
    print(shapeData)

    # obtain the squareShape data
    shapeName = shapeData[shapeLabel]
    print(shapeName)

    # get every shape within the shape name data
    # get each shape's control vertex number and position
    cv_nums = shapeName['CV_Numbers']
    cv_pos = shapeName['CV_Positions']
    degrees = shapeName['Degrees']
    print(cv_nums)

    # get the name of each shape and the amount of control vertex numbers it contains
    shapeNodes = cv_nums.items()
    
    for shapeNode, numCV in shapeNodes:
        print(shapeNode)
        print(numCV)
        cv_numsList = []
        for n in range(numCV):
            cv_numsList.append(cv_pos[f'{shapeNode}.cv[{n}]'])

        degree = degrees.get(shapeNode)
        print(degree)
        mc.curve(p=cv_numsList, n=f'{shapeNode}_SHP_GRP', d=degree)
        print(cv_numsList)

    # select and store all the transform groups containing the shape nodes
    grpsToDelete = mc.ls('*_SHP_GRP')
    print(grpsToDelete)
    for grp in grpsToDelete:
        shapeObj = mc.listRelatives(grp, shapes=True, type='nurbsCurve')[0]
        mc.parent(shapeObj, crv, relative=True, shape=True)
        mc.rename(shapeObj, f'{shapeObj}_SHP')
        mc.delete(grp)

    # clear selection
    mc.select(clear=True)

    # delete history
    mc.delete(crv,ch=True)

    if scaleValue <= 0: 
        mc.xform(crv, scale=[1,1,1])
    else:
        mc.xform(crv, scale=[scaleValue, scaleValue, scaleValue])

    mc.setAttr(f"{crv}.overrideEnabled", True)

    if typeOverride:
        # enable and set color RGB override
        print(typeOverride[0])
        print(typeOverride[1])
        print(typeOverride[2])
        mc.setAttr(f"{crv}.overrideRGBColors", True)
        mc.setAttr(f"{crv}.overrideColorRGB", typeOverride[0], typeOverride[1], typeOverride[2])
    else:
        # enable and set default (blue) color Index override
        mc.setAttr(f"{crv}.overrideColor", 6)

def customShape(shapeData:dict, shapeLabel='squareShape', scaleValue=1, name='crnode', typeOverride=None):
    '''
    typeOverride args: [float, float, float]
    '''
    # create empty group to place every shape node
    crv = mc.group(em=True, n=name)

    # gather the shape dictionary data
    print(shapeData)

    # obtain the squareShape data
    shapeName = shapeData[shapeLabel]
    print(shapeName)

    # get every shape within the shape name data
    # get each shape's control vertex number and position
    cv_nums = shapeName['CV_Numbers']
    cv_pos = shapeName['CV_Positions']
    degrees = shapeName['Degrees']
    forms = shapeName['Form_Index']

    # get the name of each shape and the amount of control vertex numbers it contains
    for shapeNode, numCV in cv_nums.items():
        print(shapeNode)
        print(numCV)
        
        form = forms.get(shapeNode)
        print(form)
        if form==2:
            shp = mc.circle( nr=(0, 1, 0), c=(0, 0, 0), r=1.0, n=shapeNode)[0]
            for n in range(numCV):
                cv_key = f'{shapeNode}.cv[{n}]'

                tr = cv_pos[cv_key]
                mc.xform(cv_key, os=True, t=tr)
        else:
            cv_positions=[]
            for n in range(numCV):
                cv_key = f'{shapeNode}.cv[{n}]'

                if cv_key in cv_pos:
                    position = cv_pos[cv_key]
                    cv_positions.append(tuple(position))

            degree = degrees.get(shapeNode)
            print(degree)
            print(cv_positions)
            shp = mc.curve(p=cv_positions, n=f'{shapeNode}_SHP_GRP', d=degree)
        mc.rename(shp, f'{shapeNode}_SHP_GRP')

    # select and store all the transform groups containing the shape nodes
    grpsToDelete = mc.ls('*_SHP_GRP')
    print(grpsToDelete)
    for grp in grpsToDelete:
        shapeObj = mc.listRelatives(grp, shapes=True, type='nurbsCurve')[0]
        mc.parent(shapeObj, crv, relative=True, shape=True)
        mc.rename(shapeObj, 'customCurveShape')
        mc.delete(grp)

    # clear selection
    mc.select(clear=True)

    # delete history
    mc.delete(crv,ch=True)

    if scaleValue <= 0: 
        mc.xform(crv, scale=[1,1,1])
    else:
        mc.xform(crv, scale=[scaleValue, scaleValue, scaleValue])
        
    mc.setAttr(f"{crv}.overrideEnabled", True)

    if typeOverride:
        # enable and set color RGB override
        print(typeOverride[0])
        print(typeOverride[1])
        print(typeOverride[2])
        mc.setAttr(f"{crv}.overrideRGBColors", True)
        mc.setAttr(f"{crv}.overrideColorRGB", typeOverride[0], typeOverride[1], typeOverride[2])
    else:
        # enable and set default (blue) color Index override
        mc.setAttr(f"{crv}.overrideColor", 6)

