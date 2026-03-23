
# Vintage Story Server CLI – Common Commands

This document lists commonly used commands for administering a Vintage Story server from the server console (CLI) or in-game as an administrator.

---

## Basic Server Commands

**Show help**
```
~/server/server.sh help
```

**List connected players**
```
~/server/server.sh command "/list"
```

**Stop the server**
```
~/server/server.sh stop
```

**Save the world**
```
~/server/server.sh command "/savegame save"
```

**Create a backup**
```
~/server/server.sh command "/savegame createbackup"
```

---

## Player Management

**Kick a player**
```
~/server/server.sh command "/kick <username>"
```

Example:
/kick PlayerName

**Ban a player**
```
~/server/server.sh command "/ban <username>"
```

**Unban a player**
```
~/server/server.sh command "/unban <username>"
```

**Ban an IP**
```
~/server/server.sh command "/banip <ip-address>"
```

**List banned players**
```
~/server/server.sh command "/banlist"
```

---

## Whitelist Management

**Enable whitelist**
```
~/server/server.sh command "/whitelist on"
```

**Disable whitelist**
```
~/server/server.sh command "/whitelist off"
```

**Add player to whitelist**
```
~/server/server.sh command "/whitelist add <username>"
```

Example:
/whitelist add PlayerName

**Remove player from whitelist**
```
~/server/server.sh command "/whitelist remove <username>"
```

---

## Player Permissions

**Grant admin role**
```
~/server/server.sh command "/player <username> role admin"
```

Example:
/player PlayerName role admin

**Remove admin role**
```
~/server/server.sh command "/player <username> role player"
```

---

## Teleportation

**Teleport yourself**
```
/tp <x> <y> <z>
```

Example:
/tp 100 80 200

**Teleport to another player**
```
/tp <player1> <player2>
```

Example:
/tp PlayerA PlayerB

---

## Time Control

**Set time of day**
```
/time set <value>
```

Example:
/time set 0.5

**Speed up or slow down time**
```
/time speed <value>
```

---

## Weather

**Set weather**
```
/weather set <type>
```

Example:
/weather set rain

**Clear weather**
```
/weather set clear
```

---

## Debug / Utility

**Show server info**
```
/serverinfo
```

**Show performance statistics**
```
/debug perf
```

**Reload server configs**
```
~/server/server.sh reload
```

---

## Tips

- Commands can be executed from the **server console** or **in‑game chat** if you are an admin.
- Replace `<username>` with the player’s exact in-game name.
- Some commands require administrator privileges.

---

Vintage Story Wiki:
https://wiki.vintagestory.at
