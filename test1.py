import paho.mqtt.client as mqtt
# Define the callback function to handle incoming messages
def on_message(topic, payload,  length):
  print(f"Received message on topic {message.topic}: {message.payload.decode()}")
# Create a MQTT client object and set the callback function
client = mqtt.Client()
client.on_message = on_message
# Connect to the HiveMQ public broker and subscribe to the "mon_tp" topic
client.connect("broker.hivemq.com")
client.subscribe("mon_tp")
# Start the MQTT client loop to process incoming messages
client.loop_forever()
