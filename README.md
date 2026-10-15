# 🔐 CYBERSECURITY TASK 2

## Reconnaissance & Nmap — Practice Exercises 1–12

### 📚 Sumerx Global

Kali Linux terminal practice: network reconnaissance, Nmap scanning, DNS analysis, a Python host-discovery script, and a complete **Automated Network Reconnaissance & Asset Discovery Toolkit** — every exercise shown as a terminal run with **real captured command output**.

---

## 📑 Exercise Index

| Ex | Topic | Image |
|----|-------|-------|
| 1 | Host discovery — ping sweep with Nmap (`nmap -sn`) | [01-host-discovery.png](01-host-discovery.png) |
| 2 | Scan common TCP ports on an authorized machine | [02-port-scan.png](02-port-scan.png) |
| 3 | Identify running services and versions (`nmap -sV`) | [03-service-version-detection.png](03-service-version-detection.png) |
| 4 | Capture and analyze DNS packets (tshark — terminal Wireshark) | [04-dns-capture-tshark.png](04-dns-capture-tshark.png) |
| 5 | DNS lookups using `dig` and `nslookup` | [05-dig-nslookup.png](05-dig-nslookup.png) |
| 6 | Compare TCP and UDP scan results | [06-tcp-vs-udp.png](06-tcp-vs-udp.png) |
| 7 | Python-based host discovery script | [07-python-host-discovery.png](07-python-host-discovery.png) |
| 8 | Export scan results to CSV and JSON | [08-export-csv-json.png](08-export-csv-json.png) |
| 9 | **Build the Automated Network Reconnaissance & Asset Discovery Toolkit** (code + run) | [09a-toolkit-code-part1.png](09a-toolkit-code-part1.png), [09b-toolkit-code-part2.png](09b-toolkit-code-part2.png), [09c-toolkit-run.png](09c-toolkit-run.png) |
| 10 | Generate HTML reconnaissance reports | [10-html-report.png](10-html-report.png) |
| 11 | Create a network asset inventory (CSV) | [11-asset-inventory.png](11-asset-inventory.png) |
| 12 | Add logging and configurable scan options | [12-logging-options.png](12-logging-options.png) |

## 🛠️ The Toolkit — `toolkit.py`

**Automated Network Reconnaissance & Asset Discovery Toolkit v1.0**

What it does:
- **Discovery** — ping sweep (`nmap -sn`) to find live hosts on a target network
- **Service scan** — per-host `nmap -sV -sT`, parsed from Nmap XML output
- **HTML report** — writes `reports/report.html` with every open port, service and version
- **Asset inventory** — writes `asset_inventory.csv` (IP, hostname, open-port count, services)
- **Logging + options** — timestamped `toolkit.log`, configurable network, ports, timeout and log level

Run it on Kali Linux against your own lab network:

```bash
python3 toolkit.py --network 192.168.56.0/24
python3 toolkit.py --network 192.168.56.0/24 --ports 1-1024 --html --inventory --log-level DEBUG
python3 toolkit.py --help
```

## 🎤 Interview Preparation — Quick Answers

**What is reconnaissance?**
The first phase of an attack or security assessment — gathering information about a target (IPs, open ports, services, OS, domains, subdomains, people) before acting. Attackers use it to plan; ethical hackers use it to find and fix weaknesses first.

**Passive vs active reconnaissance**
- *Passive:* no direct contact with the target — Google, WHOIS, DNS records, social media, job posts. The target never knows; generally legal.
- *Active:* direct interaction — Nmap port scans, ping sweeps, banner grabbing. More accurate, but detectable and logged, so it needs permission.

**Why is reconnaissance important?**
It reveals the attack surface — open ports, outdated services, exposed systems — so nothing after it is guesswork. Defenders who recon their own network see what an attacker sees and can close gaps first.

**What is Nmap used for?**
Free, open-source network discovery and security auditing: find live hosts, open ports, services and versions on those ports, OS detection, and basic vulnerability checks via NSE scripts.

**SYN scan vs TCP connect scan vs service detection**
- *SYN scan (`-sS`):* sends SYN; the port is open if SYN-ACK returns, then sends RST — the connection never completes, so it is fast and stealthier. Needs root/admin.
- *TCP connect scan (`-sT`):* completes the full handshake (SYN → SYN-ACK → ACK). No special privileges, but slower and easily logged.
- *Service detection (`-sV`):* probes open ports to identify the exact service + version (e.g. Apache 2.4.49, OpenSSH 8.2) — the version tells you which vulnerabilities may apply.

---

> ⚠️ **Lab use only.** All scans were run against machines owned by the author (a local sandbox / virtual lab and its test services). Never scan a network you do not own or have written permission to test.
