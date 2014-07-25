package edu.princeton.headupdisplay;

import android.app.Activity;
import android.content.Intent;
import android.os.Bundle;
import android.os.Handler;
import android.os.Message;
import android.util.Log;
import android.view.KeyEvent;
import android.view.Menu;
import android.view.MenuItem;
import android.view.SurfaceHolder;
import android.view.SurfaceView;
import android.view.Window;

import java.util.HashMap;
import java.util.Map;

public class HUD_Display extends Activity
{
    private DrawAll draw_all;

    private BluetoothReceiver bluetooth_recv = null;
    @Override
    public void onCreate( Bundle savedInstanceState )
    {
        super.onCreate( savedInstanceState );
        this.requestWindowFeature( Window.FEATURE_NO_TITLE );
        setContentView( R.layout.activity_hud );

        this.draw_all = new DrawAll( this );

        SurfaceView surface = ( SurfaceView )
                findViewById( R.id.surface );
        SurfaceHolder holder= surface.getHolder(  );
        holder.addCallback( draw_all );

        bluetooth_recv =
                new BluetoothReceiver( bt_broadcaster );
        bluetooth_recv.start();
    }

    private static final int menu_toggle_gps_alt =
            Menu.FIRST;
    private static final int menu_set_alti =
            Menu.FIRST + 1;
    @Override
    public boolean onCreateOptionsMenu( Menu menu )
    {
        super.onCreateOptionsMenu( menu );
        menu.add( 0, menu_toggle_gps_alt, 0,
                "Toggle GPS Alti" );
        menu.add( 0, menu_set_alti, 0,
                "Set Altimeter" );
        return true;
    }

    public static final int request_code_set_alti = 2992;
    @Override
    public boolean onOptionsItemSelected( MenuItem item )
    {
        super.onOptionsItemSelected( item );
        switch( item.getItemId(  ) )
        {
            case menu_toggle_gps_alt:
                data_process.toggle_gps_alti(  );
                break;
            case menu_set_alti:
                Intent set_alti = new Intent(  );
                set_alti.setClass( HUD_Display.this,
                        SetAltimeter.class );

                Bundle alti_info = new Bundle(  );
                alti_info.putFloat( "slp",
                        data_map.get( "SLP" ) );
                alti_info.putFloat( "bar",
                        data_map.get( "BAR" ) );
                alti_info.putFloat( "tmp",
                        data_map.get( "TMP" ) );
                set_alti.putExtras( alti_info );

                startActivityForResult( set_alti,
                        request_code_set_alti );
                break;
        }
        return true;
    }

    @Override
    public boolean onKeyDown(int keyCode, KeyEvent event)
    {
        if( keyCode == KeyEvent.KEYCODE_DPAD_CENTER )
        {
            openOptionsMenu();
            return true;
        }
        else if( keyCode == KeyEvent.KEYCODE_BACK )
        {
            finish();
        }
        return false;
    }

    @Override
    protected void onActivityResult
            ( int requestCode, int resultCode,
              Intent intent )
    {
        switch( requestCode )
        {
            case request_code_set_alti:
                Bundle alti_info = intent.getExtras();
                float slp = alti_info.getFloat( "slp" );
                data_map.put( "SLP", slp );
                break;
        }
    }

    private Map<String, Float> data_map
            = new HashMap<String, Float>(  );
    private DataProcess data_process
            = new DataProcess(  );
    private void process_plot(  )
    {
        data_map.put( "IAS", 120.f );
        data_map.put( "ALT", 7500.f );
        data_map.put( "TRK", 250f );
        data_map.put( "SLP", 29.92f );
        data_map.put( "VSP", 1200f );
        data_map.put( "BAR", 29.92f );
        data_map.put( "PIT", 7f );
        data_map.put( "BAN", -8f );
        draw_all.plot( data_map );
    }

    private Handler bt_broadcaster = new Handler(  )
    {
        @Override
        public void handleMessage(Message msg)
        {
            this.obtainMessage(  );
            switch( msg.what )
            {
                case 738:
                    Bundle bundle = msg.getData(  );
                    String s = bundle.getString( "bthud" );
                    parse_report( s );
                    process_plot();
                    break;
                case -1:
                    Log.e( "BTHUD", "Restarting" );
                    bluetooth_recv.shutdown_server();
                    bluetooth_recv = null;
                    bluetooth_recv = new BluetoothReceiver( this );
                    bluetooth_recv.start();
                    break;
            }
        }

        private void parse_report( String s )
        {
            String[ ] s_arr = s.split( "," );
            for( String s_sub : s_arr  )
            {
                String[ ] sub_arr = s_sub.split( ":" );
                String key = sub_arr[ 0 ];
                if( key.equals( "AUG" ) || key.equals( "UAG" ) )
                    continue;  // start or end

                float val;
                try
                {
                    val  = Float.parseFloat( sub_arr[ 1 ] );
                }
                catch( NumberFormatException e )
                {
                    val = 0.f;
                }
                data_map.put( key, val );
            }

        }
    };
}
