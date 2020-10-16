# SwarmUnit
This is the drone unit that belongs to a swarm group.  

**Class Type**&nbsp; &nbsp; &nbsp; &nbsp; Blueprint  
**Parent Class** &nbsp; &nbsp; Actor  

## Variables
|Variable               |Type                       |Description                                                                                    |
|-----------------------|---------------------------|-----------------------------------------------------------------------------------------------|
|**ControlSpeed**       |*Float*                    |The rate at which a unit can control a node.                                                   |
|**CurrentHP**          |*Float*                    |The current health of the unit.                                                                |
|**DefaultSceneRoot**   |*SceneComponent*           |The default root component.                                                                    |
|**HoverIdle**          |*TimelineComponent*        |Timeline that slightly varies unit position in the world for aesthetic purposes.               |
|**Material**           |*MaterialInstanceDynamic*  |                                                                                               |
|**MaxHP**              |*Float*                    |The maximum health of the unit.                                                                |
|**MeshActorComponent** |*ChildActorComponent*      |Component attched to unit and set to the specified class blueprint (e.g. "Tank", "Striker").   |
|**ParentGroup**        |*SwarmGroup*               |The group to which the unit belongs.                                                           |
|**SwarmID**            |*Integer*                  |The ID of the group to which the unit belongs.                                                 |
|**TargetLocation**     |*Vector*                   |A position relative to the group's *DefaultSceneRoot* that is the unit's destination.          |
|**UnitCost**           |*Float*                    |The cost of the unit.                                                                          |
|**UnitDamage**         |*Float*                    |The attack strength of the unit.                                                               |
|**UnitID**             |*Integer*                  |The ID of the unit.                                                                            |
|**UnitSpeed**          |*Float*                    |The speed of the unit.                                                                         |

## Functions
[**ConstructionScript**](../../Methods/ClientMethods/ConstructionScript_SwarmUnit.md)  

## Events
[**ChangeParent**](../../Events/ChangeParent.md)  
[**ChooseNewOffset**](../../Events/ChooseNewOffset.md)  
[**Destroy**](../../Events/Destroy.md)  
[**Event BeginPlay**](../../Events/BeginPlay_SwarmUnit.md)  
[**Event Tick**](../../Events/Tick_SwarmUnit.md)  
[**InitializeDrone**](../../Events/InitializeDrone.md)  
[**SetNewHP**](../../Events/SetNewHP.md)  

## Event Dispatchers
**None**

## Macros
[**GetDamagePercent**](../../Macros/GetDamagePercent.md)  
[**GetTargetLocation**](../../Macros/GetTargetLocation.md)  