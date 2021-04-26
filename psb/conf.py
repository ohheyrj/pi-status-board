"""Configuration read from config file."""
from configparser import ConfigParser
from pathlib import Path

from psb import logger


class PsbConfig:
    """Configuration parse for psb.
    """
    def __init__(self, config_file: str = '/etc/psb/conf.ini'):
        """Init of configuration, creates the config object.

        Raises
        ------
        FileNotFoundError
            Return FileNotFoundError if config file is not found.
        """
        self.allowed_actions = ['both', 'publish', 'subscribe']
        self.config_file = Path(config_file)
        if self.config_file.is_file():
            self.config = ConfigParser()
            self.config.read(self.config_file)
        else:
            logger.error(f'Cannot find config file at {config_file}')
            raise FileNotFoundError

        if self.mode not in self.allowed_actions:
            logger.error("Unknown --mode option %s. Must be one of %s" % (self.mode, str(self.allowed_actions)))
            raise ValueError("Unknown --mode option %s. Must be one of %s" % (self.mode, str(self.allowed_actions)))

        if self.use_websockets and self.aws_iot_cert and self.aws_iot_priv_key:
            logger.error("X.509 cert authentication and WebSocket are mutual exclusive. Please pick one.")
            raise SystemExit

        if not self.use_websockets:
            logger.info('Websockets false')
            if not self.aws_iot_cert or not self.aws_iot_priv_key:
                logger.error("Missing credentials for authentication.")
                raise SystemExit

        logger.info(f'Using AWS root certificate: {self.root_ca}')
        logger.info(f'Using AWS IoT Thing certificate: {self.aws_iot_cert}')
        logger.info(f'Using AWS IoT Thing private key: {self.aws_iot_priv_key}')
        logger.info(f'Websockets set to {self.use_websockets}')
        logger.info(f'Using endpoint {self.endpoint}:{self.port}')
        logger.info(f'Using topic {self.topic}')

    @property
    def root_ca(self) -> str:
        """Path to AWS root CA.conf

        Returns
        -------
        str
            The path to the root CA file.
        """
        try:
            return self.config['certs']['root_ca']
        except KeyError:
            return False

    @property
    def aws_iot_cert(self) -> str:
        """Path to AWS IoT thing certificate.conf

        Returns
        -------
        str
            The path to the certificate.
        """
        try:
            return self.config['certs']['iot_cert']
        except KeyError:
            return False

    @property
    def aws_iot_priv_key(self) -> str:
        """Path to the AWS IoT thing private key.conf

        Returns
        -------
        str
            The path to the private key.
        """
        try:
            return self.config['certs']['iot_priv_key']
        except KeyError:
            return False

    @property
    def endpoint(self) -> str:
        """Endpoint of the AWS IoT thing to connect to.

        Returns
        -------
        str
            The IoT thing endpoint.
        """
        return self.config['aws_iot'].get('endpoint')

    @property
    def port(self) -> str:
        """The port to connect to the endpoint on.

        Returns
        -------
        str
            The port number to use.
        """
        try:
            port = self.config['aws_iot']['port']
        except KeyError:
            if self.use_websockets:
                port = 443
            if not self.use_websockets:
                port = 8883
        return port

    @property
    def use_websockets(self) -> bool:
        """Bool value if websockets should be used. Return None if not set.

        Returns
        -------
        bool
            The config value.
        """
        try:
            result = None
            if self.config['aws_iot']['use_websockets'] in ['false', 'False']:
                result = False
            elif self.config['aws_iot']['use_websockets'] in ['true', 'True']:
                result = True
        except KeyError:
            result = False
        return result

    @property
    def client_id(self) -> str:
        """The client ID to use when connecting to the endpoint.

        Returns
        -------
        str
            The client ID.
        """
        return self.config['aws_iot'].get('client_id') or 'StatusBoard'

    @property
    def topic(self) -> str:
        """The desired topic to listen for and/or send messages to.

        Returns
        -------
        str
            The topic to use.
        """
        return self.config['aws_iot'].get('topic') or 'status_board'

    @property
    def mode(self) -> str:
        """
        The mode to use when connecting to the endpoint.
        Can be subscribe, publish or both.

        Returns
        -------
        str
            Mode to use when connecting.
        """
        return self.config['aws_iot'].get('mode') or 'both'

    @property
    def default_status(self) -> str:
        """The default state the screen should display when started.

        Returns
        -------
        str
            Default image to use.
        """
        return self.config['status_board'].get('default_status') or None

    @property
    def img_location(self) -> str:
        """The location of image files.

        Returns
        -------
        str
            Path to image files.
        """
        return self.config['status_board']['img_location']
