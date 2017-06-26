#!/bin/bash
for (( i=10; i>0; i--)); do
  sleep 60 &
  source disk_test.sh
  wait
done