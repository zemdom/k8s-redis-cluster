#!/bin/bash

# SPDX-License-Identifier: BSD-3-Clause
# Copyright 2021-2022, Intel Corporation

redis_nodes_count=$(kubectl get po -o wide -A | egrep 'redis-cluster-[0-9]{1,}' | awk -F ' {2,}' '{print $2}' | sort | uniq | wc -l)

echo "---MASTERS---"
kubectl get po -o wide -A | egrep redis-cluster-[0-$((redis_nodes_count / 2 - 1))] | awk -F ' {2,}' '{print $8}' | sort | uniq -c | awk {'print "Count of redis-masters on node: "$2"\n"$1'}

echo "---REPLICAS---"
kubectl get po -o wide -A | egrep redis-cluster-[$((redis_nodes_count / 2))-$((redis_nodes_count - 1))] | awk -F ' {2,}' '{print $8}' | sort | uniq -c | awk {'print "Count of redis-replicas on node: "$2"\n"$1'}
