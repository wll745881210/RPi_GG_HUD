#ifndef I2C_RAW_H_
#define I2C_RAW_H_

#include <stdint.h>
#include <stdio.h>

class i2c
{
    ////////// Initializer of class //////////
private:			// Type
    typedef uint8_t	byte;
public:				// Function
    i2c(  );
    ~i2c(  );

    ////////// Global handler //////////
private:			// Data
    static int io_handler;
    byte   dev_addr;

    ////////// Initialize the device //////////
public:				// Function
    static void select_bus( int i2c_bus_code = 1 );
    void select_device( byte dev_addr );

    ////////// Register R/W (raw) //////////
private:			// Function
    void switch_to_device(  );
    void read_reg( byte reg, byte * block, byte size );
public:				// Function
    void write_reg( byte reg, byte val );

    ////////// Data reading wrapper //////////
public:			// Function
    int read_bytes( byte reg, int size );
};

#endif
