import argparse
import csv
import os
import sys

from collections import defaultdict
from tabulate import tabulate


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--files',
        nargs='+',
        type=str,
        required=True,
        help='CSV file to read')
    parser.add_argument(
        '--report',
        type=str,
        required=True,
        choices=['performance'],
        help='Type of report to generate')
    args = parser.parse_args(argv)
    for file_path in args.files:
        if not os.path.exists(file_path):
            parser.error(f"Path doesn't exist: {file_path}")

        _, ext = os.path.splitext(file_path)
        if ext.lower() != '.csv':
            parser.error(f"Incorrect file format ({ext}): {file_path}. All files should be in 'csv' format.")
    return args

def read_rows_from_files(path_files: list[str]) -> list[dict[str, str]]:
    rows = []
    for path in path_files:
        with open(path, encoding='utf-8') as file:
            reader = csv.DictReader(file)
            rows.extend(reader)
    return rows

def build_performance_data(rows: list[dict[str, str]]) -> list[tuple[str, float]]:
    data = defaultdict(lambda: [0.0, 0])
    for row in rows:
        data[row['position']][0] += float(row['performance'])
        data[row['position']][1] += 1
    calculated_data = []
    for pos, (summary, counter) in data.items():
        calculated_data.append((pos, summary / counter))

    calculated_data.sort(key=lambda x: x[1], reverse=True)
    return calculated_data

def display_report(data: list[tuple[str, float]]):
    table = [(pos, f'{avg:.2f}') for pos, avg in data]
    print(tabulate(table, headers=['Position', 'Avg Performance'], tablefmt='github'))


def main(argv=None):
    args = parse_args(argv or sys.argv[1:])
    rows = read_rows_from_files(args.files)
    print(rows)
    calc_data = build_performance_data(rows)
    display_report(calc_data)



if __name__ == '__main__':
    main()
