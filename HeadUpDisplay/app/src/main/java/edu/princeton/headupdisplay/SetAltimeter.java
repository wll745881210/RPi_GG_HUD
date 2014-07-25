package edu.princeton.headupdisplay;

import android.app.Activity;
import android.content.Context;
import android.content.Intent;
import android.os.Bundle;
import android.util.Log;
import android.view.KeyEvent;
import android.view.MotionEvent;
import android.widget.TextView;

import com.google.android.glass.touchpad.Gesture;
import com.google.android.glass.touchpad.GestureDetector;

public class SetAltimeter extends Activity
{
    TextView text_alti_slp   = null;
    TextView text_field_alti = null;
    private GestureDetector gesture = null;
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

        Bundle alti_info = this.getIntent().getExtras();
        slp = alti_info.getFloat( "slp" );
        bar = alti_info.getFloat( "bar" );
        tmp = alti_info.getFloat( "tmp" );

        show_data();

        gesture = create_gesture(this);
    }

    private float slp, bar, tmp, field_alti;
    @Override
    public boolean onKeyDown(int keyCode, KeyEvent event)
    {
        switch( keyCode )
        {
            case KeyEvent.KEYCODE_DPAD_CENTER:
                Intent ret_slp = new Intent(  );
                Bundle alti_info = new Bundle(  );
                alti_info.putFloat( "slp", slp );
                ret_slp.putExtras( alti_info );
                setResult( HUD_Display.request_code_set_alti,
                        ret_slp );
            case KeyEvent.KEYCODE_BACK:
                finish(  );
        }
        return false;
    }

    private void get_alti(  )
    {
        float alt_std  = ( 1.f - ( float )
                Math.pow( bar / 29.92, -5.256 ) ) / 6.876e-6f;
        float alt_corr = 145442.2f *
                ( 1.f - ( float )
                        Math.pow( slp / 29.92, 0.190261 ) );
        field_alti = alt_std - alt_corr;
    }

    private void show_data(  )
    {
        get_alti(  );
        String slp_str =
                String.format( "Altimeter: %02.2f", slp );
        String field_alti_str =
                String.format( "Field Altitude: %02.0f",
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
                if( slp < 31.00 && slp > 28.00 )
                {
                    slp += 0.3 * dx;
                    show_data(  );
                }
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
