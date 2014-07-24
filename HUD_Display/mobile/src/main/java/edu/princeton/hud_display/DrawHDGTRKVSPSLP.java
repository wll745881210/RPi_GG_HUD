package edu.princeton.hud_display;

import android.graphics.Canvas;
import android.graphics.Paint;
import android.view.SurfaceHolder;

public class DrawHDGTRKVSPSLP
{
    private SurfaceHolder holder;
    public DrawHDGTRKVSPSLP(SurfaceHolder holder)
    {
        this.holder = holder;
    }

    private int hdg, trk, vsp;
    private float slp;
    public void set_hdg_trk_vsp_slp
            ( float hdg, float trk, float vsp, float slp )
    {
        this.hdg = ( int ) hdg;
        this.trk = ( int ) trk;
        this.vsp = ( int ) vsp;
        this.slp =         slp;
    }

    private void plot_frame(  )
    {
        paint.setStrokeWidth( 5.0f );
        float y_base = y_center + dy_frame_center;
        canvas.drawLine( x_center, y_base,
                x_center, y_base - 1.2f * frame_height,
                paint );


        paint.setTextAlign( Paint.Align.RIGHT );
        String trk_str = String.format( "TRK %03d", trk );
        canvas.drawText( trk_str,
                x_center - frame_width - 10, y_base, paint );

        paint.setTextAlign( Paint.Align.LEFT );
        String vsp_str = String.format( "V/S  %d", vsp );
        if( vsp > 0 )
            vsp_str = "+" + vsp_str;
        canvas.drawText( vsp_str, x_center + frame_width + 10,
                y_base, paint );

        y_base = y_center - dy_frame_center + 20;
        paint.setTextAlign( Paint.Align.LEFT );
        String slp_str = String.format( "ALTI %02.2f", slp );
        canvas.drawText( slp_str,
                x_center + frame_width + 10, y_base, paint );
    }

    private float frame_height, frame_width;
    private float dy_frame_center;
    private final float dx_hide_rule = 10.f;
    private void plot_single_rule
            ( float dx, boolean tick, int value )
    {
        if( Math.abs( dx ) > frame_width - dx_hide_rule )
            return;
        float y_base = y_center + dy_frame_center;
        float y_ext  = frame_height;
        if( ! tick )
            y_ext *= 0.618f;

        paint.setStrokeWidth( 1.0f );
        canvas.drawLine( x_center + dx, y_base,
                x_center + dx, y_base - y_ext, paint );
        if( tick )
        {
            paint.setTextAlign( Paint.Align.CENTER );
            String tick_str = String.format( "%03d", value );
            canvas.drawText( tick_str,
                    x_center + dx, y_base - y_ext, paint );
        }
    }

    private void plot_ruler( float spacing_const,
                             int center_value, int d_value,
                             int dn_tick )
    {
        int n_rules = 1 +
                ( int ) ( frame_width / spacing_const / d_value );

        for ( int i = -n_rules; i <= n_rules; ++ i )
        {
            int rule_value = d_value *
                    ( center_value / d_value + i );
            float dx = -spacing_const * ( rule_value - center_value );
            boolean is_tick = rule_value % ( d_value * dn_tick ) == 0
                    ? true : false;

            if( rule_value < 5 )
                rule_value += 360;
            else if( rule_value > 360 )
                rule_value -= 360;

            plot_single_rule( dx, is_tick, rule_value );
        }
    }

    private Canvas canvas;
    private Paint  paint;
    private float canvas_width, canvas_height;
    private float x_center, y_center;
    public void draw_hdg( Canvas canvas, Paint paint )
    {
        this.canvas = canvas;
        canvas_width  = canvas.getWidth(  );
        canvas_height = canvas.getHeight(  );
        frame_height    = canvas_height * 0.07f;
        frame_width     = canvas_width  * 0.22f;
        dy_frame_center = canvas_height * 0.5f;
        x_center = canvas_width  / 2;
        y_center = canvas_height / 2;
        this.paint = paint;

        plot_frame();
        float spacing_const = 7.f;
        int   d_value = 5;
        int   dn_tick = 2;
        plot_ruler( spacing_const, ( int ) hdg, d_value, dn_tick );
    }
}
