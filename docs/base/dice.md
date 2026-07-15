# Dice
A **Dice** is what primarly composes [`Entities`](/docs/base/entity.md) and `Skills`.

## Attributes
* **sides**: a list of [`Sides`](/docs/base/side.md) that can be used once the dice is rolled.

## Main methods
* `.roll()`: returns one of the dice `Sides`. The weight of each `Side` determines the probability of them being rolled.
