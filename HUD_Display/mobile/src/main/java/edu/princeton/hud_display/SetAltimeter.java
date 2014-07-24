package edu.princeton.hud_display;

import android.app.Activity;
import android.os.Bundle;
import android.util.Log;
import android.view.KeyEvent;

public class SetAltimeter extends Activity
{
    @Override
    public void onCreate( Bundle savedInstanceState )
    {
        super.onCreate( savedInstanceState );
        In
    }


    @Override
    public boolean onKeyDown(int keyCode, KeyEvent event)
    {
        switch( keyCode )
        {
            case KeyEvent.KEYCODE_DPAD_CENTER:
                Log.i("BTHUD", "Selected");
            case KeyEvent.KEYCODE_BACK:
                finish(  );
        }
        return false;
    }
}
