
## SSH Bastion Menu (ssh_menu.py)

### Role in the HomeLab

Within this HomeLab, the `ssh_menu.py` script is a **core access component of the bastion hosts** deployed in multiple networks (DMZ and SOC).

It is **not a convenience tool**, but a **critical interface** designed to manage and secure how users access the infrastructure.

In an environment with:

- Multiple VLANs (DMZ, Production, SOC, Admin…)
- Dozens of servers (50+ assets)
- Redundant systems (HA pairs)
- Different access methods (SSH keys, users, ports)

Direct SSH access quickly becomes **unmanageable, error-prone, and unsafe**.

This script solves that by acting as a **controlled SSH entry point**.

---

### Why this script exists in *this* HomeLab

This HomeLab is built for:

- **Cybersecurity training (Red Team / Pentest)**
- **Enterprise simulation**
- **Multi-user usage (shared lab)**

Because of that, access needs to be:

- Structured
- Predictable
- Controlled
- Easy to use under pressure (during exercises)

---

### The Problem Without It

In this infrastructure, a user would otherwise need to:

- Remember dozens of IP addresses across VLANs
- Know which user to use per machine
- Know which port is exposed (especially through DMZ/bastion)
- Use the correct SSH key every time
- Avoid mistakes while pivoting between networks

This becomes especially problematic during:

- **Pentest scenarios**
- **Lateral movement simulations**
- **SOC investigations**
- **Multi-user sessions**

---

### What the Bastion Menu Solves

The script transforms SSH access into a **guided and structured workflow**:

```
Network → Server → User → Connect
````

It provides:

- Centralized access to all assets
- Clear separation by network (DMZ, Prod, SOC…)
- Explicit user selection (avoids privilege mistakes)
- Automatic handling of:
  - Ports
  - SSH keys
  - Usernames
- Reduced cognitive load during operations

---

### Architectural Role

The script is deployed on:

- **DMZ Bastions** → Entry point from outside / VPN
- **SOC Bastions** → Controlled access to monitoring & security systems

It acts as:

> A **human-friendly access layer on top of SSH**, enforcing structure without adding heavy infrastructure.

---

### Security Perspective

From a security standpoint, this script:

- Reduces human errors (wrong target, wrong credentials)
- Standardizes access patterns
- Prevents ad-hoc and uncontrolled SSH usage
- Encourages use of bastion hosts instead of direct access

It complements:

- pfSense (network filtering)
- VLAN segmentation
- VPN access
- IDS / SIEM monitoring

---

### Multi-User Context

Since the lab is shared:

- Users may not know the full infrastructure
- Not all users should access everything the same way
- Mistakes can impact other users’ sessions

The menu ensures:

- A **consistent interface for everyone**
- A **lower learning curve**
- Safer collaboration during exercises

---

### In Practice

Instead of running:

```bash
ssh -i ~/.ssh/prod_key -p 2222 admin@192.168.70.80
````

Users simply:

```bash
python3 ssh_menu.py
```

And navigate the infrastructure interactively.

---

### Summary

This script exists because:

> **In a complex, segmented, and shared HomeLab, SSH access must be structured, guided, and reliable / not manual.**

It turns the bastion host into:

- A navigation system
- An access control helper
- A productivity tool
- A safety layer

---

### In One sentence

**This script is the bridge between a complex infrastructure and a usable one.**


---

### Annexe

- Configuration.