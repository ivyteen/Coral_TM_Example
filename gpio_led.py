import RPi.GPIO as rpigpio
import time

class LED:
	def __init__(self):
		self.pins = [20,13,12,25,22]
		rpigpio.setmode(rpigpio.BCM)
		for pin in self.pins:
			rpigpio.setwarnings(False)
			rpigpio.setup(pin, rpigpio.OUT)

	def setLED(self, index, state):
		return rpigpio.output(self.pins[index], rpigpio.LOW if state else rpigpio.HIGH)

	def setOnlyLED(self, index):
		for i in range(len(self.pins)): self.setLED(i, False)
		if index is not None: self.setLED(index, True)

	def wiggleLEDs(self, reps=3):
		for i in range(reps):
			for i in range(5):
				self.setLED(i, True)
				time.sleep(0.05)
				self.setLED(i, False)
				
	
	
