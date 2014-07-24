package edu.princeton.hud_display;

import android.graphics.Canvas;
import android.graphics.Paint;
import android.view.SurfaceHolder;

public class DrawSpeedAltitude
{
    private SurfaceHolder holder;
    public DrawSpeedAltitude(SurfaceHolder holder)
    {
        this.holder = holder;
    }

    private float kias, altitude;
    public void set_speed_altitude( float kias, float altitude )
    {
        this.kias = kias;
        this.altitude = altitude;
    }

    private float frame_height, frame_width;
    private float dx_frame_center;
    private void plot_frame(  )
    {
        paint.setStrokeWidth( 2.0f );
        canvas.drawLine( x_center - dx_frame_center,
                y_center - frame_height,
                x_center - dx_frame_center,
                y_center + frame_height,
                paint );
        canvas.drawLine( x_center + dx_frame_center,
                y_center - frame_height,
                x_center + dx_frame_center,
                y_center + frame_height,
                paint );

        canvas.drawLine( x_center - dx_frame_center,
                y_center - frame_height,
                x_center - dx_frame_center - frame_width,
                y_center - frame_height,
                paint );
        canvas.drawLine( x_center - dx_frame_center,
                y_center + frame_height,
                x_center - dx_frame_center - frame_width,
                y_center + frame_height,
                paint );

        canvas.drawLine( x_center + dx_frame_center,
                y_center - frame_height,
                x_center + dx_frame_center + frame_width,
                y_center - frame_height,
                paint );
        canvas.drawLine( x_center + dx_frame_center,
                y_center + frame_height,
                x_center + dx_frame_center + frame_width,
                y_center + frame_height,
                paint );

        canvas.drawLine( x_center + dx_frame_center, y_center,
                x_center + dx_frame_center - 30, y_center,
                paint );
        canvas.drawLine( x_center - dx_frame_center, y_center,
                x_center - dx_frame_center + 30, y_center,
                paint );
    }

    private final float dh_hide_rule = 10.f;
    private void plot_single_rule( int lr_sign, float dy,
                                   boolean tick, int value )
    {
        if( Math.abs( dy ) > frame_height - dh_hide_rule )
            return;
        float x_base = x_center + lr_sign * dx_frame_center;
        float x_ext  = lr_sign * frame_width;
        if( ! tick )
            x_ext *= 0.618f;

        paint.setStrokeWidth( 1.0f );
        canvas.drawLine( x_base, y_center + dy,
                x_base + x_ext, y_center + dy, paint );
        if( tick )
        {
            if( lr_sign < 0 )
                paint.setTextAlign(Paint.Align.LEFT);
            else
                paint.setTextAlign(Paint.Align.RIGHT);
            canvas.drawText( Integer.toString( value ),
                    x_base + x_ext, y_center + dy, paint );
        }
    }

    private void plot_ruler( int lr_sign, float spacing_const,
                             int center_value, int d_value,
                             int dn_tick )
    {
        int n_rules = 1 +
                ( int ) ( frame_height / spacing_const / d_value );

        for ( int i = -n_rules; i <= n_rules; ++ i )
        {
            int rule_value = d_value *
                    ( center_value / d_value + i );
            float dy = -spacing_const * ( rule_value - center_value );

            boolean is_tick = rule_value % ( d_value * dn_tick ) == 0
                    ? true : false;
            plot_single_rule( lr_sign, dy, is_tick, rule_value );
        }
        if( lr_sign < 0 )
            paint.setTextAlign(Paint.Align.LEFT);
        else
            paint.setTextAlign(Paint.Align.RIGHT);

        float value_x_base = x_center + lr_sign * ( dx_frame_center - 5 );

        canvas.drawText( Integer.toString( center_value ),
                value_x_base, y_center - 5, paint );
    }

    private Canvas canvas;
    private Paint  paint;
    private float canvas_width, canvas_height;
    private float x_center, y_center;
    public void draw_speed_altitude( Canvas canvas, Paint paint )
    {
        this.canvas = canvas;
        canvas_width  = canvas.getWidth(  );
        canvas_height = canvas.getHeight(  );
        frame_height    = canvas_height * 0.4f;
        frame_width     = canvas_width  * 0.1f;
        dx_frame_center = canvas_width  * 0.35f;
        x_center = canvas_width  / 2;
        y_center = canvas_height / 2;
        this.paint = paint;

        plot_frame();
        float kias_spacing_const = 7.f;
        int   kias_d_value = 5;
        int   kias_dn_tick = 2;
        plot_ruler( -1, kias_spacing_const, ( int ) kias,
                kias_d_value, kias_dn_tick );

        float alti_spacing_const = .7f;
        int   alti_d_value = 50;
        int   alti_dn_tick = 2;
        plot_ruler(  1, alti_spacing_const, ( int ) altitude,
                alti_d_value, alti_dn_tick );

    }
}
