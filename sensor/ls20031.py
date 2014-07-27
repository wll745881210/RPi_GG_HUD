#!/usr/bin/env python

from serial    import Serial
from datetime  import datetime
from time      import sleep
from threading import Thread

############################################################

class ls20031 ( Thread ):

    def __init__( self, baud = 57600 ):
        Thread.__init__( self );

        self.ser         = Serial( '/dev/ttyAMA0', baud );
        self.latitude    = 0.;
        self.longitude   = 0.;
        self.altitude    = 0.;
        self.utc         = 0.;
        self.gs          = 0.;
        self.trkt        = 0.;
        self.is_to_break = False;
        return;
    #

    def __parse_gga( self, line ):
        s_arr = line.split( ',' );
        # Latitude
        s_lat = s_arr[ 2 ];
        self.latitude = float( s_lat[ 0 : 2 ] ) \
                      + float( s_lat[ 2 :   ] ) / 60.;
        if 'S' in s_arr[ 3 ]:
            self.latititude *= -1;
        #
        # Longitude
        s_lon = s_arr[ 4 ];
        self.longitude = float( s_lon[ 0 : 3 ] ) \
                       + float( s_lon[ 3 :   ] ) / 60.;
        if 'W' in s_arr[ 5 ]:
            self.longitude *= -1;
        #
        # Altitude
        self.altitude = float( s_arr[ 9 ] );
        return;
    #

    def __parse_rmc( self, line ):
        s_arr = line.split( ',' );
        # UTC
        s_time    = s_arr[ 9 ] + s_arr[ 1 ];
        self.utc  = datetime.strptime \
                   ( s_time, '%d%m%y%H%M%S.%f' );
        # G/S
        self.gs   = float( s_arr[ 7 ] );
        # TRK_True
        self.trkt = float( s_arr[ 8 ] );
        return;
    #

    def parse_line( self, line ):
        try:
            if 'GGA' in line:
                self.__parse_gga( line );
            elif 'RMC' in line:
                self.__parse_rmc( line );
            #
        except:
            pass;
            # print 'Warning: Incorrect GPS data'
        #
        return;
    #

    def kill( self ):
        self.is_to_break = True;
    #

    def run( self ):
        while( True ):
            line = self.ser.readline(  );
            self.parse_line( line );
            if self.is_to_break:
                break;
            #
        #
    #
#
