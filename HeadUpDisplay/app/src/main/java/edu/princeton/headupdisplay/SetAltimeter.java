package edu.princeton.headupdisplay;

import android.app.Activity;
import android.content.Context;
import android.content.Intent;
import android.os.Bundle;
import android.util.Log;
import android.view.KeyEvent;
import android.view.MotionEvent;
import android.widget.TextView;

import com.google.android.glass.touchpad.GestureDetector;

public class SetAltimeter extends Activity
{
    TextView text_alti_slp   = null;
    TextView text_field_alti = null;
    private GestureDetector gesture = null;
    private final float m_to_ft = 3.28f;
    private final float hpa_to_inHg = 0.0295333727f;
    @Override
    public void onCreate( Bundle savedInstanceState )
    {
        Log.i( "BTHUD", "SetAltimeter started." );
        super.onCreate(savedInstanceState);
        setContentView( R.layout.set_altimeter );
        text_alti_slp = ( TextView )
                findViewById( R.id.alti_slp );
        text_field_alti = ( TextView )
                findViewById( R.id.field_alti );

        slp = this.getIntent().getFloatExtra( "slp", 29.92f );
        tmp = this.getIntent().getFloatExtra( "tmp", 25.00f );
        bar = this.getIntent().getFloatExtra( "bar", 1013.25f )
                * hpa_to_inHg;

        slp_original = slp;
        show_data();

        gesture = create_gesture(this);
    }

    private float slp, bar, tmp, field_alti, slp_original;
    @Override
    public boolean onKeyDown(int keyCode, KeyEvent event)
    {
        Intent ret_slp = new Intent(  );
        if( keyCode == KeyEvent.KEYCODE_DPAD_CENTER )
            ret_slp.putExtra( "slp", slp );
        else if( keyCode == KeyEvent.KEYCODE_BACK )
            ret_slp.putExtra( "slp", slp_original );
        setResult( HUD_Display.request_code_set_alti, ret_slp );
        finish(  );
        return false;
    }

    public static float get_alti( float bar, float slp )
    {
        return ( slp - bar ) * 1000.f;
    }

    private void show_data(  )
    {
        field_alti = get_alti( bar, slp );
        String slp_str =
                String.format( "Altimeter: %02.2f inHg", slp );
        String field_alti_str =
                String.format( "Field Altitude: %02.0f ft",
                        field_alti );
        text_alti_slp.setText(slp_str);
        text_field_alti.setText( field_alti_str );
    }


    private GestureDetector create_gesture( Context context )
    {
        GestureDetector ret = new GestureDetector( context );
        GestureDetector.ScrollListener scroll = new
                GestureDetector.ScrollListener(  )
        {
            @Override
            public boolean onScroll( float x, float dx, float v )
            {
                slp += 2e-4 * dx;
                if( slp > 31.00f )
                    slp = 31.00f;
                else if( slp < 28.00f )
                    slp = 28.00f;

                show_data(  );
                return false;
            }
        };
        ret.setScrollListener( scroll );
        return ret;
    }

    @Override
    public boolean onGenericMotionEvent( MotionEvent event )
    {
        if( gesture != null )
            return gesture.onMotionEvent( event );
        return false;
    }
}
