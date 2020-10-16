# evgEvents
This class contains functions that load and process events described in the telemetry files.  

**Class Type**&nbsp; &nbsp; &nbsp; &nbsp; C++  
**Header** &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; evgEvents.h  
**Parent Class** &nbsp; &nbsp; UObject  

## Variables
|Variable               |Type                           |Description                                                                                        |
|-----------------------|-------------------------------|---------------------------------------------------------------------------------------------------|
|**CurrentEventTime**   |*int*                          |The current turn number.                                                                           |
|**Events**             |*TMultiMap\<int, FString\>*    |The key is the turn number and the value is multiple strings of events during the specified turn.  |
|**LastEventTime**      |*int*                          |The previous turn number.                                                                          |

## Methods
[**GetAllFilesInDirectory()**](../../Methods/ClientMethods/GetAllFilesInDirectory().md)  
[**GetTelemetryFolders()**](../../Methods/ClientMethods/GetTelemetryFolders().md)  
[**LoadEvents()**](../../Methods/ClientMethods/LoadEvents().md)  
[**ProcessEvents()**](../../Methods/ClientMethods/ProcessEvents().md)  
[**UevgEvents()**](../../Methods/ClientMethods/UevgEvents().md)  

## Macros
**None**