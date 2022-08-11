[//]: # (SPDX-License-Identifier: BSD-3-Clause)
[//]: # (Copyright 2021-2022, Intel Corporation)

# tieredmemdb-bitnami Docker image

Please use Dockefiles in this directory to build images that will work with [Bitnami redis-cluster](https://github.com/bitnami/charts/tree/master/bitnami/redis-cluster) Docker image (versions 6.0.9 and 6.2.6).

TieredMemDB is a fork of Redis, adjusted to store objects on both Intel Optane Persistent Memory and DRAM. TieredMemDB is using PMem AppDirect volatile mode (KMEM DAX). TieredMemDB requires Linux kernel 5.1 or higher in order to take advantage of KMEM DAX feature which is used to expose PMem device as a system-ram.
> Note: To enable `--mode=system-ram` via `daxctl`, please refer to [README](../systemd_unit/README.md) in `systemd_unit` directory of this repository.  

## How to use the image?
After building the image, push it to the docker registry of your choice and update `values.yaml` file for the Helm deployment with proper registry, repository and tag entries. See [this part of values.yaml](https://github.com/bitnami/charts/blob/master/bitnami/redis-cluster/values.yaml#L70-L75) file for reference.
> Note: To use the image with benchmarking scripts, please refer to [README](../ansible-playbook/README.md) in `ansible-playbook` directory of this repository.
