package edu.princeton.headupdisplay;

import android.content.Context;
import android.graphics.Canvas;
import android.graphics.Color;
import android.graphics.Paint;
import android.view.SurfaceView;
import android.view.SurfaceHolder;
import java.util.Map;

public class DrawAll extends SurfaceView
        implements SurfaceHolder.Callback
{
    public DrawAll(Context context)
    {
        super( context );
    }

    @Override
    public void surfaceChanged
            ( SurfaceHolder holder, int format,
              int width, int height )
    {

    }

    private SurfaceHolder holder;
    private DrawAttitude draw_attitude;
    private DrawSpeedAltitude draw_speed_altitude;
    private DrawHDGTRKVSPSLP draw_hdg_trk_vsp_slp;
    @Override
    public void surfaceCreated( SurfaceHolder holder )
    {
        this.holder = holder;
        draw_attitude        = new DrawAttitude( holder );
        draw_speed_altitude  = new DrawSpeedAltitude( holder );
        draw_hdg_trk_vsp_slp = new DrawHDGTRKVSPSLP( holder );
    }

    @Override
    public void surfaceDestroyed(SurfaceHolder holder)
    {

    }

    public void plot( Map<String, Float> data )
    {
        Canvas canvas = holder.lockCanvas(  );
        if( canvas == null )
            return;

        canvas.drawColor( Color.BLACK );
        Paint  paint  = new Paint(  );

        float original_text_size = ( Float ) paint.getTextSize(  );
        int scale = 2;
        paint.setTextSize( original_text_size * scale );

        if( Math.abs( data.get( "BAN" ) ) > 45 ||
                Math.abs( data.get( "PIT" ) ) > 30 ||
                Math.abs( data.get( "VSP" ) ) > 1500 )
            paint.setColor( Color.RED );
        else
            paint.setColor( Color.GREEN );

        draw_attitude.set_angles
                ( data.get( "BAN" ), data.get( "PIT" ) );
        draw_attitude.draw_attitude( canvas, paint );

        draw_speed_altitude.set_speed_altitude
                ( data.get( "GSP" ), data.get( "ALT" ) );
        draw_speed_altitude.draw_speed_altitude( canvas, paint );

        draw_hdg_trk_vsp_slp.set_all
                ( data.get( "HDG" ), data.get( "GTR" ),
                  data.get( "VSP" ), data.get( "SLP" ) );
        draw_hdg_trk_vsp_slp.draw_hdg( canvas, paint );

        holder.unlockCanvasAndPost( canvas );
    }
}
