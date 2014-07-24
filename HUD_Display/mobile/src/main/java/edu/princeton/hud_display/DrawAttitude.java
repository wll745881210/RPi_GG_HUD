package edu.princeton.hud_display;

import android.graphics.Canvas;
import android.graphics.DashPathEffect;
import android.graphics.Paint;
import android.view.SurfaceHolder;
import java.lang.Math;

public class DrawAttitude
{
    private SurfaceHolder holder;
    public DrawAttitude( SurfaceHolder holder )
    {
        this.holder = holder;
    }

    private float pitch,    bank;
    private float cos_bank, sin_bank, tan_bank;
    private final float deg_to_rad = 0.0174532925f;
    public void set_angles( float bank, float pitch )
    {
        this.pitch = pitch;
        this.bank  = bank;
        cos_bank = ( float ) Math.cos( bank * deg_to_rad );
        sin_bank = ( float ) Math.sin( bank * deg_to_rad );
        tan_bank = sin_bank / cos_bank;
    }

    private void plot_main_line(  )
    {
        paint.setStrokeWidth( 1.0f );
        canvas.drawLine( x_center - main_line_length, y_center,
                x_center + main_line_length, y_center, paint );
        paint.setStrokeWidth( 3.0f );

        float dh = pitch * pitch_shift_base;
        float y_left  = y_center + dh / cos_bank
                - main_line_length * tan_bank;
        float y_right = y_center + dh / cos_bank
                + main_line_length * tan_bank;
        canvas.drawLine( x_center - main_line_length, y_left,
                x_center + main_line_length, y_right, paint );
    }


    private final float pitch_shift_base = 10f;
    private final float aux_line_inner_frac = 0.1f;
    private final float aux_line_outer_frac = 0.5f;
    private void plot_single_aux_line( float offset_deg )
    {
        paint.setStrokeWidth( 1.0f );
        float l_outer = main_line_length * aux_line_outer_frac;
        float x_outer = cos_bank * l_outer;
        float y_outer = sin_bank * l_outer;

        float l_inner = main_line_length * aux_line_inner_frac;
        float x_inner = cos_bank * l_inner;
        float y_inner = sin_bank * l_inner;

        float dh = ( pitch - offset_deg ) * pitch_shift_base;
        float x_line_center = x_center - dh * sin_bank;
        float y_line_center = y_center + dh * cos_bank;
        if( y_line_center < 0 ||
                y_line_center > canvas_height ||
                x_line_center < x_center - main_line_length ||
                x_line_center > x_center + main_line_length )
            return;

        canvas.drawLine( x_line_center - x_outer,
                y_line_center - y_outer,
                x_line_center - x_inner,
                y_line_center - y_inner, paint );
        canvas.drawLine( x_line_center + x_outer,
                y_line_center + y_outer,
                x_line_center + x_inner,
                y_line_center + y_inner, paint );
        paint.setTextAlign( Paint.Align.LEFT );
        canvas.drawText( Integer.toString( ( int ) offset_deg ),
                x_line_center + x_outer,
                y_line_center + y_outer, paint );
    }

    private Canvas canvas;
    private Paint  paint;
    private float canvas_width, canvas_height;
    private float x_center, y_center;
    private float main_line_length;
    public void draw_attitude( Canvas canvas, Paint paint )
    {
        this.canvas = canvas;
        canvas_width  = canvas.getWidth(  );
        canvas_height = canvas.getHeight(  );
        x_center = canvas_width  / 2;
        y_center = canvas_height / 2;
        main_line_length = canvas_width * 0.21f;
        this.paint  = paint;
        plot_main_line();
        for( int i = -90; i <= 90; i += 5 )
        {
            if( i == 0 )
                continue;
            plot_single_aux_line( ( float ) i );
        }
    }
}
