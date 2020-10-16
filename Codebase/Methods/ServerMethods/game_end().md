# game_end()
This calculates the current score and checks for game-ending conditions. It builds
game score data and places it in a string to be used for telemetry files. If the
game is over, it calls [write_output()](write_output()) to create telemetry files.

## Syntax
```python
game_end()
```

## Returns
Two pieces of data. The first is a dict with player key as the key and an integer for the
player's score as the value. The second is an integer representing the game's status. The
statuses are as follows:

|Status |Game State     |Description                                        |
|-------|---------------|---------------------------------------------------|
|0      |In progress    |The game has not met any game-ending conditions.   |
|1      |Time expired   |The game reached the maximum number of turns.      |
|2      |Base captured  |A player has captured the opponent's base.       |
|3      |Annihiliation  |A player has destroyed all enemy units.            |
 
## Parameters
**None**