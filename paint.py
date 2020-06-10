
from PyQt5 import QtCore, QtGui, QtWidgets


from formmodule import Ui_FormModule

class Paint(QtWidgets.QGraphicsView):
	factor = 1.25
	def __init__(self,parent=None):
		super(Paint, self).__init__()
		self.parent = parent

	#def	__init__(self):
	#	QtWidgets.QGraphicsView.__init__(self)

		#self.setObjectName("Paint")

		#self.setSceneRect(QtCore.QRectF(self.viewport().rect()))
		#self.setSceneRect(0.0,70,1454.0,448.0)
		
		self.scene	=	QtWidgets.QGraphicsScene()
		self.rubberBand = QtWidgets.QRubberBand(QtWidgets.QRubberBand.Rectangle, self)
		self.origin = QtCore.QPoint() 

		self.P1 = [0,0]
		self.P2 = [0,0]
		self.P3 = [0,0] #alineado con P1 x P2 y
		self.P4 = [0,0] #alineado con P2 x P1 y

		self.Pm1 = [0,0]
		self.Pm2 = [0,0]

		self.flagRelease = False
		self.flagSelection = False
		

	#	self.retranslateUi(self)
	#	QtCore.QMetaObject.connectSlotsByName(self)

		self.contextMenuEvent
		self.mousePressEvent
		self.mouseReleaseEvent
		self.mouseMoveEvent
		#self.resizeEvent

	#	print("sceneRect:",self.sceneRect())
		
		###Para realizar el zoom con teclas ctrl+ / ctrl -
		#self.selAllShort = QtWidgets.QShortcut(QtGui.QKeySequence(QtGui.QKeySequence.ZoomIn),self,context= QtCore.Qt.WidgetShortcut,)
		#self.selAllShort.activated.connect(self.zoom_in)
		#self.selAllShort = QtWidgets.QShortcut(QtGui.QKeySequence(QtGui.QKeySequence.ZoomOut),self,context= QtCore.Qt.WidgetShortcut,)
		#self.selAllShort.activated.connect(self.zoom_out)


	def retranslateUi(self, Paint):
		_translate = QtCore.QCoreApplication.translate
		Paint.setWindowTitle(_translate("Paint", "Paint"))


	def showEvent(self,event):
		print("showE")
		if self.parent.flagZoom != True:
			if self.parent.flagNormal != False: 
				self.setSceneRect(0.0,0.0,1454,448)
			else:
				self.setSceneRect(0.0,110.0,1454,448) #110

		#print("rect1:",self.sceneRect())
		self.populateCircuit()
		self.populateLabel()
		self.populateZoom()

	def populateZoom(self):
		print("populateZoom")
		print(self.parent.flagZoom)
		if len(self.parent.valueZoom) != 0:
			tr = self.parent.valueZoom[0]
			self.setTransform(tr)

			if self.parent.flagZoom != False:
				self.setSceneRect(0.0,0.0,0.0,0.0)

	def populateCircuit(self): 
		print("PopulateCircuit")
		self.parent.listSelect.clear()
		for i in range(0,len(self.parent.mylist),4):
			numberTab = self.parent.mylist[i]
			coordCell = self.parent.mylist #i+1 
			#nameCell = self.parent.mylist#[i+2]
			addrCell = self.parent.mylist[i+3].split("A=")

			z = self.parent.tabWidget.currentIndex() + 1 
			k = numberTab.replace('%','')

			if z == 0:
				z = 1

			#print("z",z)
			#print("k",k)
			if k == str(z):
				nameCell = self.parent.mylist[i+2].split()
				#print("nameCell:",nameCell)
				nameF = nameCell[0].partition('N=')
				tmp = coordCell[i+1].split()

				#print("name:",nameF[2])
				for i in range(2):
					if i == 0:
						y = tmp[0].partition('X=')
						coordx = y[2]
						y1 = int(coordx)*50
						y2 = y1 + 50
						print("cy1:",y1)
						print("cy2:",y2)
						if self.parent.flagZoom != False:
							print("TRUE")
							self.Pm1[1] = y1*1.5
							self.Pm2[1] = (y1*1.5) + 75
							print("Pm1[1]:",y1*1.5)
							print("Pm2[1]:",(y1*1.5) + 75)
						else:
							self.Pm1[1] = y1
							self.Pm2[1] = y2
					else:
						y = tmp[1].partition('Y=')
						coordy = y[2]
						x1 = int(coordy)*75
						x2 = x1 + 75

						if self.parent.flagZoom != False:
							print("true2")
							self.Pm1[0] = (x1*1.5) + 56
							self.Pm2[0] = (x1*1.5) + 56 + 110
						else:
							self.Pm1[0] = x1
							self.Pm2[0] = x2
						print("cx1:",x1)
						print("cx2:",x2)

				cbText = self.parent.comboBox.currentText()

				if self.flagRelease != False: #Se hizo una seleccion
					print("SELECTION")
					if self.P1 > self.P2:
						#print("1 es mayor")
						#print("x1:",self.posicion_1[0])
						#print("y1:",self.posicion_1[1])
						if ((self.P2[0]<=self.Pm1[0]) and (self.P2[1] <= self.Pm1[1])) and ((self.P2[0]<=self.Pm2[0]) and (self.P2[1]<= self.Pm2[1])) and ((self.P4[0]<=self.Pm1[0]) and (self.P4[1]>=self.Pm1[1])) and ((self.P4[0]<=self.Pm2[0]) and (self.P4[1]>=self.Pm2[1])) and ((self.P1[0]>=self.Pm1[0]) and (self.P1[1]>=self.Pm1[1])) and ((self.P1[0]>=self.Pm2[0]) and (self.P1[1]>=self.Pm2[1])) and ((self.P3[0]>=self.Pm1[0]) and (self.P3[1]<= self.Pm1[1])) and ((self.P3[0]>=self.Pm2[0]) and (self.P3[1]<=self.Pm2[1])):
						#	print("entra0")
							self.flagSelection = True

						elif ((self.P2[0]<=self.Pm1[0]) and (self.P2[1] >= self.Pm1[1])) and ((self.P2[0]<=self.Pm2[0]) and (self.P2[1]<= self.Pm2[1])) and ((self.P4[0]<=self.Pm1[0]) and (self.P4[1]>=self.Pm1[1])) and ((self.P4[0]<=self.Pm2[0]) and (self.P4[1]>=self.Pm2[1])) and ((self.P1[0]>=self.Pm1[0]) and (self.P1[1]>=self.Pm1[1])) and ((self.P1[0]>=self.Pm2[0]) and (self.P1[1]>=self.Pm2[1])) and ((self.P3[0]>=self.Pm1[0]) and (self.P3[1]>= self.Pm1[1])) and ((self.P3[0]>=self.Pm2[0]) and (self.P3[1]<=self.Pm2[1])):
						#	print("entra1")
							self.flagSelection = True

						elif ((self.P2[0]<=self.Pm1[0]) and (self.P2[1] <= self.Pm1[1])) and ((self.P2[0]<=self.Pm2[0]) and (self.P2[1]<= self.Pm2[1])) and ((self.P4[0]<=self.Pm1[0]) and (self.P4[1]>=self.Pm1[1])) and ((self.P4[0]<=self.Pm2[0]) and (self.P4[1]<=self.Pm2[1])) and ((self.P1[0]>=self.Pm1[0]) and (self.P1[1]>=self.Pm1[1])) and ((self.P1[0]>=self.Pm2[0]) and (self.P1[1]<=self.Pm2[1])) and ((self.P3[0]>=self.Pm1[0]) and (self.P3[1]<= self.Pm1[1])) and ((self.P3[0]>=self.Pm2[0]) and (self.P3[1]<=self.Pm2[1])):
						#	print("entra2")
							self.flagSelection = True

						elif ((self.P2[0]>=self.Pm1[0]) and (self.P2[1] <= self.Pm1[1])) and ((self.P2[0]<=self.Pm2[0]) and (self.P2[1]<= self.Pm2[1])) and ((self.P4[0]>=self.Pm1[0]) and (self.P4[1]>=self.Pm1[1])) and ((self.P4[0]<=self.Pm2[0]) and (self.P4[1]>=self.Pm2[1])) and ((self.P1[0]>=self.Pm1[0]) and (self.P1[1]>=self.Pm1[1])) and ((self.P1[0]>=self.Pm2[0]) and (self.P1[1]>=self.Pm2[1])) and ((self.P3[0]>=self.Pm1[0]) and (self.P3[1]<= self.Pm1[1])) and ((self.P3[0]>=self.Pm2[0]) and (self.P3[1]<=self.Pm2[1])):
						#	print("entra3")
							self.flagSelection = True

						elif ((self.P2[0]<=self.Pm1[0]) and (self.P2[1] <= self.Pm1[1])) and ((self.P2[0]<=self.Pm2[0]) and (self.P2[1]<= self.Pm2[1])) and ((self.P4[0]<=self.Pm1[0]) and (self.P4[1]>=self.Pm1[1])) and ((self.P4[0]<=self.Pm2[0]) and (self.P4[1]>=self.Pm2[1])) and ((self.P1[0]>=self.Pm1[0]) and (self.P1[1]>=self.Pm1[1])) and ((self.P1[0]<=self.Pm2[0]) and (self.P1[1]>=self.Pm2[1])) and ((self.P3[0]>=self.Pm1[0]) and (self.P3[1]<= self.Pm1[1])) and ((self.P3[0]<=self.Pm2[0]) and (self.P3[1]<=self.Pm2[1])):
						#	print("entra4")
							self.flagSelection = True

						elif ((self.P2[0]<=self.Pm1[0]) and (self.P2[1] >= self.Pm1[1])) and ((self.P2[0]<=self.Pm2[0]) and (self.P2[1]<= self.Pm2[1])) and ((self.P4[0]<=self.Pm1[0]) and (self.P4[1]>=self.Pm1[1])) and ((self.P4[0]<=self.Pm2[0]) and (self.P4[1]<=self.Pm2[1])) and ((self.P1[0]>=self.Pm1[0]) and (self.P1[1]>=self.Pm1[1])) and ((self.P1[0]>=self.Pm2[0]) and (self.P1[1]<=self.Pm2[1])) and ((self.P3[0]>=self.Pm1[0]) and (self.P3[1]>= self.Pm1[1])) and ((self.P3[0]>=self.Pm2[0]) and (self.P3[1]<=self.Pm2[1])):
						#	print("entra5")
							self.flagSelection = True

						elif ((self.P2[0]>=self.Pm1[0]) and (self.P2[1] <= self.Pm1[1])) and ((self.P2[0]<=self.Pm2[0]) and (self.P2[1]<= self.Pm2[1])) and ((self.P4[0]>=self.Pm1[0]) and (self.P4[1]>=self.Pm1[1])) and ((self.P4[0]<=self.Pm2[0]) and (self.P4[1]>=self.Pm2[1])) and ((self.P1[0]>=self.Pm1[0]) and (self.P1[1]>=self.Pm1[1])) and ((self.P1[0]<=self.Pm2[0]) and (self.P1[1]>=self.Pm2[1])) and ((self.P3[0]>=self.Pm1[0]) and (self.P3[1]<= self.Pm1[1])) and ((self.P3[0]<=self.Pm2[0]) and (self.P3[1]<=self.Pm2[1])):
						#	print("entra6")
							self.flagSelection = True
						
						elif ((self.P2[0]>=self.Pm1[0]) and (self.P2[1] >= self.Pm1[1])) and ((self.P2[0]<=self.Pm2[0]) and (self.P2[1]<= self.Pm2[1])) and ((self.P4[0]>=self.Pm1[0]) and (self.P4[1]>=self.Pm1[1])) and ((self.P4[0]<=self.Pm2[0]) and (self.P4[1]>=self.Pm2[1])) and ((self.P1[0]>=self.Pm1[0]) and (self.P1[1]>=self.Pm1[1])) and ((self.P1[0]>=self.Pm2[0]) and (self.P1[1]>=self.Pm2[1])) and ((self.P3[0]>=self.Pm1[0]) and (self.P3[1]>= self.Pm1[1])) and ((self.P3[0]>=self.Pm2[0]) and (self.P3[1]<=self.Pm2[1])):
						#	print("entra7")
							self.flagSelection = True

						elif ((self.P2[0]>=self.Pm1[0]) and (self.P2[1] <= self.Pm1[1])) and ((self.P2[0]<=self.Pm2[0]) and (self.P2[1]<= self.Pm2[1])) and ((self.P4[0]>=self.Pm1[0]) and (self.P4[1]>=self.Pm1[1])) and ((self.P4[0]<=self.Pm2[0]) and (self.P4[1]<=self.Pm2[1])) and ((self.P1[0]>=self.Pm1[0]) and (self.P1[1]>=self.Pm1[1])) and ((self.P1[0]>=self.Pm2[0]) and (self.P1[1]<=self.Pm2[1])) and ((self.P3[0]>=self.Pm1[0]) and (self.P3[1]<= self.Pm1[1])) and ((self.P3[0]>=self.Pm2[0]) and (self.P3[1]<=self.Pm2[1])):
						#	print("entra8")
							self.flagSelection = True

						elif ((self.P2[0]<=self.Pm1[0]) and (self.P2[1] <= self.Pm1[1])) and ((self.P2[0]<=self.Pm2[0]) and (self.P2[1]<= self.Pm2[1])) and ((self.P4[0]<=self.Pm1[0]) and (self.P4[1]>=self.Pm1[1])) and ((self.P4[0]<=self.Pm2[0]) and (self.P4[1]<=self.Pm2[1])) and ((self.P1[0]>=self.Pm1[0]) and (self.P1[1]>=self.Pm1[1])) and ((self.P1[0]<=self.Pm2[0]) and (self.P1[1]<=self.Pm2[1])) and ((self.P3[0]>=self.Pm1[0]) and (self.P3[1]<= self.Pm1[1])) and ((self.P3[0]<=self.Pm2[0]) and (self.P3[1]<=self.Pm2[1])):
						#	print("entra9")
							self.flagSelection = True

						elif ((self.P2[0]<=self.Pm1[0]) and (self.P2[1] >= self.Pm1[1])) and ((self.P2[0]<=self.Pm2[0]) and (self.P2[1]<= self.Pm2[1])) and ((self.P4[0]<=self.Pm1[0]) and (self.P4[1]>=self.Pm1[1])) and ((self.P4[0]<=self.Pm2[0]) and (self.P4[1]>=self.Pm2[1])) and ((self.P1[0]>=self.Pm1[0]) and (self.P1[1]>=self.Pm1[1])) and ((self.P1[0]<=self.Pm2[0]) and (self.P1[1]>=self.Pm2[1])) and ((self.P3[0]>=self.Pm1[0]) and (self.P3[1]>= self.Pm1[1])) and ((self.P3[0]<=self.Pm2[0]) and (self.P3[1]<=self.Pm2[1])):
						#	print("entra10")
							self.flagSelection = True

					else:
						#print("2 es mayor")
						##verificar checar funcionamiento
						if ((self.P1[0]<=self.Pm1[0]) and (self.P1[1] <= self.Pm1[1])) and ((self.P1[0]<=self.Pm2[0]) and (self.P1[1]<= self.Pm2[1])) and ((self.P3[0]<=self.Pm1[0]) and (self.P3[1]>=self.Pm1[1])) and ((self.P3[0]<=self.Pm2[0]) and (self.P3[1]>=self.Pm2[1])) and ((self.P2[0]>=self.Pm1[0]) and (self.P2[1]>=self.Pm1[1])) and ((self.P2[0]>=self.Pm2[0]) and (self.P2[1]>=self.Pm2[1])) and ((self.P4[0]>=self.Pm1[0]) and (self.P4[1]<= self.Pm1[1])) and ((self.P4[0]>=self.Pm2[0]) and (self.P4[1]<=self.Pm2[1])):
						#	print("entra0")
							self.flagSelection = True

						elif ((self.P1[0]<=self.Pm1[0]) and (self.P1[1] >= self.Pm1[1])) and ((self.P1[0]<=self.Pm2[0]) and (self.P1[1]<= self.Pm2[1])) and ((self.P3[0]<=self.Pm1[0]) and (self.P3[1]>=self.Pm1[1])) and ((self.P3[0]<=self.Pm2[0]) and (self.P3[1]>=self.Pm2[1])) and ((self.P2[0]>=self.Pm1[0]) and (self.P2[1]>=self.Pm1[1])) and ((self.P2[0]>=self.Pm2[0]) and (self.P2[1]>=self.Pm2[1])) and ((self.P4[0]>=self.Pm1[0]) and (self.P4[1]>= self.Pm1[1])) and ((self.P4[0]>=self.Pm2[0]) and (self.P4[1]<=self.Pm2[1])):
						#	print("entra1")
							self.flagSelection = True

						elif ((self.P1[0]<=self.Pm1[0]) and (self.P1[1] <= self.Pm1[1])) and ((self.P1[0]<=self.Pm2[0]) and (self.P1[1]<= self.Pm2[1])) and ((self.P3[0]<=self.Pm1[0]) and (self.P3[1]>=self.Pm1[1])) and ((self.P3[0]<=self.Pm2[0]) and (self.P3[1]<=self.Pm2[1])) and ((self.P2[0]>=self.Pm1[0]) and (self.P2[1]>=self.Pm1[1])) and ((self.P2[0]>=self.Pm2[0]) and (self.P2[1]<=self.Pm2[1])) and ((self.P4[0]>=self.Pm1[0]) and (self.P4[1]<= self.Pm1[1])) and ((self.P4[0]>=self.Pm2[0]) and (self.P4[1]<=self.Pm2[1])):
						#	print("entra2")
							self.flagSelection = True

						elif ((self.P1[0]>=self.Pm1[0]) and (self.P1[1] <= self.Pm1[1])) and ((self.P1[0]<=self.Pm2[0]) and (self.P1[1]<= self.Pm2[1])) and ((self.P3[0]>=self.Pm1[0]) and (self.P3[1]>=self.Pm1[1])) and ((self.P3[0]<=self.Pm2[0]) and (self.P3[1]>=self.Pm2[1])) and ((self.P2[0]>=self.Pm1[0]) and (self.P2[1]>=self.Pm1[1])) and ((self.P2[0]>=self.Pm2[0]) and (self.P2[1]>=self.Pm2[1])) and ((self.P4[0]>=self.Pm1[0]) and (self.P4[1]<= self.Pm1[1])) and ((self.P4[0]>=self.Pm2[0]) and (self.P4[1]<=self.Pm2[1])):
						#	print("entra3")
							self.flagSelection = True

						elif ((self.P1[0]<=self.Pm1[0]) and (self.P1[1] <= self.Pm1[1])) and ((self.P1[0]<=self.Pm2[0]) and (self.P1[1]<= self.Pm2[1])) and ((self.P3[0]<=self.Pm1[0]) and (self.P3[1]>=self.Pm1[1])) and ((self.P3[0]<=self.Pm2[0]) and (self.P3[1]>=self.Pm2[1])) and ((self.P2[0]>=self.Pm1[0]) and (self.P2[1]>=self.Pm1[1])) and ((self.P2[0]<=self.Pm2[0]) and (self.P2[1]>=self.Pm2[1])) and ((self.P4[0]>=self.Pm1[0]) and (self.P4[1]<= self.Pm1[1])) and ((self.P4[0]<=self.Pm2[0]) and (self.P4[1]<=self.Pm2[1])):
						#	print("entra4")
							self.flagSelection = True

						elif ((self.P1[0]<=self.Pm1[0]) and (self.P1[1] >= self.Pm1[1])) and ((self.P1[0]<=self.Pm2[0]) and (self.P1[1]<= self.Pm2[1])) and ((self.P3[0]<=self.Pm1[0]) and (self.P3[1]>=self.Pm1[1])) and ((self.P3[0]<=self.Pm2[0]) and (self.P3[1]<=self.Pm2[1])) and ((self.P2[0]>=self.Pm1[0]) and (self.P2[1]>=self.Pm1[1])) and ((self.P2[0]>=self.Pm2[0]) and (self.P2[1]<=self.Pm2[1])) and ((self.P4[0]>=self.Pm1[0]) and (self.P4[1]>= self.Pm1[1])) and ((self.P4[0]>=self.Pm2[0]) and (self.P4[1]<=self.Pm2[1])):
						#	print("entra5")
							self.flagSelection = True

						elif ((self.P1[0]>=self.Pm1[0]) and (self.P1[1] <= self.Pm1[1])) and ((self.P1[0]<=self.Pm2[0]) and (self.P1[1]<= self.Pm2[1])) and ((self.P3[0]>=self.Pm1[0]) and (self.P3[1]>=self.Pm1[1])) and ((self.P3[0]<=self.Pm2[0]) and (self.P3[1]>=self.Pm2[1])) and ((self.P2[0]>=self.Pm1[0]) and (self.P2[1]>=self.Pm1[1])) and ((self.P2[0]<=self.Pm2[0]) and (self.P2[1]>=self.Pm2[1])) and ((self.P4[0]>=self.Pm1[0]) and (self.P4[1]<= self.Pm1[1])) and ((self.P4[0]<=self.Pm2[0]) and (self.P4[1]<=self.Pm2[1])):
						#	print("entra6")
							self.flagSelection = True
						
						elif ((self.P1[0]>=self.Pm1[0]) and (self.P1[1] >= self.Pm1[1])) and ((self.P1[0]<=self.Pm2[0]) and (self.P1[1]<= self.Pm2[1])) and ((self.P3[0]>=self.Pm1[0]) and (self.P3[1]>=self.Pm1[1])) and ((self.P3[0]<=self.Pm2[0]) and (self.P3[1]>=self.Pm2[1])) and ((self.P2[0]>=self.Pm1[0]) and (self.P2[1]>=self.Pm1[1])) and ((self.P2[0]>=self.Pm2[0]) and (self.P2[1]>=self.Pm2[1])) and ((self.P4[0]>=self.Pm1[0]) and (self.P4[1]>= self.Pm1[1])) and ((self.P4[0]>=self.Pm2[0]) and (self.P4[1]<=self.Pm2[1])):
						#	print("entra7")
							self.flagSelection = True

						elif ((self.P1[0]>=self.Pm1[0]) and (self.P1[1] <= self.Pm1[1])) and ((self.P1[0]<=self.Pm2[0]) and (self.P1[1]<= self.Pm2[1])) and ((self.P3[0]>=self.Pm1[0]) and (self.P3[1]>=self.Pm1[1])) and ((self.P3[0]<=self.Pm2[0]) and (self.P3[1]<=self.Pm2[1])) and ((self.P2[0]>=self.Pm1[0]) and (self.P2[1]>=self.Pm1[1])) and ((self.P2[0]>=self.Pm2[0]) and (self.P2[1]<=self.Pm2[1])) and ((self.P4[0]>=self.Pm1[0]) and (self.P4[1]<= self.Pm1[1])) and ((self.P4[0]>=self.Pm2[0]) and (self.P4[1]<=self.Pm2[1])):
						#	print("entra8")
							self.flagSelection = True

						elif ((self.P1[0]<=self.Pm1[0]) and (self.P1[1] <= self.Pm1[1])) and ((self.P1[0]<=self.Pm2[0]) and (self.P1[1]<= self.Pm2[1])) and ((self.P3[0]<=self.Pm1[0]) and (self.P3[1]>=self.Pm1[1])) and ((self.P3[0]<=self.Pm2[0]) and (self.P3[1]<=self.Pm2[1])) and ((self.P2[0]>=self.Pm1[0]) and (self.P2[1]>=self.Pm1[1])) and ((self.P2[0]<=self.Pm2[0]) and (self.P2[1]<=self.Pm2[1])) and ((self.P4[0]>=self.Pm1[0]) and (self.P4[1]<= self.Pm1[1])) and ((self.P4[0]<=self.Pm2[0]) and (self.P4[1]<=self.Pm2[1])):
						#	print("entra9")
							self.flagSelection = True

						elif ((self.P1[0]<=self.Pm1[0]) and (self.P1[1] >= self.Pm1[1])) and ((self.P1[0]<=self.Pm2[0]) and (self.P1[1]<= self.Pm2[1])) and ((self.P3[0]<=self.Pm1[0]) and (self.P3[1]>=self.Pm1[1])) and ((self.P3[0]<=self.Pm2[0]) and (self.P3[1]>=self.Pm2[1])) and ((self.P2[0]>=self.Pm1[0]) and (self.P2[1]>=self.Pm1[1])) and ((self.P2[0]<=self.Pm2[0]) and (self.P2[1]>=self.Pm2[1])) and ((self.P4[0]>=self.Pm1[0]) and (self.P4[1]>= self.Pm1[1])) and ((self.P4[0]<=self.Pm2[0]) and (self.P4[1]<=self.Pm2[1])):
						#	print("entra10")
							self.flagSelection = True

				print("Name:",nameF[2])
				print("x1:",self.Pm1[0])
				print("y1:",self.Pm1[1])
				print("x2:",self.Pm2[0])
				print("y2:",self.Pm2[1])

				self.form = Ui_FormModule(nameF[2],cbText,self)
				if self.flagSelection != False: #checar que modulos entran en las coordenadas y con respecto a eso hacer la seleccion 
					self.flagSelection = False
					self.form.selectionModule()

					#print("Name:",nameF[2])
					#print("x1:",x1)
					#print("y1:",y1)
					#print("x2:",x2)
					#print("y2:",y2)
				#	print("addrCell:",addrCell[1])
					self.parent.listSelect.append(addrCell[1])

					#print("listSelect:",self.parent.listSelect)
				self.form.setAttribute(QtCore.Qt.WA_TranslucentBackground,True)
				self.form.move(x1,y1)

				self.scene.addWidget(self.form)
				self.setScene(self.scene)
				#print("listSelect:",self.parent.listSelect)

	def populateLabel(self):
		print("PopulateLabel")
		for i in range(0,len(self.parent.mylabel),3):
			numberTabL = self.parent.mylabel[i]
			coordCellL = self.parent.mylabel #[i+1]
			nameCellL = self.parent.mylabel[i+2]

			z = self.parent.tabWidget.currentIndex() + 1 
			k = numberTabL.replace('%','')

			if z == 0:
				z = 1

			#print("z2",z)
			#print("k2",k)
			label = nameCellL.split('#')
			number = label[1].split('$')
			lblt = QtGui.QFont("Arial",int(number[0]), QtGui.QFont.Black)
			#item = QtWidgets.QTableWidgetItem(label[0])
			lbltext = QtWidgets.QLabel(label[0])

			if number[1] == 'AT':
				lbltext.setAlignment(QtCore.Qt.AlignTop)
			else:
				lbltext.setAlignment(QtCore.Qt.AlignBottom)

			lbltext.setFont(lblt)
			lbltext.setStyleSheet("QLabel { background-color : white; }")
			#item.setFont(lblt)
			#item.setBackground(QtGui.QColor('white'))

			if k == str(z):
				tmpL = coordCellL[i+1].split()
				for i in range(2):
					if i == 0:
						y = tmpL[0].partition('X=')
						coordx = y[2]
					else:
						y = tmpL[1].partition('Y=')
						coordy = y[2]

				lbltext.move(int(coordy)*75,int(coordx)*50)
				self.scene.addWidget(lbltext)
				self.setScene(self.scene)

	def contextMenuEvent(self,event):
		print("contextEvent")
		self.rubberBand.hide()
		self.popMenu = QtWidgets.QMenu(self)
		startAct = self.popMenu.addAction('LoadPrograms/Start')
		pauseAct = self.popMenu.addAction('Pause')
		stopAct = self.popMenu.addAction('Stop')

		action = self.popMenu.exec_(self.mapToGlobal(event.pos()))

		if action == startAct:
			self.parent.btnIniciar()

		elif action == pauseAct:
			self.parent.btnPausar()
		
		elif action == stopAct:
			self.parent.btnDetener()

	def totalMylist(self):
		self.auxMylist = self.parent.mylist[:]

	def	mousePressEvent(self,event):
		if event.button() ==  QtCore.Qt.LeftButton:
			self.flagRelease = False

			self.P1[0] = event.pos().x()
			self.P1[1] = event.pos().y()

			print("P1:",self.P1)
			self.origin = QtCore.QPoint(event.pos())
			self.rubberBand.setGeometry(QtCore.QRect(self.origin,QtCore.QSize()))
			self.rubberBand.show()
			print("P1G:",event.globalPos())
			print("P1D:",event.localPos())


	def mouseMoveEvent(self, event):
		if self.flagRelease != True:
			if not self.origin.isNull():
				self.rubberBand.setGeometry(QtCore.QRect(self.origin,event.pos()).normalized())		


	def mouseReleaseEvent(self, event):
		if event.button() == QtCore.Qt.LeftButton:
			self.flagRelease = True
			self.P2[0] = event.pos().x()
			self.P2[1] = event.pos().y()

			self.P3[0] = self.P1[0]  #alineado con P1 x P2 y
			self.P3[1] = self.P2[1]
			
			self.P4[0] = self.P2[0]  #alineado con P2 x P1 y
			self.P4[1] = self.P1[1]

			print("P2:",self.P2)
			print("P3:",self.P3)
			print("P4:",self.P4)

			print("P2G:",event.globalPos())
			print("P1D:",event.localPos())

			self.populateCircuit()

	def zoomCmb(self,det):
		#print("zoom comb")
		#print("det:",det)

		if det > 0.8:
			print("flagZoom")
			self.parent.flagZoom = True
			self.setSceneRect(0.0,0.0,2000,1000) #rango a posible cambio
		else:
			self.parent.flagZoom = False
		
		scale_tr = QtGui.QTransform()
		scale_tr.scale(Paint.factor,Paint.factor)
		
		scale_tr2 = QtGui.QTransform()
		scale_tr2.scale(det,det)

		tr = scale_tr2 * scale_tr
		print("tr:",tr)
		self.setTransform(tr)
		#print("2:",self.transform().determinant())

		self.parent.valueZoom.clear()
		self.parent.valueZoom.append(tr)

	'''
	def zoom_in(self):
		#print("zoom_in")
		scale_tr = QtGui.QTransform()
		scale_tr.scale(Paint.factor, Paint.factor)
		tr = self.transform() * scale_tr
		
		self.setTransform(tr)
		self.parent.valueZoom.clear()

		self.parent.valueZoom.append('zoom_in')
		self.parent.valueZoom.append(tr)

	def zoom_out(self):
		#print("zoom_out")
		scale_tr = QtGui.QTransform()
		scale_tr.scale(Paint.factor, Paint.factor)
		scale_inverted, invertible = scale_tr.inverted()
		
		if invertible:
			tr = self.transform() * scale_inverted
			self.setTransform(tr)

		self.parent.valueZoom.clear()
		self.parent.valueZoom.append('zoom_out')
		self.parent.valueZoom.append(tr)
	'''


