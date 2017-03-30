# Variables

Variables enable dynamic responses based on the message

## `%USER%`

The username of the user who ran the command.

```
[2Cubed] !command add kittens %USER% likes kittens!
[CactusBot] Added command !kittens.

[ParadigmShift3d] !kittens
[CactusBot] ParadigmShift3d likes kittens!
```

## `%ARGN%`

The `N`th argument passed with the command, where `N` is a nonnegative integer.

```
[ParadigmShift3d] !command add throw Hey, %ARG2%, have a %ARG1%!
[CactusBot] Added command !throw.

[Alkali_Metal] !throw potato Innectic
[CactusBot] Hey, Innectic, have a potato!
```

## `%ARGS%`

All passed arguments, combined. (Excludes the command itself.)

```
[Innectic] !command add hug %USER% hugs %ARGS%!
[CactusBot] Added command !hug.

[BreachBreachBreach] !hug the whole chat
[CactusBot] BreachBreachBreach hugs the whole chat!
```

## `%COUNT%`

The number of times the command has been run.

```
[misterjoker] !command add derp Joker has derped %COUNT% times!
[CactusBot] Added command !derp.

[ripbandit] !derp
[CactusBot] Joker has derped 193 times!
```

## `%CHANNEL%`

The name of the channel.

```
[Rival_Laura] !command add welcome Welcome to %CHANNEL%'s stream!
[CactusBot] Added command !welcome.

[Epicness] !welcome
[CactusBot] Welcome to Xyntak's stream!
```

# Modifiers

Change the output of variables. To use a modifier, append `|` and the modifier to the end of the variable name.

Multiple modifiers may be chained, and will be evaluated from left to right.

## `=` (Default)
Any variable can be assigned a default by adding `=` and then whatever you want to be the default after it
```
[Alkali] !command add alkali Alkali is a %ARG1=Metal%
[CactusBot] Added command !alkali.
[Alkali] !alkali
[CactusBot] Alkali is a Metal
[Innectic] !alkali potato
[CactusBot] ALkali is a potato
```

## `upper`

Replace all lowercase letters with their uppercase equivalents.

```
%USER% -> 2Cubed
%USER|upper% -> 2CUBED
```

## `lower`

Replace all uppercase letters with their lowercase equivalents.

```
%USER% -> ParadigmShift3d
%USER|lower% -> paradigmshift3d
```

## `title`

Make the first letter and all letters following non-alphanumeric characters capitalized.

```
%ARG1% -> potatoes
%ARG1|title% -> Potatoes
```

## `reverse`

Reverse the text.

```
%USER% -> Jello
%USER|reverse% -> olleJ

%USER|reverse|title% -> Ollej
```

## `tag`

Remove the initial `@`, if it exists.

```
%ARG1% -> @xCausxn
%ARG1|tag% -> xCausxn

%ARG1% -> UnwrittenFun
%ARG1|tag% -> UnwrittenFun
```

```
[artdude543] !command add +raid Let's go raid @%ARG1|tag%! beam.pro/%ARG1|tag%
[CactusBot] Added command !raid.

[Chikachi] !raid @Innectic
[CactusBot] Let's go raid @Innectic! beam.pro/Innectic

[alfw] !raid TransportLayer
[CactusBot] Let's go raid @TransportLayer! beam.pro/TransportLayer
```

## `shuffle`

Shuffle the text.

```
%ARG1% -> eenofonn
%ARG1|shuffle% -> fnonneoe

%ARG1% -> @eenofonn
%ARG1|tag|shuffle% -> ononneef
```
