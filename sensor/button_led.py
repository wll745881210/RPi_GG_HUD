#!/usr/bin/env python

import RPi.GPIO
import time
from threading  import Thread

############################################################

class button ( Thread ):
    def __init__( self, gpio_num ):
        self.n_gpio              = gpio_num;
        GPIO.setmode( GPIO.BCM );
        GPIO.setup( gpio_num, GPIO_IN, \
                    pull_up_down = GPIO.PUD_DOWN );
        self.is_to_break         = False;
        self.dt_long_press       = 3;
        return;
    #

    def run( self ):
        while( True ):
            if self.is_to_break:
                break;
            #
            GPIO.wait_for_edge( self.n_gpio, GPIO.RISING  );
            t0 = time.time(  );
            GPIO.wait_for_edge( self.n_gpio, GPIO.FALLING );
            dt = time.time(  ) - t0;

            if dt < self.dt_long_press:
                self.short_press(  );
            else:
                self.long_press(  );
            #
        #
    #
                
    def kill( self ):
        self.is_to_break = True;
    #
#


class led ( Thread ):
    def __init__( self, gpio_num ):
        self.n_gpio      = gpio_num;
        GPIO.setmode( GPIO.BCM );
        GPIO.setup( gpio_num, GPIO.OUT );
        self.on          = 0.;
        self.off         = 0.;
        self.is_to_break = False;
    #

    def run( self ):
        while( True ):
            if self.is_to_break:
                break;
            #
            GPIO.output( self.n_gpio, True );
            time.sleep( self.on );
            GPIO.output( self.n_gpio, False );
            time.sleep( self.off );
        #
    #

    def set_period_ratio( self, period, ratio ):
        self.on  = period * ratio;
        self.off = period * ( 1. - ratio );
    #

    def kill( self ):
        self.is_to_break = True;
    #
#
            
            
    
        
    