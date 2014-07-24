#!/usr/bin/env python

import i2c
from math import sqrt

############################################################
class l3gd20h:

    def __init__( self, i2c_bus = 1, sa0_level = 'high' ):
        if sa0_level == 'high':
            dev = 0b1101011;
        elif sa0_level == 'low':
            dev = 0b1101010;
        else:
            raise TypeError;
        #
        self.sensor_id = i2c.init( i2c_bus, dev );

        self.gyr_dx = 0.;
        self.gyr_dy = 0.;
        self.gyr_dz = 0.;

        self.set_sample_rate(  );
        self.set_full_scale(  );
        return;
    #

    def close( self ):
        i2c.destruct( self.sensor_id );

    def write_reg( self, reg, flag ):
        # pdb.set_trace(  );
        i2c.write_reg( self.sensor_id, reg, flag );
        return;
    #

    def read_reg( self, reg, size = 2 ):
        return i2c.read( self.sensor_id, reg, size );
    #

    def magnitude( self, x, y, z ):
        return sqrt( x**2 + y**2 + z**2 );
    #

    def set_sample_rate( self, sample_rate = '200Hz', \
                         block = False ):
        self.sample_rate_dict      \
            = { '100Hz'   : 0b00, \
                '200Hz'   : 0b01, \
                '400Hz'   : 0b10, \
                '800Hz'   : 0b11  \
            };
        sample_rate_flag\
            = self.sample_rate_dict[ sample_rate ] << 6;

        bw_flag = 0b00 << 4;

        enable_flag = 0b1111;

        flag = sample_rate_flag + bw_flag + enable_flag;
        self.write_reg( self.CTRL1, flag );
        return;
    #

    def set_full_scale( self, full_scale = '245dps', \
                        block = False ):
        self.full_scale_dict      \
            = { '245dps'  : 0b00, \
                '500dps'  : 0b01, \
                '2000dps' : 0b10  \
            };
        full_scale_flag\
            = self.full_scale_dict[ full_scale ] << 4;
        
        self.full_scale_conv       \
            = { '245dps'  : 8.75,  \
                '500dps'  : 17.50, \
                '2000dps' : 70.00  \
            };
        self.gyr_conv = self.full_scale_conv[ full_scale ] \
                        / 1000.; # From mdps to dps

        if block:
            block_flag = 0b1 << 7;
        else:
            block_flag = 0b0;

        flag = full_scale_flag + block_flag;
        self.write_reg( self.CTRL4, flag );
        return;
    #

    def get_gyr( self ):
        gyr_x = self.read_reg( self.OUT_X_L ) \
                * self.gyr_conv - self.gyr_dx;
        gyr_y = self.read_reg( self.OUT_Y_L ) \
                * self.gyr_conv - self.gyr_dy;
        gyr_z = self.read_reg( self.OUT_Z_L ) \
                * self.gyr_conv - self.gyr_dz;
        return gyr_x, gyr_y, gyr_z;
    #

    #######################################################
    # Registers
    ##############################
    WHO_AM_I      = 0x0F;
    CTRL1         = 0x20;
    CTRL2         = 0x21;
    CTRL3         = 0x22;
    CTRL4         = 0x23;
    CTRL5         = 0x24;
    REFERENCE     = 0x25;
    OUT_TEMP      = 0x26;
    STATUS_REG    = 0x27;
    OUT_X_L       = 0x28;
    OUT_X_H       = 0x29;
    OUT_Y_L       = 0x2A;
    OUT_Y_H       = 0x2B;
    OUT_Z_L       = 0x2C;
    OUT_Z_H       = 0x2D;
    FIFO_CTRL_REG = 0x2E;
    FIFO_SRC_REG  = 0x2F;
    INT1_CFG      = 0x30;
    INT1_SRC      = 0x31;
    INT1_THS_XH   = 0x32;
    INT1_THS_XL   = 0x33;
    INT1_THS_YH   = 0x34;
    INT1_THS_YL   = 0x35;
    INT1_THS_ZH   = 0x36;
    INT1_THS_ZL   = 0x37;
    INT1_DURATION = 0x38;
    LOW_ODR       = 0x39;
    #######################################################
#