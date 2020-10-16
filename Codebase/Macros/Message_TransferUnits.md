# MesageTransferUnits
Parses and returns data from an array of strings containing
information regarding unit transfers.  

Target is *EvergladesGameMode*.  

## Node

## Inputs
|Name       |Type               |Description    |
|-----------|-------------------|---------------|
|**execute**|*Exec*             |Execution pin. |
|**Inputs** |*Array\<String\>*  |Transfer data. |

## Outputs
|Name           |Type               |Description                    |
|---------------|-------------------|-------------------------------|
|**Group**      |*Integer*          |The group's ID.                |
|**IDsToMove**  |*Array\<Integer\>* |The IDs of units to transfer.  |
|**Node**       |*Integer*          |The node's ID.                 |
|**Player**     |*Integer*          |The player's ID.               |
|**then**       |*Exec*             |Execution pin.                 |