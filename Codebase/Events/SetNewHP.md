# SetNewHP
Called from the *SetUnitHealth* event in *SwarmGroup* it sets the variable *CurrentHP* to
a new value. If this value is less than or equal to zero, it calls the *DestroyUnit* event
in *SwarmGroup*.  

Target is *SwarmUnit*.  

## Node

## Inputs
|Name       |Type   |Description                |
|-----------|-------|---------------------------|
|**NewHP**  |*Float*|The new health of the unit.|

## Outputs
**None**