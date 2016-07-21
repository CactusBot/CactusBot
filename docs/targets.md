## `%name%`
The `%name%` target is replaced with the name of the user who runs the command.

>     [ParadigmShift3d] !command add approve My name is %name%, and I approve this message!
>     [CactusBot] Added command !approve.

>     [ParadigmShift3d] !approve
>     [CactusBot] My name is ParadigmShift3d, and I approve this message!

>     [DnatorGames] !approve
>     [CactusBot] My name is DnatorGames, and I approve this message!

## `%argN%`
The `%argN%` target is replaced with the `N`th argument passed with the command, where `N` is a positive integer.

>     [Innectic] !command add raid Let's raid %arg1%, with the message %arg2%! beam.pro/%arg1%
>     [CactusBot] Added command !raid.

>     [Blizzy] !raid Beam #CactusRaid
>     [CactusBot] Let's raid Beam, with the message #CactusRaid! beam.pro/Beam

>     [MindlessPuppets] !raid
>     [CactusBot] Not enough arguments!

## `%args%`
The `%args%` target is replaced with all of the arguments passed.

>     [2Cubed] !command add hug Here's a giant hug for you, %args%! <3
>     [CactusBot] Added command !hug.

>     [pylang] !hug CactusBot users
>     [CactusBot] Here's a giant hug for you, CactusBot users! <3

## `%count%`
The `%count%` target is replaced with the number of times the command has been run since creation.

>     [Innectic] !command add rip The streamer has died %count% times!
>     [CactusBot] Added command !rip.

>     [QuirkySquid] !rip
>     [CactusBot] The streamer has died 1 times!

>     [ParadigmShift3d] !rip
>     [CactusBot] The streamer has died 2 times!

## `%channel%`
The `%channel%` target is replaced with the name of the channel.

>     [ParadigmShift3d] !command add welcome Welcome to %channel%'s stream!
>     [CactusBot] Added command !welcome.

>     [ProbablePrime] !welcome
>     [CactusBot] Welcome to 2Cubed's stream!
