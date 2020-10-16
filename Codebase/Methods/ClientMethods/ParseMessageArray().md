# ParseMessageArray()
This converts a string representing an array of strings into an actual array 
of strings by making use of Unreal's ParseIntoArray() function.  

## Syntax
```cpp
ParseMessageArray(FString String)
```

## Returns
A *TArray\<FString>* from parsing the given string and converting to an array.

## Parameters
|Parameter  |Description                                |
|-----------|-------------------------------------------|
|String     |A string representing an array of strings. |