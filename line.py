from pyb import Pin, ADC

class Line:
    '''A line sensor driver in a Python class'''
    
    def __init__(self, ir_3, ir_4, ir_5, ir_6, ir_7, ir_9, ir_10, ir_11, ir_12, ir_13):
        '''Initalizes a line sensor pin object'''
        
        # Creats class objects
        self.Line_sen_pin_3 = Pin(ir_3, mode=Pin.OUT_PP)
        self.Line_sen_pin_4 = Pin(ir_4, mode=Pin.OUT_PP)
        self.Line_sen_pin_5 = Pin(ir_5, mode=Pin.OUT_PP)
        self.Line_sen_pin_6 = Pin(ir_6, mode=Pin.OUT_PP)
        self.Line_sen_pin_7 = Pin(ir_7, mode=Pin.OUT_PP)
        #self.Line_sen_pin_8 = Pin(ir_8, mode=Pin.OUT_PP)
        self.Line_sen_pin_9 = Pin(ir_9, mode=Pin.OUT_PP)
        self.Line_sen_pin_10 = Pin(ir_10, mode=Pin.OUT_PP)
        self.Line_sen_pin_11 = Pin(ir_11, mode=Pin.OUT_PP)
        self.Line_sen_pin_12 = Pin(ir_12, mode=Pin.OUT_PP)
        self.Line_sen_pin_13 = Pin(ir_13, mode=Pin.OUT_PP)
        
        #Turns all line sensors into ADC outputs
        self.adc1 = ADC(self.Line_sen_pin_3)
        self.adc2 = ADC(self.Line_sen_pin_4)
        self.adc3 = ADC(self.Line_sen_pin_5)
        self.adc4 = ADC(self.Line_sen_pin_6)
        self.adc5 = ADC(self.Line_sen_pin_7)
       # self.adc6 = ADC(self.Line_sen_pin_8)
        self.adc7 = ADC(self.Line_sen_pin_9)
        self.adc8 = ADC(self.Line_sen_pin_10)
        self.adc9 = ADC(self.Line_sen_pin_11)
        self.adc10 = ADC(self.Line_sen_pin_12)
        self.adc11 = ADC(self.Line_sen_pin_13)
        
        # Initalizes space for line sensor readings and calibration data
        self.readings_list = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        self.white_cal_list = []
        self.black_cal_list = []
        
        self.black_calibrate = 0
        self.white_calibrate = 0
    
    
    def line_reading(self):
        '''Prints the ADC reading that the line sensors sees'''
        self.readings_list[0] = self.adc1.read()
        self.readings_list[1] = self.adc2.read()
        self.readings_list[2] = self.adc3.read()
        self.readings_list[3] = self.adc4.read()
        self.readings_list[4] = self.adc5.read()
       # self.readings_list[5] = self.adc6.read()
        self.readings_list[5] = self.adc7.read()
        self.readings_list[6] = self.adc8.read()
        self.readings_list[7] = self.adc9.read()
        self.readings_list[8] = self.adc10.read()
        self.readings_list[9] = self.adc11.read()
        
    def calibration(self):
        '''Calibrates the line sensor based on the white paper being used'''
        # Assumes that line_reading is ran immediatly before
        # Calibrationes the sensors on the "white" paper
        input('Press Enter to white calibrate')
        self.line_reading()        
        for value in self.readings_list:
            self.white_cal_list.append(value)
        print(self.white_cal_list)
        
        # Calibrates the sensors on the "black" paper
        input('Press Enter to black calibrate')
        self.line_reading()      
        for value in self.readings_list:
            self.black_cal_list.append(value)
        print(self.black_cal_list)
        
    def center(self):
        '''A method to determine the where which sensor is reading the center
           of the line that is being followed'''
                   
        AOC = 0
        median = 0
        center_sensor = 0
        white_readings = 0
        
        for idx, value in enumerate(self.readings_list):
            if value - self.white_cal_list[idx] > 30:
                self.readings_list[idx] = (value - self.white_cal_list[idx]) / (self.black_cal_list[idx] - self.white_cal_list[idx])
                AOC += self.readings_list[idx]
            else:
                self.readings_list[idx] = 0
                white_readings += 1
                
        # if a fork in the road is detected, drive straight          
        if self.readings_list[2] > 0.5 and self.readings_list[7] > 0.5:
            center_sensor = 8
        else:
            median = AOC/2
            for idx, value in enumerate(self.readings_list):
                median -= value
                if median < 0:
                    center_sensor = idx + 3
                    break
        return center_sensor, white_readings
