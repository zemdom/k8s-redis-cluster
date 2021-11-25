[//]: # (SPDX-License-Identifier: BSD-3-Clause)
[//]: # (Copyright 2021, Intel Corporation)

# redis-cluster and memtier_benchmark on k8s playbooks

## General info
The redis-cluster testing can be run for **Redis** or for **TieredMemDB**, to choose between the databases set the `test_mode` variable value to `redis` or to `tmdb`.

### Running single cluster testcase
By default the value of `clusters_count` variable is set to `1`, so to run single cluster testcase do not set the variable or set its value to `1`.

### Running multiple clusters testcase
To run multiple clusters testcase, the variable needs to be set to the number of redis-cluster deployments to create.

### Collecting results
Benchmark logs and run metadata are uploaded to `{{ logdir_default }}/{{ log_dir_structure }}` directory on utility host (variables values are set in `vars.yml`). The results can be optionally uploaded to an S3 bucket.

### k8s namespaces
For a single cluster case, cluster objects are deployed to `redis-cluster1` k8s namespace.\
For multiple clusters, each redis-cluster is created in separate namespace named according to the convention: `redis-cluster<cluster-number>`.

## How to run

### Prework
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

1. Deploy redis-cluster(s):
```shell
clusters_count=<optional> test_mode=<redis_or_tmdb> ansible-playbook -i inventory deploy.yml
```

2. Populate redis-cluster(s): 
```shell
clusters_count=<optional> run_id=<run_identifier> ansible-playbook -i inventory populate.yml
```

3. Run memtier_benchmark (use the same `run_id` as in the population step):
```shell
clusters_count=<optional> run_id=<run_identifier> ansible-playbook -i inventory run_benchmark.yml [--extra-vars "@s3_vars.yml"]
```

4. Cleanup - uninstall redis-cluster(s):
```shell
clusters_count=<optional> ansible-playbook -i inventory destroy.yml
```
\
Above four steps are equivalent to running:
```shell
clusters_count=<optional> test_mode=<redis_or_tmdb> run_id=<run_identifier> ansible-playbook -i inventory run_all.yml [--extra-vars "@s3_vars.yml"]
```

## Environment variables (selection)

### General
* `run_id`
* `test_mode`: Possible values - `redis` or `tmdb`;
* `clusters_count`: Number of redis-clusters to deploy (default: `1`);
* `collect_emon_data`: Specifies whether to run EMON during benchmark execution (default: `False`);
* `multiple_clusters_balanced`: (default: `True`);
* `warm_up_benchmark_run`: Specifies whether to run one warm-up benchmark run before test execution (default: `False`);

### Redis & TieredMemDB specific
* `multithreading`: Used to switch on/off io-threads parameter in Redis & TieredMemDB (default: `True`);
* `threads`: Number of io-threads to use (default: `8`);
* `dram_pmem_ratio`: Expected proportion of memory placement between DRAM and PMem (default: `1 3`);
* `pmem_variant`: Specifies variant of Persistent Memory allocation (default: `multiple`)

### memtier_benchmark specific
* `clients`
* `datasize`
* `pipeline`
* `requests`

### S3 bucket specific
* `S3_ACCESS_KEY`
* `S3_BUCKET`
* `S3_ENDPOINT`
* `S3_SECRET_KEY`
