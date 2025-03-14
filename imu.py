import time

class IMU:
    '''An IMU driver in a Python class'''

    def __init__(self, i2c):
        '''An initializer that takes in a pyb.I2C object preconfigured in CONTROLLER mode'''
        self.i2c = i2c
        self.address      = 0x28  # Address of the IMU
        self.OPR_MODE_REG = 0x3D  # Register for setting operation mode
        #self.CONFIG_MODE  = 0x00  # Configuration mode value
        #self.NDOF_MODE    = 0x0C  # NDOF mode value
        
    def set_mode(self, mode):
        """Sets the operation mode of the BNO055."""
        # Set to CONFIG_MODE before changing mode
        #self.i2c.mem_write(self.CONFIG_MODE, self.address, self.OPR_MODE_REG)

        # Set to desired mode
        #print(f"mode: {mode}")
        time.sleep(0.007)
        self.i2c.mem_write(mode, self.address, self.OPR_MODE_REG)
        time.sleep(0.007)

    def get_calibration_status(self):
        """Retrieves and parses the calibration status byte from the IMU."""
        calib_status = self.i2c.mem_read(1, self.address, 0x35)[0]
    
        return {
            "system": (calib_status >> 6) & 0x03,      # System calibration (bits 7-6)
            "gyroscope": (calib_status >> 4) & 0x03,  # Gyroscope calibration (bits 5-4)
            "accelerometer": (calib_status >> 2) & 0x03,  # Accelerometer calibration (bits 3-2)
            "magnetometer": calib_status & 0x03       # Magnetometer calibration (bits 1-0)
        }
    
    def get_calibration_coefficients(self):
        """Retrieves calibration coefficients from the IMU and saves them to calibration.txt."""
        coeffs = self.i2c.mem_read(22, self.address, 0x55)  # Read 22 bytes from register 0x55
    
        with open("calibration.txt", "wb") as file:  # Save as binary file
            file.write(coeffs)
    
        print("Calibration coefficients saved to calibration.txt.")
        return coeffs
    
    def set_calibration_coefficients(self):
        """Loads calibration coefficients from calibration.txt and writes them to the IMU."""
        try:
            with open("calibration.txt", "rb") as file:  # Read binary calibration data
                data = file.read()
    
            if len(data) != 22:
                raise ValueError("Calibration data must be exactly 22 bytes.")
    
            self.i2c.mem_write(data, self.address, 0x55)  # Write back to IMU
            print("Calibration coefficients loaded into IMU.")
    
        except FileNotFoundError:
            print("Error: calibration.txt not found. Perform calibration first.")

    def get_heading(self):
        """Reads only the heading (yaw) angle from the IMU."""
        data = self.i2c.mem_read(2, self.address, 0x1A)  # Read first 2 bytes (heading)
        heading = (data[1] << 8 | data[0]) / 16.0
        return heading
    
    def get_yaw_rate(self):
        """Reads only the yaw rate (heading rate) from the IMU."""
        data = self.i2c.mem_read(2, self.address, 0x14)  # Read first 2 bytes (yaw rate)
        yaw_rate = (data[1] << 8 | data[0]) / 16.0
        return yaw_rate
