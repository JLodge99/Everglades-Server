# exec()
Main function used for generating a 3D map

weight default value is .1

bellcurve default value is False

## Recommended settings for weight

Bellcurve Enable:   Weight should be 0.3 - 0.9

Bellcurve Disable:  Weight should be 0.1 - 0.3

## Syntax
```python
exec(int xLen, int yLen, int zLen, float weight = .1, bool bellcurve = False)
```

## Returns
**None**

## Parameters
|Parameter      |Description                                                            |
|---------------|-----------------------------------------------------------------------|
|**xLen**   |Length of x axis|
|**yLen**   |Length of y axis|
|**zLen**   |Length of z axis|
|**weight**   |Weight value to determine the density of nodes in the map|
|**bellcurve**   |true/false enable bellcurve feature|