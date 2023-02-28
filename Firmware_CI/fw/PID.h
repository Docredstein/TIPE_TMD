#ifndef PID_H 
#define PID_H 

#include <stdio.h>
#include <stdint.h>

class PID
{
private:
    /* data */
    float m_Kp,m_Ki,m_Kd,m_max_d,m_max_int;
    float m_lastError; 
    float m_integral;
    float m_consigne;
    uint32_t  m_lastMicros;
public:
    PID(float Kp,float Ki,float Kd, float max_derivative = 1000, float max_integral = 1000);
    ~PID();
    float update_measure(float mesure);
    int update_consigne(float consigne);
    //float get_command();
};



#endif