# GetAvailableMoveNode
Given a group's node destination, provides a random location within the bounds
of the node to which the group will travel.  

Target is *EvergladesGameMode*.  

## Node

## Inputs
|Name       |Type       |Description                    |
|-----------|-----------|-------------------------------|
|**In**     |*Exec*     |Execution pin.                 |
|**NodeID** |*Integer*  |The ID of the destination node.|

## Outputs
|Name           |Type       |Description                                    |
|---------------|-----------|-----------------------------------------------|
|**Position**   |*Vector*   |The position to which the group will travel.   |