## `!command`
The `!command` command is used for manipulation of custom commands. It may only be run by users of rank *Mod* or above.

- To add a command, use `!command add <command> <response>`.
    - [`%targets%`](/targets) may also be utilized to enable dynamic responses.
    - If `<command>` is of the form `x-y`, it may be run later as either `!x-y` and `!x y`.
    - To limit the users who may run the command, append one of the prefixes to the beginning of the name.
        - `+` - Moderator-Only
        - `$` - Subscriber-Only

>     [2Cubed] !command add cactusbot CactusBot! :cactus
>     [CactusBot] Added command !cactusbot.
>     [2Cubed] !cactusbot
>     [CactusBot] CactusBot! :cactus

>     [2Cubed] !command add cactusbot-twitter twitter.com/CactusBotBeam
>     [CactusBot] Added command !cactusbot-twitter.
>     [ParadigmShift3d] !cactusbot-twitter
>     [CactusBot] twitter.com/CactusBotBeam

>     [Jello] !cactusbot twitter
>     [CactusBot] twitter.com/CactusBotBeam

>     [2Cubed] !cactusbot
>     [CactusBot] CactusBot! :cactus

>     [ParadigmShift3d] !command add +raid Let's go raid %arg1%! beam.pro/%arg1%
>     [Innectic] !raid Matt
>     [CactusBot] Let's go raid Matt! beam.pro/Matt

>     [Innectic] !command add $fancy Look how fancy I am! I'm a subscriber!  O:-)
>     [Xyntak] !fancy
>     [CactusBot] Look how fancy I am! I'm a subscriber!  O:-)

- To remove a command, use `!command remove <name>`.

>     [2Cubed] !command remove waffle
>     [CactusBot] Removed command !waffle.
>     [Innectic] Oh no, my waffles! /cry

- To list custom commands, use `!command list`.

>     [ParadigmShift3d] !command list
>     [CactusBot] Commands: potato, waffle, hamster

## `!quote`
The `!quote` command manages quotes. It may only be run by users of rank *Mod* or above.

- To recall a random quote, use `!quote`.

>     [ParadigmShift3d] !quote
>     [CactusBot] ":fish :fish :fish :fish :fish :fish :fish :fish" -Matt

- To recall a specific quote based on numerical ID, use `!quote <id>`.

>     [BreachBreachBreach] !quote 8
>     [CactusBot] "...*silence*..." -Stanley

- To add a quote, use `!quote add <quote>`.

>     [Innectic] !quote add "Potatoes!" - 2Cubed
>     [CactusBot] Added quote with ID 9.

- To remove a quote, use `!quote remove <id>`.

>     [ParadigmShift3d] !quote remove 9
>     [CactusBot] Removed quote with ID 9.


## `!repeat`
The `!repeat` command manages commands that are set to run at a certain interval. It may only be run by users of rank *Mod* or above.

- To add a repeat, use `!repeat add <interval> <command> [arguments]`, where `<interval>` is in seconds.

>     [Innectic] !command add space :%arg1%inaspacesuit
>     [CactusBot] Added command !space.
>     [ParadigmShift3d] !repeat add 600 space %channel%
>     [CactusBot] Repeating command '!space' every 600 seconds.

- To remove a repeat, use `!repeat remove <command>`.

>     [2Cubed] !repeat remove space
>     [CactusBot] Removed repeat for command !space.

- To list all repeats, use `!repeat list`.

>     [ParadigmShift3d] !repeat list
>     [CactusBot] Repeats: follow 3600, tweet 1800


## `!social`
The `!social` command retrieves social media data from the Beam API.

- To retrieve links for all services, use `!social`.

>     [ParadigmShift3d] !social
>     [CactusBot] Youtube: https://youtube.com/2CubedTech, Twitter: https://twitter.com/2CubedTech

- To retrieve links for specific services, use `!social <services>`, where `<services>` is a space-delimited list of services.

>     [Alkali_Metal] !social twitter
>     [CactusBot] Twitter: https://twitter.com/CactusBotBeam


## `!spamprot`
The `!spamprot` command changes spam protection options. It may only be run by users of rank *Mod* or above.

- To update the maximum amount of characters of a message, use `!spamprot length <amount>`, where `<amount>` is the desired length. The default is 256.

>     [ParadigmShift3d] !spamprot length 100
>     [CactusBot] Maximum message length set to 100.

- To update the maximum capital characters allowed in a message, use `!spamprot caps <amount>`, where `<amount>` is the desired amount of capitals. The default is 32.

>     [2Cubed] !spamprot caps 20
>     [CactusBot] Maximum capitals per message set to 20.

- To update the maximum emoticons allowed in a message, use `!spamprot emotes <amount>`, where `<amount>` is the desired amount of emoticons. The default is 8.

>     [Innectic] !spamprot emotes 4
>     [CactusBot] Maximum emotes per message set to 4.
>     [duke] :beer :mappa <3 :cactus

- To enable or disable links in messages, use `!spamprot links <value>`, where `<value>` is either `true` or `false`. The default is `false`.

>     [ParadigmShift3d] !spamprot links true
>     [CactusBot] Links are now allowed.


## `!friend`
The `!friend` command allows users to be ignored by spam protection. It may only be run by users of rank *Mod* or above.

- To friend a user, use `!friend <username>`.

>     [2Cubed] !friend Stanley
>     [CactusBot] Added @Stanley as a friend.
