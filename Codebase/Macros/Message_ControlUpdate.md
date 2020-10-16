# Message_ControlUpdate
Parses and returns data from an array of control data that is represented as strings.  

Target is *EvergladesGameMode*.  

## Node

## Inputs
|Name       |Type               |Description    |
|-----------|-------------------|---------------|
|**Inputs** |*Array\<String\>*  |Control data.  |

## Outputs
|Name               |Type       |Description                                        |
|-------------------|-----------|---------------------------------------------------|
|**Controlled**     |*Boolean*  |Whether the player controls the node.              |
|**ControlValue**   |*Float*    |The percentage a node is under a player's control. |
|**NodeID**         |*Integer*  |The ID of the node.                                |
|**PlayerID**       |*Integer*  |The ID of the player.                              |