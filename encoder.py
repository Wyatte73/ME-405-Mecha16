from time import ticks_us, ticks_diff
from pyb import Timer

class Encoder:
    '''A quadrature encoder decoding interface encapsulated in a Python class'''
    
    def __init__(self, chA, chA_pin, chB, chB_pin, tim):
        '''Initalizes an Encoder object'''
        
        self.ENC = Timer(tim, period = 0xFFFF, prescaler = 0)
        self.ENC.channel(chA, pin=chA_pin, mode=Timer.ENC_AB)
        self.ENC.channel(chB, pin=chB_pin, mode=Timer.ENC_AB)
        
        self.past        = 0
        self.present     = 0
        self.dt          = 0
        self.prev_count  = 0
        self.count       = 0
        self.delta       = 0
        self.AR_1        = 65536
        self.position    = 0
        self.time        = 0
        self.state       = 0
    
    def update(self):
        '''Runs one update step on the encoder's timer counter to keep track of
           the change in count and check for counter relodad'''
           
        # Starts the time and ensure a divide by zero isn't occuring
        if self.state == 0: 
            self.dt = 1
            self.time = 0
            self.past = ticks_us()
            self.state = 1
        # Starts incrementing time everytime update is called    
        elif self.state == 1: 
            self.present = ticks_us()
            self.dt = ticks_diff(self.present, self.past) # [micro-seconds]
            self.past = self.present
            self.time = self.time + self.dt
        # Calculates the delta based on the encoder counts
        self.count = self.ENC.counter() 
        self.delta = self.count - self.prev_count
        self.prev_count = self.count
        # Handles any overflow to ensure the encoder count is the correct value and isn't getting reset
        if self.delta > self.AR_1/2:
            self.delta = self.delta - self.AR_1
        elif self.delta < -self.AR_1/2:
            self.delta = self.delta + self.AR_1
        # Calculates the position based on the previous encoder count and the change in encoder count  
        self.position = self.position + self.delta # [ENC counts]  
    
    def get_position(self):
        '''Returns the most recently updated value of position as determined
           within the update () method'''
        return self.position
    
    def get_velocity(self):
        '''Returns a measure of velocity using the most recently updated value
           of delta as determined within the update () method'''    
        #return velocity as encoder counts per second
        return int((self.delta / self.dt) * 1_000_000)
    
    def get_time(self):
        '''Returns the time stamp of the most recent updated value of time as
           determined within the update () method'''
        return self.time
    
    def zero(self):
        '''Sets the present encoder postiion to zero and causes future updates
           to measure with respect to the new zero position'''
        self.position     = 0 
        self.prev_count = self.ENC.counter()
        self.state = 0
