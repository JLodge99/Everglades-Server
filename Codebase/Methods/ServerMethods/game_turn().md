# game_turn()
This validates player turns and calls functions defining actions that
make up a turn including movement, combat, capture, and building knowledge output.

## Syntax
```python
game_turn(dict actions)
```

## Returns
The data returned from [game_end()](game_end().md).

## Parameters
|Parameter      |Description                                                            |
|---------------|-----------------------------------------------------------------------|
|**actions**    |The player key is the key and the value is an array of player actions. |