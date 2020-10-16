# GetLastIndex
Returns the string found at the last index of an array of strings.
Used specifically to process each portion of a turn according to
the final index of each array, which contains the type of event, 
(e.g., "IN TRANSIT", "CONTROL UPDATE").  

Target is *EvergladesGameMode*.  

## Node

## Inputs
|Name       |Type               |Description                            |
|-----------|-------------------|---------------------------------------|
|**Array**  |*Array\<String\>*  |Array of events for a specific turn.   |

## Outputs
|Name       |Type       |Description                                |
|-----------|-----------|-------------------------------------------|
|**Index**  |*String*   |The string at the last index of the array. |