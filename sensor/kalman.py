#!/usr/bin/env python

from numpy import *

############################################################

class kalman:
    y_innov_modulate = 1.;

    def __init__( self ):

        ##########################################
        # Status vector and covar matrix
        ##############################
        self.x = matrix( ( 0, 0 ) ).T;
        self.p = matrix( zeros( ( 2, 2 ) ) );
        ##########################################        

        ##########################################
        # Parameters for the filter
        ##############
        self.r = 0.003;
        self.q = matrix( diag( ( 0.001, 0.003 ) ) );
        ##########################################
        
        return;
    #

    def __call__( self, dx_gyro, x_acc, dt ):
        f         = matrix( diag( ( 1, 1 ) ) );
        f[ 0, 1 ] = - dt;
        b         = matrix( ( dt, 0 ) ).T;
        x_priori  = f * self.x + b * dx_gyro;
        p_priori  = f * self.p * f.T + self.q * dt;
        y_innov   = x_acc - x_priori[ 0, 0 ];
        s_innov   = p_priori[ 0, 0 ] + self.r;
        k_kalman  = p_priori[ :, 0 ] / s_innov;
        self.x    = x_priori + y_innov * k_kalman \
                    * self.y_innov_modulate;
        self.p    = p_priori - k_kalman * p_priori[ 0, : ];

        self.y_innov_modulate = 1.;
        return self.x[ 0, 0 ];
    #
#