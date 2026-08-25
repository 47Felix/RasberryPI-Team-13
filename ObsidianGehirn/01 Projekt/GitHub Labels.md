---
tags: [projekt, git, github, labels]
---

# GitHub Labels – Konvention für Issues & PRs

Stand: 25.08.2026. Labels wurden im Repo [`RasberryPI-Team-13`](https://github.com/47Felix/RasberryPI-Team-13/labels) per GitHub API angelegt, damit Issues und Pull Requests einheitlich einsortiert werden können.

## Bereits vorhandene Labels (unverändert)
`accessibility`, `arduino`, `bug`, `documentation`, `duplicate`, `enhancement`, `good first issue`, `hardware`, `help wanted`, `invalid`, `mqtt`, `nodered`, `question`, `software`, `tagesplan`, `wontfix`

## Neu angelegte Labels (25.08.2026)

### Priorität
| Label | Farbe | Bedeutung |
|---|---|---|
| `priority: high` | `#d93f0b` | Dringend, blockiert Fortschritt |
| `priority: medium` | `#fbca04` | Wichtig, aber nicht dringend |
| `priority: low` | `#0e8a16` | Kann warten |

### Status
| Label | Farbe | Bedeutung |
|---|---|---|
| `status: in-progress` | `#1d76db` | Wird gerade bearbeitet |
| `status: blocked` | `#e11d21` | Kann aktuell nicht weiterbearbeitet werden |
| `status: needs-review` | `#5319e7` | Wartet auf Review/Feedback |
| `status: ready-to-merge` | `#0e8a16` | PR ist fertig und mergebereit |

### Komponente
| Label | Farbe | Bedeutung |
|---|---|---|
| `component: raspberry-pi` | `#c2e0c6` | Betrifft den Pi selbst (OS, Setup, Config) |
| `component: network` | `#bfdadc` | WLAN/Netzwerk-Konfiguration |
| `component: sensor` | `#f9d0c4` | Sensorik/Aktorik |
| `component: moodle` | `#fef2c0` | Bezug zu Moodle-Inhalten/Aufgaben |
| `component: obsidian-vault` | `#d4c5f9` | Betrifft die Doku im ObsidianGehirn-Vault |

### Sonstige
| Label | Farbe | Bedeutung |
|---|---|---|
| `task` | `#c5def5` | Allgemeine Aufgabe ohne Code-Änderung |
| `WIP` | `#ededed` | Work in progress, noch nicht review-bereit |

## Nutzung
- Jedes Issue/PR bekommt idealerweise **ein Typ-Label** (bug/enhancement/documentation/question/task), **eine Priorität** und bei Bedarf **eine oder mehrere Komponenten**.
- PRs zusätzlich mit Status-Label pflegen (`status: in-progress` → `status: needs-review` → `status: ready-to-merge`), damit auf einen Blick sichtbar ist, wo ein PR steht.

## Verwandte Notizen
- [[Git Workflow]]
- [[Branch-Strategie]]

#projekt #git #github #labels
