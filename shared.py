import threading

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QFileDialog, QDialog, QMessageBox, QScrollBar, QApplication, QWidget, QMainWindow
from PyQt5.QtPrintSupport import QPrinter, QPrintDialog
from PyQt5.QtGui import QIcon, QFont, QFontDatabase, QDesktopServices
from PyQt5.QtCore import QEventLoop, QByteArray, Qt, QUrl, pyqtSignal, pyqtSlot, QObject, QTimer, QElapsedTimer, QTime

serial_number = None

# constants that will indicate a pin state
LOW = 0
HIGH = 1

lock_uart = threading.Lock() # lock will be used as a lock for the UART
lock_memory = threading.Lock() # lock will be used as a lock for the memory

devStart = 1
devStop = 2

DA_PI = [] #todos los modulos
ON_PI = [] #solo los que dieron TRUE


#la cantidad de DEV_ADDR dependera de cuantos dip. sean por raspb(15aprx)
DEV_ADDR = [
	[],
	[],
	[],
	[],
	[],
	[],
	[],
	[],
	[],
	[],
	[],
	[],
	[],
	[],
	[],
	[],
	[],
	[],
	[],
	[]
]

#ping #I #V #T #P #t #Tt #TT #I #Name #Show #Address
DEV = [
    #[False, '', '', '', '', '', '', '', ''],
    [False, '', '', '', '', '', '', '', 'I', True, 1],
    [False, '', '', '', '', '', '', '', 'I', True, 2],
    [False, '', '', '', '', '', '', '', 'I', True, 3],
    [False, '', '', '', '', '', '', '', 'I', True, 4], 
    [False, '', '', '', '', '', '', '', 'I', True, 5], 
    [False, '', '', '', '', '', '', '', 'I', True, 6], 
    [False, '', '', '', '', '', '', '', 'I', True, 7], 
    [False, '', '', '', '', '', '', '', 'I', True, 8], 
    [False, '', '', '', '', '', '', '', 'I', True, 9], 
    [False, '', '', '', '', '', '', '', 'I', True, 10], 
    [False, '', '', '', '', '', '', '', 'I', True, 11], 
    [False, '', '', '', '', '', '', '', 'I', True, 12], 
    [False, '', '', '', '', '', '', '', 'I', True, 13], 
    [False, '', '', '', '', '', '', '', 'I', True, 14], 
    [False, '', '', '', '', '', '', '', 'I', True, 15], 
    [False, '', '', '', '', '', '', '', 'I', True, 16], 
    [False, '', '', '', '', '', '', '', 'I', True, 17], 
    [False, '', '', '', '', '', '', '', 'I', True, 18], 
    [False, '', '', '', '', '', '', '', 'I', True, 19], 
    [False, '', '', '', '', '', '', '', 'I', True, 20], 
    [False, '', '', '', '', '', '', '', 'I', True, 21],
    [False, '', '', '', '', '', '', '', 'I', True, 22],
    [False, '', '', '', '', '', '', '', 'I', True, 23],
    [False, '', '', '', '', '', '', '', 'I', True, 24],
    [False, '', '', '', '', '', '', '', 'I', True, 25],
    [False, '', '', '', '', '', '', '', 'I', True, 26],
    [False, '', '', '', '', '', '', '', 'I', True, 27],
    [False, '', '', '', '', '', '', '', 'I', True, 28],

    [False, '', '', '', '', '', '', '', '', True, 29],
    [False, '', '', '', '', '', '', '', '', True, 30],
    [False, '', '', '', '', '', '', '', '', True, 31],
    [False, '', '', '', '', '', '', '', '', True, 32], 
    [False, '', '', '', '', '', '', '', '', True, 33], 
    [False, '', '', '', '', '', '', '', '', True, 34], 
    [False, '', '', '', '', '', '', '', '', True, 35], 
    [False, '', '', '', '', '', '', '', '', True, 36], 
    [False, '', '', '', '', '', '', '', '', True, 37], 
    [False, '', '', '', '', '', '', '', '', True, 38], 
    [False, '', '', '', '', '', '', '', '', True, 39], 
    [False, '', '', '', '', '', '', '', '', True, 40], 
    [False, '', '', '', '', '', '', '', '', True, 41], 
    [False, '', '', '', '', '', '', '', '', True, 42], 
    [False, '', '', '', '', '', '', '', '', True, 43], 
    [False, '', '', '', '', '', '', '', '', True, 44], 
    [False, '', '', '', '', '', '', '', '', True, 45], 
    [False, '', '', '', '', '', '', '', '', True, 46], 
    [False, '', '', '', '', '', '', '', '', True, 47], 
    [False, '', '', '', '', '', '', '', '', True, 48], 
    [False, '', '', '', '', '', '', '', '', True, 49],
    [False, '', '', '', '', '', '', '', '', True, 50],
    [False, '', '', '', '', '', '', '', '', True, 51],
    [False, '', '', '', '', '', '', '', '', True, 52],
    [False, '', '', '', '', '', '', '', '', True, 53],
    [False, '', '', '', '', '', '', '', '', True, 54],
    [False, '', '', '', '', '', '', '', '', True, 55],
    [False, '', '', '', '', '', '', '', '', True, 56], 

    [False, '', '', '', '', '', '', '', '', True, 57],
    [False, '', '', '', '', '', '', '', '', True, 58],
    [False, '', '', '', '', '', '', '', '', True, 59],
    [False, '', '', '', '', '', '', '', '', True, 60], 
    [False, '', '', '', '', '', '', '', '', True, 61], 
    [False, '', '', '', '', '', '', '', '', True, 62], 
    [False, '', '', '', '', '', '', '', '', True, 63], 
    [False, '', '', '', '', '', '', '', '', True, 64], 
    [False, '', '', '', '', '', '', '', '', True, 65], 
    [False, '', '', '', '', '', '', '', '', True, 66], 
    [False, '', '', '', '', '', '', '', '', True, 67], 
    [False, '', '', '', '', '', '', '', '', True, 68], 
    [False, '', '', '', '', '', '', '', '', True, 69], 
    [False, '', '', '', '', '', '', '', '', True, 70], 
    [False, '', '', '', '', '', '', '', '', True, 71], 
    [False, '', '', '', '', '', '', '', '', True, 72], 
    [False, '', '', '', '', '', '', '', '', True, 73], 
    [False, '', '', '', '', '', '', '', '', True, 74], 
    [False, '', '', '', '', '', '', '', '', True, 75], 
    [False, '', '', '', '', '', '', '', '', True, 76], 
    [False, '', '', '', '', '', '', '', '', True, 77],
    [False, '', '', '', '', '', '', '', '', True, 78],
    [False, '', '', '', '', '', '', '', '', True, 79],
    [False, '', '', '', '', '', '', '', '', True, 80],
    [False, '', '', '', '', '', '', '', '', True, 81],
    [False, '', '', '', '', '', '', '', '', True, 82],
    [False, '', '', '', '', '', '', '', '', True, 83],
    [False, '', '', '', '', '', '', '', '', True, 84],

    [False, '', '', '', '', '', '', '', '', True, 85],
    [False, '', '', '', '', '', '', '', '', True, 86],
    [False, '', '', '', '', '', '', '', '', True, 87],
    [False, '', '', '', '', '', '', '', '', True, 88], 
    [False, '', '', '', '', '', '', '', '', True, 89], 
    [False, '', '', '', '', '', '', '', '', True, 90], 
    [False, '', '', '', '', '', '', '', '', True, 91], 
    [False, '', '', '', '', '', '', '', '', True, 92], 
    [False, '', '', '', '', '', '', '', '', True, 93], 
    [False, '', '', '', '', '', '', '', '', True, 94], 
    [False, '', '', '', '', '', '', '', '', True, 95], 
    [False, '', '', '', '', '', '', '', '', True, 96], 
    [False, '', '', '', '', '', '', '', '', True, 97], 
    [False, '', '', '', '', '', '', '', '', True, 98], 
    [False, '', '', '', '', '', '', '', '', True, 99], 
    [False, '', '', '', '', '', '', '', '', True, 100], 
    [False, '', '', '', '', '', '', '', '', True, 101], 
    [False, '', '', '', '', '', '', '', '', True, 102], 
    [False, '', '', '', '', '', '', '', '', True, 103], 
    [False, '', '', '', '', '', '', '', '', True, 104], 
    [False, '', '', '', '', '', '', '', '', True, 105],
    [False, '', '', '', '', '', '', '', '', True, 106],
    [False, '', '', '', '', '', '', '', '', True, 107],
    [False, '', '', '', '', '', '', '', '', True, 108],
    [False, '', '', '', '', '', '', '', '', True, 109],
    [False, '', '', '', '', '', '', '', '', True, 110],
    [False, '', '', '', '', '', '', '', '', True, 111],
    [False, '', '', '', '', '', '', '', '', True, 112], 

   
    [False, '', '', '', '', '', '', '', '', True, 85],
    [False, '', '', '', '', '', '', '', '', True, 86],
    [False, '', '', '', '', '', '', '', '', True, 87],
    [False, '', '', '', '', '', '', '', '', True, 88], 
    [False, '', '', '', '', '', '', '', '', True, 89], 
    [False, '', '', '', '', '', '', '', '', True, 90], 
    [False, '', '', '', '', '', '', '', '', True, 91], 
    [False, '', '', '', '', '', '', '', '', True, 92], 
    [False, '', '', '', '', '', '', '', '', True, 93], 
    [False, '', '', '', '', '', '', '', '', True, 94], 
    [False, '', '', '', '', '', '', '', '', True, 95], 
    [False, '', '', '', '', '', '', '', '', True, 96], 
    [False, '', '', '', '', '', '', '', '', True, 97], 
    [False, '', '', '', '', '', '', '', '', True, 98], 
    [False, '', '', '', '', '', '', '', '', True, 99], 
    [False, '', '', '', '', '', '', '', '', True, 100], 
    [False, '', '', '', '', '', '', '', '', True, 101], 
    [False, '', '', '', '', '', '', '', '', True, 102], 
    [False, '', '', '', '', '', '', '', '', True, 103], 
    [False, '', '', '', '', '', '', '', '', True, 104], 
    [False, '', '', '', '', '', '', '', '', True, 105],
    [False, '', '', '', '', '', '', '', '', True, 106],
    [False, '', '', '', '', '', '', '', '', True, 107],
    [False, '', '', '', '', '', '', '', '', True, 108],
    [False, '', '', '', '', '', '', '', '', True, 109],
    [False, '', '', '', '', '', '', '', '', True, 110],
    [False, '', '', '', '', '', '', '', '', True, 111],
    [False, '', '', '', '', '', '', '', '', True, 112], 


    [False, '', '', '', '', '', '', '', '', True, 85],
    [False, '', '', '', '', '', '', '', '', True, 86],
    [False, '', '', '', '', '', '', '', '', True, 87],
    [False, '', '', '', '', '', '', '', '', True, 88], 
    [False, '', '', '', '', '', '', '', '', True, 89], 
    [False, '', '', '', '', '', '', '', '', True, 90], 
    [False, '', '', '', '', '', '', '', '', True, 91], 
    [False, '', '', '', '', '', '', '', '', True, 92], 
    [False, '', '', '', '', '', '', '', '', True, 93], 
    [False, '', '', '', '', '', '', '', '', True, 94], 
    [False, '', '', '', '', '', '', '', '', True, 95], 
    [False, '', '', '', '', '', '', '', '', True, 96], 
    [False, '', '', '', '', '', '', '', '', True, 97], 
    [False, '', '', '', '', '', '', '', '', True, 98], 
    [False, '', '', '', '', '', '', '', '', True, 99], 
    [False, '', '', '', '', '', '', '', '', True, 100], 
    [False, '', '', '', '', '', '', '', '', True, 101], 
    [False, '', '', '', '', '', '', '', '', True, 102], 
    [False, '', '', '', '', '', '', '', '', True, 103], 
    [False, '', '', '', '', '', '', '', '', True, 104], 
    [False, '', '', '', '', '', '', '', '', True, 105],
    [False, '', '', '', '', '', '', '', '', True, 106],
    [False, '', '', '', '', '', '', '', '', True, 107],
    [False, '', '', '', '', '', '', '', '', True, 108],
    [False, '', '', '', '', '', '', '', '', True, 109],
    [False, '', '', '', '', '', '', '', '', True, 110],
    [False, '', '', '', '', '', '', '', '', True, 111],
    [False, '', '', '', '', '', '', '', '', True, 112], 


    [False, '', '', '', '', '', '', '', '', True, 85],
    [False, '', '', '', '', '', '', '', '', True, 86],
    [False, '', '', '', '', '', '', '', '', True, 87],
    [False, '', '', '', '', '', '', '', '', True, 88], 
    [False, '', '', '', '', '', '', '', '', True, 89], 
    [False, '', '', '', '', '', '', '', '', True, 90], 
    [False, '', '', '', '', '', '', '', '', True, 91], 
    [False, '', '', '', '', '', '', '', '', True, 92], 
    [False, '', '', '', '', '', '', '', '', True, 93], 
    [False, '', '', '', '', '', '', '', '', True, 94], 
    [False, '', '', '', '', '', '', '', '', True, 95], 
    [False, '', '', '', '', '', '', '', '', True, 96], 
    [False, '', '', '', '', '', '', '', '', True, 97], 
    [False, '', '', '', '', '', '', '', '', True, 98], 
    [False, '', '', '', '', '', '', '', '', True, 99], 
    [False, '', '', '', '', '', '', '', '', True, 100], 
    [False, '', '', '', '', '', '', '', '', True, 101], 
    [False, '', '', '', '', '', '', '', '', True, 102], 
    [False, '', '', '', '', '', '', '', '', True, 103], 
    [False, '', '', '', '', '', '', '', '', True, 104], 
    [False, '', '', '', '', '', '', '', '', True, 105],
    [False, '', '', '', '', '', '', '', '', True, 106],
    [False, '', '', '', '', '', '', '', '', True, 107],
    [False, '', '', '', '', '', '', '', '', True, 108],
    [False, '', '', '', '', '', '', '', '', True, 109],
    [False, '', '', '', '', '', '', '', '', True, 110],
    [False, '', '', '', '', '', '', '', '', True, 111],
    [False, '', '', '', '', '', '', '', '', True, 112], 


    [False, '', '', '', '', '', '', '', '', True, 85],
    [False, '', '', '', '', '', '', '', '', True, 86],
    [False, '', '', '', '', '', '', '', '', True, 87],
    [False, '', '', '', '', '', '', '', '', True, 88], 
    [False, '', '', '', '', '', '', '', '', True, 89], 
    [False, '', '', '', '', '', '', '', '', True, 90], 
    [False, '', '', '', '', '', '', '', '', True, 91], 
    [False, '', '', '', '', '', '', '', '', True, 92], 
    [False, '', '', '', '', '', '', '', '', True, 93], 
    [False, '', '', '', '', '', '', '', '', True, 94], 
    [False, '', '', '', '', '', '', '', '', True, 95], 
    [False, '', '', '', '', '', '', '', '', True, 96], 
    [False, '', '', '', '', '', '', '', '', True, 97], 
    [False, '', '', '', '', '', '', '', '', True, 98], 
    [False, '', '', '', '', '', '', '', '', True, 99], 
    [False, '', '', '', '', '', '', '', '', True, 100], 
    [False, '', '', '', '', '', '', '', '', True, 101], 
    [False, '', '', '', '', '', '', '', '', True, 102], 
    [False, '', '', '', '', '', '', '', '', True, 103], 
    [False, '', '', '', '', '', '', '', '', True, 104], 
    [False, '', '', '', '', '', '', '', '', True, 105],
    [False, '', '', '', '', '', '', '', '', True, 106],
    [False, '', '', '', '', '', '', '', '', True, 107],
    [False, '', '', '', '', '', '', '', '', True, 108],
    [False, '', '', '', '', '', '', '', '', True, 109],
    [False, '', '', '', '', '', '', '', '', True, 110],
    [False, '', '', '', '', '', '', '', '', True, 111],
    [False, '', '', '', '', '', '', '', '', True, 112], 
    
    [False, '', '', '', '', '', '', '', '', True, 85],
    [False, '', '', '', '', '', '', '', '', True, 86],
    [False, '', '', '', '', '', '', '', '', True, 87],
    [False, '', '', '', '', '', '', '', '', True, 88], 
    [False, '', '', '', '', '', '', '', '', True, 89], 
    [False, '', '', '', '', '', '', '', '', True, 90], 
    [False, '', '', '', '', '', '', '', '', True, 91], 
    [False, '', '', '', '', '', '', '', '', True, 92], 
    [False, '', '', '', '', '', '', '', '', True, 93], 
    [False, '', '', '', '', '', '', '', '', True, 94], 
    [False, '', '', '', '', '', '', '', '', True, 95], 
    [False, '', '', '', '', '', '', '', '', True, 96], 
    [False, '', '', '', '', '', '', '', '', True, 97], 
    [False, '', '', '', '', '', '', '', '', True, 98], 
    [False, '', '', '', '', '', '', '', '', True, 99], 
    [False, '', '', '', '', '', '', '', '', True, 100], 
    [False, '', '', '', '', '', '', '', '', True, 101], 
    [False, '', '', '', '', '', '', '', '', True, 102], 
    [False, '', '', '', '', '', '', '', '', True, 103], 
    [False, '', '', '', '', '', '', '', '', True, 104], 
    [False, '', '', '', '', '', '', '', '', True, 105],
    [False, '', '', '', '', '', '', '', '', True, 106],
    [False, '', '', '', '', '', '', '', '', True, 107],
    [False, '', '', '', '', '', '', '', '', True, 108],
    [False, '', '', '', '', '', '', '', '', True, 109],
    [False, '', '', '', '', '', '', '', '', True, 110],
    [False, '', '', '', '', '', '', '', '', True, 111],
    [False, '', '', '', '', '', '', '', '', True, 112], 
    
    
    [False, '', '', '', '', '', '', '', '', True, 85],
    [False, '', '', '', '', '', '', '', '', True, 86],
    [False, '', '', '', '', '', '', '', '', True, 87],
    [False, '', '', '', '', '', '', '', '', True, 88], 
    [False, '', '', '', '', '', '', '', '', True, 89], 
    [False, '', '', '', '', '', '', '', '', True, 90], 
    [False, '', '', '', '', '', '', '', '', True, 91], 
    [False, '', '', '', '', '', '', '', '', True, 92], 
    [False, '', '', '', '', '', '', '', '', True, 93], 
    [False, '', '', '', '', '', '', '', '', True, 94], 
    [False, '', '', '', '', '', '', '', '', True, 95], 
    [False, '', '', '', '', '', '', '', '', True, 96], 
    [False, '', '', '', '', '', '', '', '', True, 97], 
    [False, '', '', '', '', '', '', '', '', True, 98], 
    [False, '', '', '', '', '', '', '', '', True, 99], 
    [False, '', '', '', '', '', '', '', '', True, 100], 
    [False, '', '', '', '', '', '', '', '', True, 101], 
    [False, '', '', '', '', '', '', '', '', True, 102], 
    [False, '', '', '', '', '', '', '', '', True, 103], 
    [False, '', '', '', '', '', '', '', '', True, 104], 
    [False, '', '', '', '', '', '', '', '', True, 105],
    [False, '', '', '', '', '', '', '', '', True, 106],
    [False, '', '', '', '', '', '', '', '', True, 107],
    [False, '', '', '', '', '', '', '', '', True, 108],
    [False, '', '', '', '', '', '', '', '', True, 109],
    [False, '', '', '', '', '', '', '', '', True, 110],
    [False, '', '', '', '', '', '', '', '', True, 111],
    [False, '', '', '', '', '', '', '', '', True, 112], 
]


'''
[1-28]
[29-56]
[59-84]
[85-112]
[113-140]
[141-168]
[169-196]
[197-224]
'''


def map(x, in_min, in_max, out_min, out_max):
    return (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min

def dec2str(number, places):
    return '{:.2f}'.format(number)

def CenterWidgets(widget:QWidget):
    screenGeometry =  QApplication.desktop().screenGeometry()
    x = (screenGeometry.width() - widget.width())/ 2
    y = (screenGeometry.height()- widget.height())/ 2
    widget.move(x, y)

