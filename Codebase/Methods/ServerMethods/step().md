# step()
This function is called at the end of every turn to report player and game state.

## Syntax
```python
step(dict actions)
```

## Returns
Four things are returned. The first is observation, returned from a call to 
[_build_observations()](_build_observations().md). The second, reward, is an integer
with values -1 for a loss, 0 for a tie, and 1 for a win. Done, the third piece of
returned data, is an integer flag that changes from zero to one when a winning
condition is met. This signals the end of the game loop. The fourth is info,
a dict that is **empty** and is not referenced, currently.

## Parameters
|Parameter      |Description                                                            |
|---------------|-----------------------------------------------------------------------|
|**actions**    |The player key is the key and the value is an array of player actions. |