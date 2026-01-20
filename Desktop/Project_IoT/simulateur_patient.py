import paho.mqtt.client as mqtt
import time
import random
import json

# 1. Configuration de la connexion
BROKER = "localhost"
PORT = 1883
TOPIC = "sante/patient1/signes_vitaux"

# 2. Connexion au serveur
# CORRECTION ICI : On précise la version de l'API (VERSION2) pour paho-mqtt 2.x
client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2, "Simulateur_Tinkercad")

try:
    client.connect(BROKER, PORT)
    print("✅ Connecté au serveur Mosquitto !")
except Exception as e:
    print(f"❌ Erreur de connexion : {e}")
    print("Vérifiez que la fenêtre noire Mosquitto est bien ouverte.")
    exit()

# 3. Boucle infinie
print("Démarrage de l'envoi des données (CTRL+C pour arrêter)...")

try:
    while True:
        # Simulation des données
        data = {
            "temperature": round(random.uniform(36.5, 39.5), 1),
            "frequence_cardiaque": random.randint(60, 100),
            "spo2": random.randint(88, 100)
        }
        
        message = json.dumps(data)
        
        # Envoi
        client.publish(TOPIC, message)
        print(f"Envoi vers le serveur : {message}")
        
        time.sleep(5)

except KeyboardInterrupt:
    print("\nArrêt de la simulation.")
    client.disconnect()