# Event AddResults
This event is called from the *evgUserWidget* parent C++ class from its *NativeTick* override.
It sets the text of *ResultsText* to display on the widget.  

Target is *StartRunWidget*.  

## Node

## Inputs
|Name       |Type               |Description                                                            |
|-----------|-------------------|-----------------------------------------------------------------------|
|**Result** |*Array\<String\>*  |String elements are Player 0 score, Player 1 score, and type of win.   |

## Outputs
**None**