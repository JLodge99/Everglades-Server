# board_state()
This finds the current state of the Everglades game board for the given player.

## Syntax
```python
board_state(int player_num)
```

## Returns
A numpy array. The first index is the turn number followed by four indices repeating
for each node in the game. The indices are:

|Index              |Description                                                                                            |
|-------------------|-------------------------------------------------------------------------------------------------------|
|0                  |Integer: The turn number.                                                                              |
|(index - 1) % 4 = 0|Integer: 0/1 used as Boolean. The node has a fortress bonus.                                           |
|(index - 1) % 4 = 1|Integer: 0/1 used as Boolean. The node has watchtower a bonus.                                         |
|(index - 1) % 4 = 2|Integer: The percent the node is controlled [-100:100]. Player 0 is positive, Player 1 is negative.    |
|(index - 1) % 4 = 3|Integer: The number of opposing player units at the node.                                              |

## Parameters
|Parameter      |Description        |
|---------------|-------------------|
|**player_num** |The player's key.  |