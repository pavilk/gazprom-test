#!/usr/bin/env bash
set -euo pipefail

sudo kubeadm init --pod-network-cidr=10.244.0.0/16

mkdir -p ~/.kube
sudo cp /etc/kubernetes/admin.conf ~/.kube/config
sudo chown "$(id -u):$(id -g)" ~/.kube/config

curl -fsSL https://raw.githubusercontent.com/helm/helm/main/scripts/get-helm-3 | bash

helm repo add cilium https://helm.cilium.io
helm install cilium cilium/cilium --version 1.18.0 -n kube-system --set ipam.mode=kubernetes
