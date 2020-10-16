# GetGroup_Macro
Get the group belonging to an ID.  

Target is *EvergladesGameMode*.  

## Node

## Inputs
|Name       |Type       |Description    |
|-----------|-----------|---------------|
|**execute**|*Exec*     |Execution pin. |
|**SwarmID**|*Integer*  |The group's ID.|

## Outputs
|Name           |Type           |Description                        |
|---------------|---------------|-----------------------------------|
|**Group**      |*SwarmGroup*   |The group associated with the ID.  |
|**NonValid**   |*Exec*         |The group was not found.           |
|**Valid**      |*Exec*         |The group was found.               |