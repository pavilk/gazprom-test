#!/usr/bin/env bash
set -euo pipefail

K8S_VERSION=v1.34

echo 'net.ipv4.ip_forward = 1' > /etc/sysctl.d/99-k8s.conf
sysctl --system >/dev/null

apt-get update
apt-get install -y containerd
mkdir -p /etc/containerd
containerd config default > /etc/containerd/config.toml
sed -i 's/SystemdCgroup = false/SystemdCgroup = true/' /etc/containerd/config.toml
systemctl restart containerd

curl -fsSL "https://pkgs.k8s.io/core:/stable:/$K8S_VERSION/deb/Release.key" \
  | gpg --dearmor --yes -o /etc/apt/keyrings/kubernetes-apt-keyring.gpg
echo "deb [signed-by=/etc/apt/keyrings/kubernetes-apt-keyring.gpg] https://pkgs.k8s.io/core:/stable:/$K8S_VERSION/deb/ /" \
  > /etc/apt/sources.list.d/kubernetes.list
apt-get update
apt-get install -y kubelet kubeadm kubectl
