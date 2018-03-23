#!usr/bin/env python3
import sys
sys.path.append('/usr/local/lib/python3.5/dist-packages')
import serial


HEAD = b'\xAA\xAA'
END = b'\xEF'
RF433_CMD = 0x01

class ZQGateway:
	def __init__(self,port,baude):
		self.ser=serial.Serial(port,baude)	
	
	def write_rf433(self,data,timers=4):
		cmd = (timers<<4)|RF433_CMD	#INT
		CMD = cmd.to_bytes(length=1,byteorder='big')	#int to bytes	
		l = len(data)
		LEN = l.to_bytes(length=2,byteorder='big')
		SUM = b'\x00'
		if type(data)==str:
			DATA = bytes(data,encoding='utf-8')
		else:
			DATA = data
		rf433_data = HEAD+CMD+LEN+DATA+SUM+END
		print(rf433_data)
		self.ser.write(rf433_data) 

	def transmit_syn(self):
		self.ser.write(b'\xAA\xAA\xAA')



