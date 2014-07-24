#!/usr/bin/env python

from lsm303d import lsm303d
from lps25h  import lps25h
from l3gd20h import l3gd20h
from ls20031 import ls20031
from time    import sleep

def altmu_test(  ):
    acc_mag = lsm303d(  );
    bar_tem = lps25h (  );
    gyro    = l3gd20h(  );
    gps     = ls20031(  );

    f_res = lambda title, x, y, z, m : title + ': ' \
            + '%4.2f %4.2f %4.2f norm %4.2f\n'      \
            % ( x, y, z, m );

    try:
        gps.start(  );
        while( True ):
            sleep( 0.2 );
            acc_x, acc_y, acc_z, acc_m = acc_mag.get_acc(  );
            mag_x, mag_y, mag_z, mag_m = acc_mag.get_mag(  );
            gyr_x, gyr_y, gyr_z, gyr_m = gyro   .get_gyr(  );

            temp = bar_tem.get_temp(  );
            baro = bar_tem.get_baro(  );

            res = f_res( 'Acc', acc_x,           \
                         acc_y, acc_z, acc_m ) + \
                f_res( 'Mag', mag_x,             \
                       mag_y, mag_z, mag_m ) +   \
                f_res( 'Gyr', gyr_x,             \
                       gyr_y, gyr_z, gyr_m ) +   \
                'Temp: %.2f\nBaro: %.2f\n'       \
                % ( temp, baro )             +   \
                'GPS: %g %g %g %g %g' \
                % ( gps.latitude, gps.longitude, \
                    gps.altitude, gps.gs, gps.trkt );
            print res;
    except KeyboardInterrupt:
        gps.kill(  );
    #
#

if __name__=='__main__':
    altmu_test(  );
#
