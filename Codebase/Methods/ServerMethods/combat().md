# combat()
This controls unit combat which occurs before movement. Combat executes in three phases: detection,
construction, and destruction. Contested nodes (nodes where both players are present) are found, with
drones available for combat at that node marked. Then, the targeting function is called and damage is built.
Finally, the built damage is applied to the targeted drones. Damage must be built first so that no drone gets
priority attacking by virtue of appearing in the front of a list.

## Syntax
```python
combat()
```

## Returns
**None**

## Parameters
**None**