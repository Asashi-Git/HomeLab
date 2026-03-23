J'ai un homeLab que je suis en train de construire !
Ce HomeLab est sense avoir 53 actifs car la plupart des machines sont double dans un soucis de haute disponibilite !

Voila les machines que nous pouvons retrouver au sein du Homelab dans leurs reseaux distinct : 

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

