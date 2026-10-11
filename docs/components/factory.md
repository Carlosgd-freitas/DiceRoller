# Factory
A **Factory** is responsible for creating objects based on their identifiers, and their functionality are tied to [`Registries`](/docs/components/registry.md).

Since factory modules make use of the `.load()` method from registries, the import of a factory module also means importing all registered modules within a registry, and thus, must be used with caution.

## Main methods
* `.create()`: returns an instantiated object of a subclass stored in the `REGISTRIES` dictionary of a Registry.
* `.get_all_objects()`: returns a list of instantiated objects of all subclasses stored in the `REGISTRIES` dictionary of a Registry.
