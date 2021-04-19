# CheckIfValidLoadout()
This takes a drone loadout and checks whether or not the loadout correctly matches the rules and is to be considered valid. Uses CheckIfValidSquad() for individual squad checks

## TODO
This function contains hardcoded values and does not fully encompas the likely future desired requirements of what a Loadout should be. Reccomend changing and editing the function (and deleting this TODO section) to better suit the future desired ruleset for the game. 

## Syntax
```pythons
CheckIfValidLoadout(string[][] loadout)
```

## Returns
Returns true or false based on whether the entire loadout is valid or not

## Parameters
|Parameter      |Description        |
|---------------|-------------------|
|**loadout**|An array of arrays where each array in the array of arrays is a string array containing the names of each unit in a particular squad.|