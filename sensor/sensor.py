#!/usr/bin/env python

from lsm303d             import lsm303d
from lps25h              import lps25h
from l3gd20h             import l3gd20h
from ls20031             import ls20031
from kalman              import kalman
from numpy               import *
from threading           import Thread
from numpy.linalg.linalg import norm

import time
import pdb

############################################################

class sensor ( Thread ):

    def __init__( self ):
        Thread.__init__( self );
        self.time_start = time.time(  );

        ################################################
        # Sensors
        #######################
        self.acc = lsm303d(  );
        self.bar = lps25h (  );
        self.gps = ls20031(  );
        self.gyr = l3gd20h(  );
        #######################
        self.gyr.set_sample_rate(  );
        self.gps.start(  );
        ################################################

        ################################################
        # Kalman filter and temporal integration of gyro
        ##################
        self.dt      = 0.;
        self.g       = zeros( 3 ); # Grav vector
        self.g0      = zeros( 3 ); # Initial grav vector
        self.Rtheta0 = 0.;
        self.Rphi0   = 0.;
        self.kalman  = [ kalman( ) for _ in range( 3 ) ];
        #################
        self.d_gravity_threashold = 0.02;
        # In case that the deviation of the magnitude
        # of acceleration vector is greater than this,
        # the data from acclerometer will not
        # contribute to the Kalman filter.
        ################################################

        ################################################
        # V/S calculation
        #####################
        self.alti_old   = 0.;
        self.alti_old_t = 0.;
        ################################################

        ################################################
        # Deg <---> Rad conversions
        ###########################
        self.rad_to_deg = 180 / pi;
        self.deg_to_rad = pi / 180;
        ################################################

        ################################################
        # Boolean flags
        ###########################
        self.is_calibrated = False;
        self.is_to_break   = False;
        ################################################

        return;
    #

    def calib( self, dt = 10 ):
        print "Calibrating accelerometer and gyroscope..."

        i = 0;
        acc_dx = acc_dy = acc_dz = 0.;
        gyr_dx = gyr_dy = gyr_dz = 0.;

        start_t = time.time(  );
        while( time.time(  ) - start_t < dt ):
            i += 1;
            acc_x, acc_y, acc_z = self.acc.get_acc(  );
            gyr_x, gyr_y, gyr_z = self.gyr.get_gyr(  );
            acc_dx += acc_x;
            acc_dy += acc_y;
            acc_dz += acc_z;
            gyr_dx += gyr_x;
            gyr_dy += gyr_y;
            gyr_dz += gyr_z;
        #

        self.acc.acc_dx = acc_dx / i;
        self.acc.acc_dy = acc_dy / i;
        self.acc.acc_dz = acc_dz / i - 1.;
        self.g [ 2 ]    = 1.;
        self.g0[ 2 ]    = 1.;
            
        self.gyr.gyr_dx += gyr_dx / i;
        self.gyr.gyr_dy += gyr_dy / i;
        self.gyr.gyr_dz += gyr_dz / i;

        print "Calibration finished.";

        res_acc = array( [ self.acc.acc_dx, \
                           self.acc.acc_dy, \
                           self.acc.acc_dz ] );
        res_gyr = array( [ self.gyr.gyr_dx, \
                           self.gyr.gyr_dy, \
                           self.gyr.gyr_dz ] );
        res     = column_stack( ( res_acc, res_gyr ) );
        savetxt( 'calib.txt', res );
        
        self.is_calibrated = True;
        return;
    #

    def load_calib( self ):
        data = loadtxt( 'calib.txt' );
        self.acc.acc_dx, self.acc.acc_dy, self.acc.acc_dx \
            = data[ :, 0 ];
        self.gyr.gyr_dx, self.gyr.gyr_dy, self.gyr.gyr_dx \
            = data[ :, 1 ];

        self.g       = array( self.acc.get_acc(  ) );
        self.g0      = copy( self.g );
        self.g0_norm = norm( self.g );
        
        theta0, phi0 = self.rot_angle( self.g0 );
        print theta0 * self.rad_to_deg, \
            phi0 * self.rad_to_deg ;
        self.Rtheta0, self.Rphi0 \
            = self.rot_matrix( theta0, phi0 );
        return;
    #        

    def normalize( self, v ):
        return v / norm( v );
    #

    def integrate_gyro( self ):
        w_gyr = array( self.gyr.get_gyr(  ) ) \
                * self.deg_to_rad;
        g_acc = array( self.acc.get_acc(  ) );
        dg    = cross( self.g, w_gyr );

        is_to_suppress_acc                 \
            = norm( g_acc ) - self.g0_norm \
            > self.d_gravity_threashold;
        #
        
        for i in range( 3 ):
            if is_to_suppress_acc:
                self.kalman[ i ].y_innov_modulate = 0.;
                print 'Suppressed acc';
            else:
                self.kalman[ i ].y_innov_modulate = 1.;
            #
            res = self.kalman[ i ] \
                  ( dg[ i ], g_acc[ i ], self.dt );
            if not isnan( res ):
                self.g[ i ] = res;
            #
        #

        self.g = self.normalize( self.g );
        return;
    #

    def convert_g( self, g ):
        return self.Rtheta0 * self.Rphi0 * matrix( g ).T;
    #

    def rot_angle( self, g ):
        g_yz  =   sqrt( g[ 1 ]**2 + g[ 2 ]**2 );
        theta =   arctan2( g[ 0 ], g_yz   );
        phi   = - arctan2( g[ 1 ], g[ 2 ] );
        return theta, phi;
    #        
        
    def rot_matrix( self, theta, phi ):
        cphi           = cos( phi   );
        sphi           = sin( phi   );
        ctheta         = cos( theta );
        stheta         = sin( theta );
        Rphi           = matrix( zeros( ( 3, 3 ) ) );
        Rphi  [ 0, 0 ] =   1.;
        Rphi  [ 1, 1 ] =   cphi;
        Rphi  [ 2, 2 ] =   cphi;
        Rphi  [ 1, 2 ] =   sphi;
        Rphi  [ 2, 1 ] = - sphi;        
        Rtheta         = matrix( zeros( ( 3, 3 ) ) );
        Rtheta[ 1, 1 ] =   1.;
        Rtheta[ 0, 0 ] =   ctheta;
        Rtheta[ 2, 2 ] =   ctheta;
        Rtheta[ 0, 2 ] = - stheta;
        Rtheta[ 2, 0 ] =   stheta;

        return Rtheta, Rphi;
    #

    def get_hdg( self, Rtheta, Rphi ):
        b = matrix( self.acc.get_mag(  ) ).T;
        b = self.Rtheta0 * self.Rphi0 * Rtheta * Rphi * b;
        #
        bx  = b[ 0, 0 ];
        by  = b[ 1, 0 ];
        hdg = arctan2( by, bx );
        if hdg < 0:
            hdg += 2 * pi;
        #
        return hdg * self.rad_to_deg;        
    #                
        
    def get_val( self ):
        self.time = time.time(  ) - self.time_start;

        g_conv       = self.convert_g( self.g );
        theta, phi   = self.rot_angle( g_conv );
        Rtheta, Rphi = self.rot_matrix( theta, phi );

        self.pitch = theta * self.rad_to_deg;
        self.bank  = phi   * self.rad_to_deg;
        
        self.hdg      = self.get_hdg( Rtheta, Rphi );
        self.gs       = self.gps.gs;
        self.gps_alti = self.gps.altitude;
        #####################################
        # Warning: should convert to TRK(Mag)
        ############
        self.gps_trk  = self.gps.trkt;
        #####################################

        self.baro = self.bar.get_baro(  ) - 5.;
        self.temp = self.bar.get_temp(  );
        self.alti = self.gps_alti;

        return;
    #
        
    def run( self ):
        self.load_calib(  );
        new_time = time.time(  );
        while( True ):
            old_time = new_time;
            new_time = time.time(  );
            self.dt  = new_time - old_time;
            self.integrate_gyro(  );
            if self.is_to_break:
                break;
            #
        #
    #

    def kill( self ):
        self.gps.kill(  );
        self.is_to_break  = True;
    #
#

    def report( self ):
        return 'AUG:0.,' +               \
            'TIM:%g,' % self.time      + \
            'PIT:%g,' % self.pitch     + \
            'BAN:%g,' % self.bank      + \
            'BAR:%g,' % self.baro      + \
            'TMP:%g,' % self.temp      + \
            'HDG:%g,' % self.hdg       + \
            'GAL:%g,' % self.gps_alti  + \
            'GTR:%g,' % self.gps_trk   + \
            'GSP:%g,' % self.gs        + \
            'UAG:0.';
    #
#
    
if __name__=='__main__':
    s = sensor(  );
    s.start(  );

    try:
        while( True ):
            time.sleep( 0.2 );
            s.get_val(  );
            print s.report(  );
        #
    #
    except KeyboardInterrupt:
        s.kill(  );
    #
#
