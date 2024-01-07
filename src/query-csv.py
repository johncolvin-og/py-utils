import argparse
from pathlib import Path
import traceback


def _get_arg_parser():
    parser = argparse.ArgumentParser(
        description='Request historic data from cme')
    parser.add_argument('file', help='CSV file to query')
    parser.add_argument('column', help='Column for which to get unique values')
    return parser


def _get_nth_occurrence(s: str, substr: str, n: int, from_i=0):
    if n < 1:
        raise ValueError(
            "n must be positive (we're finding the nth occurrence of a substr)"
        )
    i = from_i
    pos = 0
    for _ in range(0, n):
        i = s.index(substr, pos)
        if s[i] != substr[0]:
            raise ValueError(f'Seriously?!! {s[i]}')
        pos = i + len(substr)
    return i


def _get_unique_values(csv_file: Path, column: str, preserve_order=True):

    def do_add(s: set, v):
        n_before = len(s)
        s.add(v)
        n_after = len(s)
        return n_after > n_before

    vals = set()
    ordered_vals = []
    with open(csv_file) as f:
        is_header_line = True
        col_idx = -1
        is_last_col = False
        for line in f:
            if is_header_line:
                if line.endswith('\n'):
                    line = line[:-1]
                is_header_line = False
                all_cols = line.split(',')
                col_idx = all_cols.index(column)
                is_last_col = col_idx == len(all_cols) - 1
                continue
            val_start = 0 if col_idx == 0 else (
                _get_nth_occurrence(line, ',', col_idx) + 1)
            if val_start > 0 and line[val_start - 1] != ',':
                raise ValueError(f'wtf! {line[val_start]}')
            val_end = len(line) if is_last_col else _get_nth_occurrence(
                line, ',', col_idx + 1)
            val = line[val_start:val_end]
            if preserve_order:
                if do_add(vals, val):
                    ordered_vals.append(val)
            else:
                vals.add(val)
    return ordered_vals if preserve_order else vals


def _run():
    parser = _get_arg_parser()
    cli_args = parser.parse_args()
    vals = _get_unique_values(Path(cli_args.file), cli_args.column)
    for v in vals:
        print(v)


if __name__ == '__main__':
    try:
        _run()
    except Exception as e:
        print(f'An exception occurred: {e}\n{traceback.format_exc()}')
        exit(1)
