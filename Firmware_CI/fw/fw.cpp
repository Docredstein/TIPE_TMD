#include <stdio.h>
#include "pico/stdlib.h"
#include "hardware/spi.h"
#include "hardware/i2c.h"
#include "hardware/dma.h"
#include "hardware/pio.h"
#include "hardware/interp.h"
#include "hardware/timer.h"
#include "hardware/watchdog.h"
#include "hardware/clocks.h"
// #include "pico/cyw43_arch.h"
#include "pico/multicore.h"
#include "lsm6ds3tr-c_reg.h"
// #include "tusb.h"
#include "logging.h"
#include "PID.h"
#include "Motor_Control.h"
#include <strings.h>

#define NOGYRTEMP

#define HEARTBEATLED 10
// SPI Defines
// We are going to use SPI 0, and allocate it to the following GPIO pins
// Pins can be changed, see the GPIO function select table in the datasheet for information on GPIO assignments

// I2C defines
// This example will use I2C0 on GPIO8 (SDA) and GPIO9 (SCL) running at 400KHz.
// Pins can be changed, see the GPIO function select table in the datasheet for information on GPIO assignments

typedef struct
{
    i2c_inst_t *handle;
    int adress;
} acc_handle;

int64_t alarm_callback(alarm_id_t id, void *user_data)
{
    // Put your timeout handler code in here
    return 0;
}

static int32_t platform_write(void *handle, uint8_t Reg, const uint8_t *Bufp, uint16_t len)
{
    // Il faut créer un buffer en plus qui pourra stocker l'adresse du registre de destination
    uint8_t newBuf[len + 1];
    newBuf[0] = Reg;
    for (char i = 0; i < len; i++)
    {
        newBuf[i + 1] = Bufp[i];
    }
    return i2c_write_blocking(((acc_handle *)handle)->handle, ((acc_handle *)handle)->adress, newBuf, len + 1, false);
    // return i2c_write_timeout_us(((acc_handle*)handle)->handle,((acc_handle*)handle)->adress,newBuf,len+1,false,100000);
}
static int32_t platform_read(void *handle, uint8_t Reg, uint8_t *Bufp, uint16_t len)
{

    i2c_write_blocking(((acc_handle *)handle)->handle, ((acc_handle *)handle)->adress, &Reg, 1, true);
    // i2c_write_timeout_us(((acc_handle*)handle)->handle,((acc_handle*)handle)->adress,&Reg,1,false,100000);
    int ret = i2c_read_blocking(((acc_handle *)handle)->handle, ((acc_handle *)handle)->adress, Bufp, len, false);
    // int ret=i2c_read_timeout_us(((acc_handle*)handle)->handle,((acc_handle*)handle)->adress,Bufp,len,false,100000);
    if (ret < len)
    {
        return PICO_ERROR_GENERIC;
    }
    return 0;
}

stmdev_ctx_t acc1;
stmdev_ctx_t acc2;

// Core 0 : sensor read/serial com/wifi?
// Core 1 : Motor control
acc_handle handle_bas{i2c0, 0x6B};
acc_handle handle_haut{i2c0, 0x6A};
static void platform_init(void)
{
    i2c_init(handle_bas.handle, 100000);
    i2c_init(handle_haut.handle, 100000);
    i2c_set_slave_mode(handle_haut.handle, false, 0);
    i2c_set_slave_mode(handle_bas.handle, false, 0);
    gpio_set_function(4, GPIO_FUNC_I2C);
    gpio_set_function(5, GPIO_FUNC_I2C);
}

void core1_entry()
{

    gpio_init(HEARTBEATLED);
    gpio_set_dir(HEARTBEATLED, 1);
    while (1)
    {
        
        gpio_put(HEARTBEATLED, 1);
        sleep_ms(500);
        gpio_put(HEARTBEATLED, 0);
        sleep_ms(300);
    }
}

typedef enum
{
    Start_Recording = 'S',
    Stop_Recording = 'T',
    Reset = 'R'

} Uart_Control;

void Accelerometer_Config(stmdev_ctx_t *acc)
{
    lsm6ds3tr_c_block_data_update_set(acc, PROPERTY_ENABLE);
    lsm6ds3tr_c_xl_data_rate_set(acc, LSM6DS3TR_C_XL_ODR_104Hz);
    lsm6ds3tr_c_gy_data_rate_set(acc, LSM6DS3TR_C_GY_ODR_12Hz5);

    lsm6ds3tr_c_xl_full_scale_set(acc, LSM6DS3TR_C_4g);
    lsm6ds3tr_c_gy_full_scale_set(acc, LSM6DS3TR_C_2000dps);

    lsm6ds3tr_c_xl_filter_analog_set(acc,
                                     LSM6DS3TR_C_XL_ANA_BW_400Hz);
    lsm6ds3tr_c_xl_lp2_bandwidth_set(acc,
                                     LSM6DS3TR_C_XL_LOW_NOISE_LP_ODR_DIV_100);
    lsm6ds3tr_c_gy_band_pass_set(acc,
                                 LSM6DS3TR_C_HP_260mHz_LP1_STRONG);
    lsm6ds3tr_c_xl_power_mode_set(acc, LSM6DS3TR_C_XL_HIGH_PERFORMANCE);
    lsm6ds3tr_c_gy_power_mode_set(acc, LSM6DS3TR_C_GY_HIGH_PERFORMANCE);
}

void Accelerometer_Sanity_Check(stmdev_ctx_t *acc1, stmdev_ctx_t *acc2)
{

    uint8_t whoami = 0;
    auto ret = lsm6ds3tr_c_device_id_get(acc1, &whoami);
    if (ret != 0)
    {
        printf("error = %x\n", ret);
    }
    if (whoami != 0x6a)
    {
        printf("lower sensor Error");
    }
    ret = lsm6ds3tr_c_device_id_get(acc2, &whoami);
    if (ret != 0)
    {
        printf("error = %x\n", ret);
    }
    if (whoami != 0x6a)
    {
        printf("upper sensor Error");
    }
}

bool CheckSensor(stmdev_ctx_t *acc, lsm6ds3tr_c_reg_t *reg, int16_t *raw_accel, float *acceleration_mg, int16_t *raw_gyro, float *angular_mdps, int16_t *raw_temp, float *temp)
{
    bool newData_flag = false;
    lsm6ds3tr_c_status_reg_get(acc, &(reg->status_reg));
    if (reg->status_reg.xlda)
    {
        newData_flag = true;
        memset(raw_accel, 0x00, 3 * sizeof(int16_t)); // on remet le tableau à 0
        lsm6ds3tr_c_acceleration_raw_get(acc, raw_accel);
        acceleration_mg[0] = lsm6ds3tr_c_from_fs4g_to_mg(
            raw_accel[0]);
        acceleration_mg[1] = lsm6ds3tr_c_from_fs4g_to_mg(
            raw_accel[1]);
        acceleration_mg[2] = lsm6ds3tr_c_from_fs4g_to_mg(
            raw_accel[2]);
    }
    #ifndef NOGYRTEMP
    if (reg->status_reg.gda)
    {
        newData_flag = true;
        memset(raw_gyro, 0x00, 3 * sizeof(int16_t));
        lsm6ds3tr_c_angular_rate_raw_get(acc, raw_gyro);
        angular_mdps[0] = lsm6ds3tr_c_from_fs2000dps_to_mdps(raw_gyro[0]);
        angular_mdps[1] = lsm6ds3tr_c_from_fs2000dps_to_mdps(raw_gyro[1]);
        angular_mdps[2] = lsm6ds3tr_c_from_fs2000dps_to_mdps(raw_gyro[2]);
    }
    if (reg->status_reg.tda)
    {
        // newData_flag = true;
        *raw_temp = 0;
        lsm6ds3tr_c_temperature_raw_get(acc, raw_temp);
        *temp = lsm6ds3tr_c_from_lsb_to_celsius(*raw_temp);
    }
    #endif
    return newData_flag;
}

int main()
{
    static int16_t raw_accel_1[3], raw_accel_2[3], raw_gyro_1[3], raw_gyro_2[3], raw_temp_1, raw_temp_2;
    static float acceleration_mg_1[3], acceleration_mg_2[3], angular_mdps_1[3], angular_mdps_2[3], temp_1, temp_2;
    uint8_t drdy = 0;
    int save_count = 0;
    bool Measuring = true;
    lsm6ds3tr_c_reg_t reg_1, reg_2; // registre des drapeaux

    stdio_init_all();
    platform_init();

    // UART
    gpio_set_function(0, GPIO_FUNC_UART);
    gpio_set_function(1, GPIO_FUNC_UART);
    uart_init(uart0, 115200);
    uart_set_fifo_enabled(uart0, 1);

    sleep_ms(5000);
    printf("start\n");
    acc1.write_reg = &platform_write;
    acc1.read_reg = &platform_read;
    acc1.handle = &handle_bas;

    acc2.write_reg = &platform_write;
    acc2.read_reg = &platform_read;
    acc2.handle = &handle_haut;

    gpio_init(17);
    gpio_put(17, 0);
    printf("log");
    logging log;
    char filename[100]; 
    char data[100]{"FRAMBOURT Mateis PSI*, BOCQUILLON NOE PSI*, 2023"};
    sprintf(filename, "copyright.txt");

    printf("opening the file : return %i\n", log.open_file(filename));
    printf("saving the file : return %i\n", log.save(data));
    printf("closing the file : return %i\n", log.close_file());
    sprintf(filename,"reading_");
    sprintf(filename, strcat(strcat(filename, __DATE__), ".csv"));
    // sprintf(filename+8,__DATE__);
    printf("opening the file : return %i\n", log.open_file(filename));
    log.save((char*)"----------------\n");

    // configure sensor
    Accelerometer_Sanity_Check(&acc1, &acc2);

    Accelerometer_Config(&acc1);
    Accelerometer_Config(&acc2);

    // Chip select is active-low, so we'll initialise it to a driven-high state

    // I2C Initialisation. Using it at 400Khz.

    // Interpolator example code
    // interp_config cfg = interp_default_config();
    // Now use the various interpolator library functions for your use case
    // e.g. interp_config_clamp(&cfg, true);
    //      interp_config_shift(&cfg, 2);
    // Then set the config
    // interp_set_config(interp0, 0, &cfg);

    // Timer example code - This example fires off the callback after 2000ms
    // add_alarm_in_ms(2000, alarm_callback, NULL, false);
    multicore_launch_core1(&core1_entry);

    printf("initialised\n");

    while (1)
    {
        if (Measuring)
        {
            bool newData_flag = CheckSensor(&acc1, &reg_1, raw_accel_1, acceleration_mg_1, raw_gyro_1, angular_mdps_1, &raw_temp_1, &temp_1);
            newData_flag |= CheckSensor(&acc2, &reg_2, raw_accel_2, acceleration_mg_2, raw_gyro_2, angular_mdps_2, &raw_temp_2, &temp_2);

            if (newData_flag)
            {
                char tx_buf[1000];
                memset(tx_buf, 0, 500);

                auto current_time = time_us_64();
                #ifndef NOGYRTEMP
                sprintf(tx_buf, "?%lld;%f;%f;%f;%f;%f;%f;%f;%f;%f;%f;%f;%f;%f;%f;\n", current_time, acceleration_mg_1[0], acceleration_mg_1[1], acceleration_mg_1[2], angular_mdps_1[0], angular_mdps_1[1], angular_mdps_1[2], temp_1, acceleration_mg_2[0], acceleration_mg_2[1], acceleration_mg_2[2], angular_mdps_2[0], angular_mdps_2[1], angular_mdps_2[2], temp_2);
                #else 
                sprintf(tx_buf,"?%lld;%.4f;%.4f;%.4f;%.4f;%.4f;%.4f;\n",current_time,acceleration_mg_1[0], acceleration_mg_1[1], acceleration_mg_1[2],acceleration_mg_2[0], acceleration_mg_2[1], acceleration_mg_2[2]);
                #endif
                printf(tx_buf);
                log.save(tx_buf);
                save_count++;
            }

            if (save_count >= 1000)
            {
                log.close_file();
                log.open_file(filename);
                save_count = 0;
            }
        }
        if (uart_is_readable(uart0))
        {
            uint8_t command;
            uart_read_blocking(uart0, &command, 1);
            switch ((char)command)
            {
            case Start_Recording:
                Measuring = 1;
                break;
            case Stop_Recording:
                Measuring = 0;
                break;
            case Reset:
                watchdog_enable(1, false);
                break;
            default:
                break;
            }
        }
    }
    return 0;
}
