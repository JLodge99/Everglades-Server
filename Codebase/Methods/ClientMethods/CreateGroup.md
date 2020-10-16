# CreateGroup
Creates a group of units, a swarm.  

Target is *EvergladesGameMode*.  

## Node

## Inputs
|Name               |Type               |Description                                    |
|-------------------|-------------------|-----------------------------------------------|
|**In**             |*Exec*             |Execution pin.                                 |
|**PlayerID**       |*Integer*          |The player's ID.                               |
|**ID**             |*Integer*          |The group's ID.                                |
|**StartNode**      |*Integer*          |The node at which the group starts.            |
|**UnitTypes**      |*Array\<String\>*  |The types of units in the group.               |
|**UnitStartIDs**   |*Array\<String\>*  |The indices at which a unit type is located.   |
|**UnitCount**      |*Array\<String\>*  |The amount of each type of unit in the group.  |
|**Empty**          |*Boolean*          |Whether the group is empty.                    |

## Outputs
**None**