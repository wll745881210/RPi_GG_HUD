package edu.princeton.headupdisplay;

import android.util.Log;

import java.util.Map;

public class DataProcess
{
    public void DataProcess(  )
    {

    }

    private static boolean is_using_gps_alti = true;
    public void toggle_gps_alti(  )
    {
        is_using_gps_alti = ! is_using_gps_alti;
        Log.i("BTHUD", "Set gps alti "
                + Boolean.toString(is_using_gps_alti));
    }
    public static boolean get_gps_alti_status(  )
    {
        return is_using_gps_alti;
    }

    private Map<String, Float> data_map;
    public void set_data_map( Map<String, Float> data_map )
    {
        this.data_map = data_map;
    }

    private final float m_to_ft = 3.28f;
    private final float hpa_to_inHg = 0.0295333727f;
    private void set_altitude(  )
    {
        float alti;

        if( is_using_gps_alti )
        {
            alti = data_map.get("GAL") * m_to_ft;
        }
        else
        {
            float bar = data_map.get( "BAR" ) * hpa_to_inHg;
            float slp = data_map.get( "SLP" );
            alti = SetAltimeter.get_alti( bar, slp );
        }
        data_map.put( "ALT", alti );
    }

    private float t_old = 0.f;
    private float alt_old = 0.f;
    private void set_vs(  )
    {
        float t_new = data_map.get( "TIM" );
        float dt = t_new - t_old;
        if( dt < 0 )
            dt += 10.f;

        float alt_new = data_map.get( "ALT" );
        float dalt = alt_new - alt_old;

        int vs = ( int ) ( dalt / dt );
        vs = 10 * ( int ) ( vs / 10 );
        data_map.put( "VSP", ( float ) vs );
        alt_old = alt_new;
        t_old = t_new;
    }

    public void set_all(  )
    {
        set_altitude();
        set_vs();
    }
}
