# DebugCreation
Creates a string for debugging purposes stating the group ID, player ID, the list of unit counts,
and the list of unit types.  

Target is *SwarmGroup*.  

## Node

## Inputs
|Name           |Type               |Description                                    |
|---------------|-------------------|-----------------------------------------------|
|**execute**    |*Exec*             |Execution pin.                                 |
|**GroupID**    |*Integer*          |The group's ID.                                |
|**PlayerID**   |*Integer*          |The player's ID.                               |
|**UnitCounts** |*Array\<String\>*  |The amount of each type of unit in the group.  |
|**UnitTypes**  |*Array\<String\>*  |The types of units in the group.               |

## Outputs
|Name       |Type   |Description    |
|-----------|-------|---------------|
|**then**   |*Exec* |Execution pin. |