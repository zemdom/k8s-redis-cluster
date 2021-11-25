#!/bin/bash


# Copyright (c) 2015-2021 Bitnami

# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at

#     http://www.apache.org/licenses/LICENSE-2.0

# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


# shellcheck disable=SC1091

set -o errexit
set -o nounset
set -o pipefail
# set -o xtrace # Uncomment this line for debugging purpose

# Load Redis environment variables
. /opt/bitnami/scripts/redis-cluster-env.sh

# Load libraries
. /opt/bitnami/scripts/libos.sh
. /opt/bitnami/scripts/librediscluster.sh

IFS=' ' read -ra nodes <<< "$REDIS_NODES"

if ! is_boolean_yes "$REDIS_CLUSTER_CREATOR"; then
    ARGS=("--port" "$REDIS_PORT_NUMBER")
    ARGS+=("--include" "${REDIS_BASE_DIR}/etc/redis.conf")

    if ! is_boolean_yes "$ALLOW_EMPTY_PASSWORD"; then
        ARGS+=("--requirepass" "$REDIS_PASSWORD")
        ARGS+=("--masterauth" "$REDIS_PASSWORD")
    else
        ARGS+=("--protected-mode" "no")
    fi

    ARGS+=("$@")

    if am_i_root; then
        exec gosu "$REDIS_DAEMON_USER" redis-server "${ARGS[@]}"
    else
        exec redis-server "${ARGS[@]}"
    fi
else
    redis_cluster_create "${nodes[@]}"
fi
