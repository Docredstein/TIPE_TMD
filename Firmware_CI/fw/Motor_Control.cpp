#include "Motor_Control.h"
#include "pico/stdlib.h"

Motor_Control::Motor_Control(int Pin_EN,int Pin_In1,int Pin_In2)
{
    m_EN = Pin_EN;
    m_In1 = Pin_In1;
    m_In2 = Pin_In2;
    gpio_set_function(m_In1,GPIO_FUNC_PWM);
    gpio_set_function(m_In2,GPIO_FUNC_PWM);
    

}

Motor_Control::~Motor_Control()
{

}
int Motor_Control::setMotor(bool dir, uint16_t intensity)  {
    return 0;
}
