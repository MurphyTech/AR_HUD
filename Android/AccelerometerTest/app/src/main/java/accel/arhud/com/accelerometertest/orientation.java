package accel.arhud.com.accelerometertest;

import android.content.Context;
import android.hardware.Sensor;
import android.hardware.SensorEvent;
import android.hardware.SensorEventListener;
import android.hardware.SensorManager;
import android.os.Bundle;
import android.support.v7.app.AppCompatActivity;
import android.util.Log;
import android.widget.EditText;
import android.widget.TextView;

import java.util.ArrayList;

/**
 * Created by david on 07/03/18.
 */

public class orientation extends AppCompatActivity implements SensorEventListener {

    private SensorManager sensorManager;
    //private boolean started = false;
    private ArrayList sensorData = new ArrayList(1000);
    private Sensor sensorAccel;
    private Sensor sensorMagnetometer;
    private TextView rawData, Azimuth, Pitch, Roll, DataLength;

    //private double PI;
    private float averagePitch = 0;
    private float averageRoll = 0;

    private float[] pitches;
    private float[] rolls;

    int smoothness = 10;


    private double avgX, avgY, avgZ;
    private double sumX, sumY, sumZ;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        /**
         * IS THIS RIGHT???
         */
        setContentView(R.layout.activity_main);
        pitches = new float[smoothness];
        rolls = new float[smoothness];

        rawData = findViewById(R.id.textview1);
        DataLength = findViewById(R.id.DataLength);

        Azimuth = findViewById(R.id.Azimuth);
        Pitch = findViewById(R.id.Pitch);
        Roll = findViewById(R.id.Roll);



        sensorManager = (SensorManager) getSystemService(Context.SENSOR_SERVICE);
        sensorData = new ArrayList();
        sensorAccel = sensorManager.getDefaultSensor(Sensor.TYPE_ACCELEROMETER);
        sensorMagnetometer = sensorManager.getDefaultSensor(Sensor.TYPE_MAGNETIC_FIELD);
        sensorManager.registerListener(this, sensorAccel, SensorManager.SENSOR_DELAY_FASTEST);
        Log.d("CREATION", "Orientation - onCreate()");
    }

    @Override
    protected void onResume() {
        super.onResume();
        sensorManager.registerListener(this, sensorAccel, sensorManager.SENSOR_DELAY_NORMAL );
        sensorManager.registerListener(this, sensorMagnetometer, sensorManager.SENSOR_DELAY_NORMAL );
    }

    @Override
    protected void onPause() {
        super.onPause();
        sensorManager.unregisterListener(this);
    }

    @Override
    public void onAccuracyChanged(Sensor sensor, int accuracy) {

    }

    float[] mGravity;
    float[] mGeomagnetic;

    @Override
    public void onSensorChanged(SensorEvent event) {
        Sensor mySensor = event.sensor;

        if (mySensor.getType() == Sensor.TYPE_ACCELEROMETER) {
            mGravity = event.values;
            double x = mGravity[0];
            double y = mGravity[1];
            double z = mGravity[2];

            long timestamp = System.currentTimeMillis();
            AccelData data = new AccelData(timestamp, x, y, z);
            if (sensorData.size() >= 1000) {
                for (int i = 1; i == (sensorData.size()-1); i++){
                    sensorData.set(i, sensorData.get(i-1));
                    Log.d("ArrayList", "Suffle.....");
                }
                //Suffle arraydata.toString()
                sensorData.set(sensorData.size()-1, data);

                for (int i = 0; i == (sensorData.size()-1); i++ ){
                    sumX += mGravity[0];
                    sumY += mGravity[1];
                    sumZ += mGravity[2];
                }
                avgX = sumX/(sensorData.size()-1);
                avgY = sumY/(sensorData.size()-1);
                avgZ = sumZ/(sensorData.size()-1);
                Log.d("ArrayList", "Averaged - 'IF'>>>>");
            }
            else {
                sensorData.add(data);
                for (int i = 0; i == (sensorData.size()-1); i++ ){
                    sumX += mGravity[0];
                    sumY += mGravity[1];
                    sumZ += mGravity[2];
                }
                avgX = sumX/(sensorData.size()-1);
                avgY = sumY/(sensorData.size()-1);
                avgZ = sumZ/(sensorData.size()-1);
                Log.d("ArrayList", "Averaged - 'ELSE'>>>>");

            }

            Log.d("SENSOR", "Sensor value updated");
            Log.d("SENSOR", "Data: " + data.toString());
            rawData.setText("avgX: " + avgX + "\n" +
                    "avgY: " + avgY + "\n" +
                    "avgZ: " + avgZ + "\n");
            System.out.print("Data: " + "X: " + x + "Y: " + y + "Z: " + z);
        }

        if (mySensor.getType() == Sensor.TYPE_MAGNETIC_FIELD) {
            mGeomagnetic = event.values;
        }


        if (mGravity != null && mGeomagnetic != null) {
            float RotationMatrix[] = new float[9];
            float InclinationMatrix[] = new float[9];
            boolean success = sensorManager.getRotationMatrix(RotationMatrix, InclinationMatrix, mGravity, mGeomagnetic);
            if (success){
                float orientation[] = new float[3];
                sensorManager.getOrientation(RotationMatrix, orientation);


                averagePitch = addValue(orientation[1], pitches);
                averageRoll = addValue(orientation[2], rolls);

                Azimuth.setText("Azimuth: " + orientation[0]);
                Pitch.setText("Pitch: " + averagePitch);
                Roll.setText("Roll: " + (float) Math.round((Math.toDegrees(orientation[2]))));
                Log.d("AvgData", "Azimuth: " + orientation[0] + " Pitch: " + averagePitch + " Roll: " + averageRoll);

                System.out.print("Azimuth: " + orientation[0] + " Pitch: " + averagePitch + " Roll: " + averageRoll);
            }
        }

        DataLength.setText("Length: " + sensorData.size());
    }

    private float addValue(float value, float[] values) {
        value = (float) Math.round((Math.toDegrees(value)));
        float average = 0;
        for (int i = 1; i < smoothness; i++) {
            values[i - 1] = values[i];
            average += values[i];
        }
        values[smoothness - 1] = value;
        average = (average + value) / smoothness;
        return average;
    }

}
