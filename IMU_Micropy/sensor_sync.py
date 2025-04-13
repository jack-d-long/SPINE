from machine import I2C, Pin
from bno055 import BNO055 as BNO055Driver
from mpu6050 import MPU6050 as MPU6050Driver  # hardware-I2C version you just refactored

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
    def __init__(self, i2c_bus=1, sda_pin=2, scl_pin=3, freq=400_000):
        self.i2c = I2C(i2c_bus, sda=Pin(sda_pin), scl=Pin(scl_pin), freq=freq)
        self.imu = BNO055Driver(self.i2c)

    def get_value(self):
        return list(map(float, self.imu.quaternion()))

    def get_quaternion(self): return list(map(float, self.imu.quaternion()))
    def get_euler(self): return list(map(float, self.imu.euler()))
    def get_temperature(self): return int(self.imu.temperature())
    def get_gyro(self): return list(map(float, self.imu.gyro()))
    def get_accel(self): return list(map(float, self.imu.accel()))
    def get_linear_accel(self): return list(map(float, self.imu.lin_acc()))
    def get_gravity(self): return list(map(float, self.imu.gravity()))
    def get_magnetometer(self): return list(map(float, self.imu.mag()))
    def is_calibrated(self): return self.imu.calibrated()
    def get_calibration_status(self): return list(self.imu.cal_status())


class MPU6050(Sensor):
    """
    MPU6050 sensor subclass. Requires a preconfigured I2C instance.
    """
    def __init__(self, i2c):
        self.i2c = i2c
        self.imu = MPU6050Driver(i2c)

    def get_value(self):
        accel = self.imu.read_accel_data()
        gyro = self.imu.read_gyro_data()
        temp = self.imu.read_temperature()
        return {"accel": accel, "gyro": gyro, "temp": temp}

    def is_calibrated(self):
        return True

    def get_calibration_status(self):
        return [3, 3, 3, 3]
    
    
class Dummy(Sensor):
    def __init__(self, value=None, calibrated=True, cal_status=[3, 3, 3, 3]):
        self._value = value or [1.0, 0.0, 0.0, 0.0]
        self._calibrated = calibrated
        self._cal_status = cal_status

    def get_value(self): return self._value
    def is_calibrated(self): return self._calibrated
    def get_calibration_status(self): return self._cal_status
