#lab 3 subscriber
import paho.mqtt.client as mqtt

# ----- Callbacks -----
def on_connect(client, userdata, flags, reason_code, properties):
    print("Connection returned result:", reason_code)
    # Subscribing in on_connect() means subscriptions are renewed after reconnect
    client.subscribe("ece180d/team5", qos=1)

def on_disconnect(client, userdata, rc, properties=None):
    if rc != 0:
        print("Unexpected Disconnect")
    else:
        print("Expected Disconnect")

def on_message(client, userdata, message):
    print(
        f'Received message: "{message.payload.decode()}" '
        f'on topic "{message.topic}" with QoS {message.qos}'
    )

# ----- Create and configure MQTT client -----
client = mqtt.Client(callback_api_version=mqtt.CallbackAPIVersion.VERSION2)

# Attach callback functions
client.on_connect = on_connect
client.on_disconnect = on_disconnect
client.on_message = on_message

# ----- Connect to broker -----
client.connect_async("test.mosquitto.org", 1883)

# Start the network loop
client.loop_forever()  # Keeps script running to receive messages