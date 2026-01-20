import paho.mqtt.client as mqtt
import json

# --- CONFIGURATION ---
BROKER = "localhost"
PORT = 1883
TOPIC = "sante/patient1/signes_vitaux"

# Seuils d'alerte (définis par le médecin)
SEUIL_TEMP_HAUTE = 38.0
SEUIL_SPO2_BAS = 90
SEUIL_COEUR_HAUT = 100

def analyser_donnees(data):
    """
    Cette fonction cherche les anomalies dans les données reçues
    """
    temp = data['temperature']
    spo2 = data['spo2']
    bpm = data['frequence_cardiaque']
    
    alertes = []

    # 1. Analyse de la fièvre
    if temp > SEUIL_TEMP_HAUTE:
        alertes.append(f"⚠️ FIÈVRE DÉTECTÉE ({temp}°C)")

    # 2. Analyse de l'oxygène (Hypoxie)
    if spo2 < SEUIL_SPO2_BAS:
        alertes.append(f"⚠️ DANGER: MANQUE D'OXYGÈNE ({spo2}%)")
        
    # 3. Analyse cardiaque
    if bpm > SEUIL_COEUR_HAUT:
         alertes.append(f"⚠️ TACHYCARDIE ({bpm} BPM)")

    # Affichage du diagnostic
    if alertes:
        print("\n" + "!"*30)
        print(f"🚨 ALERTES POUR PATIENT {data.get('id_patient', 'Inconnu')} 🚨")
        for alerte in alertes:
            print(alerte)
        print("!"*30 + "\n")
    else:
        print(f"✅ Patient stable (T: {temp}°C | SpO2: {spo2}% | BPM: {bpm})")

# --- FONCTIONS MQTT ---

def on_connect(client, userdata, flags, rc, properties=None):
    if rc == 0:
        print("✅ Le Médecin est connecté et écoute...")
        # On s'abonne au sujet pour recevoir les messages
        client.subscribe(TOPIC)
    else:
        print(f"Erreur de connexion : {rc}")

def on_message(client, userdata, msg):
    try:
        # 1. Décoder le message reçu
        payload = msg.payload.decode()
        # 2. Convertir le texte JSON en dictionnaire Python
        data = json.loads(payload)
        # 3. Lancer l'analyse
        analyser_donnees(data)
    except Exception as e:
        print(f"Erreur de lecture : {e}")

# --- INITIALISATION ---
# On utilise la VERSION2 comme pour l'autre script
client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2, "Analyseur_Python")
client.on_connect = on_connect
client.on_message = on_message

try:
    client.connect(BROKER, PORT)
    # loop_forever bloque le script ici pour écouter en permanence
    client.loop_forever()
except KeyboardInterrupt:
    print("Arrêt du système de surveillance.")
except Exception as e:
    print(f"Erreur: {e}")