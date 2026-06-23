# Effects
An **Effect** is the smallest component of `Sides` and `Skills`, and are applied from a **source** `Entity` to one or multiple **target** `Entities`. The effect itself will be executed to one target at a time.

## Attributes
* **keyword**: a identifier that is unique per effect. Must be part of the `Keyword` enum.
* **value**: primary attribute that defines the effect's magnitude, behavior, or outcome.
* **duration**: by how many turns the effect will persist in the target.
* **decay**: by how much the `value` is decreased after each turn.
* **accuracy**: a number in the [0, 1] interval that represents the chance of the effect being executed.
* **type**: type of the effect. Effects with the same type have similar behavior.
* **trigger**: what combat situation triggers the effect.
* **persistent**: if the effect will be applied to the entity on execution, and added to their current effects; or if it is instant.
* **removable**: if the effect can be removed by other effects. The effect will still be removed after its duration expires.

## Effect types
* **BUFF**: a persistent effect that benefits the target.
* **CURSE**: an instant or persistent effect that harms self.
* **DEBUFF**: a persistent effect that harms the target.
* **DEFENSIVE**: a persistent effect that reduces direct damage that the target would recieve.
* **DETERIORATION**: an instant effect that harms the target.
* **NOTHING**: does nothing.
* **OFFENSIVE**: an instant effct directly damages the target.
* **RESTORATION**: an instant effect that benefits the target.

## Creating a new effect
- [ ] Keyword on `src/keywords`
- [ ] (Optional) Color data on `get_keyword_color()`
- [ ] Effect class on `src/effects`
- [ ] Additional effect implementation on other `src` files
- [ ] Functional test on `tests/effects`
- [ ] Localized logging messages on each `src/locales` module
- [ ] Additional logging functionality on `src/logger` files
- [ ] Added on `EffectCompendium` items
