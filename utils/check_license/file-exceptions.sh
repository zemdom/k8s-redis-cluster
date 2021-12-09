#!/bin/sh -e

# SPDX-License-Identifier: BSD-3-Clause
# Copyright 2016-2021, Intel Corporation

# file-exceptions.sh - filter out files not checked for copyright and license

grep -v -E -e '.github' -e 'docker_bitnami/Dockerfile' -e '.ansible-lint' -e 'ansible-playbook/utils/EMON_TEMPLATE_redis-cluster.xlsx' -e 'CONTRIBUTING.md' -e 'LICENSE-THIRD-PARTY.md'
