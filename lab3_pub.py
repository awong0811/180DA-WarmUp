#lab 3 publisher
import paho.mqtt.client as mqtt
import numpy as np

# ----- Callbacks -----
def on_connect(client, userdata, flags, reason_code, properties=None):
    print("Connection returned result:", reason_code)

def on_disconnect(client, userdata, disconnect_flags, reason_code, properties=None):
    if reason_code != 0:
        print('Unexpected Disconnect')
    else:
        print('Expected Disconnect')

def on_message(client, userdata, message):
    print(f'Received message: "{message.payload.decode()}" on topic "{message.topic}" with QoS {message.qos}')

# ----- Create and configure client -----
client = mqtt.Client(callback_api_version=mqtt.CallbackAPIVersion.VERSION2)

client.on_connect = on_connect
client.on_disconnect = on_disconnect
client.on_message = on_message

# Connect to public Mosquitto broker
client.connect_async("test.mosquitto.org", 1883)

# Start network loop
client.loop_start()

# Publish random values to a topic
for i in range(10):
    client.publish('ece180d/team5', np.random.random(), qos=1)

# Stop loop and disconnect
client.loop_stop()
client.disconnect()