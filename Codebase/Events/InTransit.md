# InTransit
Sets *GroupTargetLocation* and sets *StandingOrder* to "In Transit". It then
calls the *IncrementalMove* macro. Called from *InTransitEvent* in *EvergladesGameMode*.  

Target is *SwarmGroup*.  

## Node

## Inputs
|Name               |Type       |Description                                                        |
|-------------------|-----------|-------------------------------------------------------------------|
|**FinalLocation**  |*Vector*   |The coordinates of the group's destination position in the world.  |

## Outputs
**None**