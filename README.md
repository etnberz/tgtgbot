# tgtgbot

This service sends you a notification when your favorite Too Good Too Go item is available.

## Installation

In the project folder run the following line to install the environment locally:

```shell script
pip install .
```

To get your Too Good To Go credentials use this snippet

```python
from tgtg import TgtgClient


def get_credentials():
    client = TgtgClient(email="maxime.caitucoli@live.fr")
    credentials = client.get_credentials()
    print(credentials)
```

To get your telegram bot and credentials follow this
[tutorial](https://sean-bradley.medium.com/get-telegram-chat-id-80b575520659).

Declare your credential as env var:
- TGTG_ACCESS_TOKEN
- TGTG_REFRESH_TOKEN
- TGTG_USER_ID
- TGTG_COOKIE
- TGTG_TELEGRAMBOT_TOKEN
- TGTG_TELEGRAMBOT_CHAT_ID

## Quickstart

First build the docker image:

```docker build -t tgtgbot .```

If you are in the tgtgbot folder else, change `.` by the correct location.

To make it run:

`./run.sh`

If you have permission issues with `run.sh`, run the following command:

`chmod u+x run.sh`


## Project status

WIP

### Current features

- Send a Telegram message when the Too Good Too Go item you want is available on the platform.

### Known limitations / Bugs

## Acknowledgements

### Contributors

Maxime Caïtucoli

