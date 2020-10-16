# StartRun()
This runs an Everglades game and saves the results to telemetry files.  

## Syntax
```cpp
StartRun(int numRuns, FString pythonPath, FString serverBasePath, FString mapName, FString player0Script, FString player1Script)
```

## Returns
**Void**  

## Parameters
|Parameter          |Description                                |
|-------------------|-------------------------------------------|
|**numRuns**        |The number of Everglades games to run.     |
|**pythonPath**     |The location of the python something       |
|**serverBasePath** |The Everglades server directory.           |
|**mapName**        |The name of the map to use for the runs.   |
|**player0Script**  |Player 0's agent file.                     |
|**player1Script**  |Player 1's agent file.                     |