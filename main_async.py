import uasyncio as asyncio
from sensors_async import BNO055, Dummy


"""
Example code for using synchronous sensor output. Best practice is likely going to be sending over the radio
something like:

Bytes 0-3: Quat floats
Bytes 4-7: orientation data

+ any extras u need. Frontend needs only quat and orientation


"""

sensor = BNO055()
# sensor = Dummy(value=[0.0, 1.0, 0.0, 0.0])

async def main():
    while True:
        quat = await sensor.get_quaternion()
        temp = await sensor.get_temperature()
        calibrated = await sensor.is_calibrated()
        print(f"Quat: {quat} | Temp: {temp}°C | Calibrated: {calibrated}")
        await asyncio.sleep(0.1)

asyncio.run(main())
