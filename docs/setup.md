# Requirements

* [Python](https://www.python.org/) 3.4+
* [`tornado`](https://www.tornadoweb.org/) (>=4.3)
* [`sqlalchemy`](https://www.sqlalchemy.org/) (>=1.0)

# Configuration

Copy `data/config-template.json` to `data/config.json`, and open `data/config.json` with the editor of your choice. Navigate to the `auth` block, and enter the bot's Beam username and password.

```json
…
"auth": {
    "username": "YourBotName",
    "password": "p455w0rd"
},
…
```

# Control

## Bot Activation

To run CactusBot, execute `cactus.py`. The following optional arguments will alter the behavior.
- `--debug` will display logger output of level `DEBUG`. Other levels may be passed to force alternate minimum levels.
- `--quiet` will ensure no messages are sent to Beam chat. The output will be displayed in console, however, as if the messages were sent.

## Bot Deactivation

To deactivate CactusBot, simply send a `KeyboardInterrupt` to the script (typically done through `Ctrl-C`).

# Thanks!
Thanks for choosing CactusBot. May the potato powered cookies be forever in your favor.
