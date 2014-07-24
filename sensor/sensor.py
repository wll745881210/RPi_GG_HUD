#!/usr/bin/env python

from lsm303d   import lsm303d
from lps25h    import lps25h
from l3gd20h   import l3gd20h
from ls20031   import ls20031
from kalman    import kalman
from numpy     import *
from threading import Thread

import time
import pdb

############################################################

class sensor ( Thread ):

    def __init__( self ):
        Thread.__init__( self );

        ################################################
        # Sensors
        #######################
        self.acc = lsm303d(  );
        self.bar = lps25h (  );
        self.gps = ls20031(  );
        self.gyr = l3gd20h(  );
        #######################
        self.gyr.set_sample_rate(  );
        # self.gps.start(  );
        ################################################

        ################################################
        # Kalman filter and temporal integration of gyro
        #################
        self.dt     = 0.;
        self.g      = zeros( 3 ); # Grav vector
        self.kalman = [ kalman( ) for _ in range( 3 ) ];
        #################
        self.d_gravity_threashold = 0.05;
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
        self.gps_base_altitude = 0.;

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

            self.gps_base_altitude += self.gps.altitude;
        #

        self.acc.acc_dx = acc_dx / i;
        self.acc.acc_dy = acc_dy / i;
        if acc_dz > 0:
            self.acc.acc_dz = acc_dz / i - 1.;
            self.g[ 2 ]     = +1.;
        else:
            self.acc.acc_dz = acc_dz / i + 1.;
            self.g[ 2 ]     = -1.;
        #
            
        self.gyr.gyr_dx += gyr_dx / i;
        self.gyr.gyr_dy += gyr_dy / i;
        self.gyr.gyr_dz += gyr_dz / i;

        self.gps_base_altitude /= i;

        print "Calibration finished.";
        self.is_calibrated = True;
        return;
    #

    #######################################################
    # Quaternion method. Unused for now.
    ####################################
    # def gyro_dq( self ):
    #     gyr_x, gyr_y, gyr_z = self.gyr.get_gyr(  );
    #     t         =   matrix( zeros( ( 4, 4 ) ) );
    #     t[ 0, 1 ] =   gyr_x;
    #     t[ 0, 2 ] =   gyr_y;
    #     t[ 0, 3 ] =   gyr_z;
    #     t[ 1, 2 ] = - gyr_z;
    #     t[ 1, 3 ] = - gyr_y;
    #     t[ 2, 3 ] = - gyr_x;
    #     t         = ( t - t.T ) * self.deg_to_rad;
    #     dq = -0.5 * t * matrix( self.q ).T;
    #     return array( dq ).flatten(  );
    # #
    # def euler_to_quater( self, phi, theta, psy ):
    #     cphi = cos( phi   / 2 );
    #     sphi = sin( phi   / 2 );
    #     cthe = cos( theta / 2 );
    #     sthe = sin( theta / 2 );
    #     cpsy = cos( psy   / 2 );
    #     spsy = sin( psy   / 2 );
    #     q = zeros( 4 );
    #     q[ 0 ] = cphi * cthe * cpsy + sphi * sthe * spsy;
    #     q[ 1 ] = sphi * cthe * cpsy - cphi * sthe * spsy;
    #     q[ 2 ] = cphi * sthe * cpsy + sphi * cthe * spsy;
    #     q[ 3 ] = cphi * cthe * spsy - sphi * sthe * cpsy;
    #     return q;
    # #
    # def quater_to_euler( self, q ):
    #     a     = q[ 0 ];
    #     b     = q[ 1 ];
    #     c     = q[ 2 ];
    #     d     = q[ 3 ];
    #     theta = - arcsin( 2 * ( b * d - a * c ) );
    #     if   abs( theta - pi / 2 ) < 1e-4:
    #         phi =  0.;
    #         psy =  2 * arctan2( b / a );
    #     elif abs( theta + pi / 2 ) < 1e-4:
    #         phi =  0.;
    #         psy = -2 * arctan2( b / a );
    #     else:
    #         phi = arctan2( 2 * ( a * b + c * d ), \
    #                        a**2 - b**2 - c**2 + d**2 );
    #         psy = arctan2( 2 * ( a * d + b * c ), \
    #                        a**2 + b**2 - c**2 - d**2 );
    #     #
    #     return phi, theta, psy;
    # #
    #######################################################

    def normalize( self, v ):
        return v / sqrt( dot( v, v ) );
    #

    def integrate_gyro( self ):
        w_gyr = array( self.gyr.get_gyr(  ) ) \
                * self.deg_to_rad;
        g_acc = array( self.acc.get_acc(  ) );
        dg    = cross( self.g, w_gyr );

        if abs( sqrt( dot( g_acc, g_acc ) ) - 1. ) > \
           self.d_gravity_threashold:
            kalman.y_innov_modulate = 0.;
        #
        
        for i in range( 3 ):
            res = self.kalman[ i ] \
                  ( dg[ i ], g_acc[ i ], self.dt );
            if not isnan( res ):
                self.g[ i ] = res;
            #
        #

        self.g = self.normalize( self.g );
        return;
    #

    def get_hdg( self, theta, phi ):
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
        
        b   = matrix( self.acc.get_mag(  ) ).T;
        b   = Rtheta * Rphi * b;
        bx  = b[ 0, 0 ];
        by  = b[ 1, 0 ];
        hdg = -arctan2( by, bx );
        if hdg < 0:
            hdg += 2 * pi;
        #
        return hdg * self.rad_to_deg;        
    #
                
        
    def get_val( self ):
        g_yz  =    sqrt( self.g[ 1 ]**2 + self.g[ 2 ]**2 );
        theta =   arctan2( self.g[ 0 ], g_yz        );
        phi   = - arctan2( self.g[ 1 ], self.g[ 2 ] );

        self.pitch = theta * self.rad_to_deg;
        self.bank  = phi   * self.rad_to_deg;
        
        self.hdg      = self.get_hdg( theta, phi );
        self.gs       = self.gps.gs;
        self.altitude = self.gps.altitude;

        # V/S calculation
        dt              = time.time(  ) - self.alti_old_t;
        da              = self.altitude - self.alti_old;
        self.vs         = da / dt;
        self.alti_old   = self.altitude;
        self.alti_old_t = time.time(  );

        # Fake values; need more corrections.
        self.trk  = self.gps.trkt;
        self.kias = self.gs;
        #
        return;
    #
        
    def run( self ):
        self.calib( 1 );

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
        self.is_to_break     = True;
        self.gps.is_to_break = True;
    #
#

def f_report( pitch, bank, kias, alti,
              vs, hdg, trk, gs ):
    return 'AUG:0.,' + \
        'PIT:%g,' % pitch + \
        'BAN:%g,' % bank  + \
        'IAS:%g,' % kias  + \
        'ALT:%g,' % alti  + \
        'VSP:%g,' % vs    + \
        'HDG:%g,' % hdg   + \
        'TRK:%g,' % trk   + \
        'GSP:%g,' % gs    + \
        'UAG:0.';
    #
#
    
if __name__=='__main__':
    s = sensor(  );
    s.start(  );
    # s.run(  );

    try:
        while( True ):
            time.sleep( 0.2 );
            if not s.is_calibrated:
                continue;
            #
            s.get_val(  );
            report = f_report\
                 ( s.pitch, s.bank, s.kias, s.altitude,
                   s.vs, s.hdg, s.trk, s.gs );
            print report;
    #
    except KeyboardInterrupt:
        s.kill(  );
    #
#
