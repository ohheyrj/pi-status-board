"""Entry point for psb.
"""
import json
import time

from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTClient

from psb import logger
from psb.conf import PsbConfig
from psb.display import EinkDisplay


def process_message(client, userdata, message): # noqa
    config = PsbConfig()
    eink_display = EinkDisplay()
    logger.info('Processing incoming message')
    if message.topic == config.topic:
        message_payload = json.loads(message.payload)
        status_type = message_payload['type']
        if status_type == 'image':
            logger.info('Setting eink display to image')
            eink_display.image(status=message_payload['data'], path=config.img_location)
        elif status_type == 'text':
            logger.info('Setting eink display to text')
            eink_display.text(text=message_payload['data'])
    else:
        logger.info(f'Ignoring message for topic {message.topic}')


def shell():
    """Command line 'psb'.
    """
    config = PsbConfig()

    # Init AWSIoTMQTTClient
    mqtt_client = None
    if config.use_websockets:
        mqtt_client = AWSIoTMQTTClient(config.client_id, useWebsocket=True)
        mqtt_client.configureEndpoint(config.endpoint, config.port)
        mqtt_client.configureCredentials(config.root_ca)
    else:
        mqtt_client = AWSIoTMQTTClient(config.client_id)
        mqtt_client.configureEndpoint(config.endpoint, config.port)
        mqtt_client.configureCredentials(config.root_ca, config.aws_iot_priv_key, config.aws_iot_cert)

    # AWSIoTMQTTClient connection configuration
    mqtt_client.configureAutoReconnectBackoffTime(1, 32, 20)
    mqtt_client.configureOfflinePublishQueueing(-1)  # Infinite offline Publish queueing
    mqtt_client.configureDrainingFrequency(2)  # Draining: 2 Hz
    mqtt_client.configureConnectDisconnectTimeout(10)  # 10 sec
    mqtt_client.configureMQTTOperationTimeout(5)  # 5 sec

    # Connect and subscribe to AWS IoT
    mqtt_client.connect()
    if config.mode == 'both' or config.mode == 'subscribe':
        mqtt_client.subscribe(config.topic, 1, process_message)
    time.sleep(2)

    # Publish to the same topic in a loop forever
    while True:
        time.sleep(5)
