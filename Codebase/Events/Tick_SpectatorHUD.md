# Event Tick
Every tick, updates the map, player positions, group position and *ZoneControl_Fill*.  

Target is *SpectatorHUD* or *SpectatorHUD_Random*.  

## Node

## Inputs
|Name           |Type                   |Description                                                                |
|---------------|-----------------------|---------------------------------------------------------------------------|
|**InDeltaTime**|*Float*                |The time since the previous tick.                                          |
|**MyGeometry** |*Geometry Structure*   |The space alloted for *SpectatorHUD* or *SpectatorHUD_Random*. (not used)  |

## Outputs
**None**