"""EN-US localization for effect types module."""

BUFF = {
    "name": "BUFF",
    "activation": None,
    "execution": "{source} buffed {target} with {keyword} for {duration} {turns}.",
    "execution_self": "{source} buffed themselves with {keyword} for {duration} {turns}.",
    "execution_fail": "{source} tried to buff {target} with {keyword}, but",
    "execution_fail_self": "{source} tried to buff themselves with {keyword}, but",
}

CURSE = {
    "name": "CURSE",
    "activation": None,
    "execution": "{source} cursed {target} with {keyword} for {duration} {turns}.",
    "execution_self": "{source} cursed themselves with {keyword} for {duration} {turns}.",
    "execution_fail": "{source} tried to curse {target} with {keyword}, but",
    "execution_fail_self": "{source} tried to curse themselves with {keyword}, but",
}

DEBUFF = {
    "name": "DEBUFF",
    "activation": None,
    "execution": "{source} debuffed {target} with {keyword} for {duration} {turns}.",
    "execution_self": "{source} debuffed themselves with {keyword} for {duration} {turns}.",
    "execution_fail": "{source} tried to debuff {target} with {keyword}, but",
    "execution_fail_self": "{source} tried to debuff themselves with {keyword}, but",
}

DEFENSIVE = {
    "name": "DEFENSIVE",
    "activation": None,
    "execution": "{source} protected {target}. {target} recieved {effective_value} {keyword}.",
    "execution_self": "{source} protected themselves and recieved {effective_value} {keyword}.",
    "execution_fail": "{source} tried to protect {target} with {keyword}, but",
    "execution_fail_self": "{source} tried to protect themselves with {keyword}, but",
}

DETERIORATION = {
    "name": "DETERIORATION",
    "activation": None,
    "execution": "{source} deteriorated {target} with {keyword} for {duration} {turns}.",
    "execution_self": "{source} deteriorated themselves with {keyword} for {duration} {turns}.",
    "execution_fail": "{source} tried to deteriorate {target} with {keyword}, but",
    "execution_fail_self": "{source} tried to deteriorate themselves with {keyword}, but",
}

NOTHING = {
    "name": "NOTHING",
    "activation": None,
    "execution": "{source} did nothing.",
    "execution_self": "{source} did nothing.",
    "execution_fail": "{source} tried to do nothing, but",
    "execution_fail_self": "{source} tried to do nothing, but",
}

OFFENSIVE = {
    "name": "OFFENSIVE",
    "activation": None,
    "execution": "{source} {action} {target}.",
    "execution_self": "{source} {action} themselves.",
    "execution_fail": "{source} tried to {keyword} {target}, but",
    "execution_fail_self": "{source} tried to {keyword} themselves, but",
}

RESTORATION = {
    "name": "RESTORATION",
    "activation": None,
    "execution": "{source} restored {target} with {keyword} for {duration} {turns}.",
    "execution_self": "{source} restored themselves with {keyword} for {duration} {turns}.",
    "execution_fail": "{source} tried to restore {target} with {keyword}, but",
    "execution_fail_self": "{source} tried to restore themselves with {keyword}, but",
}
