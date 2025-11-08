import paho.mqtt.client as mqtt

BROKER = "localhost"
PORT = 1883
USERNAME = "wahyu"
PASSWORD = "123"

TOPIC_SUB = "coop/data/sensor"
TOPIC_PUB = "coop/control"

# callback saat connect
def on_connect(client, userdata,flags, rc):
    print("Connect with result code" + str(rc))
    client.subscribe(TOPIC_SUB)

# callback saat terima pesan
def on_message(client, userdata, msg):
    print(f"[MQTT] topic: {msg.topic} | message: {msg.payload.decode()}")


# inisialisasi client
client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

def start_mqtt():
    client.connect(BROKER, PORT, 60)
    client.loop_start()

def publish_message(topic, message):
    client.publish(topic, message)