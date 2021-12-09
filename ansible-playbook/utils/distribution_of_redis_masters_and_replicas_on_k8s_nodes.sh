#!/bin/bash

# SPDX-License-Identifier: BSD-3-Clause
# Copyright 2021, Intel Corporation

# masters
echo "---MASTERS---"
for x in 2 3 4 5 6 8; do echo "Count of redis-masters on node:" compute-1-$x; kubectl get po -o wide -A | egrep redis-cluster-[0-2] | grep compute-1-$x | wc -l; done

# replicas
echo "---REPLICAS---"
for x in 2 3 4 5 6 8; do echo "Count of redis-replicas on node:" compute-1-$x; kubectl get po -o wide -A | egrep redis-cluster-[3-5] | grep compute-1-$x | wc -l; done
