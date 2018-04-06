package accel.arhud.com.accelerometertest;

import android.content.Context;
import android.hardware.SensorManager;
import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.util.Log;
import android.view.View;
import android.widget.EditText;
import android.widget.SeekBar;
import android.widget.SeekBar.OnSeekBarChangeListener;
import android.widget.Toast;


import io.socket.client.Socket;


public class MainActivity extends AppCompatActivity implements tiltPanSensor.TiltListener{

    private float latestPitch;
    private float latestRoll;

    private static final int DEFAULT_SENSOR_SAMPLING_PERIOD_US = SensorManager.SENSOR_DELAY_GAME;
    private int sensorSamplingPeriod;
    private Context mContext;

    public static EditText mInputMessageView;
    private Socket mSocket;
    private SeekBar panSeekBar, tiltSeekBar;

    protected tiltPanSensor sensor;


    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        sensorSamplingPeriod = DEFAULT_SENSOR_SAMPLING_PERIOD_US;

        mContext = this;
        initSensor();
        sensor.startTracking(sensorSamplingPeriod);


        socket appSocket = new socket();
        mSocket = appSocket.getSocket();
        mSocket.connect();



        mInputMessageView = (EditText) findViewById(R.id.message);
        mInputMessageView.setOnEditorActionListener(new DoneOnEditorActionListener());

        //SeekBar panSeekBar=(SeekBar) findViewById(R.id.PanSeekBar); // initiate the Seekbar
        //panSeekBar.setMax(150); // 150 maximum value for the Seek bar

        //SeekBar tiltSeekBar=(SeekBar) findViewById(R.id.TiltSeekBar); // initiate the Seekbar
        //tiltSeekBar.setMax(150); // 150 maximum value for the Seek bar

        SeekBar panSeekBar=(SeekBar) findViewById(R.id.PanSeekBar);
        SeekBar tiltSeekBar=(SeekBar) findViewById(R.id.TiltSeekBar);

        panSeekBar.setOnSeekBarChangeListener(new OnSeekBarChangeListener() {
            int progressChangedValue = 0;

            public void onProgressChanged(SeekBar seekBar, int progress, boolean fromUser) {
                progressChangedValue = progress;
                mSocket.emit("servoPanEvent", progress);
            }

            @Override
            public void onStartTrackingTouch(SeekBar seekBar) {

            }

            @Override
            public void onStopTrackingTouch(SeekBar seekBar) {

            }
        });

        tiltSeekBar.setOnSeekBarChangeListener(new SeekBar.OnSeekBarChangeListener() {
            int progressChangedValue = 0;

            public void onProgressChanged(SeekBar seekBar, int progress, boolean fromUser) {
                progressChangedValue = progress;
                mSocket.emit("servoTiltEvent", progress);
            }

            @Override
            public void onStartTrackingTouch(SeekBar seekBar) {
                Toast.makeText(getApplicationContext(), "Started tracking seekbar", Toast.LENGTH_SHORT).show();
            }

            @Override
            public void onStopTrackingTouch(SeekBar seekBar) {
                Toast.makeText(getApplicationContext(), "Stopped tracking seekbar", Toast.LENGTH_SHORT).show();
            }
        });



        Log.d("CREATION", "MainActivity - onCreate()");
    }



    @Override
    public void onTiltUpdate(float yaw, float pitch, float roll) {
        this.latestPitch = pitch;
        this.latestRoll = roll;
        mSocket.emit("servoEvent", pitch, roll);
        Log.d("Tiltupdate", "Pitch: " + pitch + "\tRoll: " + roll);
    }

    private void initSensor() {
        sensor = new tiltPanSensor(mContext, orientationMode == OrientationMode.RELATIVE);
        sensor.addListener(this);
    }

    /**
     * Determines the basis in which device orientation is measured.
     */
    public enum OrientationMode {
        /**
         * Measures absolute yaw / pitch / roll (i.e. relative to the world).
         */
        ABSOLUTE,
        /**
         * Measures yaw / pitch / roll relative to the starting orientation.
         * The starting orientation is determined upon receiving the first sensor data,
         * but can be manually reset at any time using {@link #resetOrientationOrigin(boolean)}.
         */
        RELATIVE
    }

    private static final OrientationMode DEFAULT_ORIENTATION_MODE = OrientationMode.RELATIVE;
    private OrientationMode orientationMode;


}
