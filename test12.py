import tkinter as tk
from tkinter import ttk
import paho.mqtt.client as mqtt
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class PotagerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Interface du Potager")

        # Données des capteurs
        self.temperature = []
        self.humidity = []
        self.light = []
        self.x_data = []

        # MQTT
        self.client = mqtt.Client()
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message
        self.client.connect("broker.hivemq.com", 1883, 60)
        for topic in ["/Thinkitive/temp", "/Thinkitive/hum", "/Thinkitive/ldr"]:
            self.client.subscribe(topic)

        # Frame pour les données des capteurs
        sensor_frame = ttk.LabelFrame(root, text="Données des Capteurs")
        sensor_frame.grid(row=0, column=0, padx=10, pady=10, sticky=tk.W+tk.E+tk.N+tk.S)

        ttk.Label(sensor_frame, text="Température:").grid(row=0, column=0, padx=5, pady=5, sticky=tk.W)
        self.temperature_label = ttk.Label(sensor_frame, text="")
        self.temperature_label.grid(row=0, column=1, padx=5, pady=5, sticky=tk.W)

        ttk.Label(sensor_frame, text="Humidité:").grid(row=1, column=0, padx=5, pady=5, sticky=tk.W)
        self.humidity_label = ttk.Label(sensor_frame, text="")
        self.humidity_label.grid(row=1, column=1, padx=5, pady=5, sticky=tk.W)

        ttk.Label(sensor_frame, text="Luminosité:").grid(row=2, column=0, padx=5, pady=5, sticky=tk.W)
        self.light_label = ttk.Label(sensor_frame, text="")
        self.light_label.grid(row=2, column=1, padx=5, pady=5, sticky=tk.W)

        # Frame pour les graphiques de tendances
        graph_frame = ttk.LabelFrame(root, text="Graphiques de Tendances")
        graph_frame.grid(row=1, column=0, columnspan=2, padx=10, pady=10, sticky=tk.W+tk.E+tk.N+tk.S)

        self.fig, self.ax = plt.subplots(figsize=(6, 4))
        self.canvas = FigureCanvasTkAgg(self.fig, master=graph_frame)
        self.canvas.get_tk_widget().pack()

        # Mettre à jour les données des capteurs et afficher les graphiques de tendances
        self.client.loop_start()

    def on_message(self, client, userdata, msg):
     topic = msg.topic
     payload = float(msg.payload.decode())
     print("Received message:", topic, payload)  # Débogage
    
     if topic == "/Thinkitive/temp":
        self.temperature.append(payload)
     elif topic == "/Thinkitive/hum":
        self.humidity.append(payload)
        print("Humidity data:", self.humidity)  # Débogage
     elif topic == "/Thinkitive/ldr":
        self.light.append(payload)
        print("Light data:", self.light)  # Débogage
        
     self.x_data.append(len(self.x_data))  # Mise à jour une seule fois

     self.update_sensor_labels()
     self.update_graph()

    def update_sensor_labels(self):
        if self.temperature:
            self.temperature_label.config(text=f"{self.temperature[-1]} °C")
        if self.humidity:
            self.humidity_label.config(text=f"{self.humidity[-1]} %")
        if self.light:
            self.light_label.config(text=f"{self.light[-1]} lux")

    def update_graph(self):
        self.ax.clear()
        if self.temperature:
            self.ax.plot(self.x_data, self.temperature, label='Température (°C)')
        if self.humidity:
            self.ax.plot(self.x_data, self.humidity, label='Humidité (%)')
        if self.light:
            self.ax.plot(self.x_data, self.light, label='Luminosité (lux)')
        self.ax.legend()
        self.ax.set_xlabel("Temps")
        self.ax.set_ylabel("Valeur")
        self.ax.set_title("Tendances des Capteurs")
        self.canvas.draw()

if __name__ == "__main__":
    root = tk.Tk()
    app = PotagerApp(root)
    root.mainloop()
