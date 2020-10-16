# RemoveUnit
It removes the unit from the *GroupUnits* array and calls *RemoveGroup* from *EvergladesGameMode*
if this was the only unit in the group. Called from *ChangeParent* event in *SwarmUnit*.  

Target is *SwarmGroup*.  

## Node

## Inputs
|Name       |Type       |Description        |
|-----------|-----------|-------------------|
|**Unit**   |*SwarmUnit*|The unit to remove.|

## Outputs
**None**