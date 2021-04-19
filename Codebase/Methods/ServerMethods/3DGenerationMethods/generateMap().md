# generateMap()
Generates a random 3D map

## Syntax
```python
generateMap(int xLen, int yLen, int zLen, int[][][] map, float weightinit, bool bellcurve)
```

## Returns
True if map contains dead ends

False if success

## Parameters
|Parameter      |Description                                                            |
|---------------|-----------------------------------------------------------------------|
|**xLen**   |Length of x axis|
|**yLen**   |Length of y axis|
|**zLen**   |Length of z axis|
|**map**   |A 3D integer array representing the 3-Dimensional map|
|**weightinit**   |Weight value to determine the density of nodes in the map|
|**bellcurve**   |true/false enable bellcurve feature|