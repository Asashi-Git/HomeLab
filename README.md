# HomeLab


This homelab is designed as a **highly available, segmented, and production-like infrastructure** that replicates enterprise-grade architecture on a smaller scale. It contains over **50 assets**, with most critical services deployed in **redundant pairs** to ensure **high availability, fault tolerance, and service continuity**.

The infrastructure is built on a **Proxmox virtualization cluster (5 nodes)**, which hosts the majority of virtual machines. Network segmentation is enforced using **VLANs and pfSense firewalls**, isolating each functional zone to improve **security, control, and resilience**.

## Core Concepts

**I built this homelab as a shared training environment for myself and two of my friends, with the goal of developing our skills in cybersecurity, especially in Red Teaming (pentesting).** It provides a fully controlled and legal infrastructure where we can safely practice offensive security techniques.

**The environment is designed to simulate a real-world enterprise architecture, allowing us to train on realistic scenarios such as network exploitation, privilege escalation, lateral movement, and defense evasion.** By working within this isolated lab, we can experiment, learn from mistakes, and continuously improve our skills without impacting real systems.

**This homelab acts as a hands-on platform to bridge the gap between theory and practice, giving us practical experience in attacking and understanding complex infrastructures in a safe and collaborative way.**

- **High Availability (HA)**  
    Most services (web, DNS, database, monitoring, security, etc.) are duplicated across two instances to prevent single points of failure.
    
- **Network Segmentation**  
    The homelab is divided into multiple VLANs, each serving a dedicated purpose:
    
    - Shared infrastructure
    - Administration
    - DMZ (public-facing services)
    - Production
    - Pre-production
    - SOC (security operations)

- **Defense in Depth**  
    Security is enforced through multiple layers: firewalls (pfSense), reverse proxies, bastions, VPN access, IDS (Suricata), and SIEM (Wazuh).
    
- **Enterprise Simulation**  
    The architecture mimics a real-world IT environment, including Active Directory, load balancing, monitoring, and security operations.

#### Assets & Architecture

- **Hypervisor Layer**
    
    - 5 Proxmox nodes forming the virtualization backbone

- **Firewall & Routing**
    
    - pfSense instances per network (VLAN-based segmentation)

- **Access & Exposure Layer (DMZ)**
    
    - Load balancers (Nginx)
    - Reverse proxies (TLS termination, routing)
    - VPN gateways (WireGuard)
    - Bastion hosts (controlled SSH access)
    - Mail servers (Postfix)

- **Production Services**
    
    - Web servers (Apache)
    - Active Directory & DNS (Windows Server 2025)
    - External DNS (AdGuard)
    - DHCP services
    - Databases (MariaDB)

- **Pre-Production**
    
    - Isolated environment for testing with HA pfSense setup

- **SOC (Security Operations Center)**
    
    - Monitoring (Zabbix)
    - SIEM (Wazuh)
    - IDS (Suricata)
    - SOAR (Shuffle)
    - Threat Intelligence platform
    - Dedicated bastion access

- **Administration**
    
    - Secure admin workstation (Arch Linux)
    - Dedicated admin VLAN

#### Objective

This homelab aims to:

- Practice **real-world infrastructure design**
- Learn and implement **cybersecurity operations (SOC)**
- Test **high availability and failover scenarios**
- Simulate **production-grade services and architectures**
- Build hands-on expertise in **networking, virtualization, and security**

## Assets & Network

#### Shared Network

| Network 192.168.40.0/24      | OS      | IP Address     | MAC Address | Vlan    | Techno Used    | Virtualized | Purpose                               |
| ---------------------------- | ------- | -------------- | ----------- | ------- | -------------- | ----------- | ------------------------------------- |
| LAN pfSense Shared interface | FreeBSD | 192.168.40.254 | None        | Vlan 40 | pfSense Web UI | No          | Network and Firewall                  |
| Proxmox node 1               | Proxmox | 192.168.40.253 |             | Vlan 40 | Proxmox Web UI | No          | Virtualize the servers in the HomeLab |
| Proxmox node 2               | Proxmox | 192.168.40.252 |             | Vlan 40 | Proxmox Web UI | No          | Virtualize the servers in the HomeLab |
| Proxmox node 3               | Proxmox | 192.168.40.251 |             | Vlan 40 | Proxmox Web UI | No          | Virtualize the servers in the HomeLab |
| Proxmox node 4               | Proxmox | 192.168.40.250 |             | Vlan 40 | Proxmox Web UI | No          | Virtualize the servers in the HomeLab |
| Proxmox node 5               | Proxmox | 192.168.40.249 |             | Vlan 40 | Proxmox Web UI | No          | Virtualize the servers in the HomeLab |

#### Admin Network

| Network 192.168.50.0/24     | OS         | IP Address     | MAC Address | VLAN    | Techno Used    | Virtualized | Purpose                  |
| --------------------------- | ---------- | -------------- | ----------- | ------- | -------------- | ----------- | ------------------------ |
| LAN pfSense Admin interface | FreeBSD    | 192.168.50.254 | None        | Vlan 50 | pfSense Web UI | No          | Network and Firewall     |
| Admin PC                    | Arch Linux | DHCP           | None        | Vlan 50 | None           | No          | Administrate the HomeLab |

#### DMZ Network

| Network 192.168.60.0/24   | OS         | IP Address     | MAC Address               | VLAN    | Techno Used    | Virtualized | Purpose                                                                     |
| ------------------------- | ---------- | -------------- | ------------------------- | ------- | -------------- | ----------- | --------------------------------------------------------------------------- |
| LAN pfSense DMZ interface | FreeBSD    | 192.168.60.254 | None                      | Vlan 60 | pfSense Web UI | No          | Network and Firewall                                                        |
| Load Balancer 1           | Arch Linux | 192.168.60.100 | fe80::be24:11ff:fe78:bc40 | Vlan 60 | Nginx          | Yes         | Load Balance Web/SSH/VPN                                                    |
| Load Balancer 2           | Arch Linux | 192.168.60.101 |                           | Vlan 60 | Nginx          | Yes         | Load Balance Web/SSH/VPN                                                    |
| Mail 1                    | Arch Linux | 192.168.60.25  | fe80::be24:11ff:fe96:3eb4 | Vlan 60 | Postfix        | Yes         | Send/Receive email                                                          |
| Mail 2                    | Arch Linux | 192.168.60.26  |                           | Vlan 60 | Postfix        | Yes         | Send/Receive email                                                          |
| Bastion 1                 | Arch Linux | 192.168.60.22  | fe80::be24:11ff:fe1a:9e91 | Vlan 60 | Python Script  | Yes         | Connect to SSh Inside the HomeLab                                           |
| Bastion 2                 | Arch Linux | 192.168.60.23  |                           | Vlan 60 | Python Script  | Yes         | Connect to SSh Inside the HomeLab                                           |
| VPN 1                     | Arch Linux | 192.168.60.119 | fe80::be24:11ff:fe05:d903 | Vlan 60 | WireGuard      | Yes         | VPN to Administrate the HomeLab                                             |
| VPN 2                     | Arch Linux | 192.168.60.120 |                           | Vlan 60 | WireGuard      | Yes         | VPN to Administrate the HomeLab                                             |
| Reverse Proxy 1           | Arch Linux | 192.168.60.80  | fe80::be24:11ff:fe9a:d58f | Vlan 60 | Nginx          | Yes         | Protect the Web Server and send to the good Web server/Host the Certificate |
| Reverse Proxy 2           | Arch Linux | 192.168.60.81  |                           | Vlan 60 | Nginx          | Yes         | Protect the Web Server and send to the good Web server/Host the Certificate |
| Game Server               | Arch Linux | 192.168.60.220 | fe80::be24:11ff:fe1d:ee90 | Vlan 60 | Vintage Story  | Yes         | A game server that I host for some fiends                                   |

#### Production Network

| Network                          | OS                  | IP Address     | MAC Address                | VLAN    | Techno Used    | Virtualized | Purpose                                |
| -------------------------------- | ------------------- | -------------- | -------------------------- | ------- | -------------- | ----------- | -------------------------------------- |
| LAN pfSense Production interface | FreeBSD             | 192.168.70.254 | None                       | Vlan 70 | pfSense Web UI | No          | Network and Firewall                   |
| Web 1                            | Arch Linux          | 192.168.70.80  | fe80::be24:11ff:fe61:173d  | Vlan 70 | Apache         | Yes         | Store the Website shared with the word |
| Web 2                            | Arch Linux          | 192.168.70.81  |                            | Vlan 70 | Apache         | Yes         | Store the Website shared with the word |
| Windows Server 1                 | Windows Server 2025 | 192.168.70.88  | fe80::21c:7d09:7af6:8fe7%2 | Vlan 70 | ADDS DNS       | Yes         | Used for AD and DNS resolver           |
| Windows Server 2                 | Windows Server 2025 | 192.168.70.89  |                            | Vlan 70 | ADDS DNS       | Yes         | Used for AD and DNS resolver           |
| DNS 1                            | Arch Linux          | 192.168.70.53  | fe80::be24:11ff:fe38:50    | Vlan 70 | AdGuard Home   | Yes         | Used as outside DNS resolver           |
| DNS 2                            | Arch Linux          | 192.168.70.54  |                            | Vlan 70 | AdGuard Home   | Yes         | Used as outside DNS resolver           |
| DHCP 1                           | Arch Linux          | 192.168.70.67  | fe80::be24:11ff:fe5a:cb67  | Vlan 70 | DHCPD          | Yes         | Used as the DHCP of the HomeLab        |
| DHCP 2                           | Arch Linux          | 192.168.70.68  |                            | Vlan 70 | DHCPD          | Yes         | Used as the DHCP of the HomeLab        |
| DataBase 1                       | Arch Linux          | 192.168.70.33  | fe80::be24:11ff:febd:3f6f  | Vlan 70 | MariaDB        | Yes         | Used as the Data Base of the HomeLab   |
| DataBase 2                       | Arch Linux          | 192.168.70.34  |                            | Vlan 70 | MariaDB        | Yes         | Used as the Data Base of the HomeLab   |


#### Pre-Production Network

| Network                              | OS      | IP Address                        | MAC Address | VLAN    | Techno Used    | Virtualized | Purpose              |
| ------------------------------------ | ------- | --------------------------------- | ----------- | ------- | -------------- | ----------- | -------------------- |
| LAN pfSense Pre-Production interface | FreeBSD | 192.168.80.254                    | None        | Vlan 80 | pfSense Web UI | No          | Network and Firewall |
| WAN pfSense Pre-Production interface | FreeBSD | 192.168.80.249 VIP 192.168.80.250 | None        | Vlan 80 | pfSense Web UI | Yes         | Network and Firewall |
| WAN pfSense Pre-Production interface | FreeBSD | 192.168.80.248 VIP 192.168.80.250 | None        | Vlan 80 | pfSense Web UI | Yes         | Network and Firewall |

#### SOC Network

| Network                      | OS         | IP Address     | MAC Address | VLAN    | Techno Used    | Virtualized | Purpose                                                |
| ---------------------------- | ---------- | -------------- | ----------- | ------- | -------------- | ----------- | ------------------------------------------------------ |
| LAN pfSense SOC interface    | FreeBSD    | 192.168.90.254 | None        | Vlan 90 | pfSense Web UI | No          | Network and Firewall                                   |
| Monitoring 1                 | Arch Linux | 192.168.90.69  | None        | Vlan 90 | Zabbix         | Yes         | Used to monitor the HomeLab                            |
| Monitoring 2                 | Arch Linux | 192.168.90.70  | None        | Vlan 90 | Zabbix         | Yes         | Used to monitor the HomeLab                            |
| Bastion 1                    | Arch Linux | 192.168.90.22  | None        | Vlan 90 | Python Script  | Yes         | Used to connect via SSH to SOC assets                  |
| Bastion 2                    | Arch Linux | 192.168.90.23  | None        | Vlan 90 | Python Script  | Yes         | Used to connect via SSH to SOC assets                  |
| Threat Intelligence 1        | Arch Linux | 192.168.90.40  | None        | Vlan 90 | MSP            | Yes         |                                                        |
| Threat Intelligence 2        | Arch Linux | 192.168.90.41  | None        | Vlan 90 | MSP            | Yes         |                                                        |
| Intrusion Detection System 1 | Arch Linux | 192.168.90.100 | None        | Vlan 90 | Suricata       | Yes         | Monitors network traffic or system activities          |
| Intrusion Detection System 2 | Arch Linux | 192.168.90.101 | None        | Vlan 90 | Suricata       | Yes         | Monitors network traffic or system activities          |
| SOAR 1                       | Arch Linux | 192.168.90.30  | None        | Vlan 90 | Shuffle        | Yes         | Automate and streamline response to security incidents |
| SOAR 1                       | Arch Linux | 192.168.90.31  | None        | Vlan 90 | Shuffle        | Yes         | Automate and streamline response to security incidents |
| SIEM 1                       | Debian     | 192.168.90.50  | None        | Vlan 90 | Wazuh          | Yes         | Monitoring                                             |
| SIEM 2                       | Debian     | 192.168.90.51  | None        | Vlan 90 | Wazuh          | Yes         | Monitoring                                             |


## Assets Configuration

#### DMZ

- [Bastion](https://github.com/Asashi-Git/HomeLab/tree/main/bastion).
- VPN.