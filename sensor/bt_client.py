#!/usr/bin/env python

import bluetooth as bt
from time       import sleep
from sensor     import sensor
from subprocess import Popen, PIPE
from threading  import Thread

import pdb

class bt_client:

    def __init__( self ):
        self.send_dt = 0.1;
        self.is_to_break = False;
        
        with open( 'bt_address.txt', 'r' ) as f:
            for line in f:
                self.hostaddr = line.rstrip();
            #
        #
        return;
    #

    def pair_device( self ):

        args = ['sudo', 'bluez-simple-agent', \
                'hci0', self.hostaddr ];

        p = Popen( args, stdout = PIPE, stdin = PIPE, \
                   stderr = PIPE );
        res = p.communicate( input = 'yes' );
        if 'AlreadyExists' in res[ 0 ]:
            args.append( 'remove' );
            p = Popen( args, stdout = PIPE, stdin = PIPE, \
                       stderr = PIPE );
            res = p.communicate( input = 'yes' );
        #

        return res;
    #

    def start_bt( self ):
        self.sock = bt.BluetoothSocket( bt.RFCOMM );
        svc_dicts = bt.find_service\
                    ( name = 'bthud', \
                      address = self.hostaddr );
        port = svc_dicts[ 0 ][ 'port' ];
        self.sock.connect( ( self.hostaddr, port ) );
        return;
    #

    def run( self ):
        self.s = sensor(  );
        self.s.start(  );
        try:
            while( True ):
                sleep( self.send_dt );
                self.s.get_val(  );
                report = self.s.report(  );
                print report;
                self.sock.send( report );
                if( self.is_to_break ):
                    break;
                #
            #
        except ( bt.btcommon.BluetoothError, \
                 KeyboardInterrupt ):
            self.kill(  );
        #
        return;
    #

    def kill( self ):
        self.s.kill(  );
        self.is_to_break = True;
        self.sock.close(  );
    #
#

if __name__=='__main__':
    a = bt_client();
    # a.pair_device();
    a.start_bt();
    a.run( );
#
    