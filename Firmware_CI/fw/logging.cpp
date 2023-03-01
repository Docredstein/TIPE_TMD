#include "logging.h"
#include <stdio.h>
#include "string.h"
#include "SD/FatFs_SPI/ff15/source/ff.h"
#include "stdint.h"
#include "sd_card.h"
logging::logging() {

}
logging::~logging() {
    f_close(&m_fil);
}
int logging::open_file(char* filename) {
    if (!sd_init_driver()) {
        return 1;
    }
    m_fr = f_mount(&m_sd_card,"0:",1);
    if (m_fr != FR_OK) {
        return 2;
    }
    m_fr = f_open(&m_fil,filename, FA_OPEN_APPEND|FA_WRITE|FA_READ);
    if (m_fr != FR_OK) {
        return 3;
    }
    auto ret = f_printf(&m_fil, "--------------\n");
    if (ret <0) {
        f_close(&m_fil);
        return 4;
    }
 return 0;   
}
int logging::close_file() {
    return f_close(&m_fil);
}
int logging::save(char * data) {
    return f_printf(&m_fil,data);
}