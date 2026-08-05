# Monster
A **Monster** is a child class that inherits from [`Entity`](/docs/base/entity.md) and can participate in [**combat**](/docs/base/combat.md).

## Attributes
Only `Entity` attributes whose meaning depends on the child class will be covered here.

* **hp**: if this value reaches 0, the monster is considered dead.
* **max_hp**: the maximum value hp can reach.
* **speed**: determines when the monster acts in combat.
* **mana**: a resource used by `Skills`.
* **skills**: a list of `Skills` that can be used by the monster.
* **control_type**: what controls the monster actions (IA or a player).
* **ai_level**: changes IA behavior.  Higher levels means smarter strategies.
* **in_combat**: if the monster is participating in combat.
* **turn_taken**: if the monster has taken its turn in the current combat round.
* **suffix**: a suffix to differentiate monsters that have the same name.

## Main methods
* `.get_life_state()`: returns the monster life state (alive or dead).
* `.is_alive()`: if the monster is alive or not.
* `.is_dead()`: if the monster is dead or not.
