import tkinter as tk
import paho.mqtt.client as mqtt

class SensorApp:
    def __init__(self, master):
        self.master = master
        master.title("Système Potager")

        # Background color
        master.configure(bg='#c7e0a3')  # Light green background

        # Labels to display sensor data
        self.label_temperature = tk.Label(master, text="Température: ", bg='#c7e0a3', font=('Arial', 14))
        self.label_temperature.pack()
        self.temperature_var = tk.StringVar()
        self.label_temperature.config(text="Température: {}°C".format(self.temperature_var.get()))

        self.label_humidity = tk.Label(master, text="Humidité: ", bg='#c7e0a3', font=('Arial', 14))
        self.label_humidity.pack()
        self.humidity_var = tk.StringVar()
        self.label_humidity.config(text="Humidité: {}%".format(self.humidity_var.get()))

        self.label_luminosity = tk.Label(master, text="Luminosité: ", bg='#c7e0a3', font=('Arial', 14))
        self.label_luminosity.pack()
        self.luminosity_var = tk.StringVar()
        self.label_luminosity.config(text="Luminosité: {}".format(self.luminosity_var.get()))

        self.label_ntc = tk.Label(master, text="Température NTC: ", bg='#c7e0a3', font=('Arial', 14))
        self.label_ntc.pack()
        self.ntc_var = tk.StringVar()
        self.label_ntc.config(text="Température NTC: {}°C".format(self.ntc_var.get()))

        # MQTT
        self.client = mqtt.Client()
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message
        self.client.connect(MQTT_BROKER, MQTT_PORT, 60)
        self.client.loop_start()

        self.master.after(100, self.update_gui)

    def on_connect(self, client, userdata, flags, rc):
        print("Connected with result code "+str(rc))
        for topic in TOPICS:
            self.client.subscribe(topic)

    def on_message(self, client, userdata, msg):
        print(msg.topic+" "+str(msg.payload))
        if msg.topic == "/Thinkitive/temp":
            self.temperature_var.set(str(msg.payload.decode('utf-8')) + "°C")
        elif msg.topic == "/Thinkitive/hum":
            self.humidity_var.set(str(msg.payload.decode('utf-8')) + "%")
        elif msg.topic == "/Thinkitive/ldr":
            self.luminosity_var.set(str(msg.payload.decode('utf-8')))
        elif msg.topic == "/Thinkitive/ntc":
            self.ntc_var.set(str(msg.payload.decode('utf-8')) + "°C")

    def update_gui(self):
        self.label_temperature.config(text="Température: {}°C".format(self.temperature_var.get()))
        self.label_humidity.config(text="Humidité: {}%".format(self.humidity_var.get()))
        self.label_luminosity.config(text="Luminosité: {}".format(self.luminosity_var.get()))
        self.label_ntc.config(text="Température NTC: {}°C".format(self.ntc_var.get()))
        self.master.after(100, self.update_gui)

root = tk.Tk()
app = SensorApp(root)
root.mainloop()