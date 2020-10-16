# evgUserWidget

**Class Type**&nbsp; &nbsp; &nbsp; &nbsp; C++  
**Header** &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; evgUserWidget.h  
**Parent Class** &nbsp; &nbsp; UUserWidget  

## Variables
|Variable                   |Type           |Description                                                                        |
|---------------------------|---------------|-----------------------------------------------------------------------------------|
|**m_CurrentRun**           |*int*          |The number of the current run.                                                     |
|**m_FullResults**          |*FString*      |The CSV file containing agent script names, scores, and win types for the matches. |
|**m_P0Script**             |*FString*      |The name of Player 0's AI agent.                                                   |
|**m_P1Script**             |*FString*      |The name of Player 1's AI agent.                                                   |
|**m_ResultsSavePath**      |*FString*      |The name of the location to save the FullResults CSV file.                         |
|**m_RunsFinished**         |*bool*         |Indicates whether all the runs have finished.                                      |
|**m_ServerArgs**           |*FString*      |The arguments passed to the server when called.                                    |
|**m_ServerCmd**            |*FString*      |The location of the python executable.                                             |
|**m_ServerPath**           |*FString*      |The location of the Everglades server.                                             |
|**m_ServerProc**           |*FProcHandle*  |A reference to the server process.                                                 |
|**m_ServerTelemetryPath**  |*FString*      |The location of the telemetry files.                                               |
|**m_ServerWork**           |*FString*      |The location of the Everglades server.                                             |
|**m_TotalRuns**            |*int*          |The total number of matches to run.                                                |

## Methods
[**AddResults()**](../../Methods/ClientMethods/AddResults().md)  
[**GatherAIFiles()**](../../Methods/ClientMethods/GatherAIFiles().md)  
[**GatherMapFiles()**](../../Methods/ClientMethods/GatherMapFiles().md)  
[**NativeTick()**](../../Methods/ClientMethods/NativeTick().md)  
[**StartRun()**](../../Methods/ClientMethods/StartRun().md)  
[**UevgUserWidget()**](../../Methods/ClientMethods/UevgUserWidget().md)  


## Macros
**None**