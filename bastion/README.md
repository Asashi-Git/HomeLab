
# SSH Menu – HomeLab Bastion Interface

## Purpose

This script was created to solve a **real operational problem in a HomeLab environment**:  
managing multiple servers, networks, and access methods efficiently **without relying on memory, scattered notes, or complex SSH configs**.

In a typical HomeLab, you often have:

- Multiple networks (LAN, VLANs, VPN, DMZ…)
- Dozens of machines (VMs, containers, hypervisors, services)
- Different users and authentication methods (passwords, SSH keys)
- Non-standard ports and jump hosts

Over time, this becomes **hard to track, error-prone, and slow**.

This script turns your terminal into a **structured SSH bastion menu**, acting as a **single entry point to your entire infrastructure**.

---

## Why this script exists

Instead of:

- Memorizing IP addresses
- Writing long SSH commands
- Maintaining a messy `~/.ssh/config`
- Copy-pasting from notes or dashboards

You get:

A **centralized, human-readable configuration**  
A **clean interactive interface (TUI)**  
**Consistent access workflow** across all servers  
**Reduced mistakes** (wrong user, wrong port, wrong key)  
**Multi-user support** for shared environments  

---

## HomeLab Use Case

This script acts as a **lightweight bastion host interface**.

### Typical workflow:

1. You SSH into your HomeLab entry machine (or open a terminal locally)
2. Run:

```bash
./ssh_meny.py
```

3. Navigate through:
    
    - Network → Server → User
4. The script automatically:
    
    - Builds the correct SSH command
    - Applies the right port
    - Uses the correct authentication method (key/password)
    - Connects you instantly

---

## What problem it actually solves

### Without this script

```bash
ssh -i ~/.ssh/prod_key -p 2222 admin@192.168.10.42
```

- Easy to forget
- Hard to scale
- Painful with many hosts

---

### With this script

You just navigate:

```
[Production Network]
  → [Web Server]
    → [admin]
```

Done. No thinking required.

---

## Design Philosophy

This is **not a toy or demo UI**.  
It is built with real HomeLab constraints in mind:

- **Offline-first** (no external dependencies)
- **Simple JSON config**
- **Terminal-native (curses)**
- **Fast and lightweight**
- **Easily extensible**

---

## Why not just use ~/.ssh/config?

Good question — and intentional.

While `~/.ssh/config` is powerful, it:

- Becomes hard to read at scale
- Lacks hierarchy (networks, grouping)
- Is not user-friendly for non-experts
- Doesn’t provide interactive selection
- Doesn’t enforce structured validation

This script adds a **layer of organization and usability on top of SSH**.

---

## Multi-User Context

In shared HomeLab or team setups:

- Different users may have different credentials
- Some servers require specific accounts
- Keys may vary per environment

This script allows:

- Clear user descriptions
- Explicit authentication methods
- Safer and more predictable access

---

## Summary

This script exists to:

> **Turn a chaotic HomeLab SSH experience into a clean, structured, and reliable access system.**

It acts as:

- A **bastion menu**
- A **navigation layer for your infrastructure**
- A **productivity tool**
- A **mistake-prevention system**

---
