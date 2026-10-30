#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")"

echo 'network: {config: disabled}' > /etc/cloud/cloud.cfg.d/99-disable-network-config.cfg
rm -f /etc/netplan/50-cloud-init.yaml
install -m 600 netplan/01-netcfg.yaml /etc/netplan/01-netcfg.yaml
netplan apply

echo 'net.ipv4.ip_forward=1' > /etc/sysctl.d/99-nat.conf
sysctl -p /etc/sysctl.d/99-nat.conf

apt-get update
DEBIAN_FRONTEND=noninteractive apt-get install -y iptables-persistent
install -m 644 iptables/rules.v4 /etc/iptables/rules.v4
iptables-restore < /etc/iptables/rules.v4

ip -br addr
iptables -t nat -S
