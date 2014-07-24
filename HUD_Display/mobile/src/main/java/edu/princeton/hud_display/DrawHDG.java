package edu.princeton.hud_display;

import android.graphics.Canvas;
import android.graphics.Paint;
import android.view.SurfaceHolder;

public class DrawHDG
{
    private SurfaceHolder holder;
    public DrawHDG(SurfaceHolder holder)
    {
        this.holder = holder;
    }

    private float hdg;
    public void set_hdg( float hdg )
    {
        this.hdg = hdg;
    }

    private void plot_frame(  )
    {
        paint.setStrokeWidth( 5.0f );
        float y_base = y_center + dy_frame_center;
        canvas.drawLine( x_center, y_base,
                x_center, y_base - 1.2f * frame_height,
                paint );
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
            canvas.drawText( Integer.toString( value ),
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
        frame_width     = canvas_width  * 0.25f;
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
