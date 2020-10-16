# game_init()
Initializes the game by calling functions to initialize players, their
groups, and the groups' units. It builds group initialization data and places
it in a string to be used for telemetry files.

## Syntax
```python
game_init(dict player_dat)
```

## Returns
**None**

## Parameters
|Parameter      |Description                                                                                        |
|---------------|---------------------------------------------------------------------------------------------------|
|**player_dat** |The player key is the key and and the value is a dict of unit types and number of units per group. |