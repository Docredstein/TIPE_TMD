#include "Motor_Control.h"
#include "pico/stdlib.h"
#include "hardware/pwm.h"
#include "time.h"
Motor_Control::Motor_Control(int Pin_EN,int Pin_In1,int Pin_In2)
{
    int m_EN = Pin_EN;
    int m_In1 = Pin_In1;
    int m_In2 = Pin_In2;
    gpio_set_function(m_In1,GPIO_FUNC_PWM);
    gpio_set_function(m_In2,GPIO_FUNC_PWM);
    gpio_init(m_EN);
    gpio_pull_up(m_EN);
    gpio_pull_down(m_In1);
    gpio_pull_down(m_In2);
    m_channel_In1 = pwm_gpio_to_channel(m_In1);
    m_channel_In2 = pwm_gpio_to_channel(m_In2);
    m_slice_In1 = pwm_gpio_to_slice_num(m_In1);
    m_slice_In2 = pwm_gpio_to_slice_num(m_In2);
    //séléction de la fréquence : 10kHz 
    //on choisit le wrap le plus grand possible
    pwm_set_wrap(m_slice_In1,12500);
    pwm_set_wrap(m_slice_In2,12500);
    pwm_set_enabled(m_channel_In1,false);
    pwm_set_enabled(m_channel_In2,false); 

}

Motor_Control::~Motor_Control()
{

}

/* TRUTH TABLE
EN | IN1| IN2| OUT1   | OUT2
L  | X  | X  | High Z | High Z
H  | L  | L  | GND    | GND
H  | H  | L  | Vs     | GND
H  | L  | H  | GND    | Vs
H  | H  | H  | Vs     | Vs*/
int Motor_Control::setMotor(bool dir, uint16_t intensity)  {
    if (dir) {
        pwm_set_enabled(m_channel_In2,false);
        pwm_set_enabled(m_channel_In1,true);
        pwm_set_chan_level(m_slice_In1,m_channel_In1,intensity);
        pwm_set_chan_level(m_slice_In2,m_channel_In2,0);
    }
    else {
        pwm_set_enabled(m_channel_In1,false);
        pwm_set_enabled(m_channel_In2,true);
        pwm_set_chan_level(m_slice_In2,m_channel_In2,intensity);
        pwm_set_chan_level(m_slice_In1,m_channel_In1,0);
    }
    return 0;
}

int Motor_Control::stopMotor() {
    pwm_set_enabled(m_channel_In1,false);
    pwm_set_enabled(m_channel_In2,false);
    sleep_ms(250);
    gpio_put(m_EN,0);
    return 0;
}
