# ChangeCamMode
Changes the camera mode (free, trackswarm, arena). This event is bound to the
*ChangeCamMode* event dispatcher.  

Target is *EvergladesSpectatorPawn*.  

## Node

## Inputs
|Name           |Type               |Description                                |
|---------------|-------------------|-------------------------------------------|
|**CamTarget**  |*Actor*            |The target on which to focus.              |
|**NewMode**    |*SpectatorState*   |The camera mode (arena, free, trackswarm). |

## Outputs
|Name           |Type               |Description                                |
|---------------|-------------------|-------------------------------------------|
|**CamTarget**  |*Actor*            |The target on which to focus.              |
|**NewMode**    |*SpectatorState*   |The camera mode (arena, free, trackswarm). |