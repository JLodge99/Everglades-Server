# LoadAttributesBasedUnitFile()
This loads the unit data for all units being used under the designated preset.


## Syntax
```pythons
LoadAttributesBasedUnitFile(int preset)
```

## Returns
Returns an array of arrays. array[0] stores an array of strings that correspond to names. array[1] stores an array of arrays where the index of the array corresponds to the index holding the name in array[0]. In the array of arrays inside array[1], is a list of strings representing the attributes held be the unit. Therefore array[0] holds a list of names and array[1] holds a list of lists, where each list is the names of the attributes.

## Parameters
|Parameter      |Description        |
|---------------|-------------------|
|**preset**| An integer representing the preset for what units are returned. 0 returns only the default units the game was created with. 1 includes all of preset 0 as well as all preset units created by developers to be considered balanced. 2 includes all of preset 0 and 1 and also includes any custom units created by the end user|
