# NodePoint
Class containing the data related to the node.

**Class Type**&nbsp; &nbsp; &nbsp; &nbsp; Blueprint  
**Parent Class** &nbsp; &nbsp; Actor  

## Variables
|Variable                   |Type                       |Description                                                                                                                                                                    |
|---------------------------|---------------------------|-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
|**ArenaWidth**             |*Float*                    |The radius of the node in server units.                                                                                                                                        |
|**Connections**            |*Array\<ConnectionSpline\>*|The collection of *ConnectionSplines* that leave this node.                                                                                                                    |
|**ControlDome**            |*NodeControlDome*          |The *NodeControlDome* associated with this node.                                                                                                                               |
|**ControllingPlayer**      |*Integer*                  |The ID of the player attempting to capture the node or -1 (default).                                                                                                           |
|**ControlPoints**          |*Integer*                  |The amount of control points the node is worth.                                                                                                                                |
|**ControlRatio**           |*Float*                    |How much control a player has over a node, from 0 to 1.                                                                                                                        |
|**ControlValue**           |*Float*                    |The amount of control points a player has accrued for the node. Dependent on occupying unit types and amounts. When *ControlValue* == *MaxControlPoints*, the node is captured.|
|**DefaultSceneRoot**       |*SceneComponent*           |The default root component.                                                                                                                                                    |
|**DefenseBonus**           |*Float*                    |A defense multiplier for units protecting the node.                                                                                                                            |
|**MaxControlPoints**       |*Integer*                  |The maximum amount of control points the node is worth.                                                                                                                        |
|**NeutralControlPoints**   |*Integer*                  |The control points for a neutral node.                                                                                                                                         |
|**NodeCamera**             |*Camera Actor*             |The camera located at the node.                                                                                                                                                |
|**NodeCube_Mat**           |*MaterialInstanceDynamic*  |This variable gets assigned a value from *EvergladesGameMode*.                                                                                                                 |
|**NodeDisplayID**          |*String*                   |The node's ID as displayed on the map.                                                                                                                                         |
|**NodeID**                 |*Integer*                  |The ID of the node.                                                                                                                                                            |
|**NodeNotationalX**        |*Integer*                  |Simple x coordinate for this node if the central node is at (0,0) and each node is separated by one arbitrary unit (not Unreal units).                                         |
|**NodeNotationalY**        |*Integer*                  |Simply y coordinate for this node if the central node is at (0,0) and each node is separated by one arbitrary unit (not Unreal units).                                         |
|**Occupied**               |*Boolean*                  |Whether a player owns the node.                                                                                                                                                |
|**OccupyingGroups**        |*Array\<SwarmGroup\>*      |The groups occupying the node.                                                                                                                                                 |
|**OwnerText**              |*Text*                     |Debug text to display for each node.                                                                                                                                           |
|**Resources**              |*Array\<String\>*          |Resources contained in this node.                                                                                                                                              |

## Functions
[**ConstructonScript**](../../Methods/ClientMethods/ConstructionScript_NodePoint.md)  

## Events
[**AddGroup**](../../Events/AddGroup.md)  
[**Event BeginPlay**](../../Events/BeginPlay_NodePoint.md)  
[**Event Tick**](../../Events/Tick_NodePoint.md)  
[**NodeControlUpdate**](../../Events/NodeControlUpdate.md)  
[**RefreshNode**](../../Events/RefreshNode.md)  
[**RemoveGroup**](../../Events/RemoveGroup.md)  
[**UpdateControlPoints**](../../Events/UpdateControlPoints.md)  

## Event Dispatchers
**None**

## Macros
[**GetDebugString**](../../Macros/GetDebugString.md)  