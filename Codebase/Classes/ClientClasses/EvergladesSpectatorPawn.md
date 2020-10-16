# EvergladesSpectatorPawn
The class of the actor representing the user.

**Class Type**&nbsp; &nbsp; &nbsp; &nbsp; Blueprint  
**Parent Class** &nbsp; &nbsp; SpectatorPawn  

## Variables
|Variable                       |Type                   |Description                                                                |
|-------------------------------|-----------------------|---------------------------------------------------------------------------|
|**CamTarget**                  |*Actor*                |The swarm the camera tracks.                                               |
|**CurrentState**               |*SpectatorState*       |Current camera view (free, trackswarm, arena).                             |
|**DEBUG_CurrentArenaTarget**   |*Integer*              |The current node the camera should be viewing.                             |
|**GameModeRef**                |*EvergladesGameMode*   |A reference to the game mode.                                              |
|**Look**                       |*Boolean*              |Whether the user is controlling the view (free cam, right mouse button).   |
|**LookSpeed**                  |*Float*                |The speed at which the camera moves to look at something (in free cam).    |
|**MoveSpeed**                  |*Float*                |The speed at which the user translates the camera (free cam).              |
|**OrbitDirection**             |*Vector*               |The direction for the camera to rotate.                                    |

## Functions
[**ConstructionScript**](../../Methods/ClientMethods/ConstructionScript_EvergladesSpectatorPawn.md)  

## Events
[**1**](../../Events/1.md)  
[**5**](../../Events/5.md)  
[**ChangeCamMode**](../../Events/ChangeCamMode.md)  
[**Event BeginPlay**](../../Events/BeginPlay_EvergladesSpectatorPawn.md)  
[**Event Tick**](../../Events/Tick_EvergladesSpectatorPawn.md)  
[**InputAxis Elevate**](../../Events/InputAxis_Elevate.md)  
[**InputAxis Forward**](../../Events/InputAxis_Forward.md)  
[**InputAxis Mouse_Horiz**](../../Events/InputAxis_Mouse_Horiz.md)  
[**InputAxis Mouse_Vert**](../../Events/InputAxis_Mouse_Vert.md)  
[**InputAxis Strafe**](../../Events/InputAxis_Strafe.md)  
[**M**](../../Events/M.md)  
[**P**](../../Events/P.md)  
[**Right Mouse Button**](../../Events/Right_Mouse_Button.md)  
[**Z**](../../Events/Z.md)  

## Event Dispatchers
**None**

## Macros
[**LookAtTarget**](../../Macros/LookAtTarget.md)  
[**OrbitAroundAxis**](../../Macros/OrbitAroundAxis.md)  