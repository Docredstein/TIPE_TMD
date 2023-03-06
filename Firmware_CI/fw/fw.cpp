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
#include "pico/cyw43_arch.h"
#include "pico/multicore.h"
#include "lsm6ds3tr-c_reg.h"
#include "tusb.h"
#include "logging.h"
#include "PID.h"
#include "Motor_Control.h"
// SPI Defines
// We are going to use SPI 0, and allocate it to the following GPIO pins
// Pins can be changed, see the GPIO function select table in the datasheet for information on GPIO assignments


// I2C defines
// This example will use I2C0 on GPIO8 (SDA) and GPIO9 (SCL) running at 400KHz.
// Pins can be changed, see the GPIO function select table in the datasheet for information on GPIO assignments

typedef struct 
{
    i2c_inst_t *  handle;
    int adress;
}acc_handle;

int64_t alarm_callback(alarm_id_t id, void *user_data) {
    // Put your timeout handler code in here
    return 0;
   
}

static int32_t platform_write(void *handle, uint8_t Reg, const uint8_t *Bufp, uint16_t len) {
    //Il faut créer un buffer en plus qui pourra stocker l'adresse du registre de destination
    uint8_t newBuf[len+1];
    newBuf[0] = Reg;
    for (char i=0;i<len;i++) {
        newBuf[i+1] = Bufp[i];
    }
return i2c_write_blocking(((acc_handle*)handle)->handle,((acc_handle*)handle)->adress,newBuf,len+1,false);
//return i2c_write_timeout_us(((acc_handle*)handle)->handle,((acc_handle*)handle)->adress,newBuf,len+1,false,100000);
}
static int32_t platform_read(void *handle, uint8_t Reg, uint8_t *Bufp, uint16_t len) {
    
i2c_write_blocking(((acc_handle*)handle)->handle,((acc_handle*)handle)->adress,&Reg,1,true);
//i2c_write_timeout_us(((acc_handle*)handle)->handle,((acc_handle*)handle)->adress,&Reg,1,false,100000);
int ret = i2c_read_blocking(((acc_handle*)handle)->handle,((acc_handle*)handle)->adress,Bufp,len,false);
//int ret=i2c_read_timeout_us(((acc_handle*)handle)->handle,((acc_handle*)handle)->adress,Bufp,len,false,100000);
if (ret <  len) {
    return PICO_ERROR_GENERIC;
}
return 0;
}

stmdev_ctx_t acc1; 
stmdev_ctx_t acc2;


//Core 0 : sensor read/serial com/wifi?
//Core 1 : Motor control
acc_handle handle_bas{i2c0,0x6A};
acc_handle handle_haut{i2c0,0x6B};
static void platform_init(void) {
    i2c_init(handle_bas.handle,100000);
    i2c_init(handle_haut.handle,100000);
    i2c_set_slave_mode(handle_haut.handle,false,0);
    i2c_set_slave_mode(handle_bas.handle,false,0);
    gpio_set_function(4,GPIO_FUNC_I2C);
    gpio_set_function(5,GPIO_FUNC_I2C);
}

void core1_entry() {
    
    
    gpio_init(10);
    gpio_set_dir(10,1);
    while(1) {
        gpio_put(10,1);
        sleep_ms(500);
        gpio_put(10,0);
        sleep_ms(300);

    }
}

int main()
{

    stdio_init_all();
    platform_init();
        sleep_ms(5000);
    printf("start\n");
    acc1.write_reg = &platform_write;
    acc1.read_reg = &platform_read;
    acc1.handle= &handle_bas ;

    acc2.write_reg = &platform_write;
    acc2.read_reg = &platform_read;
    acc2.handle= &handle_haut;

    // SPI initialisation. This example will use SPI at 1MHz.

    
    // Chip select is active-low, so we'll initialise it to a driven-high state

    

    // I2C Initialisation. Using it at 400Khz.




    // Interpolator example code
    //interp_config cfg = interp_default_config();
    // Now use the various interpolator library functions for your use case
    // e.g. interp_config_clamp(&cfg, true);
    //      interp_config_shift(&cfg, 2);
    // Then set the config 
    //interp_set_config(interp0, 0, &cfg);

    // Timer example code - This example fires off the callback after 2000ms
    //add_alarm_in_ms(2000, alarm_callback, NULL, false);
    multicore_launch_core1(&core1_entry);


    printf("initialised\n");
    puts("Hello, world!\n");


    while(1) {
        uint8_t whoami = 0; 
        printf("reading\n");
        auto ret = lsm6ds3tr_c_device_id_get(&acc1,&whoami);
        if (ret != 0 ) {
            printf("error = %x\n",ret);
        }
        printf("ID_1=%x, expected = %x\n",whoami,LSM6DS3TR_C_ID);
        ret = lsm6ds3tr_c_device_id_get(&acc2,&whoami);
        if (ret != 0 ) {
            printf("error = %x\n",ret);
        }
        printf("ID_2=%x, expected = %x\n",whoami,LSM6DS3TR_C_ID);
        sleep_ms(1000);
    }
    return 0;
}


