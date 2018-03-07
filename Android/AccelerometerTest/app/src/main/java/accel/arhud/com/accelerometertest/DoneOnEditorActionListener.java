package accel.arhud.com.accelerometertest;

import android.text.TextUtils;
import android.util.Log;
import android.view.KeyEvent;
import android.view.inputmethod.EditorInfo;
import android.widget.TextView;
import io.socket.client.Socket;

/**
 * Created by david on 07/03/18.
 */

public class DoneOnEditorActionListener implements TextView.OnEditorActionListener{
    private Socket mSocket;

    @Override
    public boolean onEditorAction(TextView v, int actionId, KeyEvent event) {
        boolean handled = false;
        if (actionId == EditorInfo.IME_ACTION_SEND || actionId == EditorInfo.IME_ACTION_GO
                || actionId == EditorInfo.IME_ACTION_DONE
                || actionId == EditorInfo.IME_ACTION_NEXT) {
            /**
             * attemptSend();
             * NEED TO FIX THIS....
             */

            socket appSocket = new socket();
            mSocket = appSocket.getSocket();
            mSocket.connect();

            attemptSend();
            orientation.mInputMessageView.setText("");
            handled = true;
            Log.d("SOCKET", "Message Sent");
        }
        return handled;
    }
    protected void attemptSend() {
        String message = orientation.mInputMessageView.getText().toString().trim();
        if (TextUtils.isEmpty(message)) {
            return;
        }

        mSocket.emit("servoEvent", message);
    }


    //@Override
    //public void onDestroy() {
    //    super.onDestroy();
    //    mSocket.disconnect();
    //}
}