# Message_Init
Parses and returns data from an array of strings containing
information regarding an initial group to be created.  

Target is *EvergladesGameMode*.  

## Node

## Inputs
|Name       |Type               |Description    |
|-----------|-------------------|---------------|
|**execute**|*Exec*             |Execution pin. |
|**Inputs** |*Array\<String\>*  |Group data.    |

## Outputs
|Name               |Type               |Description                                        |
|-------------------|-------------------|---------------------------------------------------|
|**Group**          |*Integer*          |The group's ID.                                    |
|**NodeID**         |*Integer*          |The node's ID.                                     |
|**Player**         |*Integer*          |The player's ID.                                   |
|**then**           |*Exec*             |Execution pin.                                     |
|**UnitCounts**     |*Array\<String\>*  |The counts of each unit type in the group.         |
|**UnitStartIDs**   |*Array\<String\>*  |The start index of each unit type from this group. |
|**UnitTypes**      |*Array\<String\>*  |The types of units in the group.                   |