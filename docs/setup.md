# Prerequisites

* Python 3.4+
* Pip for Python 3.4+
* Git

# Linux

#### Installing Dependencies
You need Git.
Debian-Based: `sudo apt-get install git-core`

RHel-Based: `sudo yum install git-core`

Gentoo: `sudo emerge --ask dev-vcs/git`

Arch: `sudo pacman -i git`

Suse: `sudo zypper addrepo http://download.opensuse.org/repositories/devel:/tools:/scm/SLE_11_SP2/devel:tools:scm.repo && sudo zypper install git-core`

There's only two dependencies needed for CactusBot. To install them, open a terminal, and type `pip3 install tornado sqlalchemy`.

#### Configuring the Bot
To configure the bot, first run the bot with `python3 cactus.py`. This will create a base config, and close the bot. After doing that, open `config.json` with the editor of your choice. Find `auth` section. Enter the bot's username and password as shown below:

```json
...
auth: {
    "username": "myamazingname",
    "password": "mappafishf1sh"
},
...
```

After doing that, you can run the bot with `python3 cactus.py`.

# Windows
## TODO

# Thanks
Thanks for choosing CactusBot. May the potato powered cookies be forever in your favor.
