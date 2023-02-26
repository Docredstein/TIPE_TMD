#ifndef MOTOR_CONTROL_DEF 
#define MOTOR_CONTROL_DEF

#include "stdint.h"
#include <stdio.h>
#include "pico/stdlib.h"
class Motor_Control 
{
private:
    int m_EN,m_In1,m_In2;
    uint m_channel_In1,m_channel_In2,m_slice_In1,m_slice_In2;
public:
    Motor_Control(int Pin_EN,int Pin_In1,int Pin_In2);
    ~Motor_Control();
    int setMotor(bool dir, uint16_t intensity);
    int stopMotor();
};




#endif