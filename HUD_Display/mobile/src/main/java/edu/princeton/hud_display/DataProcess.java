package edu.princeton.hud_display;

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

    private float sea_level_pressue = 29.92f;
    public void set_sea_level_pressue
            ( float sea_level_pressue )
    {
        this.sea_level_pressue = sea_level_pressue;
        Log.i( "BTHUD", "Set sea level pressure "
                + Float.toString( sea_level_pressue ) );
    }

}
