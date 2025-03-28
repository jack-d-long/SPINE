#include "pico/stdlib.h"
#include "imu_module.h"
#include <stdio.h>

int main() {
    stdio_init_all();
    
    IMU imu;
    if (!imu.begin()) {
        printf("IMU initialization failed!\n");
        return 1;
    }

    while (true) {
        IMU_DATA data = imu.getSensorData();
        printf("Orientation: x=%.2f, y=%.2f, z=%.2f\n",
               data.values.orientation.x, data.values.orientation.y, data.values.orientation.z);
        printf("Quaternion: w=%.4f, x=%.4f, y=%.4f, z=%.4f\n",
               data.values.quaternion.w, data.values.quaternion.x,
               data.values.quaternion.y, data.values.quaternion.z);
        printf("Calibration: sys=%d, gyro=%d, accel=%d, mag=%d\n\n",
               data.calibration.sys, data.calibration.gyro,
               data.calibration.accel, data.calibration.mag);

        sleep_ms(500);
    }
}
