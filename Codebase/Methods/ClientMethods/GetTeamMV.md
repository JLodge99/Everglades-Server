# GetTeamMV
Given a team (red or blue), returns a slate brush representing
the machine vision image associated with that player's current turn.  

Target is *EvergladesGameMode*.  

## Node

## Inputs
|Name           |Type       |Description                                |
|---------------|-----------|-------------------------------------------|
|**In**         |*Exec*     |Execution pin.                             |
|**BlueTeam**   |*Boolean*  |Whether this is the blue team (Player 1).  |

## Outputs
|Name       |Type           |Description                                            |
|-----------|---------------|-------------------------------------------------------|
|**Brush**  |*SlateBrush*   |The machine vision image of the player's current turn. |