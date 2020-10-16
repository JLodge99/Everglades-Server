# ProcessStandingOrder
If *StandingOrder* is "RdyMove", "InTransit", or "Arrived", it calls *IncrementalMove* macro and
sets *OrderProcessed* to true. Sets to false otherwise.  

Target is *SwarmGroup*.  

## Node

## Inputs
**None**

## Outputs
|Name               |Type       |Description                            |
|-------------------|-----------|---------------------------------------|
|**OrderProcessed** |*Boolean*  |Whether the order has been processed.  |