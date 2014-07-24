package edu.princeton.hud_display;

import android.graphics.Canvas;
import android.graphics.Paint;
import android.graphics.Path;
import android.view.SurfaceHolder;
import java.lang.Math;

public class DrawAttitude
{
    private SurfaceHolder holder;

    Path plot_region_path = new Path();
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

    private void plot_bank_frame_single
            ( float phi, float r_in, float r_out,
              float width )
    {
        paint.setStrokeWidth( width );
        float cos_phi = ( float ) Math.cos( - phi * deg_to_rad  );
        float sin_phi = ( float ) Math.sin( - phi * deg_to_rad  );
        float x_in    = x_center - r_in  * sin_phi;
        float y_in    = y_center - r_in  * cos_phi;
        float x_out   = x_center - r_out * sin_phi;
        float y_out   = y_center - r_out * cos_phi;
        canvas.drawLine( x_in, y_in, x_out, y_out, paint);
    }

    private void plot_bank(  )
    {
        final float w_frame       = 2.0f;
        final float w_indicator   = 6.0f;
        float r_in  = main_line_length * 1.12f;
        float r_out = main_line_length * 1.20f;
        float phi_arr[]
                = { 90.f, 60.f, 45.f, 30.f, 20.f, 10.f, 0.f };
        for( float phi : phi_arr )
        {
            plot_bank_frame_single(  phi, r_in, r_out, w_frame );
            plot_bank_frame_single( -phi, r_in, r_out, w_frame );
        }

        r_in  = main_line_length * 1.05f;
        r_out = main_line_length * 1.16f;
        plot_bank_frame_single( bank, r_in, r_out, w_indicator );
    }

    private Canvas canvas;
    private Paint  paint;
    private float canvas_width, canvas_height;
    private float x_center, y_center;
    private float main_line_length;

    public void draw_attitude( Canvas canvas, Paint paint )
    {
        this.canvas = canvas;
        this.paint  = paint;

        canvas_width  = canvas.getWidth(  );
        canvas_height = canvas.getHeight(  );
        x_center = canvas_width  / 2;
        y_center = canvas_height / 2;
        main_line_length = canvas_width * 0.18f;

        canvas.save();
        plot_region_path.reset();
        plot_region_path.addCircle
                ( x_center, y_center, main_line_length,
                        Path.Direction.CCW );
        canvas.clipPath( plot_region_path );

        plot_main_line();
        for( int i = -90; i <= 90; i += 5 )
        {
            if( i == 0 )
                continue;
            plot_single_aux_line( ( float ) i );
        }

        canvas.restore();
        plot_bank(  );
    }
}
