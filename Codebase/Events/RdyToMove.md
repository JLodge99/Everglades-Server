# RdyToMove
Sets *CurrentConnectionSpline* and *GroupTargetLocation*. Also sets *CurrentDistanceAlongSpline*
to 0 and *StandingOrder* to "RdyMove". Called from *RdyToMoveEvent* in *EvergladesGameMode*.  

Target is *SwarmGroup*.  

## Node

## Inputs
|Name               |Type               |Description                                            |
|-------------------|-------------------|-------------------------------------------------------|
|**NewTarget**      |*Vector*           |The position in the world of the group's destination.  |
|**TargetSpline**   |*ConnectionSpline* |The spline the group will travel along.                |

## Outputs
**None**