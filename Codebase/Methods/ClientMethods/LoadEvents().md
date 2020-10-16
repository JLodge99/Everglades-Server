# LoadEvents()
This parses the telemetry files in the specified folder. Each event from each file is
converted to a string and uniquely added to the Events MultiMap with the key, *time*.
Here, *time* is the turn number multiplied by *TickInterval* (note TickInterval is set to 1).
Each string value for each key is appended with a string (e.g. *SCORES*, *CONTROL_UPDATE*)
specifying the type of data the string value contains.  
  
If any image (i.e. *bmp*) files exist in the telemetry folders, the file names are stored in an array.  

## Syntax
```cpp
LoadEvents(FString FolderName, int TickInterval)
```

## Returns
An array of image (*bmp*) file names.  

## Parameters
|Parameter          |Description                                                                        |
|-------------------|-----------------------------------------------------------------------------------|
|**FolderName**     |The name of the telemetry folder.                                                  |
|**TickInterval**   |Multiplier relating turn number to match time. Currently set to 1 in blueprints.   |