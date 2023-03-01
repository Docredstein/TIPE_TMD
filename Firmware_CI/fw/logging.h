#ifndef LOGGING_H 
#define LOGGING_H 
#include <stdio.h>
#include "string.h"
#include "SD/FatFs_SPI/ff15/source/ff.h"
#include "stdint.h"
class logging
{
private:
    /* data */ 
    FATFS m_sd_card; 
    FIL m_fil ; 
    FRESULT m_fr; 
public:
    logging(/* args */);
    ~logging();
    int open_file(char* filename);
    int close_file();
    int save(char * data);
};













#endif