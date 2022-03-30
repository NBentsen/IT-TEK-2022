import time
import sys
import curses

import smbus

class KAmodRPiADCDAC:

	bus = smbus.SMBus(1) # Definere vores bus forbindelse som SMBus 
	adAddress = 0x49 #Det er vores fysiske adresse på ADC chippen på Pi hat (slaven)

	def readMCP3021(self):
		rd = self.bus.read_word_data(self.adAddress, 0)
		return ((rd & 0xFF) << 8) | ((rd & 0xFF00) >> 8)
