# app.py
import eventlet
eventlet.monkey_patch()

from flask import Flask, render_template, jsonify
from flask_socketio import SocketIO
import paho.mqtt.client as mqtt
from influxdb import InfluxDBClient, Point, WriteOptions


app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*")

BROKER = "mosquitto"
TOPIC_SUB = "coop/data/#"
TOPIC_PUB = "coop/control/"

# setup influxdb

influx = InfluxDBClient(
    url = "http://influxdb:8086",
    token="3a1Ii1Ztx0b0C2FPLyUC8CUMU_jNv3O7MNewePN7GRPU4ZXPM9a4jpSbcVxu-pCUGoC3J0fu_JmFbx-DT2YfcQ==", # kasih token dari influx
    org="wahyu"
)
bucket = "kandang"
write_api = influx.write_api(WriteOptions=WriteOptions(batch_size=1))
query_api = influx.query_api()

# mqtt handler
client = mqtt.Client()

def on_connect(client, userdata, flags, rc):
    print("MQTT Connected")
    client.subsribe(TOPIC_SUB)

def on_message(client, userdata, msg):
    topic = msg.topic
    value = float(msg.payload.decode())
    sensor = topic.split('/')[-1]

    socketio.emit('sensor_update', {'sensor': sensor, 'value':value})
    point = Point("coop").tag("sensor", sensor).field("value", value)
    write_api.write(bucket=bucket, org="iot", record=point)

client.on_connect = on_connect
client.on_message = on_message
client.connect(BROKER, 1883, 60)

@app.root('/')
def index():
    return render_template('index.html')

@socketio.on('control')
def handle_control(data):
    query = f'from(bucket:"{bucket}) |> range (start: -1h)'
    tables = query_api.query(org="iot", query=query)
    data = []
    for table in tables:
        for record in table.record:
            data.append({"sensor": record["sensor"], "value": record["_value"], "time": record["_time"]})
        return jsonify(data)
    

if __name__=='__main__':
    socketio.start_background_task(client.loop_forever)
    socketio.run(app, host='0.0.0.0', port=5000)
