# AddResults()
This function is declared in evgUserWidget class, but is defined in the StartRunWidget, which
inherits from the evgUserWidget class. It hides the "Awaiting results..." text box in the StartRunWidget and
instead adds the results of the match to the "Server Running" pane.  

## Syntax
```cpp
AddResults(const TArray<FString> &result)
```

## Returns
**Void**  

## Parameters
|Parameter  |Description                                                        |
|-----------|-------------------------------------------------------------------|
|**result** |The elements are Player 0 score, Player 1 score, and type of win.  |