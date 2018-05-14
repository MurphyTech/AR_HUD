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

import static java.lang.Math.abs;


public class MainActivity extends AppCompatActivity implements tiltPanSensor.TiltListener{

    private float latestPitch;
    private float latestRoll;

    private static final int DEFAULT_SENSOR_SAMPLING_PERIOD_US = SensorManager.SENSOR_DELAY_GAME;
    private int sensorSamplingPeriod;
    private Context mContext;

    public static EditText mInputMessageView;
    private Socket mSocket;

    public long lastUpdate = 0;
    //private SeekBar panSeekBar, tiltSeekBar;

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

        SeekBar panSeekBar=(SeekBar) findViewById(R.id.PanSeekBar);
        SeekBar tiltSeekBar=(SeekBar) findViewById(R.id.TiltSeekBar);

        panSeekBar.setOnSeekBarChangeListener(new OnSeekBarChangeListener() {
            int progressChangedValue = 0;

            public void onProgressChanged(SeekBar seekBar, int progress, boolean fromUser) {
                progressChangedValue = progress;
                mSocket.emit("servoPanEvent", progress);
                Log.d("PanSensor", "Porgress: " + progress);
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
                Log.d("TiltSensor", "Porgress: " + progress);
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
        long currentTime = System.currentTimeMillis();

        if ((currentTime-lastUpdate)>=100) {
            lastUpdate = currentTime;
            mSocket.emit("servoEvent", abs(yaw), abs(pitch));
            Log.d("Tiltupdate", "Pan: " + abs(yaw) + "\tTilt: " + abs(pitch));
        }
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
