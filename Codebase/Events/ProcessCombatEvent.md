# ProcessCombatEvent
This processes combat events that are in the respective telemetry file.  

Target is *EvergladesGameMode*.  

## Node

## Inputs
|Name           |Type               |Description                                        |
|---------------|-------------------|---------------------------------------------------|
|**Groups**     |*Array\<Integer\>* |The group ID of each unit involved in combat event.|
|**Health**     |*Array\<Float\>*   |The health of each unit involved in combat event.  |
|**NodeID**     |*Integer*          |The ID of the node where combat occured.           |
|**PlayerID**   |*Integer*          |The ID of the player.                              |
|**Units**      |*Array\<Integer\>* |The IDs of the units involved in combat event.     |

## Outputs
**None**