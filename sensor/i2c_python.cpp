#include <Python.h>

#include <vector>
#include <iostream>
#include "i2c_raw.h"

static std::vector<i2c *> sensor_list;

static PyObject * i2c_init
( PyObject * self, PyObject * args )
{
    int i2c_bus( 1 ), dev_addr( 0 );

    const bool is_parse_args_successful
	= PyArg_ParseTuple( args, "ii", & i2c_bus,
			    & dev_addr );
    if( ! is_parse_args_successful )
	return NULL;
    
    try
    {
	i2c * new_sensor = new i2c;
	new_sensor->select_bus( i2c_bus );
	new_sensor->select_device( dev_addr );
	sensor_list.push_back( new_sensor );
    }
    catch( const char * err )
    {
	std::cerr << "Error: " << err << std::endl;
	return NULL;
    }

    int sensor_idx = sensor_list.size(  ) - 1;
    return Py_BuildValue( "i", sensor_idx );
}

static PyObject * i2c_write_reg
( PyObject * self, PyObject * args )
{
    int sensor_idx( 0 ), reg( 0 ), value( 0 );
    
    const bool is_parse_args_successful
    	= PyArg_ParseTuple( args, "iii", & sensor_idx,
    			    & reg, & value );
    if( ! is_parse_args_successful )
    	return NULL;

    try
    {
    	i2c * sensor = sensor_list.at( sensor_idx );
    	if( sensor == NULL )
    	    throw "Null sensor pointer.";

    	sensor->write_reg( reg, value );
    }
    catch( const char * err )
    {
    	std::cerr << "Error: " << err << std::endl;
    	return NULL;
    }

    Py_INCREF( Py_None );
    return Py_None;
}

static PyObject * i2c_read
( PyObject * self, PyObject * args )
{
    int sensor_idx( -1 ), reg( 0 ), size( 0 );

    const bool is_parse_args_successful
	= PyArg_ParseTuple( args, "iii", & sensor_idx,
			    & reg,  & size );
    if( ! is_parse_args_successful )
	return NULL;

    int result( 0 );
    try
    {
	i2c * sensor = sensor_list.at( sensor_idx );
	if( sensor == NULL )
	    throw "Null sensor pointer.";

	result = sensor->read_bytes( reg, size );
    }
    catch( const char * err )
    {
	std::cerr << "Error: " << err << std::endl;
	return NULL;
    }

    return Py_BuildValue( "i", result );
}

static PyObject * i2c_destruct
( PyObject * self, PyObject * args )
{
    int sensor_idx( -1 );

    const bool is_parse_args_successful
	= PyArg_ParseTuple( args, "i", & sensor_idx );
    if( ! is_parse_args_successful )
	return NULL;

    try
    {
	i2c * sensor = sensor_list.at( sensor_idx );
	if( sensor != NULL )
	    delete sensor;
	sensor_list.at( sensor_idx ) = NULL;
    }
    catch( const char * err )
    {
	std::cerr << "Error: " << err << std::endl;
	return NULL;
    }

    Py_INCREF( Py_None );
    return Py_None;
}

static PyMethodDef I2cMethods[  ] =
{
    {
	"init", i2c_init, METH_VARARGS,
	"Initlialize single sensor."
    },

    {
    	"write_reg", i2c_write_reg, METH_VARARGS,
    	"Write to registers."
    },

    {
    	"read", i2c_read, METH_VARARGS,
    	"Read from registers."
    },

    {
    	"destruct", i2c_destruct, METH_VARARGS,
    	"Close the connection to the registers."
    },

    { NULL, NULL, 0, NULL }
};

PyMODINIT_FUNC initi2c( void )
{
     ( void ) Py_InitModule( "i2c", I2cMethods );
}
