# NodeControlUpdate
Called from *ProcessNodeControlUpdate* event in *EvergladesGameMode*, this updates
*ControlRatio* and determines if a player occupies the node. If so, it *SetControlColor*
from *NodeControlDome* to change the node to the player's color.  

Target is *NodePoint*.  

## Node

## Inputs
|Name               |Type       |Description                                                            |
|-------------------|-----------|-----------------------------------------------------------------------|
|**Controlled**     |*Boolean*  |Whether this node is controlled by the player (not used in function)   |
|**Control Value**  |*Float*    |The amount of control points the player has for this node on this turn.|
|**PlayerID**       |*Integer*  |The ID of the player.                                                  |

## Outputs
**None**