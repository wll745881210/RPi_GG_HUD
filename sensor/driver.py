#!/usr/bin/env python

from button_led import *
from bt_client import bt_client
from sensor import sensor
import time

############################################################

indicator = led( gpio_num = 24 );
bt = bt_client(  );

class button_start_stop ( button ):
    def __init__( self, gpio_num ):
        button.__init__( self, gpio_num );
        return;
    #

    def short_press( self ):
        indicator.set_period_ratio( 0.1 )
        bt.start_bt(  );
        bt.start(  );
    #

    def long_press( self ):
        indicator.set_period_ratio( 0.0 );
        bt.kill(  );
    #
#

class button_pair_calib ( button ):
    def __init__( self, gpio_num ):
        button.__init__( self, gpio_num );
        return;
    #

    def short_press( self ):
        indicator.set_period_ratio( 0.5 );
        bt.pair_device(  );
        indicator.set_period_ratio( 0.0 );
    #

    def long_press( self ):
        indicator.set_period_ratio( 0.5 );
        s = sensor(  );
        s.calib(  );
        indicator.set_period_ratio( 0.0 );
    #
#

def main(  ):
    button1 = button_start_stop( 22 );
    button2 = button_start_stop( 22 );
    indicator.start(  );
    button1.start(  );
    button2.start(  );
    try:
        while( True ):
            time.sleep( 1000 );
        #
    except ( bt.btcommon.BluetoothError, \
             KeyboardInterrupt ):
        bt.kill(  );
    #
#

if __name__=='__main__':
    main(  );
#
        
        
