from PyQt5 import QtWidgets, uic
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import sys
import os
import serial.tools.list_ports
import threading
from subprocess import call



base = os.path.dirname(os.path.realpath(__file__))
class Ui(QtWidgets.QMainWindow):
    def __init__(self):

        self.root = ''

        super(Ui, self).__init__()
        uic.loadUi(os.path.join(base,'APP.ui'), self)
        
        self.kaizen_pb = self.findChild(QtWidgets.QPushButton, 'kaizen_pb')
        self.kaizen_pb.clicked.connect(lambda: self.ButtonPressed('kaizen_pb'))
        self.generous_pb = self.findChild(QtWidgets.QPushButton, 'generous_pb')
        self.generous_pb.clicked.connect(lambda: self.ButtonPressed('generous_pb'))
        self.bride_pb = self.findChild(QtWidgets.QPushButton, 'bride_pb')
        self.bride_pb.clicked.connect(lambda: self.ButtonPressed('bride_pb'))
        self.queen_pb = self.findChild(QtWidgets.QPushButton, 'queen_pb')
        self.queen_pb.clicked.connect(lambda: self.ButtonPressed('queen_pb'))
        self.arduino_pb = self.findChild(QtWidgets.QPushButton, 'arduino_pb')
        self.arduino_pb.clicked.connect(lambda: self.ButtonPressed('arduino_pb'))
        self.lcd_pb = self.findChild(QtWidgets.QPushButton, 'lcd_pb')
        self.lcd_pb.clicked.connect(lambda: self.ButtonPressed('lcd_pb'))
        self.raspberrypi_pb = self.findChild(QtWidgets.QPushButton, 'raspberrypi_pb')
        self.raspberrypi_pb.clicked.connect(lambda: self.ButtonPressed('raspberrypi_pb'))

        # self.raspberrypi_pb.setEnabled(True)

        # self.showFullScreen()
        self.show()





    #upload_busy = False
    def upload_cmd(self,port,code_address):
        #global upload_busy
        
        # upload_busy = True

        os.system('avrdude -p atmega2560 -cwiring -P'
        +str(port)+' -b115200 -D -Uflash:w:'
        +str(code_address))
        
        # upload_busy = False


    def upload_arduino_code(self,machine):
        try:
            
            port = [tuple(p) for p in list(serial.tools.list_ports.comports())][0][0]
        
            if(port.find('AMA') != -1):
                raise 'no port found'
            
            self.upload_cmd(port,machine) # polling
            # threading.Thread(target=self.upload_cmd, args=(port,machine,)).start()
            
        
        except Exception as e:
            print('error in upload arduino',e)






    def find_usb(self):
        usb_base_dir = '/media/usb'

        call(['sudo', 'umount', '/dev/sda1'])

        call(['sudo', 'mkdosfs', '-F 32','-I','/dev/sda1'])

        call(['sudo', 'mount', '/dev/sda1', usb_base_dir])
        print('done mounting and formating')


    def cp_dir(self,source, target):
        call(['sudo','rsync ', '-a', source, target]) # Linux
    
    def cp_file(self,source, target):
        call(['sudo','cp', source, target]) # Linux


    def disable_other(self):
        self.arduino_pb.setEnabled(False)
        self.raspberrypi_pb.setEnabled(False)
        self.lcd_pb.setEnabled(False)

    def uncheck_other(self):
        self.kaizen_pb.setChecked(False)
        self.generous_pb.setChecked(False)
        self.bride_pb.setChecked(False)
        self.queen_pb.setChecked(False)

    def ButtonPressed(self,name):
        
        if name == "kaizen_pb":
            self.root = name
            self.uncheck_other()
            self.kaizen_pb.setChecked(True)

            self.disable_other()
            self.arduino_pb.setEnabled(True)


        elif name == "generous_pb":
            self.root = name
            self.uncheck_other()
            self.generous_pb.setChecked(True)

            self.disable_other()
            self.arduino_pb.setEnabled(True)
            self.lcd_pb.setEnabled(True)

        elif name == "bride_pb":
            self.root = name
            self.uncheck_other()
            self.bride_pb.setChecked(True)

            self.disable_other()
            self.arduino_pb.setEnabled(True)
            self.lcd_pb.setEnabled(True)

        elif name == "queen_pb":
            self.root = name
            self.uncheck_other()
            self.queen_pb.setChecked(True)

            self.disable_other()
            self.arduino_pb.setEnabled(True)
            self.raspberrypi_pb.setEnabled(True)

        elif name == "arduino_pb":
            self.find_usb()
            if self.root ==  "bride_pb":
                src = os.path.join(base,"bride/arduino/firmware.bin")
                self.cp_file(src, os.path.join(base, '/media/usb'))
            
            if self.root == "kaizen_pb":
                src = os.path.join(base,"kaizen/arduino/Robin_nano35.bin")
                self.cp_file(src, os.path.join(base, '/media/usb'))

            if self.root == "generous_pb":
                self.upload_arduino_code(os.path.join(base,"generous/arduino/generous.hex"))

            if self.root == "queen.pb":
                self.upload_arduino_code(os.path.join(base,"queen/arduino/queen.hex"))
        
        elif name == "lcd_pb":
            self.find_usb()
            if self.root ==  "bride_pb":
                self.cp_dir(os.path.join(base,"bride/lcd",'.'), '/media/usb')
                
            if self.root ==  "generous_pb":
                self.cp_dir(os.path.join(base,"generous/lcd",'.'), '/media/usb')

        elif name == "raspberrypi_pb":
            self.find_usb()
            if self.root == "queen.pb":
                call(['dd','bs=4M','if=%s.img'%(os.path.join(base,'queen/raspberry/nanodlp.img')),'of=/medai/usb','conv=fsync'])
                print('done')

    def showdialog(self):
        msg = QtWidgets.QMessageBox()
        msg.setIcon(QtWidgets.QMessageBox.Information)

        msg.setText("This is a message box")
        #msg.setInformativeText("This is additional information")
        msg.setWindowTitle("MessageBox demo")
        #msg.setDetailedText("The details are as follows:")
        #msg.setStandardButtons(QtWidgets.QMessageBox.Ok | QtWidgets.QMessageBox.Cancel)
        #msg.buttonClicked.connect(msgbtn)
            
        retval = msg.exec_()
        print ("value of pressed message box button:", retval )      



app = QtWidgets.QApplication(sys.argv)
window = Ui()
app.exec_()





"""
avrdude -v -v -v -v -p atmega2560 -cwiring -P/dev/ttyUSB0 -b115200 -D -Uflash:w:/home/pi/Desktop/fade.hex

"""
