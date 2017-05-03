# `!command`

Minimum Role Required: **Moderator**

## `!command add [limiter]<command> <response...>`

Create a custom command.

If `<command>` is in the form of `main-sub`, it may be run later as either `!main-sub` or `!main sub`.

- `limiter` signifies the minimum role required to access the command.

  - `+`: Moderator-Only
  - `$`: Subscriber-Only

`%VARIABLES%` may be used to create dynamic responses.

If `!<command>` already exists, its response is updated.

```
[Jello] !command add waffle Time to feed %ARGS% some waffles!
[CactusBot] Added command !waffle.
[BreachBreachBreach] !waffle Innectic
[CactusBot] Time to feed Innectic some waffles!
```

## `!command remove <command>`

Remove a custom command.

```
[Epicness] !command remove waffle
[CactusBot] Removed command !waffle.
[Innectic] Oh no, my waffles! /cry
```

## `!command list`

List all custom commands.

```
[Xyntak] !command list
[CactusBot] Commands: explosions, kittens, potato
```

## `!command enable <command>`

Enable a custom command.

```
[artdude543] !command enable typescript
[CactusBot] Command !typescript has been enabled.
```

## `!command disable <command>`

Disable a custom command.

```
[Innectic] !command disable typescript
[CactusBot] Command !typescript has been disabled.
```

## `!command count <command> [action]`

Retrieve or modify the `count` value for a custom command.

If `action` is not specified, the `count` is returned.

```
[AlphaBravoKilo] !command count derp
[CactusBot] !derp's count is 9001.
```

Otherwise, the value is modified.

If `action` is a number (optionally preceded by an `=`), the count value is set to that exact number.

```
[Kondrik] !command count derp 9053
[CactusBot] Count updated.
```

Otherwise, `action` may begin with either a `+` or `-`, to increase or decrease the count value, respectively.

```
[MindlessPuppetz] !command count derp +12
[CactusBot] Count updated.
```

## `!command role <command> [role]`

Retrieve or set the `role` of a custom command.

If `role` is not supplied, the current `role` is returned.

```
[EvilNotion] !command role magical
[CactusBot] Minimum role for !magical is 'Moderator'
```

Otherwise, the role is set:

```
[HauntedKnight] !command role magical User
[CactusBot] Updated role for !magical to 'User'
```
