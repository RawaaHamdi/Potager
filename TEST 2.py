import paho.mqtt.publish as publish
# Define the topic and message to publish
topic = "mon_tp"
message = "Hello, World!"
# Publish the message using the HiveMQ public broker
publish.single(topic, message, hostname="broker.hivemq.com")
