# getNodeID()
Converts x, y, and z index into ID

(Y * xLen) + X + (xLen * yLen * Z) + 1

## Syntax
```python
getNodeID(Point point, int xLen, int yLen, int zLen):
```

## Returns
Returns an integer

## Parameters
|Parameter      |Description                                                            |
|---------------|-----------------------------------------------------------------------|
|**point**   |Custom class storing 3D coordinates|
|**xLen**   |Length of x axis|
|**yLen**   |Length of y axis|
|**zLen**   |Length of z axis|