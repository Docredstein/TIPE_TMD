#include "PID.h"
#include "hardware/timer.h"
PID::PID(float Kp,float Ki,float Kd, float max_derivative, float max_integral) {
    m_Kp = Kp;
    m_Ki = Ki;
    m_Kd = Kd;
    m_max_d = max_derivative;
    m_max_int = max_integral; 
    m_integral = 0; 
    m_lastError = 0;
    m_lastMicros = time_us_32();
    m_consigne = 0;
}
int PID::update_consigne(float consigne) {
    m_consigne = consigne;
    return 0;
    
}
float PID::update_measure(float measure) {
    auto current_micros = time_us_32();
    float dt = (current_micros - m_lastMicros)/1e6; 
    float error = (m_consigne-measure);
    float derivative = MIN((error-m_lastError)/dt,m_max_d);
    m_integral = MIN(m_integral + error*dt,m_max_int);
    m_lastError = error;
    m_lastMicros = current_micros;
    return m_Kp*error+m_Ki*m_integral+m_Kd*derivative;
}