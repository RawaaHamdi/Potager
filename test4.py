import tkinter as tk
import paho.mqtt.client as mqtt

# MQTT Settings
MQTT_BROKER = "broker.hivemq.com"
MQTT_PORT = 1883
TOPICS = ["/Thinkitive/temp", "/Thinkitive/hum", "/Thinkitive/ldr", "/Thinkitive/ntc"]

# Tkinter App
class SensorApp:
    def __init__(self, master):
        self.master = master
        master.title("Système Potager")

        # Background color
        master.configure(bg='#c7e0a3')  # Light green background

        # Labels to display sensor data
        self.label_temperature = tk.Label(master, text="Température: ", bg='#c7e0a3', font=('Arial', 14))
        self.label_temperature.pack()

        self.label_humidity = tk.Label(master, text="Humidité: ", bg='#c7e0a3', font=('Arial', 14))
        self.label_humidity.pack()

        self.label_luminosity = tk.Label(master, text="Luminosité: ", bg='#c7e0a3', font=('Arial', 14))
        self.label_luminosity.pack()

        self.label_ntc = tk.Label(master, text="Température NTC: ", bg='#c7e0a3', font=('Arial', 14))
        self.label_ntc.pack()

        # MQTT
        self.client = mqtt.Client()
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message
        self.client.connect(MQTT_BROKER, MQTT_PORT, 60)
        self.client.loop_start()

    def on_connect(self, client, userdata, flags, rc):
        print("Connected with result code "+str(rc))
        for topic in TOPICS:
            client.subscribe(topic)

    def on_message(self, client, userdata, msg):
        print(msg.topic+" "+str(msg.payload))
        # Update GUI with sensor data
        if msg.topic == "/Thinkitive/temp":
            self.label_temperature.config(text="Température: {}°C".format(msg.payload.decode('utf-8')))
        elif msg.topic == "/Thinkitive/hum":
            self.label_humidity.config(text="Humidité: {}%".format(msg.payload.decode('utf-8')))
        elif msg.topic == "/Thinkitive/ldr":
            self.label_luminosity.config(text="Luminosité: {}".format(msg.payload.decode('utf-8')))
        elif msg.topic == "/Thinkitive/ntc":
            self.label_ntc.config(text="Température NTC: {}°C".format(msg.payload.decode('utf-8')))

root = tk.Tk()
app = SensorApp(root)
root.mainloop()
