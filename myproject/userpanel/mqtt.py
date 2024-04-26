import paho.mqtt.client as mqtt
import time
import logging

broker_address = "localhost"
port = 1883
username = "admin"  # Replace with your MQTT broker username
password = "admin"  # Replace with your MQTT broker password

class MQTTHandler:
    def __init__(self):
        self.connected = False
        self.received_message = ""
        self.client = mqtt.Client()
        self.client.username_pw_set(username, password)  # Set username and password
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message

        # Add logging configuration
        logging.basicConfig(level=logging.DEBUG)
        self.logger = logging.getLogger(__name__)

        self.client.connect(broker_address, port, 60)
        self.client.loop_start()

    def on_connect(self, client, userdata, flags, rc):
        if rc == 0:
            self.logger.info('Client is connected')
            self.connected = True
        else:
            self.logger.error(f'Client failed to connect with result code {rc}')
            self.connected = False

    def on_message(self, client, userdata, msg):
        try:
            self.logger.info("Received message: %s %s", msg.topic, msg.payload)
            self.received_message = msg.payload.decode()
            # Handle the received message as needed
        except Exception as e:
            self.logger.error("Error in on_message: %s", str(e))

    def subscribe_with_timeout(self, topic, timeout=10):
        self.received_message = ""  # Reset the received message
        self.client.subscribe(topic)

        start_time = time.time()
        while not self.received_message and time.time() - start_time < timeout:
            time.sleep(1)  # Adjust the sleep duration as needed
            self.logger.debug("Waiting for message on topic '%s'", topic)

        self.logger.info("Subscribed to topic '%s': %s", topic, self.received_message)
        return self.received_message

    def publish(self, topic, payload):
        self.client.publish(topic, payload)
        self.logger.info("Published to topic '%s': %s", topic, payload)

    def get_received_message(self):
        return self.received_message
