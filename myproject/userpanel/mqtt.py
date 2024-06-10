import paho.mqtt.client as mqtt
import json
import logging
import time
import threading

# MQTT settings
broker_address = "localhost"
port = 1883
client_id = "781c4edc-c965-444a-a78b-d0d3d5cd00ea"
topic = "home/appliance/status"
username = "admin"
password = "admin"

class MQTTHandler:
    def __init__(self):
        self.client = mqtt.Client(client_id)
        self.client.username_pw_set(username, password)
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message
        self.client.on_disconnect = self.on_disconnect

        self.connected = False
        self.received_message = {}
        self.logger = logging.getLogger(__name__)

        logging.basicConfig(level=logging.DEBUG)
        self.connect()

    def connect(self):
        try:
            self.logger.info("Connecting to MQTT broker...")
            self.client.connect(broker_address, port, 60)
            self.client.loop_start()
        except Exception as e:
            self.logger.error(f"Failed to connect to MQTT broker: {str(e)}")
            self.schedule_reconnect()

    def on_connect(self, client, userdata, flags, rc):
        if rc == 0:
            self.logger.info('Connected to MQTT broker')
            self.connected = True
            self.client.subscribe(topic)
        elif rc == 5:
            self.logger.error('Authentication failed - not authorized')
        else:
            self.logger.error(f'Failed to connect with result code {rc}')
            self.connected = False
            self.schedule_reconnect()

    def on_message(self, client, userdata, msg):
        try:
            self.logger.info("Received message: %s %s", msg.topic, msg.payload)
            self.received_message = json.loads(msg.payload.decode())
            self.handle_message(self.received_message)
        except Exception as e:
            self.logger.error(f"Error in on_message: {str(e)}")
            self.received_message = {}

    def handle_message(self, message):
        try:
            if 'status' in message:
                status_topic = "home/appliance/processed_status"
                self.publish(status_topic, json.dumps(message))
                self.logger.info(f"Published processed status to {status_topic}")
        except Exception as e:
            self.logger.error(f"Error handling message: {e}")

    def on_disconnect(self, client, userdata, rc):
        self.logger.warning("Client got disconnected with code %s", rc)
        self.connected = False
        if rc != 0:
            self.schedule_reconnect()

    def schedule_reconnect(self, delay=300):
        self.logger.info(f"Reconnecting in {delay} seconds...")
        time.sleep(delay)
        self.reconnect()

    def reconnect(self):
        while not self.connected:
            try:
                self.logger.info("Attempting to reconnect to MQTT broker")
                self.client.reconnect()
                self.connected = True
                self.logger.info("Reconnected to MQTT broker")
            except Exception as e:
                self.logger.error(f"Reconnection failed: {str(e)}")
                delay = min(60, delay * 2)  # exponential backoff
                self.schedule_reconnect(delay)

    def subscribe_with_timeout(self, topic, timeout=10):
        self.received_message = {}
        self.client.subscribe(topic)

        start_time = time.time()
        while not self.received_message and time.time() - start_time < timeout:
            time.sleep(1)
            self.logger.debug(f"Waiting for message on topic '{topic}'")

        self.logger.info(f"Subscribed to topic '{topic}': {self.received_message}")
        return self.received_message

    def publish(self, topic, payload):
        self.client.publish(topic, payload)
        self.logger.info(f"Published to topic '{topic}': {payload}")

    def get_received_message(self):
        return self.received_message

    def disconnect(self):
        self.client.disconnect()
        self.client.loop_stop()

mqtt_handler = MQTTHandler()

def start_mqtt_loop():
    try:
        while True:
            if not mqtt_handler.connected:
                mqtt_handler.reconnect()
            time.sleep(300)
    except KeyboardInterrupt:
        mqtt_handler.disconnect()
        mqtt_handler.logger.info("MQTT loop stopped and disconnected cleanly")

mqtt_thread = threading.Thread(target=start_mqtt_loop)
mqtt_thread.daemon = True
mqtt_thread.start()

class sample:
    pass
