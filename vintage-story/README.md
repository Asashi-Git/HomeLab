
# Vintage Story Server CLI – Common Commands

This document lists commonly used commands for administering a Vintage Story server from the server console (CLI) or in-game as an administrator.

---

## Basic Server Commands

**Show help**
/help

**List connected players**
/list

**Stop the server**
/stop

**Save the world**
/savegame save

**Create a backup**
/savegame createbackup

---

## Player Management

**Kick a player**
/kick <username>

Example:
/kick PlayerName

**Ban a player**
/ban <username>

**Unban a player**
/unban <username>

**Ban an IP**
/banip <ip-address>

**List banned players**
/banlist

---

## Whitelist Management

**Enable whitelist**
/whitelist on

**Disable whitelist**
/whitelist off

**Add player to whitelist**
/whitelist add <username>

Example:
/whitelist add PlayerName

**Remove player from whitelist**
/whitelist remove <username>

---

## Player Permissions

**Grant admin role**
/player <username> role admin

Example:
/player PlayerName role admin

**Remove admin role**
/player <username> role player

---

## Teleportation

**Teleport yourself**
/tp <x> <y> <z>

Example:
/tp 100 80 200

**Teleport to another player**
/tp <player1> <player2>

Example:
/tp PlayerA PlayerB

---

## Time Control

**Set time of day**
/time set <value>

Example:
/time set 0.5

**Speed up or slow down time**
/time speed <value>

---

## Weather

**Set weather**
/weather set <type>

Example:
/weather set rain

**Clear weather**
/weather set clear

---

## Debug / Utility

**Show server info**
/serverinfo

**Show performance statistics**
/debug perf

**Reload server configs**
/reload

---

## Tips

- Commands can be executed from the **server console** or **in‑game chat** if you are an admin.
- Replace `<username>` with the player’s exact in-game name.
- Some commands require administrator privileges.

---

Vintage Story Wiki:
https://wiki.vintagestory.at
