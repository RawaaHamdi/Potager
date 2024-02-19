import tkinter as tk
from tkinter import scrolledtext
from PIL import Image, ImageTk
import paho.mqtt.client as mqtt

# MQTT Settings
MQTT_BROKER = "broker.hivemq.com"
MQTT_PORT = 1883
TOPICS = ["/Thinkitive/temp", "/Thinkitive/hum", "/Thinkitive/ldr", "/Thinkitive/ntc"]

# Couleursc
BACKGROUND_COLOR = "#FFFFFF"  # Blanc
TEXT_COLOR = "#333333"

# Fonction pour charger et redimensionner une image
def load_and_resize_image(file_path, width, height):
    original_image = Image.open(file_path)
    resized_image = original_image.resize((width, height), resample=Image.BILINEAR)
    return ImageTk.PhotoImage(resized_image)

# Tkinter App
class SensorApp:
    def __init__(self, master):
        self.master = master
        master.title("Système de potager")
        master.configure(background=BACKGROUND_COLOR)

        # Canvas pour l'image d'arrière-plan
        self.canvas = tk.Canvas(master, width=800, height=600, bg=BACKGROUND_COLOR)  # Ajustez la taille selon vos besoins
        self.canvas.pack()

        # Charger et afficher l'image d'arrière-plan à droite avec une taille réduite
        self.background_image = load_and_resize_image("C:/Users/rabou/Desktop/projetdomo/image d'une plante.png", 400, 300)  # Réduire la taille de l'image
        self.canvas.create_image(400, 0, anchor=tk.NW, image=self.background_image)  # Déplacer vers la droite

        # Images des capteurs
        self.temperature_icon = load_and_resize_image("C:/Users/rabou/Desktop/projetdomo/image temperature.png", 50, 50)  # Modifier le chemin en conséquence
        self.humidity_icon = load_and_resize_image("C:/Users/rabou/Desktop/projetdomo/humidity_wather_16790.png", 50, 50)  # Modifier le chemin en conséquence
        self.luminosity_icon = load_and_resize_image("C:/Users/rabou/Desktop/projetdomo/image du lumiére.png", 50, 50)  # Modifier le chemin en conséquence
        self.ntc_icon = load_and_resize_image("C:/Users/rabou/Desktop/projetdomo/RTC Image.jpg", 50, 50)  # Modifier le chemin en conséquence

        # Labels pour afficher les données des capteurs avec texte blanc
        self.label_temperature = tk.Label(master, text="Température: ", font=("Helvetica", 14), fg=TEXT_COLOR, bg=BACKGROUND_COLOR, compound=tk.LEFT, image=self.temperature_icon)
        self.label_temperature.place(x=50, y=50)  # Ajustez la position selon vos besoins

        self.label_humidity = tk.Label(master, text="Humidité: ", font=("Helvetica", 14), fg=TEXT_COLOR, bg=BACKGROUND_COLOR, compound=tk.LEFT, image=self.humidity_icon)
        self.label_humidity.place(x=50, y=100)  # Ajustez la position selon vos besoins

        self.label_luminosity = tk.Label(master, text="Luminosité: ", font=("Helvetica", 14), fg=TEXT_COLOR, bg=BACKGROUND_COLOR, compound=tk.LEFT, image=self.luminosity_icon)
        self.label_luminosity.place(x=50, y=150)  # Ajustez la position selon vos besoins

        self.label_ntc = tk.Label(master, text="Température NTC: ", font=("Helvetica", 14), fg=TEXT_COLOR, bg=BACKGROUND_COLOR, compound=tk.LEFT, image=self.ntc_icon)
        self.label_ntc.place(x=50, y=200)  # Ajustez la position selon vos besoins

        # Bouton pour exécuter les actions
        self.action_button = tk.Button(master, text="Consulter l'état de potager", command=self.execute_actions, bg="#4CAF50", fg="white",font=("Helvetica", 12, "bold"))
        self.action_button.place(x=220, y=250)  # Ajustez la position selon vos besoins

        # Widget Text pour afficher les actions avec un fond de couleur différente
        self.action_text = scrolledtext.ScrolledText(master, width=50, height=10, bg=BACKGROUND_COLOR, fg=TEXT_COLOR)  # Changement de la couleur de fond
        self.action_text.place(x=50, y=300)  # Ajustez la position selon vos besoins

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

    def execute_actions(self):
        temperature_str = self.label_temperature.cget("text")
        humidity_str = self.label_humidity.cget("text")
        luminosity_str = self.label_luminosity.cget("text")

        temperature_value = float(temperature_str.split(": ")[1].rstrip("°C"))
        humidity_value = float(humidity_str.split(": ")[1].rstrip("%"))
        luminosity_value = float(luminosity_str.split(": ")[1])

        # Ajoutez ici vos conditions et actions correspondantes en fonction des valeurs des capteurs
        actions = []
        if temperature_value > 25:
            actions.append("Température élevée, arrosage nécessaire")
        else:
            actions.append("Température acceptable, pas besoin d'arrosage")

        if humidity_value < 40:
            actions.append("Humidité basse, arrosage nécessaire")
        else:
            actions.append("Humidité acceptable, pas besoin d'arrosage")

        if luminosity_value < 5000:
            actions.append("Faible luminosité, déplacer les plantes vers un endroit plus lumineux")
        else:
            actions.append("Luminosité suffisante")

        # Afficher les actions dans le widget Text
        self.action_text.delete("1.0", tk.END)
        for action in actions:
            self.action_text.insert(tk.END, action + "\n")

root = tk.Tk()
app = SensorApp(root)
root.mainloop()
