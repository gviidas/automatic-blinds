import utime
'''
Connecting ESP32 to L298
IN1 -->  32
IN2 -->  33
IN3 -->  25
IN4 -->  26

4wires from 28BYJ Blue, Pink, Orange, Yellow
Blue and Yellow in circuit, Pink and Orange in circuit

L298 outs:
OUT1 Pink
OUT2 Orange
OUT3 Yellow
OUT4 Blue
'''
#s1.angle(180) rotate 180 degrees or -180
#s1.step(100,-1) rotate 100 steps
#full rotation 509steps
#mode='HALF_STEP' or 'FULL_STEP'
#delay = speed
#TEST_STEP min delay 1000
#HALF_STEP min delay 1000
#FULL_STEP min delay 1900-2000 5V arduino 15RPM // 1300 9V AA 22RPM
#s1.delay = x to change in action

class Stepper:
    
    FULL_ROTATION = int(4075.7728395061727 / 8) # http://www.jangeox.be/2013/10/stepper-motor-28byj-48_25.html
    TEST_STEP = [
        [1, 0, 1, 0],
        [0, 1, 1, 0],
        [0, 1, 0, 1],
        [1, 0, 0, 1],
    
    ]
    HALF_STEP = [
        [0, 1, 0, 1],
        [0, 0, 0, 1],
        [1, 0, 0, 1],
        [1, 0, 0, 0],
        [1, 0, 1, 0],
        [0, 0, 1, 0],
        [0, 1, 1, 0],
        [0, 1, 0, 0],
    ]

    FULL_STEP = [
        [1, 0, 1, 0],
        [0, 1, 1, 0],
        [0, 1, 0, 1],
        [1, 0, 0, 1]
    ]
    def __init__(self, mode, pin1, pin2, pin3, pin4, delay):
    	if mode=='FULL_STEP':
        	self.mode = self.FULL_STEP
        elif mode=='HALF_STEP':
        	self.mode = self.HALF_STEP
        else:
        	self.mode = self.TEST_STEP
        self.pin1 = pin1
        self.pin2 = pin2
        self.pin3 = pin3
        self.pin4 = pin4
        self.delay = delay
        
        # Initialize all to 0
        self.reset()
        
    def step(self, count, direction=1):
        """Rotate count steps. direction = -1 means backwards"""
        if count<0:
            direction = -1
            count = -count
        for x in range(count):
            for bit in self.mode[::direction]:
                self.pin1(bit[0])
                self.pin2(bit[1])
                self.pin3(bit[2])
                self.pin4(bit[3])
                utime.sleep_us(self.delay)
        self.reset()
    def angle(self, r, direction=1):
    	self.step(int(self.FULL_ROTATION * r / 360), direction)
    def reset(self):
        # Reset to 0, no holding, these are geared, you can't move them
        self.pin1(0) 
        self.pin2(0) 
        self.pin3(0) 
        self.pin4(0)

def create(pin1, pin2, pin3, pin4, delay=2000, mode='HALF_STEP'):
	return Stepper(mode, pin1, pin2, pin3, pin4, delay)