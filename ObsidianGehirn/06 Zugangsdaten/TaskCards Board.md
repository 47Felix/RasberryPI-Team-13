---
tags: [sicherheit, zugangsdaten, taskcards]
---

# TaskCards-Board (ITECH)

Das Team nutzt ein TaskCards-Board (`itech-bs14.taskcards.app`) für Kursmaterialien/Dokumente (u.a. eine Datei zu "Digi"/"Demo", Stand 30.08.2026 noch nicht inhaltlich geprüft).

> [!warning] Link enthält Zugriffs-Token – bewusst NICHT hier hinterlegt
> Der Board-Link enthält einen `token=`-Parameter, der direkten Zugriff gewährt. Da das Repo öffentlich ist (siehe [[⚠️ Zugangsdaten - Hinweis]]), würde ein Commit des vollständigen Links den Zugriff für jeden offenlegen. Den Link bei Anton/Felix erfragen bzw. wie andere Zugangsdaten außerhalb des Repos ablegen.

## Technische Einschränkung für Claude
TaskCards ist eine reine JavaScript-Single-Page-App (Quasar/Vue) – der HTML-Quelltext ist leer (`<div id=q-app></div>`), Inhalte laden erst per API-Call nach dem Laden. Claude kann den Board-Inhalt über WebFetch **nicht** auslesen. Für Auswertungen von Dokumenten auf dem Board: Inhalt/Text direkt im Chat einfügen oder als Datei/Screenshot bereitstellen.

## Verwandte Notizen
- [[⚠️ Zugangsdaten - Hinweis]]

#sicherheit #zugangsdaten #taskcards
