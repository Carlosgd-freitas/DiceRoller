# Team
A **Team** is composed of [`Monsters`](/docs/base/monster.md) that participate in combat together. A `Monster` see the others in the same team as **allies**, and the others on different teams as **enemies**. The AI control of `Monsters` takes this in consideration when executing actions, like rolling [`Dice`](/docs/base/dice.md) and using `Skills`. As such, if the majority of [`Effects`](/docs/base/effect.md) in an action is mostly:
* benefitial, like healing or applying buffs, the AI will target the `Monster` themselves and its allies.
* detrimental, like dealing damage or applying debuffs, the AI will target the `Monster`'s enemies.

## Attributes
* **name**: the **team** name.
* **members**: a list of `Monsters` which are part of the **team**.

## Main methods
* `.get_status()`: returns if the team is still on combat or if was defeated.
* `.is_member()`: returns if a `Monster` is one of the **team members**.
