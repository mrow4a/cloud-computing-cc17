#!/bin/bash

echo "*** Deleting old stack... ***"
openstack floating ip list
openstack server remove floating ip frontend 10.200.1.176

sleep 5

openstack stack delete group32-stack
#
sleep 25

echo "*** Create new stack... ***"
openstack stack create --template cc-ex-02/intro-heat/server-landscape.yaml --parameter "key_pair=piotr-key;flavor=610f44b0-d25a-44bc-a6b1-8b22e68675e5;image=ubuntu-16.04" group32-stack

sleep 20
#
echo "*** Assign floating ip... ***"
openstack stack show group32-stack
#ssh-keygen -f "/home/mrow4a/.ssh/known_hosts" -R 10.200.1.169
#openstack server add floating ip group32-instance 10.200.1.169
#ssh -i cloud.key ubuntu@10.200.1.169
#
echo "*** DONE ***"
