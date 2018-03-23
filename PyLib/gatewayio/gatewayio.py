#!usr/bin/env python3
import asyncio
from threading import Thread
import types
import sys
sys.path.append('/usr/local/lib/python3.5/dist-packages')
import serial


HEAD = b'\xAA\xAA'
END = b'\xEF'
RF433_CMD = 0x01

class open_serial(Thread):
	def __init__(self,port,baude):
		Thread.__init__(self)
		self.port = port
		self.baude = baude
		self.result = None

	def run(self):
		try:
			self.result = serial.Serial(self.port,self.baude)	
		except e:
			print(e.message)
	def get_result(self):
		return self.result

@types.coroutine
def async_Serial(port,baude):
	thd = open_serial(port,baude)
	thd.start()
	while(True):
		yield from asyncio.sleep(0.1)
		if not thd.is_alive():
			return thd.get_result()

class write_serial(Thread):
	def __init__(self,ser,data):
		Thread.__init__(self)
		self.data = data
		self.ser = ser
		self.result = None

	def run(self):
		self.result = self.ser.write(self.data.encode())

	def get_result(self):
		return self.result

@types.coroutine
def async_write(ser,data):
	thd = write_serial(ser,data)
	thd.start()
	while(True):
		yield from asyncio.sleep(0.1)
		if not thd.is_alive():
			return thd.get_result()

class async_ZQGateway:
	def __init__(self):
		self.ser = None

	@asyncio.coroutine
	def init(self,port,baude):
		self.ser = yield from async_Serial(port,baude)	
	
	@asyncio.coroutine
	def async_write_rf433(self,data,timers=4):
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
		return (yield from async_write(self.ser,data))

	@asyncio.coroutine
	def async_transmit_syn(self):
		return (yield from async_write(self.ser,b'\xAA\xAA\xAA'))

if __name__ == '__main__':
	print('test')
	loop = asyncio.get_event_loop()
	zq1112wg = async_ZQGateway()
	@asyncio.coroutine
	def send():
		yield from zq1112wg.init('/dev/ttyS0',115200)
		while(True):
			yield from asyncio.sleep(3)
			yield from zq1112wg.async_write_rf433(b'\x12\x34\x56',4)
	
	loop = loop.run_until_complete(asyncio.wait([send()]))


