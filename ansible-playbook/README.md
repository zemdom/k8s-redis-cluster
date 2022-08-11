[//]: # (SPDX-License-Identifier: BSD-3-Clause)
[//]: # (Copyright 2021-2022, Intel Corporation)

# redis-cluster and memtier_benchmark on k8s playbooks

## General info
The redis-cluster testing can be run for **Redis** or for **TieredMemDB**, to choose between the databases set the `test_mode` variable value to `redis` or to `tmdb`.

The test can be run in three variants:
* **single cluster** - when only one redis-cluster is deployed and benchmarked;
* **multiple clusters** - when more than one redis-cluster is created and benchmarked. The variant comes in two flavours:
    * **multiple clusters balanced** - the same number of master and replica instances are assiged to each k8s compute node;
    * **multiple clusters unbalanced** - master and replica instances are assigned randomly to the compute nodes;

### Before execution

#### Inventory file
To create an `inventory` file, copy the content of `inventory.example` file and replace the example hostnames for `[computes]`, `[utility]` and `[clients]` groups with own hostnames or IPs.
* The `[computes]` group specifies k8s nodes, where redis-cluster(s) instances are deployed.
* The `[utility]` group specifies a node, which runs the playbooks (ansible controller). The node can reside outside of the k8s cluster, but it needs to be able to communicate with the cluster.
* The `[clients]` group specifies k8s nodes, which run memtier_benchmark instances.

#### Changing default values of environment variables
There are two ways to change default values of environment variables:
* by passing new values as command-line arguments when invoking playbooks:
```shell
<variable1>=<value1> <variable2>=<value2> ansible-playbook -i inventory <playbook_name>.yml
```
* by modifying content of `vars/*` files. To change the value, find corresponding variable name (named according to convention: `<variable name>_default`) in `vars/vars.yml` and overwrite its value. A share of the environment variables is described in [Environment variables (selection)](#environment-variables-selection) paragraph.

#### Preparing for TieredMemDB testcase
To deploy redis-cluster(s) based on TieredMemDB, supply default values of [Registry specific - TieredMemDB](#registry-specific---tieredmemdb) variables in `vars/vars.yml`. Then, set `test_mode` to `tmdb` when invoking playbooks.

#### Preparing for exporting benchmark results to S3 bucket
To export benchmark results to S3 bucket right after testcase run, specify [S3 bucket specific](#s3-bucket-specific) variables in `vars/s3_vars.yml`. Then, pass the file as command-line argument when invoking `run_benchmark.yml` playbook:
```shell
clusters_count=<optional> run_id=<run_identifier> ansible-playbook -i inventory run_benchmark.yml --extra-vars "@vars/s3_vars.yml"
```

#### Preparing for running playbooks behind proxy server
To run playbooks behind proxy, specify default values of [Proxy specific](#proxy-specific) variables in `vars/proxy_vars.yml`. Then, invoke playbooks as usual (as described in [How to run](#how-to-run) section).

### Testcase execution

#### Running single cluster testcase
By default the value of `clusters_count` variable is set to `1`, so to run single cluster testcase do not set the variable or set its value to `1`.

#### Running multiple clusters testcase
To run multiple clusters testcase, the `clusters_count` variable needs to be set to the number of redis-cluster deployments to create.

#### k8s namespaces
For a single cluster case, cluster objects are deployed to `redis-cluster1` k8s namespace.\
For multiple clusters, each redis-cluster is created in separate namespace named according to the convention: `redis-cluster<cluster-number>`.

#### Test run identifier
By default the value of `run_id` variable is set according to the convention: `<four-character-random-hash>-th{{ threads }}-cln{{ clients }}-p{{ pipeline }}-req{{ requests }}`. It can be accessed after execution of `populate.yml` playbook in `group_vars/all` file.

### After execution

#### Collecting results
Benchmark logs and run metadata are uploaded to `{{ logdir_default }}/{{ log_dir_structure }}` directory on utility host (those variables values are set in `vars/vars.yml`). The results can be optionally uploaded to an S3 bucket, as described in [Preparing for exporting benchmark results to S3 bucket](#preparing-for-exporting-benchmark-results-to-s3-bucket) paragraph.

## How to run

### Prework
Prepare OS for running Ansible playbooks - install Ansible and other necessary Python packages using pip (needs to be run only once):
```shell
pip3 install -r utils/controller_requirements.txt
```
Prepare OS for running benchmarking playbooks - install necessary Python packages and Ansible collections (needs to be run only once):
```shell
ansible-playbook -i inventory setup.yml
```
Prepare k8s cluster for running benchmarking playbooks - add Helm chart repositories and label nodes (needs to be run only once):
```shell
ansible-playbook -i inventory setup_k8s_specific.yml
```

### Run test 
You can choose to run the test step by step or to run all the steps at once.

Running step by step:

**1. Deploy redis-cluster(s):**
```shell
clusters_count=<optional> test_mode=<redis_or_tmdb> ansible-playbook -i inventory deploy.yml
```
> For this step you can modify [Redis & TieredMemDB specific](#redis--tieredmemdb-specific) variables (as described in [Changing default values of environment variables](#changing-default-values-of-environment-variables)).

\
**2. Populate redis-cluster(s):**
```shell
clusters_count=<optional> run_id=<run_identifier> ansible-playbook -i inventory populate.yml
```
> For this step you can modify selected [memtier_benchmark specific](#memtier_benchmark-specific) variables.

\
**3. Run memtier_benchmark**:
```shell
clusters_count=<optional> ansible-playbook -i inventory run_benchmark.yml [--extra-vars "@vars/s3_vars.yml"]
```
> For this step you can modify [memtier_benchmark specific](#memtier_benchmark-specific) variables.

\
**4. Cleanup - uninstall redis-cluster(s):**
```shell
clusters_count=<optional> ansible-playbook -i inventory destroy.yml
```
\
Above four steps are equivalent to running:
```shell
clusters_count=<optional> test_mode=<redis_or_tmdb> run_id=<run_identifier> ansible-playbook -i inventory run_all.yml [--extra-vars "@vars/s3_vars.yml"]
```

## Environment variables (selection)

### General
* `test_mode`: Possible values - `redis` or `tmdb`;
* `clusters_count`: Number of redis-clusters to deploy (default: `1`);
* `collect_emon_data`: Specifies whether to run EMON during benchmark execution (default: `False`);
* `multiple_clusters_balanced`: Specifies whether to run balanced testcase (default: `True`) (further description in [General info](#general-info));
* `run_id`: Test run identifier (default: auto-generated value) (further description in [Test run identifier](#test-run-identifier));
* `warm_up_benchmark_run`: Specifies whether to run one warm-up benchmark run before test execution (default: `False`);

### Redis & TieredMemDB specific
* `multithreading`: Used to switch on/off io-threads parameter in Redis & TieredMemDB (default: `True`);
* `threads`: Number of io-threads to use (default: `8`);
* `dram_pmem_ratio`: Expected proportion of memory placement between DRAM and PMem (default: `1 3`);
* `pmem_variant`: Specifies variant of Persistent Memory allocation (default: `multiple`)

### memtier_benchmark specific
* `clients`: Number of clients per thread (default: `3`);
* `datasize`: Object data size in bytes (default: `1024`);
* `key_pattern`: Set:Get requests pattern used for benchmark execution (default: `G:G`);
* `pipeline`: Number of concurrent pipelined requests (default: `1`);
* `ratio`: Set:Get requests ratio used for benchmark execution (default: `1:4`);
* `requests`: Number of total requests per client (default: `150000000`);
* `run_count`: Number of full-test iterations to perform during benchmark execution (default: `3`);
* `test_time`: Number of seconds to run one full-test iteration during benchmark execution (default: `1800`);
* `threads`: Number of threads (default: `8`);

### S3 bucket specific
* `S3_ACCESS_KEY`
* `S3_BUCKET`
* `S3_ENDPOINT`
* `S3_SECRET_KEY`

### Registry specific - Redis
* `redis_registry`
* `redis_repository`
* `redis_tag`

### Registry specific - TieredMemDB
* `tmdb_registry`
* `tmdb_repository`
* `tmdb_tag`

### Proxy specific
* `no_proxy`
* `proxy`