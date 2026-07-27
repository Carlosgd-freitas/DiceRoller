# Effect
An **Effect** is the smallest component of the game mechanics, and is executed by a **source** [`Entity`](/docs/base/entity.md) to one or multiple **target** `Entities`. The effect itself will be executed to one target at a time.

Each **effect** has its own behavior, and are to be used by "bigger" components, such as [`Sides`](/docs/base/side.md), to "compose" the wanted interaction between `Entities`. Therefore, new interactions require new **effects** to be implemented.

## Attributes
* **keyword**: a identifier that is unique per effect. Must be part of the `Keyword` enum.
* **type**: type of the effect. Effects with the same type have similar behavior.
* **value**: effect magnitude.
* **min_value**: minimum threshold for effect value.
* **max_value**: maximum threshold for effect value.
* **duration**: by how many turns the effect will persist in the target.
* **delta**: increases or decreases effect value at each turn end.
* **accuracy**: a floating-point number in the [0, 1] interval that represents the chance of the effect being executed.
* **trigger**: what combat situation triggers the effect execution.
* **persistent**: if the effect will be applied to the entity on execution, and added to their current effects; or if it is instant.
* **removable**: if the effect can be removed by other effects. The effect will still be removed after its duration expires.
* **target_keywords**: other keywords that the effect can use in it's behavior.

## Effect types
* **BUFF**: a persistent effect that benefits the target.
* **CURSE**: an instant or persistent effect that harms self and allies.
* **DEBUFF**: a persistent effect that harms the target.
* **DEFENSIVE**: a persistent effect that reduces direct damage that the target would recieve.
* **DETERIORATION**: an instant effect that harms the target.
* **NOTHING**: does nothing.
* **OFFENSIVE**: an instant effct directly damages the target.
* **RESTORATION**: an instant effect that benefits the target.

## Main methods
* `.get_requirements()`: returns the requirements for executing the effect.
* `.on_apply()`: what happens when the effect is first applied on an `Entity`.
* `.activate()`: what happens when the effect is executed.
* `.stack()`: how the effect interacts with an `Entity` that is under another effect with the same keyword.

## Creating a new effect
- [ ] Keyword on `src/keywords`
- [ ] (Optional) Color data on `get_keyword_color()`
- [ ] Effect class on `src/effects`
- [ ] Additional effect implementation on other `src` files
- [ ] Functional test on `tests/effects`
- [ ] Localized logging messages on each `src/locales` module
- [ ] Additional logging functionality on `src/logger` files
- [ ] Added to `ALL_EFFECTS` variable in `src/compendium/effects.py`
