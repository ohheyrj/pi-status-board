# Pi Status Board (psb)

![GitHub Workflow Status](https://img.shields.io/github/workflow/status/rj175/pi-status-board/Python%20package)
![GitHub issues](https://img.shields.io/github/issues/rj175/pi-status-board)
![GitHub](https://img.shields.io/github/license/rj175/pi-status-board)
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/psb)
![PyPI - Downloads](https://img.shields.io/pypi/dm/psb)

The Pi Status Board (psb) can be used to display text or pre-defined images on an eInk display attached to a Raspberry Pi. It is controlled via AWS IoT Core and uses mqtt.

## Requirements

Psb has been designed to work on a Raspberry Pi using and an [Inky pHAT display.](https://shop.pimoroni.com/products/inky-phat)

## Install

Use package manager `pip` or `pipenv` to install psb:

```bash
pip install psb
```

## Usage

Psb is a command line utility. The configuration file should be stored in `/etc/psb/conf.ini`.  A sample config file can be found within the [resources folder](resources/conf.ini).

For a full breakdown of all configuration options please see the [configuration](docs/configuration.md) documentation.

To run psb, run the following command without any arguments:

```bash
psb
```

Psb will connect to the mqtt broker specified in the configuration file.

To trigger the changing of the display, a message needs to be sent to the configured mqtt topic. There are two types of messages that can be processed.

For a text message the message sent to the topic should be:

```json
{
    "type": "text",
    "data": "This is a message"
}
```

For images, the data field should contain the name of the image to display without the extension:

```json
{
    "type": "image",
    "data": "meeting"
}
```

### Running as a service

If you would like to run psb as a service, copy the example systemd [service file](resources/status-board.serice) to `/lib/systemd/system/pi-status-board.service`. You may need to change the path to the location of psb, this can be found by using the `whereis` command:

```bash
> whereis psb
psb: /etc/psb /home/pi/.local/bin/psb
```

After creating the file, reload the systemd daemon:

```bash
> sudo systemctl daemon-reload
```

You should now be able to see the status of the service by running:

```bash
> sudo systemctl status pi-status-board
```

## Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.

## License

Released under GNU General Public License v3.0.
