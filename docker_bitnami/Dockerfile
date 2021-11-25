# SPDX-License-Identifier: BSD-3-Clause
# Copyright 2021, Intel Corporation
#

FROM debian:buster-slim AS builder
LABEL maintainer="tbd"

# define variables
ARG TIEREDMEMDB_COMMIT=0d0d383
ENV REDIS_REPO="https://github.com/TieredMemDB/TieredMemDB.git" \
    REDIS_COMMIT="${TIEREDMEMDB_COMMIT}" \
    LD_LIBRARY_PATH="/usr/local/lib" \
    PREFIX="/opt/bitnami/redis" \
    HOME="/" \
    OS_ARCH="amd64" \
    OS_FLAVOUR="debian-10" \
    OS_NAME="linux" \
    BITNAMI_APP_NAME="redis" \
    BITNAMI_IMAGE_VERSION="6.0.9-debian-10-r7" \
    PATH="/opt/bitnami/common/bin:/opt/bitnami/redis/bin:$PATH"

RUN set -eux; \
    \
    savedAptMark="$(apt-mark showmanual)"; \
    echo "deb http://deb.debian.org/debian buster-backports main" | tee /etc/apt/sources.list.d/buster-backports.list; \
    apt-get update; \
    apt-get install -y --no-install-recommends \
        acl \
        autoconf \
        automake \
        binutils \
        ca-certificates \
        curl \
        daxctl \
        g++ \
        gcc \
        git \
        gzip \
        libc6 \
        libc6-dev \
        libcap2-bin \
        libssl1.1 \
        libssl-dev \
        libtool \
        libdaxctl-dev \
        libnuma-dev \
        make \
        ndctl \
        numactl \
        pkg-config \
        procps \
        tar \
        tcl \
        unzip \
        wget \
    ; \
    apt-get install -y --no-install-recommends -t buster-backports libdaxctl-dev ndctl libcap2-bin; \
    rm -rf /var/lib/apt/lists/*; \
    \
# redis download and choose specific commit
    mkdir -p /opt/redis; \
    git clone ${REDIS_REPO} /opt/redis; \
    cd /opt/redis && git reset --hard ${REDIS_COMMIT}; \
    cd /opt/redis && git submodule init && git submodule update; \
    \
# disable Redis protected mode [1] as it is unnecessary in context of Docker
# (ports are not automatically exposed when running inside Docker, but rather explicitly by specifying -p / -P)
# [1]: https://github.com/antirez/redis/commit/edd4d555df57dc84265fdfb4ef59a4678832f6da
    grep -E '^ *createBoolConfig[(]"protected-mode",.*, *1 *,.*[)],$' /opt/redis/src/config.c; \
    sed -ri 's!^( *createBoolConfig[(]"protected-mode",.*, *)1( *,.*[)],)$!\10\2!' /opt/redis/src/config.c; \
    grep -E '^ *createBoolConfig[(]"protected-mode",.*, *0 *,.*[)],$' /opt/redis/src/config.c; \
# for future reference, we modify this directly in the source instead of just supplying a default configuration flag because apparently "if you specify any argument to redis-server, [it assumes] you are going to specify everything"
# see also https://github.com/docker-library/redis/issues/4#issuecomment-50780840
# (more exactly, this makes sure the default behavior of "save on SIGTERM" stays functional by default)
    cd /opt/redis && make MALLOC=memkind; \
    cd /opt/redis && make install; \
    \
# TODO https://github.com/antirez/redis/pull/3494 (deduplicate "redis-server" copies)
    serverMd5="$(md5sum ${PREFIX}/bin/redis-server | cut -d' ' -f1)"; export serverMd5; \
    find ${PREFIX}/bin/redis* -maxdepth 0 \
            -type f -not -name redis-server \
            -exec sh -eux -c ' \
                    md5="$(md5sum "$1" | cut -d" " -f1)"; \
                    test "$md5" = "$serverMd5"; \
            ' -- '{}' ';' \
            -exec ln -svfT 'redis-server' '{}' ';' \
    ; \
    \
    rm -r /opt/redis; \
    \
    apt-mark auto '.*' > /dev/null; \
    [ -z "$savedAptMark" ] || apt-mark manual $savedAptMark > /dev/null; \
    find $PREFIX -type f -executable -exec ldd '{}' ';' \
            | awk '/=>/ { print $(NF-1) }' \
            | sort -u \
            | xargs -r dpkg-query --search \
            | cut -d: -f1 \
            | sort -u \
            | xargs -r apt-mark manual \
    ; \
    apt list;
    #apt-get purge -y --auto-remove -o APT::AutoRemove::RecommendsImportant=false;

COPY prebuildfs /
RUN chmod g+rwX /opt/bitnami
COPY rootfs /
RUN /opt/bitnami/scripts/redis-cluster/postunpack.sh

EXPOSE 6379

ENTRYPOINT [ "/opt/bitnami/scripts/redis-cluster/entrypoint.sh" ]
CMD [ "/opt/bitnami/scripts/redis-cluster/run.sh" ]
