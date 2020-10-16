# Z
Calls *DebugWinner* event from *EvergladesGameMode* when **Z** key is pressed. 
Since this is used for debugging purposes, the key event is not connected and 
therefore does nothing.  

Target is *EvergladesSpectatorPawn*.  

## Node

## Inputs
**None**

## Outputs
|Name           |Type           |Description                        |
|---------------|---------------|-----------------------------------|
|**Pressed**    |*Exec*         |Execution path if key was pressed. |
|**Released**   |*Exec*         |Execution path if key was released.|
|**Key**        |*Key Structure*|A reference to the key.            |