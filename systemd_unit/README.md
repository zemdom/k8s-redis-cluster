[//]: # (SPDX-License-Identifier: BSD-3-Clause)
[//]: # (Copyright 2021, Intel Corporation)

# What is it for?

The goal is to have PMem devices exposed as a system-ram after system reboots, when PMem dimms are ready.
In order to achieve that following command
```shell
daxctl reconfigure-device --mode=system-ram all
```
should be executed before `kubelet.service` starts but not earlier than PMem dimms are available in the OS.
This way kubelet and docker will have visibility on all `/sys/fs/cgroup/cpuset/cpuset.mems` available on the host node
(additional PMem numa nodes).

# How to use systemd units in this directory?

1. Copy `dax*` files to `/etc/systemd/system/`:
```shell
cp dax* /etc/systemd/system/
```
2. Enable necessary units:
```shell
systemctl enable dax-waitdev.path
systemctl enable dax.timer
```
