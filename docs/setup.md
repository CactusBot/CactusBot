# Requirements

* [Python](https://www.python.org/) 3.4+
* [`tornado`](https://www.tornadoweb.org/) (>=4.3)
* [`sqlalchemy`](https://www.sqlalchemy.org/) (>=1.0)

# Configuration

Copy `config-template.py` to `config.py`, and open `config.py` with the editor of your choice. Navigate to the `USERNAME` block, and enter the bot's Beam username and password. Put the channel you want the bot to be in `CHANNEL`

```python
…
USERNAME = "BotUsername"
PASSWORD = "BotPassword"

CHANNEL = "TargetChannel"
…
```

To keep down spam, you may wish to cache the followers, this can be done by changing the config setting to `True`
`CACHE_FOLLOWS = True`
Aditionally if you wish to only cache the users for a set time, you can change `CACHE_FOLLOWS_TIME` to a time in minutes. If left at 0, the users will be cached FOREVER (Mwahaha).

To have custom messages for events such as a follower or a subscriber change the `FOLLOW_MESSAGE`, `SUB_MESSAGE`, or `HOST_MESSAGE` to whatever you want, `{0}` in the message will be replaced with the player name.

# Control

## Bot Activation

To run CactusBot, execute `cactus.py`. The following optional arguments will alter the behavior.
- `--debug` will display logger output of level `DEBUG`. Other levels may be passed to force alternate minimum levels.

## Bot Deactivation

To deactivate CactusBot, simply send a `KeyboardInterrupt` to the script (typically done through `Ctrl-C`).

# Thanks!
Thanks for choosing CactusBot. May the potato powered cookies be forever in your favor.
