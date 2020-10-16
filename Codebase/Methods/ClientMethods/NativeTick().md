# NativeTick()
Override function for *NativeTick()*. This allows multiple Everglades game runs to be completed and 
creates related output such as calling the *AddResults* event in the *StartRunWidget* blueprint.  

## Syntax
```cpp
NativeTick(const FGeometry& MyGeometry, float InDeltaTime)
```

## Returns
**Void**  

## Parameters
|Parameter          |Description                                    |
|-------------------|-----------------------------------------------|
|**MyGeometry**     |The position and size of a Widget in Slate.    |
|**InDeltaTime**    |The time passed since the previous tick.       |