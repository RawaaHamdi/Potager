import tkinter as tk
from tkinter import ttk
import paho.mqtt.client as mqtt
from ttkthemes import ThemedStyle

# Callback function to handle incoming MQTT messages
def on_message(client, userdata, message):
    topic = message.topic
    payload = message.payload.decode()

    if topic.endswith("/temp"):
        temperature_label.config(text=f"Temperature: {payload} °C")
    elif topic.endswith("/hum"):
        humidity_label.config(text=f"Humidity: {payload} %")
    elif topic.endswith("/ldr"):
        luminosity_label.config(text=f"Luminosity: {payload} lux")

# Create MQTT client and set the callback function
mqtt_client = mqtt.Client()
mqtt_client.on_message = on_message

# Connect to MQTT broker
mqtt_client.connect("broker.hivemq.com")

# Subscribe to MQTT topics with the "AA" prefix
mqtt_client.subscribe("AA/temp")
mqtt_client.subscribe("AA/hum")
mqtt_client.subscribe("AA/ldr")

# Tkinter app setup
app = tk.Tk()
app.title("IoT Data Display")

# Use ThemedStyle from ttkthemes
style = ThemedStyle(app)
style.set_theme("plastik")  # Change theme here

# Labels to display data
temperature_label = ttk.Label(app, text="Temperature: ")
temperature_label.pack()

humidity_label = ttk.Label(app, text="Humidity: ")
humidity_label.pack()

luminosity_label = ttk.Label(app, text="Luminosity: ")
luminosity_label.pack()

# Function to start the MQTT loop
def start_mqtt_loop():
    mqtt_client.loop_start()

# Button to start MQTT loop
start_button = ttk.Button(app, text="Start MQTT", command=start_mqtt_loop)
start_button.pack()

# Run the Tkinter app
app.mainloop()
