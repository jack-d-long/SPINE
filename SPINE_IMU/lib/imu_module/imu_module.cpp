#include "imu_module.h"
#include <stdio.h>

// Initialize I2C and BNO055 IMU
void init_imu() {
    i2c_init(I2C_PORT, 400 * 1000);
    gpio_set_function(SDA_PIN, GPIO_FUNC_I2C);
    gpio_set_function(SCL_PIN, GPIO_FUNC_I2C);
    gpio_pull_up(SDA_PIN);
    gpio_pull_up(SCL_PIN);
    printf("I2C Initialized.\n");

    // Check if BNO055 is detected
    uint8_t chip_id = read_register(0x00);
    if (chip_id != 0xA0) {
        printf("Error: BNO055 not detected!\n");
    } else {
        printf("BNO055 detected. Initializing...\n");
        write_register(0x3F, 0x00); // Set to CONFIG mode
        write_register(0x3B, 0x01); // Enable external crystal
        write_register(0x3F, 0x0C); // Set to NDOF mode
    }
}

// Write to a register on BNO055
void write_register(uint8_t reg, uint8_t value) {
    uint8_t data[2] = {reg, value};
    i2c_write_blocking(I2C_PORT, BNO055_ADDR, data, 2, false);
}

// Read from a register on BNO055
uint8_t read_register(uint8_t reg) {
    uint8_t value;
    i2c_write_blocking(I2C_PORT, BNO055_ADDR, &reg, 1, true);
    i2c_read_blocking(I2C_PORT, BNO055_ADDR, &value, 1, false);
    return value;
}

// Retrieve sensor details
sensor_t getSensorDetails() {
    sensor_t sensor;
    // This function would need to read specific sensor info from BNO055
    return sensor;
}

// Retrieve IMU sensor data
IMU_DATA getSensorData() {
    IMU_DATA data_out;
    uint8_t buffer[6];

    // Read Euler angles (registers 0x1A - 0x1F)
    uint8_t reg = 0x1A;
    i2c_write_blocking(I2C_PORT, BNO055_ADDR, &reg, 1, true);
    i2c_read_blocking(I2C_PORT, BNO055_ADDR, buffer, 6, false);

    data_out.values.orientation.x = (buffer[0] | (buffer[1] << 8)) / 16.0;
    data_out.values.orientation.y = (buffer[2] | (buffer[3] << 8)) / 16.0;
    data_out.values.orientation.z = (buffer[4] | (buffer[5] << 8)) / 16.0;

    // Read quaternion (registers 0x20 - 0x27)
    reg = 0x20;
    i2c_write_blocking(I2C_PORT, BNO055_ADDR, &reg, 1, true);
    i2c_read_blocking(I2C_PORT, BNO055_ADDR, buffer, 8, false);

    data_out.values.quaternion.w = (buffer[0] | (buffer[1] << 8)) / (1 << 14);
    data_out.values.quaternion.x = (buffer[2] | (buffer[3] << 8)) / (1 << 14);
    data_out.values.quaternion.y = (buffer[4] | (buffer[5] << 8)) / (1 << 14);
    data_out.values.quaternion.z = (buffer[6] | (buffer[7] << 8)) / (1 << 14);

    // Read calibration status (register 0x35)
    reg = 0x35;
    i2c_write_blocking(I2C_PORT, BNO055_ADDR, &reg, 1, true);
    i2c_read_blocking(I2C_PORT, BNO055_ADDR, buffer, 1, false);

    data_out.calibration.sys = (buffer[0] >> 6) & 0x03;
    data_out.calibration.gyro = (buffer[0] >> 4) & 0x03;
    data_out.calibration.accel = (buffer[0] >> 2) & 0x03;
    data_out.calibration.mag = buffer[0] & 0x03;

    return data_out;
}
