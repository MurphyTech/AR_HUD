package davidmurphy.io.dronecamx2;

import android.util.Log;

import org.eclipse.paho.client.mqttv3.MqttClient;
import org.eclipse.paho.client.mqttv3.MqttException;
import org.eclipse.paho.client.mqttv3.MqttMessage;
import org.eclipse.paho.client.mqttv3.persist.MemoryPersistence;

public class MqttPublisher {
  public static void main(String content) throws MqttException {
    //String messageString = "10.1,20.2";
    String messageString = content;

    Log.i("INFO", "===START PUBLISHER===");

    try {
      //MqttClient client = new MqttClient("tcp://192.168.1.103:1883", MqttClient.generateClientId(), new MemoryPersistence());
      MqttClient client = new MqttClient("tcp://10.0.2.2:1883", MqttClient.generateClientId(), new MemoryPersistence());
      Log.i("INFO", "Attempting connection");
      client.connect();

      MqttMessage message = new MqttMessage();

      message.setPayload(messageString.getBytes());
      Log.i("INFO", "Attempting Sending message");
      client.publish("servoEvent", message);

      Log.i("INFO","Message: " + messageString + "to #servoEvent'");
      client.disconnect();

    } catch (MqttException connectionException) {
      Log.e("Error", "Connection error!" + connectionException);
    }

    Log.i("INFO","===END PUBLISHER===");
  }
}
