#include <iostream>
#include <string>
#include <sstream>
#include <cmath>

#include <stdlib.h>
#include <fcntl.h>
#include <sys/ioctl.h>
#include <linux/i2c-dev.h>

#include "i2c_raw.h"

////////////////////////////////////////////////////////////
// Static variables

int i2c::io_handler = -1;

////////////////////////////////////////////////////////////
// Constructor and destructor

i2c::i2c(  )
{

}

i2c::~i2c(  )
{

}

////////////////////////////////////////////////////////////
// Init the device

void i2c::select_bus( int i2c_bus_code )
{
    // Select the I2C bus
    std::string dev_name;
    std::stringstream ss;
    
    ss << "/dev/i2c-" << i2c_bus_code;
    ss >> dev_name;

    io_handler = open( dev_name.c_str(  ), O_RDWR );
    if( io_handler < 0 )
    {
	dev_name = "Unable to open I2C bus: " + dev_name
		 + " (Hint: run with root)";
	throw dev_name.c_str(  );
    }

    return;
}

void i2c::select_device( byte dev_addr )
{
    this->dev_addr = dev_addr;
    switch_to_device(  );
    return;
}

////////////////////////////////////////////////////////////
// Registers read and write (raw)

void i2c::switch_to_device(  )
{
    // Taking over the control of I/O for specific device
    if( ioctl( io_handler, I2C_SLAVE, dev_addr ) < 0 )
	throw "Unable to select i2c.";
    return;
}

void i2c::write_reg( byte reg, byte val )
{
    switch_to_device(  );
    const int ret = i2c_smbus_write_byte_data
	( io_handler, reg, val );
    if( ret < 0 )
	throw "Unable to write to reg.";
    return;
}

void i2c::read_reg( byte reg, byte * block, byte size )
{
    // Black Magic, leave it here temporarily.
    reg = reg | 0x80;
    
    switch_to_device(  );
    const int ret  = i2c_smbus_read_i2c_block_data
	( io_handler, reg, size, block );
    if( ret != size )
	throw "Incorrect reading from reg.";
    return;
}

////////////////////////////////////////////////////////////
// Wrapped data reading interface

int i2c::read_bytes( byte reg, int size )
{
    if( size > sizeof( int ) )
	throw "Unable to read number: size too large.";
    
    byte b[ size ];	// "b" for "block"
    read_reg( reg, b, sizeof( b ) );

    const bool positive = ( ( b[ size - 1 ] >> 7 ) == 0 );
    long long int result( positive ? 0 : -1 );
	
    for( int i = size - 1; i >= 0; -- i )
    {
	result <<= 8;
	result |= b[ i ];
    }
    return result;
}
