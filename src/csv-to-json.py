import csv
import json
import os
import sys
import argparse


def _get_arg_parser():
    parser = argparse.ArgumentParser(description='Converts csv data to json')
    parser.add_argument('csv-data', help='The csv data to convert')
    parser.add_argument(
        '--indent',
        help='The number of spaces to indent (0 formats without new lines)')
    parser.set_defaults(indent=2)
    return parser

def _run():
    parser = _get_arg_parser()
    args = parser.parse_args()
    print(args)
    max_file_len = os.pathconf('/', 'PC_PATH_MAX')
    csv_data = ''
    # csv_data = args.csv_data
    if csv_data.__len__() <= max_file_len and csv_data.endswith('.csv'):
        pass
    # print(json.dumps([dict(r) for r in csv.DictReader(sys.stdin)], indent=2))


if __name__ == '__main__':
    _run()
