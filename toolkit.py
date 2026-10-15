#!/usr/bin/env python3
"""Automated Network Reconnaissance & Asset Discovery Toolkit v1.0"""
import argparse, csv, json, logging, os, re, socket, subprocess, sys, time
import xml.etree.ElementTree as ET

def discover(network):
    """Ping sweep with Nmap: return list of live host IPs."""
    r = subprocess.run(["nmap", "-sn", network],
                       capture_output=True, text=True)
    hosts = []
    for line in r.stdout.splitlines():
        m = re.search(r"(\d+\.\d+\.\d+\.\d+)", line)
        if line.startswith("Nmap scan report") and m:
            hosts.append(m.group(1))
            logging.debug("Host %s answered ping sweep", m.group(1))
    return hosts

def scan_host(ip, ports=None):
    """Service/version scan of one host, parsed from Nmap XML."""
    cmd = ["nmap", "-sV", "-sT", "-oX", "-", ip]
    if ports:
        cmd[3:3] = ["-p", ports]
    r = subprocess.run(cmd, capture_output=True, text=True)
    found = []
    for port in ET.fromstring(r.stdout).iter("port"):
        if port.find("state").get("state") != "open":
            continue
        svc = port.find("service")
        ver = " ".join(x for x in [svc.get("product", ""),
                       svc.get("version", ""), svc.get("extrainfo", "")] if x)
        found.append({"port": port.get("portid"),
                      "service": svc.get("name"), "version": ver})
    return found

def write_html(results, path="reports/report.html"):
    os.makedirs("reports", exist_ok=True)
    rows = "".join(
        f"<tr><td>{ip}</td><td>{p['port']}</td><td>{p['service']}</td>"
        f"<td>{p['version']}</td></tr>"
        for ip, ports in results.items() for p in ports)
    html = ("<!DOCTYPE html>\n<html><head><title>Recon Report</title>"
            "</head>\n<body><h1>Network Reconnaissance Report</h1>\n"
            f"<p>Hosts up: {len(results)}</p>\n"
            "<table><tr><th>IP</th><th>Port</th><th>Service</th>"
            f"<th>Version</th></tr>{rows}</table>\n</body></html>")
    with open(path, "w") as f:
        f.write(html)
    return path

def update_inventory(results, path="asset_inventory.csv"):
    with open(path, "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["ip", "hostname", "open_ports", "services"])
        for ip, ports in results.items():
            try:
                name = socket.gethostbyaddr(ip)[0]
            except Exception:
                name = "-"
            services = "; ".join(p["service"] for p in ports)
            w.writerow([ip, name, len(ports), services])
    return path

if __name__ == "__main__":
    ap = argparse.ArgumentParser(description="Recon Toolkit v1.0")
    ap.add_argument("--network", required=True,
                    help="target network, e.g. 192.168.56.0/24")
    ap.add_argument("--ports", help="port range (default: top 1000)")
    ap.add_argument("--timeout", type=int, default=60,
                    help="per-host timeout in seconds")
    ap.add_argument("--log-level", default="INFO",
                    choices=["DEBUG", "INFO", "WARNING"])
    ap.add_argument("--html", action="store_true", help="write HTML report")
    ap.add_argument("--inventory", action="store_true",
                    help="write asset inventory CSV")
    args = ap.parse_args()

    logging.basicConfig(filename="toolkit.log", filemode="a",
                        level=getattr(logging, args.log_level),
                        format="%(asctime)s [%(levelname)s] %(message)s",
                        datefmt="%Y-%m-%d %H:%M:%S")
    start = time.time()
    logging.info("Scan started: network=%s ports=%s",
                 args.network, args.ports or "top-1000")
    print("[*] Recon Toolkit v1.0")
    print(f"[*] Discovering live hosts in {args.network} ...")
    hosts = discover(args.network)
    print(f"[+] {len(hosts)} live hosts found: {' '.join(hosts)}")
    results = {}
    for ip in hosts:
        results[ip] = scan_host(ip, args.ports)
        logging.info("%s: %d open ports found", ip, len(results[ip]))
        if results[ip]:
            print(f"[+] {ip}: {len(results[ip])} open ports")
    if args.html:
        p = write_html(results)
        print(f"[+] {p} written ({os.path.getsize(p)} bytes)")
        logging.info("HTML report written to %s", p)
    if args.inventory:
        p = update_inventory(results)
        print(f"[+] {p} updated ({len(results)} assets)")
        logging.info("Asset inventory written to %s", p)
    elapsed = time.time() - start
    print(f"[+] Done in {elapsed:.2f} seconds")
    logging.info("Scan finished in %.2f seconds", elapsed)
