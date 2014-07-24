#!/usr/bin/env python

import i2c
from math import sqrt

############################################################
class lsm303d:

    def __init__( self, i2c_bus = 1, sa0_level = 'high' ):
        if sa0_level == 'high':
            dev = 0b0011101;
        elif sa0_level == 'low':
            dev = 0b0011110;
        else:
            raise TypeError;
        #
        self.sensor_id = i2c.init( i2c_bus, dev );

        self.acc_dx = 0.;
        self.acc_dy = 0.;
        self.acc_dz = 0.;

        self.set_sample_rate(  );
        self.set_acc_full_scale_anti_alias(  );
        self.set_mag_mode(  );
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

    def magnitude( self, x, y, z ):
        return sqrt( x**2 + y**2 + z**2 );
    #

    def set_sample_rate( self, sample_rate = '50Hz', \
                         block = False ):
        self.sample_rate_dict       \
            = { 'Down'    : 0b0000, \
                '3.125Hz' : 0b0001, \
                '6.25Hz'  : 0b0010, \
                '12.5Hz'  : 0b0011, \
                '25Hz'    : 0b0100, \
                '50Hz'    : 0b0101, \
                '100Hz'   : 0b0110, \
                '200Hz'   : 0b0111, \
                '400Hz'   : 0b1000, \
                '800Hz'   : 0b1001, \
                '1600Hz'  : 0b1010  \
            };
        sample_rate_flag\
            = self.sample_rate_dict[ sample_rate ] << 4;

        if block:
            block_flag = 0b1000;
        else:
            block_flag = 0b0000;
        #

        enable_flag = 0b111;

        flag = sample_rate_flag + block_flag + enable_flag;
        self.write_reg( self.CTRL1, flag );
        return;
    #

    def set_acc_full_scale_anti_alias\
        ( self, full_scale = '4g', aa_bw = '773Hz' ):

        self.aa_bw_dict         \
            = { '773Hz' : 0b00, \
                '194Hz' : 0b01, \
                '362Hz' : 0b10, \
                '50Hz'  : 0b11  \
            };
        aa_bw_flag              \
            = self.aa_bw_dict[ aa_bw ] << 6;

        self.full_scale_dict   \
            = { '2g'  : 0b000, \
                '4g'  : 0b001, \
                '6g'  : 0b010, \
                '8g'  : 0b011, \
                '16g' : 0b100  \
            };
        full_scale_flag        \
            = self.full_scale_dict[ full_scale ] << 3;
        self.full_scale_conv   \
            = { '2g'  : 0.061, \
                '4g'  : 0.122, \
                '6g'  : 0.183, \
                '8g'  : 0.244, \
                '16g' : 0.732  \
            };
        self.acc_conv = self.full_scale_conv[ full_scale ] \
                        * 0.001; # From mg to g

        flag = aa_bw_flag + full_scale_flag;
        self.write_reg( self.CTRL2, flag );
        return;
    #

    def set_mag_mode( self, full_scale = '4gauss' ):
        self.full_scale_dict   \
            = { '2gauss'  : 0b00, \
                '4gauss'  : 0b01, \
                '8gauss'  : 0b10, \
                '12gauss' : 0b11, \
            };
        full_scale_flag        \
            = self.full_scale_dict[ full_scale ] << 5;

        self.full_scale_conv   \
            = { '2gauss'  : 0.080, \
                '4gauss'  : 0.160, \
                '8gauss'  : 0.320, \
                '12gauss' : 0.479, \
            };
        self.mag_conv = self.full_scale_conv[ full_scale ] \
                        * 0.001; # From mGauss to Gauss

        flag = full_scale_flag;
        self.write_reg( self.CTRL6, flag );

        flag = 0b00000000;
        self.write_reg( self.CTRL7, flag );
    #

    def get_acc( self ):
        acc_x = self.read_reg( self.OUT_X_L_A ) \
                * self.acc_conv - self.acc_dx;
        acc_y = self.read_reg( self.OUT_Y_L_A ) \
                * self.acc_conv - self.acc_dy;
        acc_z = self.read_reg( self.OUT_Z_L_A ) \
                * self.acc_conv - self.acc_dz;
        return acc_x, acc_y, acc_z;
    #

    def get_mag( self ):
        mag_x = self.read_reg( self.OUT_X_L_M ) \
                * self.mag_conv;
        mag_y = self.read_reg( self.OUT_Y_L_M ) \
                * self.mag_conv;
        mag_z = self.read_reg( self.OUT_Z_L_M ) \
                * self.mag_conv;
        return mag_x, mag_y, mag_z;
    #

    #######################################################
    # Registers
    ##############################
    TEMP_OUT_L   = 0x05;
    TEMP_OUT_H   = 0x06;
    STATUS_M     = 0x07;
    INT_CTRL_M   = 0x12;
    INT_SRC_M    = 0x13;
    INT_THS_L_M  = 0x14;
    INT_THS_H_M  = 0x15;
    OFFSET_X_L_M = 0x16;
    OFFSET_X_H_M = 0x17;
    OFFSET_Y_L_M = 0x18;
    OFFSET_Y_H_M = 0x19;
    OFFSET_Z_L_M = 0x1A;
    OFFSET_Z_H_M = 0x1B;
    REFERENCE_X  = 0x1C;
    REFERENCE_Y  = 0x1D;
    REFERENCE_Z  = 0x1E;
    CTRL0        = 0x1F;
    CTRL1        = 0x20;
    CTRL2        = 0x21;
    CTRL3        = 0x22;
    CTRL4        = 0x23;
    CTRL5        = 0x24;
    CTRL6        = 0x25;
    CTRL7        = 0x26;
    STATUS_A     = 0x27;
    OUT_X_L_A    = 0x28;
    OUT_X_H_A    = 0x29;
    OUT_Y_L_A    = 0x2A;
    OUT_Y_H_A    = 0x2B;
    OUT_Z_L_A    = 0x2C;
    OUT_Z_H_A    = 0x2D;
    OUT_X_L_M    = 0x08;
    OUT_X_H_M    = 0x09;
    OUT_Y_L_M    = 0x0A;
    OUT_Y_H_M    = 0x0B;
    OUT_Z_L_M    = 0x0C;
    OUT_Z_H_M    = 0x0D;
    FIFO_CTRL    = 0x2E;
    FIFO_SRC     = 0x2F;
    IG_CFG1      = 0x30;
    IG_SRC1      = 0x31;
    IG_THS1      = 0x32;
    IG_DUR1      = 0x33;
    IG_CFG2      = 0x34;
    IG_SRC2      = 0x35;
    IG_THS2      = 0x36;
    IG_DUR2      = 0x37;
    CLICK_CFG    = 0x38;
    CLICK_SRC    = 0x39;
    CLICK_THS    = 0x3A;
    TIME_LIMIT   = 0x3B;
    TIME_LATENCY = 0x3C;
    TIME_WINDOW  = 0x3D;
    Act_THS      = 0x3E;
    Act_DUR      = 0x3F;
    WHO_AM_I     = 0x0F;
    #######################################################
#