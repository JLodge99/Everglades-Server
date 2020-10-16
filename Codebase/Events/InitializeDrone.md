# InitializeDrone
Called from the *InitializeGroup* event in *SwarmGroup*, this initializes the unit's
variables, mesh, and position. Data is read from the *SwarmUnitTypes* data table.  

Target is *SwarmUnit*.  

## Node

## Inputs
|Name           |Type           |Description                            |
|---------------|---------------|---------------------------------------|
|**ParentGroup**|*SwarmGroup*   |The group to which the unit belongs.   |
|**Type**       |*String*       |The type of the unit (e.g. "Tank").    |
|**UnitID**     |*Integer*      |The unit's ID.                         |

## Outputs
**None**