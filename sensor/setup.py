#!/usr/bin/env python

from distutils.core import setup, Extension
 
i2c = Extension( 'i2c', \
                 sources = [ 'i2c_python.cpp', \
                             'i2c_raw.cpp' ] );
 
setup ( name = 'PythonI2C',
        version = '0.1',
        description = 'Controlling I2C and more by python.',
        ext_modules = [ i2c ] );
