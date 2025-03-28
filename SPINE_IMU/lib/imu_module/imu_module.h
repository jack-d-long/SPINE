#ifndef IMU_MODULE_H
#define IMU_MODULE_H

#include "pico/stdlib.h"
#include "hardware/i2c.h"
#include <Adafruit_Sensor.h>
#include <Adafruit_BNO055.h>
#include <utility/imumaths.h>

// Define I2C settings for RP2040
#define I2C_PORT i2c0
#define SDA_PIN  4
#define SCL_PIN  5
#define BNO055_ADDR 0x28

// Structs for sensor data
struct IMU_CALIBRATION {
    uint8_t sys, gyro, accel, mag;
};

struct IMU_SENSORVALS {
    sensors_vec_t orientation;
    imu::Quaternion quaternion;
};

struct IMU_DATA {
    IMU_SENSORVALS values;
    IMU_CALIBRATION calibration;
};

// IMU class definition
class IMU {
public:
    IMU();
    bool begin();
    IMU_DATA getSensorData();
    sensor_t getSensorDetails();

private:
    Adafruit_BNO055 bno;
};

#endif // IMU_MODULE_H
