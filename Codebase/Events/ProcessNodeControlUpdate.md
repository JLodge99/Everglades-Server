# ProcessNodeControlUpdate
Processes a ControlUpdate event found in the telemtry file.  

Target is *EvergladesGameMode*.  

## Node

## Inputs
|Name               |Type       |Description                                                                                            |
|-------------------|-----------|-------------------------------------------------------------------------------------------------------|
|**Controlled**     |*Boolean*  |Whether the player controls the node.                                                                  |
|**ControlValue**   |*Float*    |The amount of control the player has over the node. >= 100 means the player is in control of the node. |
|**NodeID**         |*Integer*  |The ID of the node.                                                                                    |
|**PlayerID**       |*Integer*  |The ID of the player.                                                                                  |

## Outputs
**None**