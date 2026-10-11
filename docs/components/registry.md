# Registry
A **Registry** is responsible for "storing" all subclasses of a main class in a `REGISTRIES` dictionary on the same module, where each key is the unique identifier of that subclass, and the value is the subclass itself (not an instantiated object).

## Main methods
* `.register()`: used on main class `__init_subclass__()`, it stores the subclass in the `REGISTRIES` dictionary.
* `.load()`: loads all modules of the stored subclasses, and as such, *must be used with caution*.
