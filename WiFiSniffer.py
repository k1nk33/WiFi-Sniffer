# from menu import analysis
from NetUtil import NetUtil
import time
import collections
# Import PyQT Stuff
from PyQt4 import QtCore, QtGui
from main import Ui_MainWindow


# MainClass
class wifi_class(QtGui.QMainWindow, Ui_MainWindow):

    '''
    This is the Main Class which builds and processes the data required to
    run the program
    '''
    # Initialize mega__class
    def __init__(self):
        QtGui.QMainWindow.__init__(self)

        # Call the UI Main window class
        self.setupUi(self)
        self.nextCount = 0
        self.scanArray = []
        self.setStyleSheet(" font-size: 10px; font-family: Ubuntu Light;")
        self.viewOne.setGeometry(QtCore.QRect(10, 10, 580, 580))
        self.viewTwo.setGeometry(QtCore.QRect(10, 600, 580, 580))
        self.viewThree.setGeometry(QtCore.QRect(10, 600, 580, 580))

        self.floorNext.setEnabled(True)
        self.floorNext.clicked.connect(self.next)
        self.roomNext.clicked.connect(self.next)

        # Link Actions
        self.groundFloor.clicked.connect(self.getFloorWing)
        self.firstFloor.clicked.connect(self.getFloorWing)
        self.secondFloor.clicked.connect(self.getFloorWing)

        self.u.clicked.connect(self.getFloorWing)
        self.v.clicked.connect(self.getFloorWing)
        self.w.clicked.connect(self.getFloorWing)
        self.x.clicked.connect(self.getFloorWing)
        self.y.clicked.connect(self.getFloorWing)
        self.z.clicked.connect(self.getFloorWing)
        
        self.csv.clicked.connect(self.enableSave)
        self.database.clicked.connect(self.enableSave)
        self.logFile.clicked.connect(self.enableSave)
        self.allFiles.clicked.connect(self.enableSave)
        self.saveFileBttn.clicked.connect(self.saveFile)
        self.restartButton.clicked.connect(self.resetProgram)
        self.exitButton.clicked.connect(self.closeProgram)
        
        
        # Build Room Data
        self.roomsU = [['', 'U103', 'U105', 'U107', 'U108', 'U110'],
                       ['', 'U201', 'U211', 'U212', 'U213', 'U214'],
                       ['', 'U301', 'U302', 'U303', 'U304', 'U305', 'U306', 'U309', 'U310']]
        
        self.roomsV = [['', 'V103', 'V104', 'V105', 'V106', 'V107', 'V108', 'V109'],
                       ['', 'V203', 'V204', 'V205', 'V206', 'V207'],
                       ['', 'V301', 'V302', 'V303', 'V304', 'V305', 'V306', 'V308', 'V311']]
        
        self.roomsW = [['', 'W Coffee Area','W101', 'W106', 'W107', 'W108'],
                       ['', 'W201', 'W202', 'W205', 'W206', 'W207', 'W208'],
                       ['', 'W301 MSC Lab', 'W304', 'W305']]
        
        self.roomsX = [['', 'X101', 'X101B', 'X106', 'X107', 'X108', 'X109'],
                       ['', 'X203', 'X204', 'X205', 'X206', 'X207'],
                       ['',
                        'X Head of Administration',
                        'X Head of Dept Office 2',
                        'X Head of Dept Office',
                        'X Head of School Office',
                        'X Meeting Room General',
                        'X School Admin General', 'X309', 'X310']]
        
        self.roomsY = [['', 'Y102', 'Y103', 'Y105', 'Y107'],
                       ['', 'Y201', 'Y202', 'Y205', 'Y206', 'Y207'],
                       ['', 'Y301', 'Y302', 'Y303', 'Y304', 'Y305', 'Y306', 'Y307', 'Y308']]
        
        self.roomsZ = [['','Z103', 'Z104', 'Z105', 'Z107'],
                       ['', 'Z203', 'Z204', 'Z205', 'Z206', 'Z207'],
                       ['', 'Z301', 'Z302', 'Z303', 'Z304', 'Z305', 'Z306', 'Z308']]
        

        # Load U by Default
        self.selectRoom.addItems(self.roomsU[0])
        self.getRoom()
        # Monitor the ComboBox
        self.selectRoom.currentIndexChanged.connect(self.getRoom)
        self.scanButton.clicked.connect(self.scanUpdate)
        self.scanCount = 0

        # Dictionary for results dictionary
        self.results = []
        self.counter = 0
        self.nsewc=["","North","South","East","West","Central"]
        
    # Gather the Room Information
    def getRoom(self):

        if self.selectRoom.currentText() == '':
            self.floorNext.setEnabled(False)
        else:
            self.floorNext.setEnabled(True)
            self.floorImage.setPixmap(
                QtGui.QPixmap(
                    ("assets/rooms/" + str(self.selectRoom.currentText())
                        + ".jpg")))
            self.room = self.selectRoom.currentText()
            self.fname = str(
                ('/' + self.room + '_' + time.strftime("%d-%m-%Y-%H:%M:%S")))

    # Gather the Floor and Wing Information
    def getFloorWing(self):

        # Set the Floor Index
        if self.groundFloor.isChecked():
            self.floor = 0
        elif self.firstFloor.isChecked():
            self.floor = 1
        elif self.secondFloor.isChecked():
            self.floor = 2

        # Set the Room Information
        self.selectRoom.clear()

        if self.u.isChecked():
            self.selectRoom.addItems(self.roomsU[self.floor])
            self.floorImage.setPixmap(
                QtGui.QPixmap(("assets/" + str(self.floor) + "U.jpg")))

        elif self.v.isChecked():
            self.selectRoom.addItems(self.roomsV[self.floor])
            self.floorImage.setPixmap(
                QtGui.QPixmap(("assets/" + str(self.floor) + "V.jpg")))

        elif self.w.isChecked():
            self.selectRoom.addItems(self.roomsW[self.floor])
            self.floorImage.setPixmap(
                QtGui.QPixmap(("assets/" + str(self.floor) + "W.jpg")))

        elif self.x.isChecked():
            self.selectRoom.addItems(self.roomsX[self.floor])
            self.floorImage.setPixmap(
                QtGui.QPixmap(("assets/" + str(self.floor) + "X.jpg")))

        elif self.y.isChecked():
            self.selectRoom.addItems(self.roomsY[self.floor])
            self.floorImage.setPixmap(
                QtGui.QPixmap(("assets/" + str(self.floor) + "Y.jpg")))

        elif self.z.isChecked():
            self.selectRoom.addItems(self.roomsZ[self.floor])
            self.floorImage.setPixmap(
                QtGui.QPixmap(("assets/" + str(self.floor) + "Z.jpg")))

    # Turn the Page - Room Scan
    def next(self):

        if self.nextCount == 0:
            self.roomImage.setPixmap(
                QtGui.QPixmap(
                    ("assets/rooms/" + str(self.selectRoom.currentText())
                     + ".jpg")))
            self.viewOne.setGeometry(QtCore.QRect(10, 600, 580, 580))
            self.viewThree.setGeometry(QtCore.QRect(10, 600, 580, 580))
            self.viewTwo.setGeometry(QtCore.QRect(10, 10, 580, 580))
            self.nextCount += 1

        else:
            self.viewOne.setGeometry(QtCore.QRect(10, 600, 580, 580))
            self.viewTwo.setGeometry(QtCore.QRect(10, 600, 580, 580))
            self.viewThree.setGeometry(QtCore.QRect(10, 10, 580, 580))

            # Force Column Widths
            self.dataTable.setColumnWidth(0, 90)
            self.dataTable.setColumnWidth(1, 105)
            self.dataTable.setColumnWidth(2, 50)
            self.dataTable.setColumnWidth(3, 65)
            self.dataTable.setColumnWidth(4, 50)
            self.dataTable.setColumnWidth(5, 75)

            # Build Table from Arrays
            x = 0
            for item in self.scanArray:
                y = 0

                for data in self.scanArray[x]:
                    self.dataTable.setItem(x, y, QtGui.QTableWidgetItem(data))
                    y += 1
                x += 1

    # Initiate Scan Sequence
    def scanUpdate(self):

        self.scanCount += 1

        if self.scanCount == 1:
            self.gatherData()
            self.scanButton.setText("Scan South")

        if self.scanCount == 2:
            self.gatherData()
            self.scanButton.setText("Scan East")

        if self.scanCount == 3:
            self.gatherData()
            self.scanButton.setText("Scan West")

        if self.scanCount == 4:
            self.gatherData()
            self.scanButton.setText("Scan Center")

        if self.scanCount == 5:
            self.gatherData()

            # Disable the Scan Button
            self.scanButton.setEnabled(False)
            self.scanButton.setText("SCAN COMPLETE")
            self.roomNext.setEnabled(True)

    def gatherData(self):
        '''
        Method responsible for gathering data
        '''

        # Returns NetUtil object for each NSEW test, in case gateway
        # changes with location
        self.nt = NetUtil()

        # Calls Ping method with arg ping, returns unused list
        p_results = self.nt.pingTest('ping')
        type(p_results)
        quality, level = self.nt.signalTest()
        res_dict = collections.OrderedDict()
        res_dict['GatewayIP'] = self.nt.ping_ip
        res_dict['GatewayMac'] = self.nt.gw_mac
        res_dict['PacketLoss %'] = self.nt.pingTest('loss')
        res_dict['Delay ms'] = self.nt.pingTest('delay')        
        res_dict['Quality /70'] = quality
        res_dict['Level dBms'] = level
        res_dict['Throughput Mbps'] = self.nt.pingTest('tput')

        self.results.append(res_dict)
        self.counter += 1

        # Apply gathered information to a variable
        scanData = []
        scanData2 = []
        for k, v in res_dict.items():
            # String for Text Area
            string = '%s\n%s\n' % (k, v)
            # String for scanArray
            string2 = '%s\n' % v
            # Append arrays
            scanData.append(string)
            scanData2.append(string2)

        # Store Information in an array
        self.scanArray.append(scanData2)
        scanData = ' '.join(scanData)
        scanData2 = ', '.join(scanData2)
        
        # Apply information to vtext Field
        if self.nt.ping_ip == None:
            self.scanInfo.setPlainText("Scan Failed, Error!\n\nPlease check your wireless connection!")
        else:         
            self.scanInfo.setPlainText("{} Test:\r\n\n {}\r\n ".format(self.nsewc[self.scanCount],
                                                               scanData
                                                               ))

        #if self.counter == 5:
         #   nt.saveFile(self.fname, self.results)
    
    #Save File
    def enableSave(self):        
        #Enabled the Save Button
        self.saveFileBttn.setEnabled(True)
    def saveFile(self):
        # nt=NetUtil()
        if self.csv.isChecked():
            self.nt.saveFile(self.fname, self.results,2)
        elif self.database.isChecked():
            self.nt.saveFile(self.fname, self.results,0)
        elif self.logFile.isChecked():
            self.nt.saveFile(self.fname, self.results,1)
        elif self.allFiles.isChecked():    
            self.nt.saveFile(self.fname, self.results,4)
        
        
    #Reset The Program
    def resetProgram(self):
        self.viewTwo.setGeometry(QtCore.QRect(10, 600, 580, 580))
        self.viewThree.setGeometry(QtCore.QRect(10, 600, 580, 580))
        self.viewOne.setGeometry(QtCore.QRect(10, 10, 580, 580))
        self.nextCount = 0
        self.scanCount = 0
        self.scanArray = []
        self.scanButton.setText("Scan South")
        self.scanButton.setEnabled(True)
        self.roomNext.setEnabled(False)
    
    #Close The Program
    def closeProgram(self):
        #Terminate the program
        self.close()
        
if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    MainWindow = wifi_class()
    MainWindow.show()
    sys.exit(app.exec_())
