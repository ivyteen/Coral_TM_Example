import RPi.GPIO as rpigpio
import time

class LED:
        
	RED = 0
	GREEN = 1
	BLUE = 2
	YELLOW = 3
	PUPPLE = 4
	LIGHT_BLUE = 5
	WHITE = 6

	def __init__(self):
		'''
		GPIO16(pin #36) : RED 
		GPIO20(pin #38) : GREEN
		GPIO21(pin #40) : BLUE
		'''
		self.pins = [16,20,21]
		rpigpio.setmode(rpigpio.BCM)
		for pin in self.pins:
			rpigpio.setwarnings(False)
			rpigpio.setup(pin, rpigpio.OUT)

	def setLedOn(self,color):
		for i in range(len(self.pins)): rpigpio.output(self.pins[i], rpigpio.LOW)

		if color == self.RED:    
			rpigpio.output(self.pins[self.RED], rpigpio.HIGH) 
		elif color == self.GREEN:    
			rpigpio.output(self.pins[self.GREEN], rpigpio.HIGH) 
		elif color == self.BLUE:    
			rpigpio.output(self.pins[self.BLUE], rpigpio.HIGH) 
		elif color == self.YELLOW:    
			rpigpio.output(self.pins[self.RED], rpigpio.HIGH) 
			rpigpio.output(self.pins[self.GREEN], rpigpio.HIGH) 
		elif color == self.PUPPLE:    
			rpigpio.output(self.pins[self.RED], rpigpio.HIGH) 
			rpigpio.output(self.pins[self.BLUE], rpigpio.HIGH) 
		elif color == self.LIGHT_BLUE:    
			rpigpio.output(self.pins[self.GREEN], rpigpio.HIGH) 
			rpigpio.output(self.pins[self.BLUE], rpigpio.HIGH) 
		elif color == self.WHITE:    
			rpigpio.output(self.pins[self.RED], rpigpio.HIGH) 
			rpigpio.output(self.pins[self.GREEN], rpigpio.HIGH) 
			rpigpio.output(self.pins[self.BLUE], rpigpio.HIGH) 


	def setLedOff(self):
		for i in range(len(self.pins)): rpigpio.output(self.pins[i], rpigpio.LOW)

	def startLEDs(self, reps=1):
		for i in range(reps):
			for i in range(3):
				self.setLedOn(i)
				time.sleep(0.5)
		self.setLedOff()

'''
	def setLED(self, index, state):
		return rpigpio.output(self.pins[index], rpigpio.HIGH if state else rpigpio.LOW)

	def setOnlyLED(self, index):
		for i in range(len(self.pins)): self.setLED(i, False)
		if index is not None: self.setLED(index, True)

	def wiggleLEDs(self, reps=2):
		for i in range(reps):
			for i in range(3):
				self.setLED(i, True)
				time.sleep(0.5)
				self.setLED(i, False)				
'''	
	
