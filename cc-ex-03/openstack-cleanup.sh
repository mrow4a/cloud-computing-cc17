#!/bin/bash
# This script removes all floating ips and ports of the current project.
# Floating ips and ports often prevent Heat from deleting a stack. If a stack delete command fails (stack is in state DELETE_FAILED),
# this script can be executed to avoid manual cleanup. Afterwards, the stack should be deleted with another stack delete command.
# Before executing this script, make sure that all instances are deleted, as they might still be using a floating ip or port.
#
# WARNING: this script deletes all floating IPs and ports in your entire project, not only the ones that are part of a Heat stack!
#
# openstack command line client version: 3.11.0
echo "Starting"
# Check parameters
test $# = 1 || { echo "Need 1 parameter: Name of the stack to create"; exit 1; }
STACK="$1"

# Query all floating IPs and ports in the project
floating_ips=$(openstack floating ip list -f value -c ID)
port_ids=$(openstack port list -f value -c ID)

echo "Deleting the following floating IP(s):" $floating_ips
for i in $floating_ips; do
	openstack floating ip unset $i
	openstack floating ip delete $i
done
echo "Deleting the following port(s):" $port_ids
for i in $port_ids; do
	openstack port delete $i
done

openstack stack delete $STACK