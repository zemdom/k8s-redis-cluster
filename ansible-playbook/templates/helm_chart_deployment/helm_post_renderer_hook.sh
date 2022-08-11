#!/bin/bash

# SPDX-License-Identifier: BSD-3-Clause
# Copyright 2021-2022, Intel Corporation

cat <&0 > $KUSTOMIZE_DIR/all.yml
kubectl kustomize $KUSTOMIZE_DIR
