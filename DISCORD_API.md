# Discord-Server per API verwalten

Der Bot hat Administrator-Rechte auf dem Server. Änderungen am Server (Rollen, Kanäle, Kategorien, Berechtigungen) laufen über die Discord-REST-API mit dem Bot-Token, nicht über den Chat selbst.

Verfügbare Umgebungsvariablen (bereits im Prozess gesetzt): `DISCORD_BOT_TOKEN`, `GUILD_ID`.

## Grundsätzliches Muster

```bash
curl -s -X <METHOD> "https://discord.com/api/v10/<endpoint>" \
  -H "Authorization: Bot $DISCORD_BOT_TOKEN" \
  -H "Content-Type: application/json" \
  -d '<json-body>'
```

## Vor jeder Änderung: bestehenden Zustand prüfen

Immer zuerst GET aufrufen, um Duplikate zu vermeiden (z.B. nicht zweimal dieselbe Rolle anlegen):

```bash
curl -s "https://discord.com/api/v10/guilds/$GUILD_ID/roles" \
  -H "Authorization: Bot $DISCORD_BOT_TOKEN"

curl -s "https://discord.com/api/v10/guilds/$GUILD_ID/channels" \
  -H "Authorization: Bot $DISCORD_BOT_TOKEN"
```

## Rolle erstellen

```bash
curl -s -X POST "https://discord.com/api/v10/guilds/$GUILD_ID/roles" \
  -H "Authorization: Bot $DISCORD_BOT_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"name": "Team-Lead", "color": 15158332, "hoist": true, "mentionable": true, "permissions": "8"}'
```

`permissions` ist ein String mit einem Bitfeld-Wert (Summe der einzelnen Rechte als Zahl, als String übergeben):
- `"8"` = Administrator (alles)
- `"0"` = keine besonderen Rechte (normales Mitglied)
- Für feinere Rechte: https://discord.com/developers/docs/topics/permissions#permissions-bitwise-permission-flags (z.B. `SEND_MESSAGES`, `MANAGE_CHANNELS` einzeln addieren)

## Kategorie erstellen

```bash
curl -s -X POST "https://discord.com/api/v10/guilds/$GUILD_ID/channels" \
  -H "Authorization: Bot $DISCORD_BOT_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"name": "PROJEKT", "type": 4}'
```

`type: 4` = Kategorie. Die zurückgegebene `id` der Kategorie als `parent_id` bei Text-/Voice-Kanälen verwenden, um sie einzuordnen.

## Text-Kanal erstellen (optional in einer Kategorie)

```bash
curl -s -X POST "https://discord.com/api/v10/guilds/$GUILD_ID/channels" \
  -H "Authorization: Bot $DISCORD_BOT_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"name": "pi-projekt", "type": 0, "parent_id": "<kategorie-id>"}'
```

`type: 0` = Text-Kanal, `type: 2` = Voice-Kanal.

## Kanal-Berechtigungen für eine Rolle setzen

```bash
curl -s -X PUT "https://discord.com/api/v10/channels/<channel-id>/permissions/<role-id>" \
  -H "Authorization: Bot $DISCORD_BOT_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"type": 0, "allow": "1024", "deny": "0"}'
```

`type: 0` = Rolle (statt einzelnem Mitglied). `allow`/`deny` sind wieder Bitfeld-Summen (z.B. `1024` = `VIEW_CHANNEL`).

## Vorgehen bei "gestalte den Server"

1. Erst GET auf `/roles` und `/channels`, um zu sehen, was schon existiert.
2. Plan aus der Nutzeranfrage ableiten (welche Rollen, welche Kanäle/Kategorien, welche Berechtigungen).
3. Rollen anlegen, dann Kategorien, dann Kanäle darin, dann ggf. Berechtigungen pro Kanal/Rolle setzen.
4. Kurze Zusammenfassung zurückmelden, was angelegt wurde (Namen + IDs).
