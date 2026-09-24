"""Geteilter Zustand zwischen der Node-RED-Bridge (Challenge II, Track C,
#195) und dem Challenge-I-Regelkreis (app.py): Fernsteuerung vom Handy
ueberschreibt die automatische Regellogik (rules.py), solange
mode == "manual" ist.

Kein Server/Socket noetig - Node-RED (fn_validate) ruft set_control.py nur
als kurzlebigen Exec-Node-Subprozess auf, app.py liest read_state() einmal
pro Poll-Zyklus (5s, siehe app.py: POLL_INTERVAL_SECONDS). Pfad ist relativ
zu dieser Datei (nicht zum cwd), weil app.py (systemd, WorkingDirectory=
pi-backend) und set_control.py (Node-RED-Exec-Node, anderes cwd) sonst auf
unterschiedliche Dateien schreiben/lesen wuerden.
"""

from __future__ import annotations

import json
import os
import tempfile
from pathlib import Path

STATE_PATH = str(Path(__file__).resolve().parent / "control_state.json")

DEFAULT_STATE = {"mode": "auto", "fan_pwm": 0, "valve_angle": 0}


def read_state(path: str = STATE_PATH) -> dict:
    try:
        with open(path, "r", encoding="utf-8") as f:
            state = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return dict(DEFAULT_STATE)
    merged = dict(DEFAULT_STATE)
    merged.update(state)
    return merged


def write_field(field: str, value, path: str = STATE_PATH) -> dict:
    if field not in DEFAULT_STATE:
        raise ValueError(f"Unbekanntes Feld: {field}")
    state = read_state(path)
    state[field] = value
    _atomic_write(state, path)
    return state


def _atomic_write(state: dict, path: str) -> None:
    directory = os.path.dirname(os.path.abspath(path)) or "."
    fd, tmp_path = tempfile.mkstemp(dir=directory, prefix=".control_state_", suffix=".tmp")
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as f:
            json.dump(state, f)
        os.replace(tmp_path, path)
    except BaseException:
        os.unlink(tmp_path)
        raise
