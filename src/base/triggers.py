"""Trigger condition for effects, skills, etc."""

from enum import Enum


class Trigger(Enum):
    """Triggers for Effects or Skills activations."""

    ATTACK = "ATTACK"
    BEING_ATTACKED = "BEING_ATTACKED"
    BEING_BUFFED = "BEING_BUFFED"
    BEING_DEBUFFED = "BEING_DEBUFFED"
    BEING_DEFENDED = "BEING_DEFENDED"
    BEING_RESTORED = "BEING_RESTORED"
    BEING_DETERIORATED = "BEING_DETERIORATED"
    BUFF = "BUFF"
    COMBAT_END = "COMBAT_END"
    COMBAT_START = "COMBAT_START"
    DEATH = "DEATH"
    DEBUFF = "DEBUFF"
    DEFEND = "DEFEND"
    DETERIORATE = "DETERIORATE"
    DURATION_DECAY = "DURATION_DECAY"
    REMOVE = "REMOVE"
    RESTORE = "RESTORE"
    ROLL = "ROLL"
    ROUND_END = "ROUND_END"
    ROUND_START = "ROUND_START"
    TURN_END = "TURN_END"
    TURN_START = "TURN_START"
