# HUD_LargeMap
The large, 2D map representing the Everglades game default arena.  

**Class Type**&nbsp; &nbsp; &nbsp; &nbsp; Blueprint  
**Parent Class** &nbsp; &nbsp; User Widget  

## Variables
|Variable                       |Type                           |Description                                    |
|-------------------------------|-------------------------------|-----------------------------------------------|
|**Base_Blue**                  |*Image*                        |Blue home icon.                                |
|**Base_Red**                   |*Image*                        |Red home icon.                                 |
|**Btn_Close**                  |*Button*                       |Button to close large map.                     |
|**CameraOrient**               |*Image*                        |Shows camera direction.                        |
|**CloseMap**                   |*WidgetAnimation*              |Animation for closing large map.               |
|**GroupIndicators**            |*Array\<HUD_GroupIndicator\>*  |Collection of group indicators.                |
|**HUD_GroupIndicator**         |*HUD_GroupIndicator*           |Icon representing a player's group.            |
|**HUD_LargeMap_Zone_A**        |*HUD_LargeMap_Zone*            |A neutral node.                                |
|**HUD_LargeMap_Zone_B**        |*HUD_LargeMap_Zone*            |A neutral node.                                |
|**HUD_LargeMap_Zone_Base_1**   |*HUD_LargeMap_Zone*            |A home base node.                              |
|**HUD_LargeMap_Zone_Base_2**   |*HUD_LargeMap_Zone*            |A home base node.                              |
|**HUD_LargeMap_Zone_C**        |*HUD_LargeMap_Zone*            |A neutral node.                                |
|**HUD_LargeMap_Zone_D**        |*HUD_LargeMap_Zone*            |A neutral node.                                |
|**HUD_LargeMap_Zone_E**        |*HUD_LargeMap_Zone*            |A neutral node.                                |
|**HUD_LargeMap_Zone_F**        |*HUD_LargeMap_Zone*            |A neutral node.                                |
|**HUD_LargeMap_Zone_G**        |*HUD_LargeMap_Zone*            |A neutral node.                                |
|**HUD_LargeMap_Zone_H**        |*HUD_LargeMap_Zone*            |A neutral node.                                |
|**HUD_LargeMap_Zone_I**        |*HUD_LargeMap_Zone*            |A neutral node.                                |
|**Image_592**                  |*Image*                        |Icon representing the camera.                  |
|**KeyImage_Defense**           |*Image*                        |Icon in map key representing increased defense.|
|**KeyImage_MaxDefense**        |*Image*                        |Icon in map key representing a fortress.       |
|**KeyImage_Vision**            |*Image*                        |Icon in map key representing a watchtower.     |
|**LargeMap**                   |*Border*                       |LargeMap's border.                             |
|**Map**                        |*CanvasPanel*                  |The map's canvas panel.                        |
|**Map_Base**                   |*Image*                        |The 2D image of the terrain.                   |
|**REF_LargeMap**               |*Image*                        |A reference image.                             |

## Functions
[**GetGroupIndicator**](../../Methods/ClientMethods/GetGroupIndicator.md)  
[**RemoveGroupIndicator**](../../Methods/ClientMethods/RemoveGroupIndicator.md)  

## Events
[**On Clicked(Btn_Close)**](../../Events/Clicked_Btn_Close.md)  
[**SetNodePointReferences**](../../Events/SetNodePointReferences.md)  
[**UpdateGroupPos**](../../Events/UpdateGroupPos.md)  
[**UpdateMap**](../../Events/UpdateMap_HUD_LargeMap.md)  
[**UpdatePlayerPos**](../../Events/UpdatePlayerPos.md)  

## Event Dispatchers
[**OnCloseMap**](../../Dispatchers/OnCloseMap.md)  

## Macros
[**SelectZoneByID**](../../Macros/SelectZoneByID_Default.md)  