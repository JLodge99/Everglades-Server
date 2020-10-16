# ProcessTransferUnitsUpdate
Processes unit transfer events found in the telemetry file.  

Target is *EvergladesGameMode*.  

## Node

## Inputs
|Name           |Type               |Description                                        |
|---------------|-------------------|---------------------------------------------------|
|**Group**      |*Integer*          |The target group.                                  |
|**Node**       |*Integer*          |The node ID. (unused)                              |
|**Player**     |*Integer*          |The player ID. (unused)                            |
|**UnitsToMove**|*Array\<Integer\>* |The ID of units to transfer to the target group.   |

## Outputs
**None**