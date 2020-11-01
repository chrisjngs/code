"""

This script was made for the purpose of easily creating hair tubes for xGen hair simulation.

"""

import maya.cmds as cmds
import maya.mel as mel

class hairAssistTool(object):

	def __init__(self):

		self.selEdge 		= []
		self.strandDict 	= {}
		self.allCrvs 		= {}
		self.all_jnts		= {}
		self.hairCrv_list	= []
		self.all_list		= []

	def createGUI(self, *args):

		"""

		Creates a window with two lists of objects and buttons. This is the main GUI of the script

		"""

		self.strandDict['All Curves'] = cmds.ls(type='nurbsCurve')

		realStrands = cmds.listRelatives(self.strandDict['All Curves'], p=1)
		mainWindow = 'mainWindow'

		if cmds.window(mainWindow, ex=1):
			cmds.deleteUI(mainWindow)


		windowSize = cmds.window('mainWindow', t='Hair Tubes Tool', wh=(300, 400), rtf=1, s=0)
		cmds.rowColumnLayout('mainLayout', nc=2, cw=[(1,300), (2, 100)])
		###########################Hair Tubes Section###########################
		cmds.rowColumnLayout('hairStrands', nc=1)

		##lists##
		cmds.setParent('hairStrands')
		cmds.textScrollList('hairStrandList', a=self.hairTubesInScene(), selectCommand=self.selHair, h=300)


		##buttons##
		cmds.setParent('mainLayout')
		cmds.rowColumnLayout('buttons', nc=1)
		cmds.text('\t')
		cmds.text('\t')
		cmds.text('\t')
		cmds.text('\t')
		cmds.button(l='New Hair Strand', c=self.buildCurve, h=30, bgc=(0,1,0))
		cmds.button(l='Create Tube', h=30,c=self.makeTube, bgc=(1,.6,.2))
		cmds.button(l='Tube Visibility', h=30, bgc=(.5,0,0))
		cmds.button(l='Show Cap', h=30, bgc=(.5,0,0))
		cmds.button(l='Update Tube Color', h=30, bgc=(.5,0,0))
		cmds.button(l='Shape Tubes', h=30, bgc=(.5,0,0))

		###########################Hair Groups Section###########################
		cmds.rowColumnLayout('sepLayout', nc=1)
		cmds.setParent('sepLayout')
		cmds.separator()
		cmds.separator()

		##lists##
		cmds.setParent('hairStrands')
		cmds.textScrollList('hairGroups', a=self.hairGrpInScene(), selectCommand=self.updateGroups, h=100)

		##buttons##
		cmds.setParent('buttons')
		cmds.text('\t')
		cmds.text('\t')
		cmds.text('\t')
		cmds.text('\t')
		cmds.text('\t')

		cmds.button(l='Add to Hair Group', h=30, c=self.appendGroup, bgc=(0,1,0))
		cmds.button(l='New Hair Group', h=30, c=self.hairGroup, bgc=(0,1,0))
		cmds.button(l='Send To xGen', h=30, bgc=(.5,0,0))


		cmds.showWindow(mainWindow)

		return

	def hairTubesInScene(self, *args):

		if cmds.objExists('hairTubes_GRP'):
			activeGroup = cmds.listRelatives('hairTubes_GRP', children=1)
			activeTubes = cmds.listRelatives(activeGroup, children=1)
			my_list = activeTubes
			return activeTubes
		else:
			emptyScene = 'No Tubes Found'
			return emptyScene

	def hairGrpInScene(self, *args):
		'''
		checks if there are any hairTubes in the scene, if there are then they will be added to the list. If not,
		then the list will show an "all curves" group.
		:param args:
		:return:
		'''

		groupDict = {}

		if cmds.objExists('hairTubes_GRP'):
			activeGroups = cmds.listRelatives('hairTubes_GRP', c=1)
			my_list = activeGroups
			return activeGroups
		else:
			emptyScene = 'All Curves'
			return emptyScene

	def updateGroups(self, *args):

		"""

		updates the hairStrandList when a new hair group is active

		"""

		activeSelection = cmds.textScrollList('hairGroups', q=1, selectItem=1)[0]
		groupsTubes = cmds.listRelatives(activeSelection, children=1)
		cmds.textScrollList('hairStrandList', q=1, e=1, removeAll=1)
		if groupsTubes <= 0:
			cmds.textScrollList('hairStrandList', e=1, a='Nothing in hair group')
			return
		else:
			for tube in groupsTubes:
				cmds.textScrollList('hairStrandList', e=1, a=tube)
			return

	def appendGroup(self, *args):

		"""

		Appends the selected curves to the selected hair group. It does this by grouping the hair strands together under
		the hair groups name.

		"""

		curGroup = cmds.textScrollList('hairGroups', q=1, si=1)[0]

		for x in cmds.ls(sl=1):
			cmds.parent(x, curGroup)

		return

	def selHair(self, *args):

		"""

		This function will select the hair tube group when it is selected in the textScrollList.

		"""

		selectedhair = cmds.textScrollList('hairStrandList', q=1, si=1)
		cmds.select(selectedhair)
		print selectedhair
		return

	def hairGroup(self, *args):

		"""

		Creates a prompt for user input to either create a new hair group or cancel the input. If the user creates a new
		group then it takes the name that the user makes and checks for a master group to parent under. If the parent group
		is not made then it makes it and then parents the new group under it. Finally, the new group is added to the
		dictionary strandDict and appended to the textScrollList.

		"""

		instructions = 'Enter the name of the new hair group.'
		result = cmds.promptDialog(t='New Hair Group', m=instructions, b=['Create', 'Cancel'], db='Create', cb='Cancel')

		if result == 'Create':

			text = cmds.promptDialog(q=1, tx=1)
			self.strandDict['newKey'] = text

			if cmds.ls(sl=0):
				newGroup = cmds.group(n=text, em=1)
			else:
				newGroup = cmds.group(n=text)
			if not cmds.objExists('hairTubes_GRP'):
				cmds.group(n='hairTubes_GRP', em=1)
			cmds.parent(newGroup, 'hairTubes_GRP')

			cmds.textScrollList('hairGroups', a=self.strandDict['newKey'], e=1)
			return

		return

	def checkEdgeSel(self, *args):

		"""

		Checks if there are any edges selected, if there are edges selected a window appears with a confirmation that you
		want to create curves from the selected edge. If you press the confirm button it will return True, otherwise it will
		return False.

		"""
		confirmMessage = 'You have edges selected, would you like to use these edges to make a hair strand?\n'
		' If you would like to use the selected edges click Confirm, otherwise click Create Curve'

		if cmds.filterExpand(ex=1, sm=32):
			selEdge = [cmds.filterExpand(ex=1, sm=32)]

			result = cmds.confirmDialog(t='Confirm Creation', m=confirmMessage, b=['Confirm', 'Create Curve'],
										db='Confirm', cb='Create Curve')
			if result =='Confirm':
				return True

			return False

		return False

	def buildCurve(self, *args):

		"""

		If the edge selection returns True then the selected edges are converted to a curve and added to the textScrollList.
		Otherwise the EP curve tool is activated.

		"""

		#access the EP Curve tool if checkEdgeSel returns false
		if self.checkEdgeSel() == True:
			newConCurve = cmds.polyToCurve(f=2, dg=3, ch=0)
			cmds.textScrollList('hairStrandList', a=newConCurve, e=1)
			return

		mel.eval('EPCurveTool')
		return

	def createJoints(self, deci=10, name=''):
		"""
		Creates joints at the selected hair strands CV locations and store the new joints in a list so that they can be
		easily deleted

		"""
		self.all_jnts = {}
		precision = pow(10, deci)
		for crv in cmds.ls(selection=True):
			if not name:
				name=crv
			cmds.select(clear=True)
			jnt = ''
			prnt_jnt=''
			inc=1
			jnt_list = []
			for cv in cmds.ls(crv+'.ep[*]', flatten=True):

				# Get cv position.
				pos = cmds.xform(cv, worldSpace=True, translation=True, query=True)
				# Truncate to the requested decimal place.
				pos = [int(x*precision) for x in pos]
				pos = [float(x)/precision for x in pos]

				jnt = cmds.joint(name='%s_%s_JNT'%(name, inc), position=pos, absolute=True)
				jnt_list.append(jnt)

				if prnt_jnt:
					cmds.joint(prnt_jnt, edit=True, orientJoint='xyz')

					# Ensure Y and Z are always facing the same direction along the chain.
					cmds.parent(jnt, world=True)
					cmds.setAttr(prnt_jnt+'.jointOrientX', 0.0)
					cmds.parent(jnt, prnt_jnt)

				prnt_jnt = jnt
				inc+=1
			# Ensure the final joint is zero'd out to face the same direction as the parents.
			cmds.setAttr(prnt_jnt+'.jointOrient', *(0,0,0))
			name=''
			self.all_jnts[crv]=jnt_list
		cmds.select(self.all_jnts.keys())
		return self.all_jnts

	def createCircle(self, *args):
		"""
		Creates CV Circles for each joint that was created in the makeJoints function. Once the circles are made they are
		parent constrained to the corresponding joints and name correctly. The newly created circles are stored in an array
		so that they can easily be called up.
		"""
		name =''
		allCrvs = {}
		for crv in cmds.ls(selection=True):
			if not name:
				name=crv

			#cmds.select(clear=True)
			hairCrv = ''
			inc=1
			hairCrv_list = []
			for cv in cmds.ls(crv+'.ep[*]', flatten=True):
				hairCrv = cmds.circle(name='hairControl_CRV', c=(0, 0, 0), nr=(1, 0, 0), sw=360, r=1, d=3, ch=0)
				hairCrv_list.append(hairCrv)
				inc+=1
			name=''
			self.allCrvs[crv] = hairCrv_list
		cmds.select(self.allCrvs.keys())
		return self.allCrvs

	def parentCircles(self, *args):


		print "break"
		count = 0
		for crv in self.allCrvs.values():
			print str(self.allCrvs.keys()) + "\n"
			print str(self.allCrvs.values()) + "\n"
			#print "the count is now %s" % count
		print 'the curves were parented'
		return

	def makeTube(self, *args):
		"""
		Calls the makeJoints function and the createCircle function before selecting the new CV Circles and lofting between
		them.
		"""
		print "it started"
		self.createJoints()
		self.createCircle()
		self.parentCircles()
		print "it went through"

		return

	def hideTube(self):
		"""

		Checks the visibility of the hair tubes in the scene, if it is set to 0 (off) then it turns it to 1 (on) and
		vise-versa.

		"""
		return

	def showCap(self):

		"""

		Checks everything related with each hair tube except for the CV Circle with the suffix of _BASE and toggles the
		visibility from 0 (off) to 1(on) and vis-versa.

		"""
		return

	def tubeColor(self):

		"""

		Assigns an object override to each hair tube changing the color of each tube group to a unique RGB value.

		"""
		return

	def shapeTube(self):

		"""

		Select each lofted hair tube and changes the object override to reference so that shaping can be done without
		changing the nurbs object.

		"""
		return

	def xGen(self):

		"""

		Checks for selected geometry, if there is nothing selected a new window opens with available geometry in the scene
		to build an xGen description off of. Once a correct polygonal object is chosen an xGen collection is created with
		a user specified name and the description is pulled from the hair group list. Once an xGen description is made
		the hair tubes that correspond to the selected hair group list are converted to polygonal objects. After that xGen
		creates guides using the Tube Groom feature.

		"""
		return

	def thingsToDo(self):

		"""
			Pending Fixes:
			-------------------------------------------------------------------------------------------------------------
			- Once you make a new hair group the 'All Curves' option in the hairGroups scroll list goes away.
			- When you make a new hair strand it isn't added to the textScrollList, you have to relaunch the tool.
				- Possible fix is to add a refresh button
			- When a hair group is active and you create a new hair strand it is not automatically added to the active group


			Future Updates.
			--------------------------------------------------------------------------------------------------------------

			def densitySlider:

				'''

				this is the slider that will control how many curves are created when you press the create tube button.
				1= a curve for each ep along the source curve
				ex. Ep-----Ep-----Ep-----Ep
				2= a curve for each ep along the source curve as well as one between each.
				ex. Ep--x--Ep--x--Ep--x--Ep
				3= a curve for each ep along the source curve as well as two between each.
				ex. Ep-x-x-Ep-x-x-Ep-x-x-Ep

				it might do this by rebuilding the original curve at a higher count.
				'''

			def blockingSlider:

				'''

				This is the slider that controls which tube mesh is shown.
				1 = Blocking. This is the biggest hair tube and should only be used to set the major flow of the hair.
				2 = Forming. This is the middle ground for tubes, it should be used when you have the major flow and want to
					put in major forms.
				3 = Refine. This is the final position for the slider. This should be the last thing that you do before you
					convert your tubes to xGen. There will be a lot of tubes at this point so it should only be used on very
					complicated hair.
				'''

			def perTubeApplication:

				This is a check box that will make it so that any changes are made per tube and not scene wide.


			def enableTapper:

				This is a check box that will make it so that when a tube is created it will have a tapper effect applied
				to it.

			def addIsoparm:

				This is would allow the ability to manually add isoparms for refinement of the tube. It would do this by
				using the isoparm selection tool and then querying the newly created isoparm and converting it to a
				cv curve. If the new isoparm runs vertically through the tube it would add a new cv for every control
				circle. If the new isoparm runs horizontally across the tube it would be converted to a new control curve.

				ex. Vertically through tube:      Horizontally across tube:
					  Ep------------Ep				Ep-----Nc-----Ep
						------------					   Nc
					  Ep------------Ep				Ep-----Nc-----Ep

				One way that it might work is by creating new control circles when a new isoparm is inserted vertically.
				This might be easier then trying to calculate the location for new cv placement.

		"""

hairAssistTool().createGUI()
