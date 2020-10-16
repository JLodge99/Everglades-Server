# SwarmGroup
A group of drone units.

**Class Type**&nbsp; &nbsp; &nbsp; &nbsp; Blueprint  
**Parent Class** &nbsp; &nbsp; Actor  

## Variables
|Variable                       |Type                       |Description                                                                |
|-------------------------------|---------------------------|---------------------------------------------------------------------------|
|**Cube**                       |*StaticMeshComponent*      |Cube mesh used when simplified map is **True**.                            |
|**CurrentConnectionSpline**    |*ConnectionSpline*         |The spline the group is moving along.                                      |
|**CurrentDistanceAlongSpline** |*Float*                    |The group's distance traveled along a spline in Unreal units.              |
|**CurrentNode**                |*Integer*                  |The ID of the node the group occupies or, if in transit, the source node.  |
|**CurrentTargetLocation**      |*Vector*                   |Where the group's current position should be this tick.                    |
|**DefaultSceneRoot**           |*SceneComponent*           |The default root component.                                                |
|**FacingDirection**            |*Rotator*                  |*unused*                                                                   |
|**GameModeRef**                |*EvergladesGameMode*       |A reference to the game mode.                                              |
|**GroupHP**                    |*Float*                    |The total health of the units in the group.                                |
|**GroupID**                    |*Integer*                  |The ID of the group.                                                       |
|**GroupSpeed**                 |*Float*                    |The speed of the group. Equal to the speed of the slowest member unit.     |
|**GroupTargetLocation**        |*Vector*                   |The position of the group's travel destination in the world.               |
|**GroupUnits**                 |*Array\<SwarmUnit\>*       |The collection of units in the group.                                      |
|**InNode**                     |*NodePoint*                |*unused*                                                                   |
|**MovementDir**                |*Vector*                   |For debugging purposes, the direction the group should be moving this tick.|
|**PlayerID**                   |*Integer*                  |The ID of the player.                                                      |
|**PotentialAttackers**         |*Array\<SwarmGroup\>*      |Other groups that have overlapped this group's sphere component.*unused*   |
|**ReceivedMoveOrder**          |*Boolean*                  |Whether the group should move this tick.                                   |
|**SimplifiedMat**              |*MaterialInstanceDynamic*  |Dynamic material for use when simplified map is **True**.                  |
|**Sphere**                     |*SphereComponent*          |Sphere component used for overlapping.                                     |
|**StandingOrder**              |*String*                   |Represents the group's current command.                                    |
|**TextRender**                 |*TextRenderComponent*      |A debug text placed over the group.                                        |


## Functions
[**ConstructionScript**](../../Methods/ClientMethods/ConstructionScript_SwarmGroup.md)  
[**GetUnit**](../../Methods/ClientMethods/GetUnit_SwarmGroup.md)  
[**ProcessStandingOrder**](../../Methods/ClientMethods/ProcessStandingOrder.md)  
[**SetDebugText**](../../Methods/ClientMethods/SetDebugText.md)  

## Events
[**AddUnit**](../../Events/AddUnit_SwarmGroup.md)  
[**AttackUnit**](../../Events/AttackUnit.md)  
[**CalcHealth**](../../Events/CalcHealth.md)  
[**DestroyUnit**](../../Events/DestroyUnit.md)  
[**Event BeginPlay**](../../Events/BeginPlay_SwarmGroup.md)  
[**Event Tick**](../../Events/Tick_SwarmGroup.md)  
[**InitializeBlankGroup**](../../Events/InitializeBlankGroup.md)  
[**InitializeGroup**](../../Events/InitializeGroup.md)  
[**InTransit**](../../Events/InTransit.md)  
[**MoveOnSpline**](../../Events/MoveOnSpline.md)  
[**MoveOrder**](../../Events/MoveOrder.md)  
[**On Component Begin Overlap**](../../Events/ComponentBeginOverlap_SwarmGroup.md)  
[**On Component End Overlap**](../../Events/ComponentEndOverlap_SwarmGroup.md)  
[**RdyToMove**](../../Events/RdyToMove.md)  
[**RemoveUnit**](../../Events/RemoveUnit.md)  
[**SetUnitHealth**](../../Events/SetUnitHealth.md)  
[**ToggleSwarmVisibility**](../../Events/ToggleSwarmVisibility.md)

## Event Dispatchers
[**AttackCompleted**](../../Dispatchers/AttackCompleted.md)  
[**EventCompleted**](../../Dispatchers/EventCompleted.md)  

## Macros
[**BuildDebugString**](../../Macros/BuildDebugString.md)  
[**CalculateGroupHealth**](../../Macros/CalculateGroupHealth.md)  
[**DebugCreation**](../../Macros/DebugCreation.md)  
[**GetNextMoveChunk_Normal**](../../Macros/GetNextMoveChunk_Normal.md)  
[**GetNextMoveChunk_Spline**](../../Macros/GetNextMoveChunk_Spline.md)  
[**GetRandomAttacker**](../../Macros/GetRandomAttacker.md)  
[**GetRandomUnit**](../../Macros/GetRandomUnit.md)  
[**IncrementalMove**](../../Macros/IncrementalMove.md)  