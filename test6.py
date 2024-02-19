import tkinter as tk
from PIL import Image, ImageTk
import paho.mqtt.client as mqtt

# MQTT Settings
MQTT_BROKER = "broker.hivemq.com"
MQTT_PORT = 1883
TOPICS = ["/Thinkitive/temp", "/Thinkitive/hum", "/Thinkitive/ldr", "/Thinkitive/ntc"]

# Couleurs
BACKGROUND_COLOR = "#F0F0F0"
TEXT_COLOR = "#333333"

# Tkinter App
class SensorApp:
    def __init__(self, master):
        self.master = master
        master.title("Potager Monitor")
        master.configure(background=BACKGROUND_COLOR)

        # Images
        self.temperature_icon = ImageTk.PhotoImage(Image.open("C:/Users/rabou/Desktop/projetdomo/578113.png"))
        self.humidity_icon = ImageTk.PhotoImage(Image.open("C:/Users/rabou/Desktop/projetdomo/humidity_wather_16790.png"))
        self.luminosity_icon = ImageTk.PhotoImage(Image.open("C:/Users/rabou/Desktop/projetdomo/téléchargement.png"))
        self.ntc_icon = ImageTk.PhotoImage(Image.open("C:/Users/rabou/Desktop/projetdomo/téléchargement.jpg"))  # Remplacer par l'icone appropriée

        # Labels pour afficher les données des capteurs
        self.label_temperature = tk.Label(master, text="Température: ", font=("Helvetica", 14), fg=TEXT_COLOR, bg=BACKGROUND_COLOR, compound=tk.LEFT, image=self.temperature_icon)
        self.label_temperature.pack(pady=5)

        self.label_humidity = tk.Label(master, text="Humidité: ", font=("Helvetica", 14), fg=TEXT_COLOR, bg=BACKGROUND_COLOR, compound=tk.LEFT, image=self.humidity_icon)
        self.label_humidity.pack(pady=5)

        self.label_luminosity = tk.Label(master, text="Luminosité: ", font=("Helvetica", 14), fg=TEXT_COLOR, bg=BACKGROUND_COLOR, compound=tk.LEFT, image=self.luminosity_icon)
        self.label_luminosity.pack(pady=5)

        self.label_ntc = tk.Label(master, text="Température NTC: ", font=("Helvetica", 14), fg=TEXT_COLOR, bg=BACKGROUND_COLOR, compound=tk.LEFT, image=self.ntc_icon)
        self.label_ntc.pack(pady=5)

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
        # Mise à jour de l'interface graphique avec les données des capteurs
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
