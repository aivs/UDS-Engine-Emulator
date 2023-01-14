# -*- coding: utf-8 -*-


import binascii
import can
bus = can.interface.Bus(channel='can0', bustype='socketcan')
uds_data = {
	"03 55": 	["06 50 03 00 32 01 F4 55"],	# DiagnosticSessionControl
	"F1 9E": 	["10 1B 62 F1 9E 45 56 5F",	# ODXFileDataIdentifier
				"21 45 43 4D 32 30 54 46", 
				"22 53 30 31 31 38 4B 35", 
				"23 39 30 37 31 31 35 00"], 
	"F1 A2": 	["10 09 62 F1 A2 30 30 31", 
				"21 30 31 30 55 55 55 55"],
	"02 00": 	["10 14 49 02 01 57 41 55 ",
				"21 5A 5A 5A 38 4B 32 44",
				"22 41 31 37 30 32 39 37"],
	"F1 87": 	["10 0E 62 F1 87 38 4B 35",	# vehicleManufacturerSparePartNumberDataIdentifier
				"21 39 30 37 31 31 35 20", 
				"22 20 55 55 55 55 55 55"],
	"F1 89": 	["07 62 F1 89 30 30 30 38"],	# vehicleManufacturerECUSoftwareVersionNumberDataIdentifier
	"F1 91": 	["10 0E 62 F1 91 38 4B 32",	# vehicleManufacturerECUHardwareNumberDataIdentifier
				"21 39 30 37 31 31 35 4C",
				"22 20 55 55 55 55 55 55"],
	"F1 A3": 	["06 62 F1 A3 48 30 39 55"],
	"F1 A5": 	["10 09 62 F1 A5 80 00 00 ",
				"21 04 71 30 55 55 55 55"],
	"F1 DF": 	["04 62 F1 DF 40 55 55 55"],
	"F1 97": 	["10 10 62 F1 97 32 2E 30",	# systemNameOrEngineTypeDataIdentifier
				"21 6C 20 52 34 2F 34 56",
				"22 20 54 46 55 55 55 55"],
	"06 01": 	["04 62 06 01 0A 55 55 55"],
	"06 00": 	["10 0D 62 06 00 32 19 00",
				"21 13 24 26 01 02 20 00",
				"",
				""],
	"negative": ["03 7F 22 31 55 55 55 55"]
}

pid = ""

def send(message):
	bus.send(can.Message(arbitration_id=0x7E8,data=bytes.fromhex(message),is_extended_id=False))

class CanListener(can.Listener):
	def on_message_received(self, message):
		global pid
		print(hex(message.arbitration_id), binascii.hexlify(message.data, " "))
		if message.arbitration_id == 0x7E0:
			if (message.data[0] != 0x30 and message.data[0] != 0xA8):
				pid = "%0.2X" % message.data[2] + " " + "%0.2X" % message.data[3]
	#1
			if(message.data == bytearray(b'\x02\x10\x03UUUUU')):
				send(uds_data[pid][0])
	#2
			elif (message.data == bytearray(b'\x03\x22\xF1\x9EUUUU')):
				send(uds_data[pid][0])
			elif (message.data == bytearray(b'\x30\x00\x01UUUUU') and pid == "F1 9E"):
				send(uds_data[pid][1])
				if uds_data[pid][2]: send(uds_data[pid][2])
				if uds_data[pid][3]: send(uds_data[pid][3])
	#3
			elif (message.data == bytearray(b'\x03\x22\xF1\xA2UUUU')):
				send(uds_data[pid][0])
			elif (message.data == bytearray(b'\x30\x00\x01UUUUU') and pid == "F1 A2"):
				send(uds_data[pid][1])
	#4
			elif (message.data == bytearray(b'\x02\x09\x02\x00\x00\x00\x00\x00')):
				send(uds_data[pid][0])
			elif (message.data == bytearray(b'\x30\x00\x00\x00\x00\x00\x00\x00') and pid == "02 00"):
				send(uds_data[pid][1])
				if uds_data[pid][2]: send(uds_data[pid][2])
	#5
			elif (message.data == bytearray(b'\x03\x22\xF1\x87UUUU')):
				send(uds_data[pid][0])
			elif (message.data == bytearray(b'\x30\x00\x01UUUUU') and pid == "F1 87"):
				send(uds_data[pid][1])
				if uds_data[pid][2]: send(uds_data[pid][2])
	#6
			elif (message.data == bytearray(b'\x03\x22\xF1\x89UUUU')):
				send(uds_data[pid][0])
	#7
			elif (message.data == bytearray(b'\x03\x22\xF1\x91UUUU')):
				send(uds_data[pid][0])
			elif (message.data == bytearray(b'\x30\x00\x01UUUUU') and pid == "F1 91"):
				send(uds_data[pid][1])
				if uds_data[pid][2]: send(uds_data[pid][2])
	#8
			elif (message.data == bytearray(b'\x03\x22\xF1\xA3UUUU')):
				send(uds_data[pid][0])
	#9
			elif (message.data == bytearray(b'\x03\x22\xF1\xA5UUUU')):
				send(uds_data[pid][0])
			elif (message.data == bytearray(b'\x30\x00\x01UUUUU') and pid == "F1 A5"):
				send(uds_data[pid][1])
	#10
			elif (message.data == bytearray(b'\x03\x22\xF1\xDFUUUU')):
				send(uds_data[pid][0])
	#11
			elif (message.data == bytearray(b'\x03\x22\xF1\x97UUUU')):
				send(uds_data[pid][0])
			elif (message.data == bytearray(b'\x30\x00\x01UUUUU') and pid == "F1 97"):
				send(uds_data[pid][1])
				if uds_data[pid][2]: send(uds_data[pid][2])
	#12
			elif (message.data == bytearray(b'\x03\x22\x06\x01UUUU')):
				send(uds_data[pid][0])
	#13
			elif (message.data == bytearray(b'\x03\x22\x06\x00UUUU')):
				send(uds_data[pid][0])
			elif (message.data == bytearray(b'\x30\x00\x01UUUUU') and pid == "06 00"):
				send(uds_data[pid][1])
				if uds_data[pid][2]: send(uds_data[pid][2])
				if uds_data[pid][3]: send(uds_data[pid][3])
	##
			else:
				send(uds_data["negative"][0])

if __name__ == "__main__":
	listener = CanListener()
	can.Notifier(bus, [listener])
	while True:
		pass