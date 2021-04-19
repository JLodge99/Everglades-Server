# generateCenterPlane()
Generates a center plane. Used if the dimensions of the map is odd.

## Syntax
```python
generateCenterPlane(int xLen, int yLen, int zLen, int[][][] map, float weightinit)
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
|**weightinit**   |Weight value to determine the density of nodes in the map|