[//]: # (SPDX-License-Identifier: BSD-3-Clause)
[//]: # (Copyright 2021-2022, Intel Corporation)

# redis-cluster on k8s testcase

In this repository you can find scripts to run a memtier_benchmark on a cluster of k8s-hosted [Redis](https://redis.io/) & [TieredMemDB](https://tieredmemdb.io/) servers. 

## Repository structure
The repository is divided into subdirectories as follows:
* [`ansible-playbook`](./ansible-playbook) - contains Ansible playbooks to run a memtier_benchmark on a k8s-hosted redis-cluster(s).
* [`docker_bitnami`](./docker_bitnami) - contains TieredMemDB Docker image. Dockerfile is aligned with [Bitnami redis-cluster](https://github.com/bitnami/bitnami-docker-redis-cluster) image.
* [`systemd_unit`](./systemd_unit) - contains systemd unit files for exposing PMem devices as system-ram.

To get more information about usage of scripts in the subdirectories, follow their respective READMEs.

## Prerequisites
Before you start working with the repository, make sure you have installed:
* **Python 3.6+**
* **Helm**
* **Kubernetes**
* **Docker** (required to build TieredMemDB image)
