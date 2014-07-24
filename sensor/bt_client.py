#!/usr/bin/env python

import bluetooth as bt
from time import sleep
from sensor import sensor

# LG
# hostaddr = "C4:43:8F:97:08:F5";

# Google Glass
hostaddr = "F8:8F:CA:11:E9:59"

sock = bt.BluetoothSocket( bt.RFCOMM );
svc_dicts = bt.find_service\
            ( name = 'bthud', address = hostaddr );
port = svc_dicts[ 0 ][ 'port' ];

sock.connect( ( hostaddr, port ) );

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

s = sensor(  );
s.start(  );

try:
    while( True ):
        sleep( 0.1 );
        if not s.is_calibrated:
            continue;
        #
        s.get_val(  );
        report = s.report()
        print report;
        sock.send( report );
    #
except:
    s.kill;
#

s.kill(  );
sock.close(  );
print "Socket is closed."
