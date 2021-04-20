from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTClient
import logging
import time
import json
import configparser
import os
from inky import BLACK
from inky.auto import auto
from font_fredoka_one import FredokaOne
from PIL import Image, ImageFont, ImageDraw
from pathlib import Path

AllowedActions = ['both', 'publish', 'subscribe']

# Configure logging
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)
streamHandler = logging.StreamHandler()
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
streamHandler.setFormatter(formatter)
logger.addHandler(streamHandler)


def process_message(client, userdata, message):
    if message.topic == topic:
        message_payload = json.loads(message.payload)
        status_type = message_payload['type']
        if status_type == 'image':
            set_eink_image(status=message_payload['data'])


def set_eink_image(status: str = 'idle', path: str = "img"):
    filename = f"{status}.png"
    print(f'Using filename: {filename}')
    inky_display = auto(ask_user=True, verbose=True)
    inky_display.set_border(BLACK)

    img = Image.open(os.path.join(path, filename))
    # inky_display.set_image(img.rotate(180))
    inky_display.set_image(img)
    inky_display.show()


base_path = Path(__file__).absolute().parent

config = configparser.ConfigParser()
config.read(base_path.join('config.ini'))

if Path(config['certs']['root_ca']).is_absolute():
    rootCAPath = config['certs']['root_ca']
else:
    rootCAPath = base_path.join(config['certs']['root_ca'])

if Path(config['certs']['iot_cert']).is_absolute():
    certificatePath = config['certs']['iot_cert']
else:
    certificatePath = base_path.join(config['certs']['iot_cert'])

if Path(config['certs']['iot_priv_key']).is_absolute():
    privateKeyPath = config['certs']['iot_priv_key']
else:
    privateKeyPath = base_path.join(config['certs']['iot_priv_key'])

host = config['aws_iot'].get('endpoint')
port = config['aws_iot'].get('port') or None
useWebsocket = config['aws_iot'].get('port') or False
clientId = config['aws_iot'].get('client_id') or 'StatusBoard'
topic = config['aws_iot'].get('topic') or 'status_board'
mode = config['aws_iot'].get('mode') or 'both'
defaultStatus = config['status_board'].get('default_status') or None

if mode not in AllowedActions:
    logger.error("Unknown --mode option %s. Must be one of %s" % (mode, str(AllowedActions)))
    exit(2)

if useWebsocket and certificatePath and privateKeyPath:
    logger.error("X.509 cert authentication and WebSocket are mutual exclusive. Please pick one.")
    exit(2)

if not useWebsocket and (not certificatePath or not privateKeyPath):
    logger.error("Missing credentials for authentication.")
    exit(2)

# Port defaults
if useWebsocket and not port:  # When no port override for WebSocket, default to 443
    port = 443
if not useWebsocket and not port:  # When no port override for non-WebSocket, default to 8883
    port = 8883

# Init AWSIoTMQTTClient
myAWSIoTMQTTClient = None
if useWebsocket:
    myAWSIoTMQTTClient = AWSIoTMQTTClient(clientId, useWebsocket=True)
    myAWSIoTMQTTClient.configureEndpoint(host, port)
    myAWSIoTMQTTClient.configureCredentials(rootCAPath)
else:
    myAWSIoTMQTTClient = AWSIoTMQTTClient(clientId)
    myAWSIoTMQTTClient.configureEndpoint(host, port)
    myAWSIoTMQTTClient.configureCredentials(rootCAPath, privateKeyPath, certificatePath)

# AWSIoTMQTTClient connection configuration
myAWSIoTMQTTClient.configureAutoReconnectBackoffTime(1, 32, 20)
myAWSIoTMQTTClient.configureOfflinePublishQueueing(-1)  # Infinite offline Publish queueing
myAWSIoTMQTTClient.configureDrainingFrequency(2)  # Draining: 2 Hz
myAWSIoTMQTTClient.configureConnectDisconnectTimeout(10)  # 10 sec
myAWSIoTMQTTClient.configureMQTTOperationTimeout(5)  # 5 sec

# Connect and subscribe to AWS IoT
myAWSIoTMQTTClient.connect()
if mode == 'both' or mode == 'subscribe':
    myAWSIoTMQTTClient.subscribe(topic, 1, process_message)
time.sleep(2)

# Publish to the same topic in a loop forever
loopCount = 0
while True:
    time.sleep(5)
