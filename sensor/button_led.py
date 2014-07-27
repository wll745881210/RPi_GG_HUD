#!/usr/bin/env python

import RPi.GPIO as GPIO
import time
from threading  import Thread

############################################################
    
class button ( Thread ):
    def __init__( self, gpio_num ):
        Thread.__init__( self );
        self.n_gpio              = gpio_num;
        GPIO.setmode( GPIO.BCM );
        GPIO.setup( gpio_num, GPIO.IN, \
                    pull_up_down = GPIO.PUD_DOWN );
        self.is_to_break         = False;
        self.dt_long_press       = 3;
        self.dt_ultra_long_press = 6;
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

            print "Button " + str( self.n_gpio );

            if dt < self.dt_long_press:
                print "short pressed"
                self.short_press(  );
            elif dt < self.dt_ultra_long_press:
                print "long pressed"
                self.long_press(  );
            else:
                print "ultra-long pressed"
                self.ultra_long_press(  );
            #
        #
    #

    def ultra_long_press( self ):
        pass;
    #
                
    def kill( self ):
        self.is_to_break = True;
    #
#


class led ( Thread ):
    def __init__( self, gpio_num ):
        Thread.__init__( self );
        self.n_gpio      = gpio_num;
        GPIO.setmode( GPIO.BCM );
        GPIO.setup( gpio_num, GPIO.OUT );
        self.on          = 0.;
        self.off         = 0.1;
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

    def set_ratio_period( self, ratio, period = 1. ):
        self.on  = period * ratio;
        self.off = period * ( 1. - ratio );
    #

    def kill( self ):
        self.is_to_break = True;
    #
#
            
            
    
        
    