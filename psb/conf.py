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
        self.config_file = Path(config_file)
        if self.config_file.is_file():
            self.config = ConfigParser()
            self.config.read(self.config_file)
        else:
            logger.error(f'Cannot find config file at {config_file}')
            raise FileNotFoundError

    @property
    def root_ca(self) -> str:
        """Path to AWS root CA.conf

        Returns
        -------
        str
            The path to the root CA file.
        """
        return self.config['certs']['root_ca']

    @property
    def aws_iot_cert(self) -> str:
        """Path to AWS IoT thing certificate.conf

        Returns
        -------
        str
            The path to the certificate.
        """
        return self.config['certs']['iot_cert']

    @property
    def aws_iot_priv_key(self) -> str:
        """Path to the AWS IoT thing private key.conf

        Returns
        -------
        str
            The path to the private key.
        """
        return self.config['certs']['iot_priv_key']

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
            return self.config['aws_iot']['use_websockets']
        except KeyError:
            return None

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
