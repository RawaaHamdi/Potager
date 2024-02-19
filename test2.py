import tkinter as tk
from tkinter import ttk
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

# Set up style
style = ttk.Style()
style.theme_use('clam')  # Choose one of the available themes
style.configure('TButton', foreground='blue')  # Customizing button color

# Create widgets for publishing
publish_frame = ttk.LabelFrame(window, text='Publish Message')
publish_frame.grid(row=0, column=0, padx=10, pady=10, sticky='ew')

topic_label = ttk.Label(publish_frame, text="Enter the topic:")
topic_entry = ttk.Entry(publish_frame)
topic_entry.insert(0, "Hala")  # Default value

message_label = ttk.Label(publish_frame, text="Enter the message:")
message_entry = ttk.Entry(publish_frame)
message_entry.insert(0, "on")  # Default value

host_label = ttk.Label(publish_frame, text="Enter the host adrs:")
host_entry = ttk.Entry(publish_frame)
host_entry.insert(0, "broker.hivemq.com")  # Default value

publish_button = ttk.Button(publish_frame, text="Publish", command=publish_message, width=20)  # Set custom width

# Create widgets for subscribing
subscribe_frame = ttk.LabelFrame(window, text='Subscribe Topic')
subscribe_frame.grid(row=1, column=0, padx=10, pady=10, sticky='ew')

subscribe_label = ttk.Label(subscribe_frame, text="Enter the topic to subscribe:")
subscribe_entry = ttk.Entry(subscribe_frame)
subscribe_entry.insert(0, "Holo")  # Default value

subscribe_button = ttk.Button(subscribe_frame, text="Subscribe", command=subscribe_topic, width=20)  # Set custom width

received_message_label = ttk.Label(window, text="Received Message:")
received_message = tk.StringVar()
received_message_entry = ttk.Entry(window, textvariable=received_message, state='readonly')

# Arrange widgets using grid
topic_label.grid(row=0, column=0, padx=10, pady=5, sticky='w')
topic_entry.grid(row=0, column=1, padx=10, pady=5, sticky='ew')

message_label.grid(row=1, column=0, padx=10, pady=5, sticky='w')
message_entry.grid(row=1, column=1, padx=10, pady=5, sticky='ew')

host_label.grid(row=2, column=0, padx=10, pady=5, sticky='w')
host_entry.grid(row=2, column=1, padx=10, pady=5, sticky='ew')

publish_button.grid(row=3, column=0, columnspan=2, pady=10, sticky='ew')

subscribe_label.grid(row=0, column=0, padx=10, pady=5, sticky='w')
subscribe_entry.grid(row=0, column=1, padx=10, pady=5, sticky='ew')
subscribe_button.grid(row=1, column=0, columnspan=2, pady=10, sticky='ew')

received_message_label.grid(row=2, column=0, padx=10, pady=5, sticky='w')
received_message_entry.grid(row=2, column=1, padx=10, pady=5, sticky='ew')

# Set up MQTT client for subscribing
subscribe_client = mqtt.Client()
subscribe_client.on_subscribe = on_subscribe
subscribe_client.on_message = on_message
subscribe_client.connect("broker.hivemq.com", 1883, 60)

# Start the MQTT loop for the subscriber client
subscribe_client.loop_start()

# Start the GUI event loop
window.mainloop()
