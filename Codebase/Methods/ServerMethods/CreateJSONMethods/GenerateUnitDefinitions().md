# GenerateUnitDefinitions()
This function creates the UnitDefinitions.json file in the config folder which is used for the game to understand what units have what properties. Loads in the various attribute based unit preset config JSONs.


## Syntax
```pythons
GenerateUnitDefinitions(int gameType)
```

## Returns
Does not return anything. Creates the UnitDefinitions.json file in the config folder which is used for the game to understand what units have what properties.

## Parameters
|Parameter      |Description        |
|---------------|-------------------|
|**gameType**| An integer representing the preset to be generate. This determines which files are loaded in to make up the current unit definitions.|
