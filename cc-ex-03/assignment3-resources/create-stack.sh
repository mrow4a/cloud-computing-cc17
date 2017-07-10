#!/bin/bash

# Check parameters
test $# = 1 || { echo "Need 1 parameter: Name of the stack to create"; exit 1; }
STACK="$1"

# Create the stack using server-landscape.yaml and defining all necessary parameters
[[TODO]]
openstack stack create --template server-landscape.yaml --parameter "external_net=tu-internal;key_pair=piotr-key;flavor=610f44b0-d25a-44bc-a6b1-8b22e68675e5;image=ubuntu-16.04;zone=Cloud Computing 2017" --wait $1

