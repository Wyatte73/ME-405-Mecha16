from pyb import Pin, Timer

class Motor:
    '''A motor driver interface encapsulated in a Python class. Works with
       motor drivers using separate PWM and direction inputs such as the 
       DRV8838 drivers present on the Romi chassis from Pololu.'''
       
    def __init__(self, PWM, DIR, nSLP, TIM, CHAN):
        '''Initializes a Motor object. Enables the motors and sets values that
           allow the motors to start turning when give a PWM'''
        self.PWM_pin = TIM.channel(CHAN, pin=PWM, mode=Timer.PWM, pulse_width_percent=0)
        self.DIR_pin = Pin(DIR, mode=Pin.OUT_PP, value=0)
        self.nSLP_pin = Pin(nSLP, mode=Pin.OUT_PP, value=0)
    
    def set_effort(self, effort):
        '''Sets the present effort requested from the motor based on an
           input value between -100 and 100'''   
          
        if effort <= 0: # Determines the direction
            self.DIR_pin.high()
        else:           # Determines the direction
            self.DIR_pin.low()
        self.PWM_pin.pulse_width_percent(abs(effort)) # Sets the PWM  
    
    def enable(self):
        '''Enables the motor driver by taking it out of sleep mode into brake
           mode'''
        self.nSLP_pin.high()
        self.PWM_pin.pulse_width_percent(0)
    
    def disable(self):
        '''Disables the motor driver by taking it into sleep mode'''
        self.nSLP_pin.low()
