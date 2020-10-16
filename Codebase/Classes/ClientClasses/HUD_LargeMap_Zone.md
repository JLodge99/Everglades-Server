# HUD_LargeMap_Zone 
A node's 2D representation on the default large map.  

**Class Type**&nbsp; &nbsp; &nbsp; &nbsp; Blueprint  
**Parent Class** &nbsp; &nbsp; User Widget  

## Variables
|Variable                   |Type                       |Description                                                            |
|---------------------------|---------------------------|-----------------------------------------------------------------------|
|**CurrentControlRatio**    |*Float*                    |Current interpolated control value of the node for the current frame.  |
|**FillEdge**               |*Image*                    |Image separates the color filling the ring from the previous color.    |
|**InnerDynamicMaterial**   |*MaterialInstanceDynamic*  |Dynamic material for node's inner ring.                                |
|**InnerRing_Blue**         |*Image*                    |A blue inner ring.                                                     |
|**InnerRing_Red**          |*Image*                    |A red inner ring.                                                      |
|**InnerRing_White**        |*Image*                    |A white inner ring.                                                    |
|**LetterHousing**          |*Image*                    |The housing for the *NodeDisplayID*.                                   |
|**M_FillCircle_Inner**     |*Image*                    |Image used for dynamic material of inner ring.                         |
|**M_FillCircle_Outer**     |*Image*                    |Image used for dynamic material of outer ring.                         |
|**MinimapZoneRef**         |*HUD_MiniMap_Zone*         |A reference to the minimap.                                            |
|**NodeDisplayID**          |*TextBlock*                |The displayed ID of the node.                                          |
|**OuterDynamicMaterial**   |*MaterialInstanceDynamic*  |Dynamic material for the node's outer ring.                            |
|**OuterRing_Blue**         |*Image*                    |A blue outer ring.                                                     |
|**OuterRing_Red**          |*Image*                    |A red outer ring.                                                      |
|**OuterRing_White**        |*Image*                    |A white outer ring.                                                    |
|**TargetNode**             |*NodePoint*                |The current node in question.                                          |
|**ZoneType_Defense**       |*Image*                    |Image denotes fortress.                                                |
|**ZoneType_Watchtower**    |*Image*                    |Image denotes watchtower.                                              |

## Functions
**None**  

## Events
[**Event Construct**](../../Events/Construct_LargeMap_Zone.md)  
[**SetTargetNode**](../../Events/SetTargetNode.md)  
[**UpdateMap**](../../Events/UpdateMap_HUD_LargeMap_Zone.md)  

## Event Dispatchers
**None**  

## Macros
**None**  