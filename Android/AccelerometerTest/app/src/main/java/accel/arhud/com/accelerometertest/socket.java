package accel.arhud.com.accelerometertest;

import java.net.URISyntaxException;
import io.socket.client.IO;
import io.socket.client.Socket;

/**
 * Created by david on 06/03/18.
 */

public class socket {

    private Socket mSocket;
    {
        try{
            mSocket = IO.socket("http://192.168.0.31:8088");
        } catch (URISyntaxException e) {}
    }

    public Socket getSocket() {
        return mSocket;
    }
}
