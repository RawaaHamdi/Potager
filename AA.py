Python 3.12.2 (tags/v3.12.2:6abddd9, Feb  6 2024, 21:26:36) [MSC v.1937 64 bit (AMD64)] on win32
Type "help", "copyright", "credits" or "license()" for more information.
>>> import paho.mqtt.publish as publish
... # Define the topic and message to publish
... topic = "AA"
... message = "Hello, World!"
... # Publish the message using the HiveMQ public broker
publish.single(topic, message, hostname="broker.hivemq.com")
