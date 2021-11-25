[//]: # (SPDX-License-Identifier: BSD-3-Clause)
[//]: # (Copyright 2021, Intel Corporation)

# docker-image-tieredmemdb-bitnami

Please use this Dockefile and accompanying scripts in subdirectories to build image that will work with https://github.com/bitnami/charts/tree/master/bitnami/redis-cluster

TieredMemDB is a fork of Redis, adjusted to store objects on both Intel Optane Persistent Memory and DRAM. TieredMemDB is using PMem AppDirect volatile mode.  
TieredMemDB requires Linux kernel 5.1 or higher in order to take advantage of KMEM DAX feature which is used to expose PMem device as a system-ram.   
Note: To enable `--mode=system-ram` via `daxctl` refer to README.md in `systemd_unit` directory in this repository.  

After building the image, push it to the docker registry of your choice and update `values.yaml` file for the helm deployment with proper registry, repository and tag entries
see: https://github.com/bitnami/charts/blob/master/bitnami/redis-cluster/values.yaml#L70-L75 for reference

