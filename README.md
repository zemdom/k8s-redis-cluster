[//]: # (SPDX-License-Identifier: BSD-3-Clause)
[//]: # (Copyright 2021, Intel Corporation)

# redis-cluster on k8s testcase

In this repository you can find scripts to run a memtier benchmark on a cluster of k8s-hosted Redis & TieredMemDB servers. 

## Repository structure
The repository is divided into subdirectories as follows:
* [`ansible-playbook`](./ansible-playbook) - contains ansible playbooks to run a memtier benchmark on a k8s-hosted redis-cluster(s).
* [`docker_bitnami`](./docker_bitnami) - contains TieredMemDB Docker image. Dockerfile is aligned with [Bitnami redis-cluster](https://github.com/bitnami/bitnami-docker-redis-cluster) image.
* [`systemd_unit`](./systemd_unit) - contains systemd unit files for exposing PMem devices as system-ram.

To get more information about usage of scripts in the subdirectories, follow their respective READMEs.

## Prerequisites
Before you start working with the repository, make sure you have installed:
* **Ansible 2.9**
* **Helm**
* **k8s**
* **Docker** (required to build TieredMemDB image)
