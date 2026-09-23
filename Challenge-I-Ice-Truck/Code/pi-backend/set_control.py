"""CLI-Wrapper um control_state.write_field(), aufgerufen vom Node-RED-
Exec-Node (Challenge II, Track C, #195, siehe
../../Challenge-II-Ice-Truck-Extension/Code/node-red/flows.json:
fn_validate -> exec1) fuer jeden validierten control/*-Befehl vom Handy.

Aufruf: python3 set_control.py <field> <value>
  field: "mode" | "fan_pwm" | "valve_angle" (von fn_validate bereits
  validiert/geclampt, hier nur noch defensiv gegengeprueft)
"""

from __future__ import annotations

import sys

import control_state

VALID_FIELDS = {"mode", "fan_pwm", "valve_angle"}


def main(argv: list[str]) -> int:
    if len(argv) != 3:
        print(f"Usage: {argv[0]} <field> <value>", file=sys.stderr)
        return 2

    field, raw_value = argv[1], argv[2]
    if field not in VALID_FIELDS:
        print(f"Unbekanntes Feld: {field}", file=sys.stderr)
        return 2

    value = raw_value if field == "mode" else int(raw_value)
    control_state.write_field(field, value)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
