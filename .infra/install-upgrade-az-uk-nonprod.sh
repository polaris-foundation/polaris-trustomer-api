#!/bin/bash

# the dhos-trustomer-api runs on its own namespace -
# the plan is to have microservices run on their own namespaces in a pure multi-tenanted deployment
API_NAMESPACE=dhos-trustomer-api
kubectl get ns ${API_NAMESPACE} > /dev/null 2>&1

# create our namespace if it doesn't exist
if [[ "$?" -ne "0" ]]; then
  kubectl create ns ${API_NAMESPACE}
fi

## check helm version - we need helm 3
helm version --client --short | grep "v3." > /dev/null 2>&1

if [[ "$?" -ne "0" ]]; then
  echo "error: incorrect helm version helm3."
  exit 1
fi

echo Installing or upgrading helm chart
helm upgrade --install --namespace ${API_NAMESPACE} dhos-trustomer-api $(dirname ${BASH_SOURCE})/helm-chart/dhos-trustomer-api \
     -f $(dirname ${BASH_SOURCE})/helm-chart/dhos-trustomer-api/values.yaml \
     -f $(dirname ${BASH_SOURCE})/helm-chart/dhos-trustomer-api/values-az-uk-nonprod001.yaml
