#!/bin/bash

# SPDX-License-Identifier: BSD-3-Clause
# Copyright 2021, Intel Corporation

cat <&0 > $KUSTOMIZE_DIR/all.yml
kustomize build $KUSTOMIZE_DIR
