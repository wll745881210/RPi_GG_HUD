package edu.princeton.hud_display;

import android.os.Bundle;
import android.os.Handler;
import android.os.Message;

public class BluetoothMessageHandler extends Handler
{
    @Override
    public void handleMessage(Message msg)
    {
        super.handleMessage(msg);

        switch(msg.what)
        {
            case 738:
                Bundle bundle=msg.getData(  );
                System.out.println(bundle.get("add"));
                break;
        }
    }
}
