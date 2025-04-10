from machine import I2C, Pin
from bno055 import BNO055 as BNO055Driver

class Sensor:
    """
    Abstract synchronous base class for all sensors.
    """
    def get_value(self):
        raise NotImplementedError

    def is_calibrated(self):
        raise NotImplementedError

    def get_calibration_status(self):
        raise NotImplementedError


class BNO055(Sensor):
    """
    Synchronous interface to BNO055 IMU sensor.
    """
    def __init__(self, i2c_bus=1, sda_pin=2, scl_pin=3, freq=400_000):
        self.i2c = I2C(i2c_bus, sda=Pin(sda_pin), scl=Pin(scl_pin), freq=freq)
        self.imu = BNO055Driver(self.i2c)

    def get_value(self):
        """
        Returns quaternion [w, x, y, z].
        
        """
        return list(map(float, self.imu.quaternion()))

    def get_quaternion(self):
        """
            This is the important one -- returns quaternion angles easily interpreted by the Adafruit frontend
            (https://github.com/adafruit/Adafruit_WebSerial_3DModelViewer)
            
        """
        return list(map(float, self.imu.quaternion()))

    def get_euler(self):
        """
            Also could be useful as the Adafruit frontend can read it, but the math is much worse and less reliable
            to translate into 3d-modelled motion (see "gimbal lock")
        """
        return list(map(float, self.imu.euler()))

    def get_temperature(self):
        return int(self.imu.temperature())

    def get_gyro(self):
        return list(map(float, self.imu.gyro()))

    def get_accel(self):
        return list(map(float, self.imu.accel()))

    def get_linear_accel(self):
        return list(map(float, self.imu.lin_acc()))

    def get_gravity(self):
        return list(map(float, self.imu.gravity()))

    def get_magnetometer(self):
        return list(map(float, self.imu.mag()))

    def is_calibrated(self):
        return self.imu.calibrated()

    def get_calibration_status(self):
        return list(self.imu.cal_status())


class Dummy(Sensor):
    """
    Simplified dummy sensor for testing. Returns a generic value and calibration status that u can set.
    Might be useful for the second hub/"sensor" pair.
    I feel like the second sensor could rly just be an RP2/PN532/NRF without any other sensor, using this class
    """
    def __init__(self, value=None, calibrated=True, cal_status=[3, 3, 3, 3]):
        self._value = value or [1.0, 0.0, 0.0, 0.0]
        self._calibrated = calibrated
        self._cal_status = cal_status

    def get_value(self):
        return self._value

    def is_calibrated(self):
        return self._calibrated

    def get_calibration_status(self):
        return self._cal_status
