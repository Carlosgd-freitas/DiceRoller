# Locale

A **locale** is the collection of all the game's messages, localized into a specific language.

## Language

A **language** must be part of the `Language` enum at `/src/locales/languages.py` to be recognizable. All of the currently available languages can be located on this enum.

Each pair of this enum is composed by a name and value, where the name is the language abbreviation, in upper case, separated by an underline; and the value is the same abbreviation, but in lower case, also separated by an underline. For example, the American English language is present on the `Language` enum as:
```
EN_US = "en_us"
```

The American English (EN-US) language is considered as the game's default language, and used as a pivot to validate the integrity of other languages through tests. As such, other languages should mirror the file and data structure of the `src/locales/en_us` module.

## Locale Module Structure

A locale module for a language is a directory located inside `/src/locales`, and its name must be the same as the name in the corresponding `Language` enum pair.

The module is composed by **namespaces**, files that contains messages that are used in a broad and similar context.

Each namespace is composed by **message groups**, dictionaries where each key is a message identifier and each value is the **message** itself. Message groups contain messages of a more restrict context, in relation to namespaces. Their names are composed by uppercase letters, and can't start with "__", so that they can be easily differentiated from "\_\_builtins\_\_" components of Python itself, and be approprietly imported from the module.

## Implementing a new language

- [ ] Name/value pair at `/src/locales/languages.py`
- [ ] Language directory at `src/locales`
- [ ] Namespaces files inside the new language directory
- [ ] Message groups inside each namespace file
- [ ] Localized messages inside each message group
