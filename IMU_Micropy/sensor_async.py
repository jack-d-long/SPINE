import uasyncio as asyncio
from machine import I2C, Pin
from bno055 import BNO055 as BNO055Driver

class Sensor:
    """
    Abstract asynchronous base class for all sensors.
    """
    async def get_value(self):
        raise NotImplementedError

    async def is_calibrated(self):
        raise NotImplementedError

    async def get_calibration_status(self):
        raise NotImplementedError


class BNO055(Sensor):
    """
    Async interface to BNO055 IMU sensor.
    """
    def __init__(self, i2c_bus=1, sda_pin=2, scl_pin=3, freq=400_000):
        self.i2c = I2C(i2c_bus, sda=Pin(sda_pin), scl=Pin(scl_pin), freq=freq)
        self.imu = BNO055Driver(self.i2c)

    async def get_value(self):
        """
        Default value: quaternion [w, x, y, z]
        """
        await asyncio.sleep(0)
        return list(map(float, self.imu.quaternion()))

    async def get_quaternion(self):
        
        
        """
            This is the important one -- returns quaternion angles easily interpreted by the Adafruit frontend
            (https://github.com/adafruit/Adafruit_WebSerial_3DModelViewer)
            
        """
        await asyncio.sleep(0)
        return list(map(float, self.imu.quaternion()))

    async def get_euler(self):
        await asyncio.sleep(0)
        return list(map(float, self.imu.euler()))

    async def get_temperature(self):
        await asyncio.sleep(0)
        return int(self.imu.temperature())

    async def get_gyro(self):
        await asyncio.sleep(0)
        return list(map(float, self.imu.gyro()))

    async def get_accel(self):
        await asyncio.sleep(0)
        return list(map(float, self.imu.accel()))

    async def get_linear_accel(self):
        await asyncio.sleep(0)
        return list(map(float, self.imu.lin_acc()))

    async def get_gravity(self):
        await asyncio.sleep(0)
        return list(map(float, self.imu.gravity()))

    async def get_magnetometer(self):
        await asyncio.sleep(0)
        return list(map(float, self.imu.mag()))

    async def is_calibrated(self):
        await asyncio.sleep(0)
        return self.imu.calibrated()

    async def get_calibration_status(self):
        await asyncio.sleep(0)
        return list(self.imu.cal_status())


class Dummy(Sensor):
    """
    Simplified dummy sensor for testing. Returns a generic value and calibration status.
    """
    def __init__(self, value=None, calibrated=True, cal_status=[3, 3, 3, 3]):
        self._value = value or [1.0, 0.0, 0.0, 0.0]
        self._calibrated = calibrated
        self._cal_status = cal_status

    async def get_value(self):
        await asyncio.sleep(0)
        return self._value

    async def is_calibrated(self):
        await asyncio.sleep(0)
        return self._calibrated

    async def get_calibration_status(self):
        await asyncio.sleep(0)
        return self._cal_status
