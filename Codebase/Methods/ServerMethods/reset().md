# reset()
Resets the game by reinitializing the game server, players, and observations.

## Syntax
```python
reset(**kwargs)
```

## Returns
An initial game state from [_build_observations()](_build_observations().md).

## Parameters
This function uses the following keyword arguments:

|Parameter      |Description                                                                                                |
|---------------|-----------------------------------------------------------------------------------------------------------|
|**players**    |A dict with the player number (i.e. 0 or 1) as the key and an instance of the player as the value.         |
|**config_dir** |A string containing the configuration folder location.                                                     |
|**map_file**   |A string containing the map json file name with its location.                                              |
|**unit_file**  |A string containing the unit definition json file name with its location.                                  |
|**output_dir** |A string containing the location to output telemetry files.                                                |
|**pnames**     |A dict with the player number (i.e. 0 or 1) as the key and the name of the player's module as the value.   |
|**debug**      |A boolean indicating debug mode.                                                                           |