# Stat
A **Stat** is a helper class for [`Effect`](/docs/base/effect.md), which can store combinations of values in different formats. The **Effect** can then orchestrate each value format in its implementation, allowing different behaviors.

## Attributes
* **flat**: value in flat format (e.g. 1, 5, 100).
* **percent**: value in percentage format (e.g. 0.5, which means 50%).

## Main methods
* `.add()`: adds a value from another Stat into itself.
* `.subtract()`: subtracts a value from another Stat into itself.
* `.lowest()`: sets the lowest value between itself and another Stat.
* `.highest()`: sets the highest value between itself and another Stat.
