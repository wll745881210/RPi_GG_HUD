package edu.princeton.hud_display;

import android.app.Activity;
import android.os.Bundle;
import android.os.Handler;
import android.os.Message;
import android.util.Log;
import android.view.SurfaceHolder;
import android.view.SurfaceView;

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

    private Map<String, Float> data_map
            = new HashMap<String, Float>(  );

    private void process_plot(  )
    {
        data_map.put( "IAS", 5.f );
        data_map.put( "ALT", 10.f );
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
