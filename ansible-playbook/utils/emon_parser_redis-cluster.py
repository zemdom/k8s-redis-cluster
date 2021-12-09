#!/usr/bin/python3

# SPDX-License-Identifier: BSD-3-Clause
# Copyright 2021, Intel Corporation

import os
import sys
from argparse import ArgumentParser
from os.path import basename, dirname, isfile, join

import openpyxl


def get_labels():
    template_wb = openpyxl.load_workbook(template_name)
    sheet = template_wb.active

    sheet_labels = [c.value for c in sheet['A']]
    return sheet_labels


def parse_emon_workbook(name):
    avg_column = 'B'
    emon_params = [name]

    curr_wb = openpyxl.load_workbook(name)
    script = curr_wb.active
    for label in labels:
        for cell in script['A']:
            if cell.value == label:
                emon_params.append(script[avg_column + str(cell.row)].value)

    return emon_params


def fill_in_workbook(_file, types, script, run_number, all_compared_runs_number):
    emon_params = parse_emon_workbook(_file)
    for type in types:
        if type in _file.lower():
            col = types[type]
            col = (col * all_compared_runs_number) + col + run_number + 2

            for i, r in enumerate(emon_params):
                script.cell(row=i+1, column=col).value = r

single_cluster_types = {
    'master1': 0,
    'master2': 1,
    'master3': 2,
    'replica1': 3,
    'replica2': 4,
    'replica3': 5
}
multiple_clusters_types = {
    'compute-1-2': 0,
    'compute-1-3': 1,
    'compute-1-4': 2,
    'compute-1-5': 3,
    'compute-1-6': 4,
    'compute-1-8': 5
}

template_name = join(dirname(sys.argv[0]), 'EMON_TEMPLATE_redis-cluster.xlsx')
labels = get_labels()


def main():
    parser = ArgumentParser(
        description="Excel generator agregating data collected by Emon monitor while running various benchmarks")
    parser.add_argument(
        '-p', '--paths', dest='paths', help='Paths to directories with *.xlsx files to compare', nargs='+', default=[])
    parser.add_argument(
        '-n', '--name', dest='result_file_name', default='results', help='Name of the aggregated result file name')
    parser.add_argument(
        '--single-cluster', dest='single_cluster', default=False, help='Create comparison of redis-cluster instances instead of compute nodes', action='store_true')
    args = vars(parser.parse_args())

    paths = args['paths']
    result_wb = openpyxl.load_workbook(template_name)
    script = result_wb.active

    directories = [[join(path, obj) for obj in os.listdir(path)] for path in paths]
    directories = [[obj for obj in directory if isfile(obj) and obj.endswith('.xlsx')] for directory in directories]
    all_compared_runs_number = len(directories) - 1

    types = single_cluster_types if args['single_cluster'] else multiple_clusters_types

    for run_number, _directory_content in enumerate(directories):
        for _file in _directory_content:
            print('Processing: ' + basename(_file))
            fill_in_workbook(_file, types, script, run_number, all_compared_runs_number)

    result_wb.save(filename=args['result_file_name'] + '.xlsx')
    print('Saving output file ' + args['result_file_name'] + '.xlsx')


if __name__ == '__main__':
    main()
