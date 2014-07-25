package edu.princeton.headupdisplay;

import android.util.Log;

public class DataProcess
{
    public void DataProcess(  )
    {

    }

    private boolean is_using_gps_alti = true;
    public void toggle_gps_alti(  )
    {
        is_using_gps_alti = ! is_using_gps_alti;
        Log.i("BTHUD", "Set gps alti "
                + Boolean.toString(is_using_gps_alti));
    }
    public boolean get_gps_alti_status(  )
    {
        return is_using_gps_alti;
    }

}
