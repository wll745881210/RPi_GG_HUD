#!/usr/bin/env python

import bluetooth as bt
from button_led import *
from bt_client import bt_client
from sensor import sensor
import subprocess
import time
import os

############################################################

indicator   = led( 24 );

class button_start_stop ( button ):
    def __init__( self, gpio_num ):
        button.__init__( self, gpio_num );
        self.bt_driver = bt_client(  );
        self.is_started = False;
        return;
    #

    def short_press( self ):
        if self.is_started:
            return;
        else:
            self.is_started = True;
        #
        try:
            self.bt_driver.start_bt(  );
            self.bt_driver.start(  );
            indicator.set_ratio_period( 0.1 )
        except:
            pass;
        #
            
        self.is_blocked = False;
    #

    def long_press( self ):
        try:
            self.bt_driver.kill(  );
            indicator.set_ratio_period( 0.0 );
        except:
            pass;
        #
        self.bt_driver = bt_client(  );
        self.is_started = False;
    #

    def ultra_long_press( self ):
        self.is_blocked = False;
        print "Shutting down...";
        subprocess.call( [ 'sudo', 'shutdown', '-h', 'now' ] )
    #
    
    def kill( self ):
        self.bt_driver.kill(  );
        self.is_to_exit = True;
        subprocess
    #
#

class button_pair_calib ( button ):
    def __init__( self, gpio_num ):
        button.__init__( self, gpio_num );
        self.is_blocked = False;
        self.is_to_exit = False;
        return;
    #

    def short_press( self ):
        if self.is_blocked:
            return;
        else:
            self.is_blocked = True;
        #
        try:
            indicator.set_ratio_period( 0.5 );
            print "Going to paring";
            bt_driver = bt_client(  );
            print bt_driver.pair_device(  );
        except:
            pass;
        #
        indicator.set_ratio_period( 0.0 );
        self.is_blocked = False;
    #

    def long_press( self ):
        if self.is_blocked:
            return;
        else:
            self.is_blocked = True;
        #
        try:
            indicator.set_ratio_period( 1. );
            s = sensor(  );
            s.calib(  );
        except:
            pass;
        #
        indicator.set_ratio_period( 0.0 );
        self.is_blocked = False;
    #

    def ultra_long_press( self ):
        self.is_to_exit = True;
        print "Exiting...";
    #
#

def main(  ):
    button1 = button_start_stop( 22 );
    button2 = button_pair_calib( 23 );
    indicator.start(  );
    button1.start(  );
    button2.start(  );
    try:
        while( True ):
            time.sleep( 1 );
            if button2.is_to_exit:
                break;
            #
        #
    except ( bt.btcommon.BluetoothError, \
             KeyboardInterrupt ):
        button1.kill(  );
        indicator.kill(  );
    #
#

if __name__=='__main__':
    main(  );
#
        
        
