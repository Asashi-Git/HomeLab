# HomeLab HA

## The architecture

The HA inside my HomeLab is powered via multiple elements to achieve an **Enterprise High Availability (HA)**.
- All of my pfSense router have a twin synced with CARP, PfSync, XML-RPC to avoid single point of failure.
- Every request for an internal resssouces are handled by:
	- First the pfSense that have HAProxy installed and configured that send the resquest to the two Load Balancer.
	- Then the two Load-Balancer  that balance the request to the dedicated servers.
- Every server inside my HomeLab have a twin that is synchronized with the main server (2 web server, 2 reverse proxy, ect) to achieve a service HA and avoid single point of failure.

```
graph TD User((Internet User)) -->|Connection| pfSense[pfSense Router  
running HAProxy]

subgraph "The Load Balancing Tier"
    pfSense -->|Round Robin| LB1[Arch NGINX LB 1]
    pfSense -->|Round Robin| LB2[Arch NGINX LB 2]
end

subgraph "The Application Tier"
    LB1 --> Bastion_Cluster
    LB1 --> Web_Cluster
    LB2 --> Bastion_Cluster
    LB2 --> Web_Cluster
end

Bastion_Cluster[Bastion 1 & 2]
Web_Cluster[Web Server 1 & 2]
```

