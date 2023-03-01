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

static int32_t platform_write(acc_handle *handle, uint8_t Reg, const uint8_t *Bufp, uint16_t len) {
    //Il faut créer un buffer en plus qui pourra stocker l'adresse du registre de destination
    
return 0;
}
static int32_t platform_read(void *handle, uint8_t Reg, uint8_t *Bufp, uint16_t len) {
return 0;
}

stmdev_ctx_t acc1; 
stmdev_ctx_t acc2;
static void platform_init(void);

//Core 0 : sensor read/serial com/wifi?
//Core 1 : Motor control
acc_handle handle_bas{i2c0,0x6A};
acc_handle handle_haut{i2c0,0x6B};




int main()
{
    stdio_init_all();
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
    interp_config cfg = interp_default_config();
    // Now use the various interpolator library functions for your use case
    // e.g. interp_config_clamp(&cfg, true);
    //      interp_config_shift(&cfg, 2);
    // Then set the config 
    interp_set_config(interp0, 0, &cfg);

    // Timer example code - This example fires off the callback after 2000ms
    add_alarm_in_ms(2000, alarm_callback, NULL, false);




    puts("Hello, world!");


    while(1) {

    }
    return 0;
}


void core1_entry() {
    PID pid = PID(1,0,0);
    


    while(1) {
        
    }
}