#!/usr/bin/python3

# SPDX-License-Identifier: BSD-3-Clause
# Copyright 2021-2022, Intel Corporation

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
    for column_index, type in enumerate(types):
        if type in _file.lower():
            col = (column_index * all_compared_runs_number) + column_index + run_number + 2

            for row_index, cell_value in enumerate(emon_params):
                script.cell(row=row_index+1, column=col).value = cell_value

single_cluster_types = [
    'master1',
    'master2',
    'master3',
    'replica1',
    'replica2',
    'replica3'
]

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
        '--multiple-clusters-hostnames', dest='multiple_clusters_hostnames', help='Create comparison of k8s compute nodes instead of redis-cluster instances', nargs='+', default=[], required=False)
    args = vars(parser.parse_args())

    paths = args['paths']
    result_wb = openpyxl.load_workbook(template_name)
    script = result_wb.active

    directories = [[join(path, obj) for obj in os.listdir(path)] for path in paths]
    directories = [[obj for obj in directory if isfile(obj) and obj.endswith('.xlsx')] for directory in directories]
    all_compared_runs_number = len(directories) - 1

    types = args['multiple_clusters_hostnames'] if args['multiple_clusters_hostnames'] else single_cluster_types

    for run_number, _directory_content in enumerate(directories):
        for _file in _directory_content:
            print('Processing: ' + basename(_file))
            fill_in_workbook(_file, types, script, run_number, all_compared_runs_number)

    result_wb.save(filename=args['result_file_name'] + '.xlsx')
    print('Saving output file ' + args['result_file_name'] + '.xlsx')


if __name__ == '__main__':
    main()
