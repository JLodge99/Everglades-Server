# generateJsonFile()
Generates a JSON file representing the 3D map. Includes ID, connectionIDs, distance, radius, resource, structure defence, teamstart, controlpoints.

## Syntax
```python
generateJsonFile(int xLen, int yLen, int zLen, int[][][] map)
```

## Returns
**None**

## Parameters
|Parameter      |Description                                                            |
|---------------|-----------------------------------------------------------------------|
|**xLen**   |Length of x axis|
|**yLen**   |Length of y axis|
|**zLen**   |Length of z axis|
|**map**   |A 3D integer array representing the 3-Dimensional map|