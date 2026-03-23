# Physical Infrastructure

The HomeLab is powered by **7 physical machines**, forming the foundation of a segmented and highly available environment.

---

### Router (pfSense)

A dedicated physical router ensures **network segmentation, routing, and security enforcement** across all VLANs.

- **OS:** pfSense (FreeBSD-based)
- **CPU:** Intel N150
- **RAM:** 16 GB DDR5
- **Storage:** 120 GB SSD
- **Networking:**
    - 1 × 10 GbE
    - 2 × 2.5 GbE

Acts as the **core firewall**, managing inter-VLAN traffic, NAT, VPN, and security policies.

---

### Proxmox Cluster (4 Nodes)

Four mini PCs form the **core virtualization cluster**, providing compute resources for the majority of the infrastructure.

- **Nodes:** 4 × Mini PCs
- **CPU:** Intel N150 (per node)
- **RAM:** 16 GB DDR5 (per node)
- **Storage:** 500 GB SSD (per node)

These nodes are grouped into a **Proxmox Datacenter**, enabling:

- High Availability (HA)
- Workload distribution
- Fault tolerance

---

### High-Capacity Node

A more powerful machine complements the cluster for **resource-intensive workloads**.

- **CPU:** Intel i7-7700K
- **RAM:** 32 GB DDR4
- **Storage:** 2 × 500 GB SSD

Integrated into the Proxmox cluster, this node is typically used for:

- Heavier services (SIEM, IDS, etc.)
- Testing demanding scenarios
- Handling peak workloads

---

### Managed Switch

A managed switch provides **layer 2 segmentation and VLAN enforcement** across the infrastructure.

- **Ports:**
    - 8 × 2.5 GbE
    - 1 × 10 GbE
- **Management:** Web interface
- **Configured VLANs:**  
    `40, 50, 60, 70, 80, 90, 100, 150, 200, 250`

Ensures proper **traffic isolation** between:

- DMZ
- Production
- Administration
- SOC
- and other network zones

---

### Architecture Overview

This hardware stack enables:

- Enterprise-like **network segmentation (VLANs + pfSense)**
- **High availability** via Proxmox cluster
- **Scalable compute resources** across multiple nodes
- **High-speed networking** (2.5 GbE / 10 GbE backbone)

---

### Summary

> This physical infrastructure provides a **robust, scalable, and production-like foundation**, capable of supporting a complex, segmented, and security-focused HomeLab environment.

---
