# Entity
An **Entity** is a base class inherited by [`Monsters`](/docs/base/monster.md), `Items` and `Skills` having common attributes and methods betwween these child classes.

## Attributes
* **global_id**: a identifier that is unique per class. Must be part of the `Keyword` enum.
* **local_id**: a generated identifier that is unique per object and is limited to a context, such as combat.
* **name**: entity name, which depends on the game's current locale.
* **description**: entity description, which depends on the game's current locale.
* **hp**: its meaning depends on the child class.
* **max_hp**: its meaning depends on the child class.
* **speed**: its meaning depends on the child class.
* **mana**: its meaning depends on the child class.
* **dice**: a list of [`Dice`](/docs/base/dice.md) that can be used.
* **effects**: a list of [`Effects`](/docs/base/effect.md) the entity is currently under.

## Main methods
* `.roll()`: rolls all of the entity `Dice` and returns a list containing all of the rolled `Sides`.
* `.has_effect()`: if the entity is currently under the specified `Effect`.
* `.get_effect()`: returns the specified `Effect` if the entity is currently under it.
* `.apply_effect()`: adds an `Effect` to the entity, executing the `Effect` `.on_apply()` and `.stack()` methods.
* `.remove_effect()`: removes an `Effect` the entity is currently under.
* `.can_act()`: returns if the entity can act.
