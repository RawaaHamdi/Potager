import tkinter as tk
import paho.mqtt.publish as publish
import paho.mqtt.client as mqtt

def publish_message():
    # Get values from textboxes
    topic = topic_entry.get()
    message = message_entry.get()
    host = host_entry.get()

    # Publish the message using the HiveMQ public broker
    publish.single(topic, message, hostname=host)

def on_subscribe(client, userdata, mid, granted_qos):
    print("Subscribed with QoS", granted_qos[0])

def on_message(client, userdata, msg):
    received_message.set(msg.payload.decode("utf-8"))

def subscribe_topic():
    subscribe_topic = subscribe_entry.get()
    subscribe_client.subscribe(subscribe_topic)

# Create main window
window = tk.Tk()
window.title("MQTT Publisher and Subscriber")

# Create widgets for publishing
topic_label = tk.Label(window, text="Enter the topic:")
topic_entry = tk.Entry(window)
topic_entry.insert(0, "Hala")  # Default value

message_label = tk.Label(window, text="Enter the message:")
message_entry = tk.Entry(window)
message_entry.insert(0, "on")  # Default value

host_label = tk.Label(window, text="Enter the host adrs:")
host_entry = tk.Entry(window)
host_entry.insert(0, "broker.hivemq.com")  # Default value

publish_button = tk.Button(window, text="Publish", command=publish_message)

# Create widgets for subscribing
subscribe_label = tk.Label(window, text="Enter the topic to subscribe:")
subscribe_entry = tk.Entry(window)
subscribe_entry.insert(0, "Holo")  # Default value

subscribe_button = tk.Button(window, text="Subscribe", command=subscribe_topic)

received_message_label = tk.Label(window, text="Received Message:")
received_message = tk.StringVar()
received_message_entry = tk.Entry(window, textvariable=received_message, state='readonly')

# Arrange widgets using grid
topic_label.grid(row=0, column=0, padx=10, pady=10)
topic_entry.grid(row=0, column=1, padx=10, pady=10)

message_label.grid(row=1, column=0, padx=10, pady=10)
message_entry.grid(row=1, column=1, padx=10, pady=10)

host_label.grid(row=2, column=0, padx=10, pady=10)
host_entry.grid(row=2, column=1, padx=10, pady=10)

publish_button.grid(row=3, column=0, columnspan=2, pady=10)

subscribe_label.grid(row=4, column=0, padx=10, pady=10)
subscribe_entry.grid(row=4, column=1, padx=10, pady=10)
subscribe_button.grid(row=5, column=0, columnspan=2, pady=10)

received_message_label.grid(row=6, column=0, padx=10, pady=10)
received_message_entry.grid(row=6, column=1, padx=10, pady=10)

# Set up MQTT client for subscribing
subscribe_client = mqtt.Client()
subscribe_client.on_subscribe = on_subscribe
subscribe_client.on_message = on_message
subscribe_client.connect("broker.hivemq.com", 1883, 60)

# Start the MQTT loop for the subscriber client
subscribe_client.loop_start()

# Start the GUI event loop
window.mainloop()
