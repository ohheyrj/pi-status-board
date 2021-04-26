"""Tests for config parsing."""
import pytest
from psb import conf


def test_config_read_file_not_found():
    """Test that a FileNotFoundError is raised if config file does not exist.
    """
    with pytest.raises(FileNotFoundError):
        conf.PsbConfig(config_file='conf-none.ini')


def test_config_read():
    """Test no error when config file exists and is read.
    """
    conf.PsbConfig(config_file="tests/test-config-files/conf.ini")


def test_config_root_ca():
    """Test that the correct value is returned for root CA.
    """
    config = conf.PsbConfig(config_file="tests/test-config-files/conf.ini")
    assert config.root_ca == '/etc/psb/rootCA.crt'


def test_config_iot_cert():
    """Test that the correct value is returned for the IoT cert.
    """
    config = conf.PsbConfig(config_file="tests/test-config-files/conf.ini")
    assert config.aws_iot_cert == '/etc/psb/cert.crt'


def test_config_iot_priv_key():
    """Test that the correct value is returned for the IoT private key.
    """
    config = conf.PsbConfig(config_file="tests/test-config-files/conf.ini")
    assert config.aws_iot_priv_key == '/etc/psb/private.key'


def test_config_endpoint():
    """Test that endpoint value is returned.
    """
    config = conf.PsbConfig(config_file="tests/test-config-files/conf.ini")
    assert config.endpoint == "endpoint.iot.us-east-1.amazonaws.com"


def test_config_port():
    """Test that the port is returned if value is in config.
    """
    config = conf.PsbConfig(config_file="tests/test-config-files/conf-with-port.ini")
    assert config.port == "1234"


def test_config_port_no_websocket():
    """Test that the default port is returned when not using websockets.
    """
    config = conf.PsbConfig(config_file="tests/test-config-files/conf.ini")
    assert config.port == 8883


def test_config_port_websocket():
    """Test that the default port is returned when not using websockets.
    """
    config = conf.PsbConfig(config_file="tests/test-config-files/conf-use-websocket.ini")
    assert config.port == 443


def test_config_default_status():
    """Test that the correct default_status from config is returned.
    """
    config = conf.PsbConfig(config_file="tests/test-config-files/conf.ini")
    assert config.default_status == "idle"


def test_config_img_location():
    """Test that the correct img_location from config is returned.
    """
    config = conf.PsbConfig(config_file="tests/test-config-files/conf.ini")
    assert config.img_location == "/etc/psb/img"


def test_config_client_id():
    """Test that the correct client_id from config is returned.
    """
    config = conf.PsbConfig(config_file="tests/test-config-files/conf.ini")
    assert config.client_id == "test_client_id"


def test_config_incorrect_mode_value_error():
    """Test that a ValueError exception is raise when mode is not a valid value.
    """
    with pytest.raises(ValueError):
        conf.PsbConfig(config_file='tests/test-config-files/conf-incorrect-mode.ini')


def test_config_websockets_and_certs_system_exit():
    """Test that a SystemExit exception is raise when use_websockets is true and certs provided.
    """
    with pytest.raises(SystemExit):
        conf.PsbConfig(config_file='tests/test-config-files/conf-use-websocket-certs-provided.ini')


def test_config_no_certs_system_exit():
    """Test that a SystemExit exception is raise when no certs provided when not using websockets`.
    """
    with pytest.raises(SystemExit):
        conf.PsbConfig(config_file='tests/test-config-files/conf-no-certs.ini')
