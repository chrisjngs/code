

import pymel.all as pma

BOOLEANMODE_ADD = 1
BOOLEANMODE_SUBTRACT = 2
PRIMITIVE_CUBE = 0
PRIMITIVE_CYLINDER = 1
PRIMITIVE_SPHERE = 2
PRIMITIVE_CUSTOM = 3


def cleanUp ():
    pma.delete (constructionHistory=True)
    #pma.select ()
    pma.delete ("*_ctrl*")

def hider(option):
    if (option == 0):
        pma.hide ()
    elif (option == 1):
        pma.select ("*_ctrl*")
        pma.hide ()
    elif (option == 2):
        pma.select ("*_ctrl*")
        pma.showHidden ()
        pma.select (clear=True)

def fixMaterial():
    pma.hyperShade( assign="lambert1" )

def triangulate():
    pma.polyTriangulate()

def creator(primitives):
    selection = pma.ls(sl=True)
    for x in selection:

        if primitives == PRIMITIVE_CUBE:
            a = makeCube() #Create cube
        if primitives == PRIMITIVE_CYLINDER:
            a = makeCyl() #Create cyl
        if primitives == PRIMITIVE_SPHERE:
            a = makeSphere() #Create sphere
        if primitives == PRIMITIVE_CUSTOM:
            a = selection[1]
            x = selection[0]
            pma.select (a)
        b = createController(a)
        meshConstrainer (b,a)
        operator(x,a)
        pma.select (b)


def operator(meshA, meshB):
   booleanmode = get_boolean_mode()
   pma.polyBoolOp( meshA, meshB, op=booleanmode, n="basemesh" )
   pma.hyperShade( assign="lambert1" )   #REMINDER: Need to be replaced with the actual assigned material and not with a lambert1 so for who is working with other materials can easyly keep using that


def get_boolean_mode():
    if pma.radioButton(addRadioB, query = True, select = True) :
        return BOOLEANMODE_ADD
    if pma.radioButton(subRadioB, query = True, select = True) :
        return BOOLEANMODE_SUBTRACT
    return None

def makeCube():
    cubeTransform = pma.polyCube(n="cubetobool", w=1, h=1, d=1, sx=1, sy=1, sz=1)[0]
    return cubeTransform

def makeCyl():
    cylTransform = pma.polyCylinder(n="cubetobool", r=1, h=2, sx=20)[0]
    return cylTransform

def makeSphere():
    sphereTransform = pma.polySphere(n="cubetobool", r=1, sx=20, sy=20, cuv=2)[0]
    return sphereTransform


def meshConstrainer(constrainer, constrained):
    pma.scaleConstraint( constrainer, constrained, maintainOffset=True)
    pma.parentConstraint( constrainer, constrained, maintainOffset=True)


def createController(object):
    #object = pma.ls(sl=True)
    pivotObj = pma.xform(object,query=True,t=True,worldSpace=True)
    edges = pma.filterExpand(pma.polyListComponentConversion(te=1),sm=32,ex=1) # convert edges to curve ancd create one object
    for edge in edges:
    	vtx = pma.ls(pma.polyListComponentConversion(edge,fe=1,tv=1),fl=1)
    	p1 = pma.pointPosition(vtx[0])
    	p2 = pma.pointPosition(vtx[1])
    	curves = pma.curve(n="line_ctrl_curve", d=1,p=(p1,p2))

    ctrl = pma.curve (n="bool_ctrl", d=1,ws=True, p=pivotObj)
    pma.xform (centerPivots=True)
    for curveEdge in pma.ls ("line_ctrl*"):
        pma.parent(curveEdge,ctrl, s=1, r=1)
        pma.rename(curveEdge, "shapeunused")


    transforms =  pma.ls(type='transform')
    deleteList = []
    for tran in transforms:
        if pma.nodeType(tran) == 'transform':
            children = pma.listRelatives(tran, c=True)
            if children is None:
                #print '%s, has no childred' %(tran)
                deleteList.append(tran)

    if not deleteList:
       pma.delete(deleteList)
    return ctrl




#################TUTORIAL
windowNameTut = "Tutorial"
if (pma.window(windowNameTut , exists=True)):
    pma.deleteUI(windowNameTut)
windowTutorial = pma.window(windowNameTut, title = windowNameTut, width = 400, height = 300, backgroundColor = [0.2, 0.2, 0.2])
pma.columnLayout( "testColumn", adjustableColumn = True)
pma.text("intro", label = "This tool is a super tool to make booleans wrote by Leonardo Iezzi. To make it works correctly, you need to have your base mesh already even if just a cube. With your base mesh selected just press one of the three buttons on the windows to subtract or add those primitives. If you want to use a custom mesh for the operation: select your base mesh then the custom one (it's important to pick your base mesh first) and then press the 'Use custom mesh' button. After you have done, select your base mesh and press 'Clean Up.'",wordWrap= True, height = 100, backgroundColor = [0.2, 0.2, 0.2], align='left', parent = "testColumn")

 #pma.text("first", label = "1- Select always your main mesh first",wordWrap= True, height = 40, backgroundColor = [0.2, 0.2, 0.2], align='left', parent = "testColumn")
 #pma.text("secondo", label = "2- In case you want to use a custom mesh: Select first your main mesh then the mesh you want to add or subtract",wordWrap= True, height = 40, backgroundColor = [0.2, 0.2, 0.2], align='left', parent = "testColumn")
 #pma.text("third", label = "3- Everythong should works",wordWrap= True, height = 40, backgroundColor = [0.2, 0.2, 0.2], align='left', parent = "testColumn")



pma.separator(parent = "testColumn", height=20)
pma.button("goit", label = "Got it", width = 120, height = 40, backgroundColor = [0.5, 0.5, 0.5], parent = "testColumn", command = "pma.deleteUI(windowNameTut)")

pma.showWindow()

################################################################################################UI#################################################
#pma.deleteUI(windowNameTut)
windowName = "SuperBool"
windowSize = (120, 200)
if (pma.window(windowName , exists=True)):
    pma.deleteUI(windowName)
window = pma.window( windowName, title= windowName, width = 120, height = 200 )
pma.columnLayout( "mainColumn", adjustableColumn = True)

################################################################################################UI#################################################
pma.gridLayout("nameGridLayout01", numberOfRowsColumns = (1,4), cellWidthHeight = (40,40), parent = "mainColumn")
pma.symbolButton("nameButton1", image = "polyCube.png", width = 40, height = 40, backgroundColor = [0.2, 0.2, 0.2], parent = "nameGridLayout01", command = "creator(PRIMITIVE_CUBE)")
pma.symbolButton("nameButton2", image = "polyCylinder.png", width = 40, height = 40, backgroundColor = [0.2, 0.2, 0.2], parent = "nameGridLayout01", command = "creator(PRIMITIVE_CYLINDER)")
pma.symbolButton("nameButton3", image = "polySphere.png", width = 40, height = 40, backgroundColor = [0.2, 0.2, 0.2], parent = "nameGridLayout01", command = "creator(PRIMITIVE_SPHERE)")
pma.columnLayout("columnLayoutName01", adjustableColumn = True, backgroundColor = [0.2, 0.2, 0.2])
pma.radioCollection("collection10", parent = "columnLayoutName01")
subRadioB = pma.radioButton("subRadio", select = True, label = "Sub")
addRadioB = pma.radioButton("addRadio", label = "Add")
pma.setParent( '..' )
pma.setParent( '..' )
################################################################################################UI#################################################
pma.separator(parent = "mainColumn", height=20)

pma.button("customMeshB", label = "Use Custom Mesh", width = 120, height = 40, backgroundColor = [0.2, 0.2, 0.2], parent = "mainColumn", command = "creator(PRIMITIVE_CUSTOM)")

pma.separator(parent = "mainColumn", height=20)
################################################################################################UI#################################################
pma.gridLayout("nameGridLayout03", numberOfRowsColumns = (1,3), cellWidthHeight = (53,40), parent = "mainColumn")
pma.button("hidSelB", label = "Hide Sel",  height = 40, backgroundColor = [0.2, 0.2, 0.2], parent = "nameGridLayout03", command = "hider(0)")
pma.button("hidAllB", label = "Hide All",  height = 40, backgroundColor = [0.2, 0.2, 0.2], parent = "nameGridLayout03", command = "hider(1)")
pma.button("showAll", label = "Show All",  height = 40, backgroundColor = [0.2, 0.2, 0.2], parent = "nameGridLayout03", command = "hider(2)")

pma.separator(parent = "mainColumn", height=20)

pma.button("clean", label = "Clean Up", width = 120, height = 40, backgroundColor = [0.2, 0.2, 0.2], parent = "mainColumn", command = "cleanUp()")

pma.separator(parent = "mainColumn", height=20)
################################################################################################UI#################################################
################################################################################################UI#################################################
pma.gridLayout("nameGridLayout02", numberOfRowsColumns = (1,2), cellWidthHeight = (80,40), parent = "mainColumn")
pma.button("triangB", label = "Triangulate", width = 120, height = 40, backgroundColor = [0.2, 0.2, 0.2], parent = "nameGridLayout02", command = "triangulate()")
pma.button("fixMatB", label = "FixMaterial", width = 120, height = 40, backgroundColor = [0.2, 0.2, 0.2], parent = "nameGridLayout02", command = "fixMaterial()")
################################################################################################UI#################################################
pma.showWindow()