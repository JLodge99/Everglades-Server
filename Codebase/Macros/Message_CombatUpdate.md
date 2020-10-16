# Message_CombatUpdate
Parses and returns combat data from an array of strings representing said data.  

Target is *EvergladesGameMode*.  

## Node

## Inputs
|Name           |Type               |Description                        |
|---------------|-------------------|-----------------------------------|
|**exectute**   |*Exec*             |Execution pin.                     |
|**Inputs**     |*Array\<String\>*  |An array of strings of combat data.|

## Outputs
|Name           |Type               |Description                            |
|---------------|-------------------|---------------------------------------|
|**Groups**     |*Array\<Integer\>* |Group IDs of units in combat.          |
|**Health**     |*Array\<Float\>*   |The health of the units in combat.     |
|**NodeID**     |*Integer*          |The node location of combat event.     |
|**PlayerID**   |*Integer*          |The ID of the player.                  |
|**then**       |*Exec*             |Execution pin.                         |
|**Units**      |*Array\<Integer\>* |The IDs of units in combat at the node.|