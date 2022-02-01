from machine import Pin
import utime

'''
DRV8825 circuit             8,2V-45V MOTOR SUPPLY--)|--|with 100uF
D23---------ENABLE PIN |O (X)    O| VMOT--------------------|    |
                    M0 |O        O| GND--------------------------|
                    M1 |O        O| B2-----(blue wire with 28byj-48)
                    M2 |O        O| B1-----(yellow wire with 28byj-48)
3,3V-|-----------RESET |O IIIIII O| A1-----(orange wire with 28byj-48) 
     |-----------SLEEP |O IIIIII O| A2-----(pink wire with 28byj-48)         
D22---------------STEP |O IIIIII O| FAULT(empty
D21----------------DIR |O        O| GND-----3,3V

'''

class StepperMotor:

    def __init__(self, dir_pin, step_pin, enable_pin, stepperMIN, stepperMAX, stepperPos, delay):
        """
        :param dir_pin: input direction PIN
        :param step_pin: input steps PIN
        :param enable_pin: input enable PIN
        :param delay: input time to delay between steps 400 (us) - fastest, more - slower
        """
        self.stepper_dir = Pin(dir_pin, Pin.OUT)
        self.stepper_step = Pin(step_pin, Pin.OUT)
        self.stepper_enable = Pin(enable_pin, Pin.OUT)
        self.stepperPos = stepperPos
        self.stepperMIN = stepperMIN
        self.stepperMAX = stepperMAX
        self.delay = delay
        self.stepper_enable.value(1)

    def steps(self, steps):
        """
        :param steps: 509full rotation
        """
        if steps >= 0:

            self.stepper_enable.value(0)  # enable motor
            self.stepper_dir.value(1)  # setting motor rotation 1 - clockwise, 0 - CCW
            for step in range(steps): #giving some steps, by enable and disable PIN
                self.stepper_step.value(1) 
                utime.sleep_us(self.delay)
                self.stepper_step.value(0)
                utime.sleep_us(self.delay)
            self.stepper_enable.value(1)  # disable motor (not holding)

        elif steps < 0:

            self.stepper_enable.value(0)  # enable motor
            self.stepper_dir.value(0)  # setting motor rotation 1 - clockwise, 0 - CCW
            for step in range(abs(steps)): #giving some steps, by enable and disable PIN
                self.stepper_step.value(1)
                utime.sleep_us(self.delay)
                self.stepper_step.value(0)
                utime.sleep_us(self.delay)
            self.stepper_enable.value(1)  # disable motor (not holding)

    def blinds_open(self):  # function to fully open blinds
        print('Blinds opening')
        self.steps(self.stepperMAX - self.stepperPos)
        self.stepperPos = self.stepperMAX  # updating blinds position in steps
        return self.stepperPos
        print('Blinds opened')

    def blinds_close(self):  # function to fully close blinds
        print('Blinds closing')
        self.steps(self.stepperMIN - self.stepperPos)
        self.stepperPos = self.stepperMIN  # updating blinds position in steps
        return self.stepperPos
        print('Blinds closed')

    def blinds_control(self, inputValue):  # function to control blinds position
        print("blinds control working")
        if inputValue > self.stepperPos:
            self.steps(inputValue - self.stepperPos)
            self.stepperPos = inputValue  # updating blinds position in steps
            return self.stepperPos

        elif inputValue < self.stepperPos:
            self.steps(inputValue - self.stepperPos)
            self.stepperPos = inputValue  # updating blinds position in steps
            return self.stepperPos
        elif inputValue == self.stepperPos:
            self.stepperPos = inputValue  # updating blinds position in steps
            return self.stepperPos

