# Combat
A **combat** is composed of [`Teams`](/docs/base/team.md) facing each other, each of them having the objective of eliminating all [`Monsters`](/docs/base/monster.md) from other teams.

## Concepts
* **Turn**: equivalent to **one monster** currently in combat. Dead monsters are not considered in combat, and can't take their turn.
* **Round**: equivalent to **all monsters** currently in combat taking **one turn**. This equivalency changes when monsters are added or removed from combat.

## Order Strategy
In what order the monsters still alive and in combat takes their turns:
* **FASTER**: monsters with **higher speed** take their turn before those with lower speed.
* **SLOWER**: monsters with **lower speed** take their turn before those with higher speed.
* **SEQUENTIAL**: monsters take their turn in the same order as they are in the `CombatManager` **teams** attribute.
* **SHUFFLE**: monsters take their turn **randomly**.

## Steps
1. Combat starts
2. Round starts
3. Turn of the current monster starts
4. Current monster takes its action
5. Turn of the current monster ends
6. The next monster from the turn order is decided
7. Steps **3** to **6** repeat until all monsters in combat take their turn
8. Round ends
9. Steps **2** to **8** repeat until the combat reaches an end condition
10. Combat ends

## End conditions
A combat ends in a:
* **Victory**, when only one team remains in combat, and all monsters from other teams are dead.
* **Draw**, when no teams are remaining in combat and all monsters are dead, or a softlock state happens in a number of sequential rounds (by default, 3 rounds), avoiding that the game softlocks perpetually.

## Softlock state
A **softlock state** happens when no major changes occurs in the combat in the entirety of a round. This includes, most notably:
* No hp from any monsters changes
* No monsters are added or removed from combat
* No effects are applied on or removed from monsters
