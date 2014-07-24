#!/usr/bin/env python

import i2c

############################################################
class lps25h:

    def __init__( self, i2c_bus = 1, sa0_level = 'high' ):
        if sa0_level == 'high':
            dev = 0b1011101;
        elif sa0_level == 'low':
            dev = 0b1011100;
        else:
            raise TypeError;
        #
        self.sensor_id = i2c.init( i2c_bus, dev );

        self.set_sample_rate(  );
        return;
    #

    def close( self ):
        i2c.destruct( self.sensor_id );

    def write_reg( self, reg, flag ):
        i2c.write_reg( self.sensor_id, reg, flag );
        return;
    #

    def read_reg( self, reg, size = 2 ):
        return i2c.read( self.sensor_id, reg, size );
    #

    def set_sample_rate( self, sample_rate = '12.5Hz', \
                         block = False ):
        self.sample_rate_dict      \
            = { 'Once'    : 0b000, \
                '1Hz'     : 0b001, \
                '7Hz'     : 0b010, \
                '12.5Hz'  : 0b011, \
                '25Hz'    : 0b100  \
            };
        sample_rate_flag\
            = self.sample_rate_dict[ sample_rate ] << 4;

        if block:
            block_flag = 0b100;
        else:
            block_flag = 0b000;
        #

        enable_flag = 0b1 << 7;

        flag = sample_rate_flag + block_flag + enable_flag;
        self.write_reg( self.CTRL_REG1, flag );
        return;
    #

    def get_baro( self ):
        baro = self.read_reg( self.PRESS_OUT_XL, size = 3 ) \
               / 4096.;
        return baro;
    #

    def get_temp( self ):
        temp = self.read_reg( self.TEMP_OUT_L );
        temp = 42.5 + ( temp / 480. );
        return temp;
    #

    #######################################################
    # Registers
    ##############################
    REF_P_XL       = 0x08;
    REF_P_L        = 0x09;
    REF_P_H        = 0x0A;
    WHO_AM_I       = 0x0F;
    RES_CONF       = 0x10;
    CTRL_REG1      = 0x20;
    CTRL_REG2      = 0x21;
    CTRL_REG3      = 0x22;
    CTRL_REG4      = 0x23;
    STATUS_REG     = 0x27;
    PRESS_OUT_XL   = 0x28;
    PRESS_OUT_L    = 0x29;
    PRESS_OUT_H    = 0x2A;
    TEMP_OUT_L     = 0x2B;
    TEMP_OUT_H     = 0x2C;
    FIFO_CTRL      = 0x2E;
    FIFO_STATUS    = 0x2F;
    RPDS_L         = 0x39;
    RPDS_H         = 0x3A;
    INTERRUPT_CFG  = 0x24;
    INT_SOURCE     = 0x25;
    THS_P_L        = 0x30;
    THS_P_H        = 0x31;
    #######################################################
#