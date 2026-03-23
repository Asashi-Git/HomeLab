
# Annexe – Bastion Hardening (User & SSH Configuration)

To securely integrate this script into the infrastructure, a **dedicated service account** named `jumphost` has been created.

This account is specifically designed to act as a **controlled entry point** to the HomeLab via SSH.

---

#### Service Account: `jumphost`

- The `jumphost` user does **not provide a standard interactive shell**
- It is restricted to running the SSH menu script only
- It has its own **isolated SSH configuration**

When a user connects to the bastion:

```bash
ssh jumphost@<bastion-ip>
````

The `ssh_menu.py` script is **automatically launched**

---

#### Forced Command Execution

The SSH configuration enforces the execution of the script using:

- `ForceCommand` or
- a forced command in `authorized_keys`

This ensures that:

- Users **cannot bypass the menu**
- No arbitrary shell access is granted
- All interactions go through the controlled interface

---

#### Session Control & Exit Behavior

The environment is intentionally restricted:

- If the user exits the script or presses `CTRL+C`  
    → the SSH session is **immediately terminated**

This prevents:

- Dropping into a shell
- Executing unauthorized commands
- Escaping the bastion control layer

---

#### Additional Hardening Measures

To reinforce the security of the bastion host, several protections have been implemented:

- **Two-Factor Authentication (2FA)**  
    The `jumphost` user requires an additional authentication factor (e.g., TOTP), ensuring that SSH access is protected even if credentials are compromised.
    
- **UFW Rate Limiting**  
    SSH access is protected using UFW rate limiting to mitigate brute-force attempts:
    
    ```bash
    ufw limit ssh
    ```
    
- **Fail2Ban Protection**  
    Fail2Ban is configured to monitor SSH authentication logs and automatically ban IP addresses exhibiting malicious behavior (e.g., repeated failed login attempts).
    

---

#### Security Benefits

This setup provides:

- Strict access control through a single entry point
- Strong authentication with 2FA
- Protection against brute-force attacks (UFW + Fail2Ban)
- Elimination of unmanaged shell access
- Reduced attack surface on bastion hosts
- Consistent and auditable user behavior

It aligns with the HomeLab’s **defense-in-depth strategy**, complementing:

- VLAN segmentation
- pfSense firewalling
- VPN access
- IDS / SIEM monitoring

---

#### Configuration Reference

You can find the SSH configuration file here:

```
<path-to-your-sshd_config-or-authorized_keys>
```

---

### Summary

> The `jumphost` user transforms the bastion into a **hardened, monitored, and controlled access gateway**, where the SSH menu is not optional — it is the only allowed interface.


---
