from colorama import init

from src.combat.manager import CombatManager
from src.monsters.slime import Slime

init()

slimes = []

for i in range(4):
    suffix = chr(i + 65)

    slimes.append(
        Slime(
            name=f"Slime {suffix}",
        )
    )

combat_manager = CombatManager(
    teams=[
        slimes[:2],
        slimes[2:],
    ],
    team_names=[
        "Red Team",
        "Blue Team",
    ],
    order_strategy="SET",
    language="EN-US",
)

# ----------------------------

combat_manager.run()
