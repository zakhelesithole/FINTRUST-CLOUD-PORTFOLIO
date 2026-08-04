# Week 5 Day 1 - FinTrust Multi-AZ VPC Build

## VPC Architecture Summary

| Resource | Name | CIDR | AZ |
|----------|------|------|-----|
| VPC | fintrust-vpc | 10.0.0.0/16 | Regional |
| Public Subnet 1 | fintrust-public-1a | 10.0.0.0/24 | af-south-1a |
| Public Subnet 2 | fintrust-public-1b | 10.0.1.0/24 | af-south-1b |
| App Subnet 1 | fintrust-app-1a | 10.0.10.0/24 | af-south-1a |
| App Subnet 2 | fintrust-app-1b | 10.0.11.0/24 | af-south-1b |
| Data Subnet 1 | fintrust-data-1a | 10.0.20.0/24 | af-south-1a |
| Data Subnet 2 | fintrust-data-1b | 10.0.21.0/24 | af-south-1b |

## Resources Created

- VPC: fintrust-vpc (10.0.0.0/16)
- Internet Gateway: fintrust-igw (Attached)
- NAT Gateways: fintrust-nat-1a, fintrust-nat-1b (one per AZ)
- Elastic IPs: 2 allocated (one per NAT Gateway)
- Route Tables: 1 public, 2 private (one per AZ)
- Security Groups: alb-sg, app-sg, db-sg

## Route Tables

| Route Table | Route | Associated Subnets |
|-------------|-------|-------------------|
| fintrust-rt-public | 0.0.0.0/0 -> IGW | public-1a, public-1b |
| fintrust-rt-private-1a | 0.0.0.0/0 -> nat-1a | app-1a, data-1a |
| fintrust-rt-private-1b | 0.0.0.0/0 -> nat-1b | app-1b, data-1b |

## Security Groups

### alb-sg (Public)
| Rule | Source | Port | Description |
|------|--------|------|-------------|
| Inbound | 0.0.0.0/0 | 443 | HTTPS from internet |
| Inbound | 0.0.0.0/0 | 80 | HTTP from internet (redirect) |
| Outbound | app-sg | 8080 | Forward to application tier |

### app-sg (Application)
| Rule | Source | Port | Description |
|------|--------|------|-------------|
| Inbound | alb-sg | 8080 | From ALB only |
| Outbound | db-sg | 5432, 6379, 27017 | To database tier |
| Outbound | 0.0.0.0/0 | 443 | HTTPS for updates |

### db-sg (Data)
| Rule | Source | Port | Description |
|------|--------|------|-------------|
| Inbound | app-sg | 5432 | PostgreSQL from app only |
| Inbound | app-sg | 6379 | Redis from app only |
| Inbound | app-sg | 27017 | MongoDB from app only |

## Security Group vs NACL Challenge Answers

| # | Requirement | Answer | Why? |
|---|-------------|--------|------|
| 1 | Block all traffic from 41.0.0.0/8 | NACL DENY rule on app subnet | Security Groups cannot DENY. NACL is subnet-level and can explicitly block IP ranges. |
| 2 | Allow ALB to forward to ECS on port 8080 | Security Group rule on app-sg | SG is stateful and can reference alb-sg as source. This follows instance identity, not just IPs. |
| 3 | Database only from app tier | Security Group rule on db-sg | SG reference ensures only app-tier ENIs qualify. CIDR would not prevent ALB directly accessing the database. |

## NACL Statelessness Trap

If you add a NACL inbound rule allowing HTTP (port 80), you must also add an outbound rule allowing ephemeral ports 1024-65535. Without this, the server processes the request but the response is dropped at the subnet boundary.

## Traffic Path

User HTTPS Request -> Internet -> IGW -> ALB -> Security Group (alb-sg) -> Security Group (app-sg) -> ECS Task -> Security Group (db-sg) -> Database

## Reflection Questions

### 1. If af-south-1a NAT Gateway fails, which resources lose internet access?
App-1a and data-1a subnets lose internet access because they route through nat-1a. App-1b and data-1b continue to work through nat-1b. This is why we use one NAT per AZ.

### 2. If EC2 instance has public IP in public-1a, can internet reach it?
Yes, if:
- It has a public IP or Elastic IP
- The subnet is associated with the public route table (0.0.0.0/0 -> IGW)
- IGW is attached to the VPC
- Security Group allows inbound on the required port
- NACL allows inbound and outbound ephemeral ports

### 3. Why does db-sg reference app-sg instead of CIDR?
Security Group references follow instance identity, not IP addresses. If app instances scale or change IPs, the rules stay valid. CIDR would only cover a static IP range and would not scale with the application.

### 4. One thing that surprised me about VPC networking
NACL statelessness. The fact that allowing inbound traffic doesn't automatically allow outbound responses is counterintuitive. You need to explicitly allow ephemeral ports outbound.

## Verification Checkpoints

- [ ] VPC exists with CIDR 10.0.0.0/16
- [ ] 6 subnets exist with correct AZ and CIDR
- [ ] IGW is attached to VPC
- [ ] Public route table has 0.0.0.0/0 -> IGW
- [ ] Public subnets are associated with public route table
- [ ] Both NAT Gateways show status Available
- [ ] Private route tables point to their AZ's NAT Gateway
- [ ] app and data subnets are associated with correct private route tables
- [ ] alb-sg, app-sg, db-sg created with correct rules