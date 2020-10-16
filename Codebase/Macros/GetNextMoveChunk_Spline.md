# GetMoveChunk_Spline
Calculates the new postion of a group moving along a spline based on the distance
traveled. If it's no longer on the spline, it calls *GetNextMoveChunk_Normal*.  

Target is *SwarmGroup*.  

## Node

## Inputs
**None**

## Outputs
|Name           |Type       |Description                    |
|---------------|-----------|-------------------------------|
|**MovementDir**|*Vector*   |Only outputs (0, 0, 0).        |
|**Position**   |*Vector*   |The new position of the group. |