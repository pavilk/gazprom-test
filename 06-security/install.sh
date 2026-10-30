#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")"

curl -fsSL https://istio.io/downloadIstio | sh -
sudo install istio-*/bin/istioctl /usr/local/bin/
istioctl install --set profile=minimal \
  --set values.pilot.resources.requests.cpu=100m \
  --set values.pilot.resources.requests.memory=256Mi -y

helm repo add gatekeeper https://open-policy-agent.github.io/gatekeeper/charts
helm install gatekeeper gatekeeper/gatekeeper -n gatekeeper-system --create-namespace \
  --set replicas=1 --wait

LIB=https://raw.githubusercontent.com/open-policy-agent/gatekeeper-library/master/library
kubectl apply \
  -f "$LIB/pod-security-policy/users/template.yaml" \
  -f "$LIB/pod-security-policy/read-only-root-filesystem/template.yaml" \
  -f "$LIB/general/containerlimits/template.yaml"

kubectl -n istio-system get pods
kubectl -n gatekeeper-system get pods
kubectl get constrainttemplates
