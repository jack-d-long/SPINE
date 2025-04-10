from sensor_sync import BNO055, Dummy
import time

"""
Example code for using synchronous sensor output. Best practice is likely going to be sending over the radio
something like:

Bytes 0-3: Quat floats
Bytes 4-7: orientation data

+ any extras u need. Frontend needs only quat and orientation


"""
sensor = BNO055()

sensor1 = Dummy(value=[0.707, 0.0, 0.707, 0.0], calibrated=True)


while True:
    quat = sensor.get_quaternion()
    temp = sensor.get_temperature() if hasattr(sensor, "get_temperature") else None
    calibrated = sensor.is_calibrated()
    print(f"Quat: {quat} | Temp: {temp}°C | Calibrated: {calibrated}")
    time.sleep(0.1)  # Timing handled here, not inside methods
