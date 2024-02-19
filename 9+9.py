import tkinter as tk
from tkinter import ttk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import random

class PotagerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Interface du Potager")

        # Données des capteurs
        self.temperature = tk.StringVar()
        self.humidity = tk.StringVar()
        self.light = tk.StringVar()

        # Frame pour les données des capteurs
        sensor_frame = ttk.LabelFrame(root, text="Données des Capteurs")
        sensor_frame.grid(row=0, column=0, padx=10, pady=10, sticky=tk.W+tk.E+tk.N+tk.S)

        ttk.Label(sensor_frame, text="Température:").grid(row=0, column=0, padx=5, pady=5, sticky=tk.W)
        ttk.Label(sensor_frame, textvariable=self.temperature).grid(row=0, column=1, padx=5, pady=5, sticky=tk.W)

        ttk.Label(sensor_frame, text="Humidité:").grid(row=1, column=0, padx=5, pady=5, sticky=tk.W)
        ttk.Label(sensor_frame, textvariable=self.humidity).grid(row=1, column=1, padx=5, pady=5, sticky=tk.W)

        ttk.Label(sensor_frame, text="Luminosité:").grid(row=2, column=0, padx=5, pady=5, sticky=tk.W)
        ttk.Label(sensor_frame, textvariable=self.light).grid(row=2, column=1, padx=5, pady=5, sticky=tk.W)

        # Frame pour les graphiques de tendances
        graph_frame = ttk.LabelFrame(root, text="Graphiques de Tendances")
        graph_frame.grid(row=1, column=0, padx=10, pady=10, sticky=tk.W+tk.E+tk.N+tk.S)

        self.fig, self.ax = plt.subplots(figsize=(6, 4))
        self.canvas = FigureCanvasTkAgg(self.fig, master=graph_frame)
        self.canvas.get_tk_widget().pack()

        # Boutons pour configurer les paramètres du potager
        settings_frame = ttk.LabelFrame(root, text="Paramètres du Potager")
        settings_frame.grid(row=0, column=1, rowspan=2, padx=10, pady=10, sticky=tk.W+tk.E+tk.N+tk.S)

        ttk.Button(settings_frame, text="Configurer", command=self.configure_garden).grid(row=0, column=0, padx=5, pady=5)

        # Mettre à jour les données des capteurs et afficher les graphiques de tendances
        self.update_sensor_data()
        self.update_graph()

    def update_sensor_data(self):
        # Simuler des données de capteurs
        self.temperature.set(f"{random.randint(15, 30)} °C")
        self.humidity.set(f"{random.randint(40, 80)} %")
        self.light.set(f"{random.randint(100, 1000)} lux")

        # Mettre à jour les données toutes les 5 secondes
        self.root.after(5000, self.update_sensor_data)

    def update_graph(self):
        # Simuler des données de tendances
        x = range(10)
        y = [random.randint(20, 30) for _ in x]
        
        self.ax.clear()
        self.ax.plot(x, y)
        self.ax.set_xlabel("Temps")
        self.ax.set_ylabel("Valeur")
        self.ax.set_title("Tendance Température")
        self.canvas.draw()

        # Mettre à jour les graphiques toutes les 10 secondes
        self.root.after(10000, self.update_graph)

    def configure_garden(self):
        # Fonction pour configurer les paramètres du potager
        pass

if __name__ == "__main__":
    root = tk.Tk()
    app = PotagerApp(root)
    root.mainloop()
