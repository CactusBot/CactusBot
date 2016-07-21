# CactusBot Setup

If you're planning on hosting your own copy of CactusBot, read on.

It's pretty simple, but if you end up deciding you don't want to, we're more than happy to provide fairly stable hosting for you for free!

## Initial Setup
You're going to have to go through a few steps before you're up and running! Nothing too complicated, but we're going to need a few different things installed first!

Note, we're going to give these instructions assuming you're running a Linux distro. We're developing and hosting on Ubuntu 14.04/15.10/16.04 and so CactusBot is known to work on there. These instructions will work for any Debian-based distro.

### Installation

* First, you'll need to have `git` and Python3 installed. Ubuntu 16.04 comes with  Python 3.5.1, so that's not going to have to be installed, but you will have to install `git` if you're intending on easily keeping your CactusBot instance up-to-date.

 If you're not as worried about having the latest & greatest release, you can skip this step and [manually download the ZIP from GitHub](https://github.com/CactusBot/CactusBot/archive/master.zip), but we strongly suggest you utilize `git`.

 On Ubuntu, this is fairly straightforward, just run `sudo apt-get install git`.

* Once git is installed, we'll need to install pip for Python 3. This is also easily installable via `sudo apt-get install python3-pip`.

* Once pip3 is installed, we're going to have to install a number of Python modules:

 * `tornado`
 * `sqlalchemy`

 The `coloredlogs` module is optional, but it is highly recommended. It makes things look a lot nicer

### Configuration

Once we have everything installed, we're going to have to configure the bot.

In the `data` folder there is a file called `config-template.json`. We're going to copy that and create the config file that CactusBot uses.

To do this, just run `cp data/config-template.json data/config.json`. This will create the file that CactusBot is expecting, and will allow us to continue configuring your bot.

Once the file has been copied, we're going to have to change a few values in the config file. Most of the options are just fine being left alone, but you can tweak them if you want later.

Here are the options we need to edit:

 * `channel`: Change this to channel name of whatever channel you want CactusBot to connect to. For example:

  >     {
  >        "channel": "channel", <-- change this string
  >        "autorestart": true,
  >        ...
  >     }

 * `auth`: You're going to have to add the username and password of the bot account you want to use.

 If you want a custom name, then just create that account on Beam and add the login information as labeled. Otherwise, if you want to use the CactusBot account, you'll need to have us host the instance for you.

  >     "auth": {
  >        "username": "USERNAME",
  >       "password": "PASSWORD"
  >      },

 * `points` (optional): You can adjust these values if you want to utilize the currency/viewer reward system built into CactusBot.

   You can customize the currency name, as well as how often currency is awarded and how many are awarded at a time:

  >     "points": {
  >        "name": "coin",
  >        "per_interval": 5,
  >        "interval": 1,
  >        "enabled": true
  >     }  

You can edit the other configuration options, but these are the only ones that are required to get CactusBot up and running.

## Profit!
Once you complete all of the above tasks, you can go ahead and launch CactusBot via `python3 cactus.py`!

Thank you for choosing CactusBot and may the cookie-munching hamsters be ever in your favor!
