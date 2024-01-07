from pathlib import Path
import traceback
from typing import Optional


def _get_nth_occurrence(s: str, substr: str, n: int, from_i=0):
    if n < 1:
        raise ValueError(
            "n must be positive (we're finding the nth occurrence of a substr)"
        )
    i = from_i
    pos = 0
    for _ in range(0, n):
        i = s.index(substr, pos)
        pos = i + len(substr)
    return i


def remove_column(
    csv_file: Optional[str] = None,
    csv_lines: Optional[list] = None,
    col_name: Optional[str] = None,
    col_index: Optional[int] = None,
):
    if col_index is None == col_name is None:
        raise ValueError("Must specify 'col_name' XOR 'col_idx'")
    if csv_file is None == csv_lines is None:
        raise ValueError("Must specify 'csv_file' XOR 'lines'")
    rv = []
    col_idx = col_index
    is_last_col = False

    def on_row(row, col_idx):
        if col_idx is None:
            col_char_idx = row.find(col_name)
            col_idx = row.count(',', 0, col_char_idx)
            is_last_col = row.find(',', col_char_idx) == -1
        new_row = None
        if row.startswith('asset') or len(row) < 2:
            return
        if col_idx == 0:
            new_row = row[row.find(',') + 1:]
        elif is_last_col:
            new_row = row[0:row.rfind(',')] + '\n'
        else:
            val_start = _get_nth_occurrence(row, ',', col_idx) + 1
            val_end = _get_nth_occurrence(
                row, ',', col_idx + 1, from_i=val_start) + 1
            new_row = row[0:val_start] + row[val_end:]
        rv.append(new_row)

    if csv_lines is None:
        with open(csv_file) as f:
            for row in f:
                on_row(row, col_idx)
    else:
        for row in csv_lines:
            on_row(row, col_idx)
    return rv


def get_unique_values(csv_file: Path, column: str, preserve_order=True):

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


if __name__ == '__main__':
    csv_file = '/home/john/Documents/repos/blue-trading-solutions/cme-websocket-connector/src/py/order_record.2023-03-01_XCEC_Energy.csv'
    cols_line = 'symbol,asset,securitytype,underlyingproduct,securityid,currencycode,level1bidprice,level1askprice,tradeprice,tradequantity,volume,tradeflag,atask,hightradeprice,lowtradeprice,tradedate,transacttime,nanotime,hour'
    # all_cols = cols_line.split(',')
    new_lines = remove_column(csv_file=csv_file, col_name='symbol')
    new_lines = remove_column(csv_lines=new_lines, col_name='asset')
    new_lines = remove_column(csv_lines=new_lines, col_name='securitytype')
    new_lines = remove_column(csv_lines=new_lines, col_name='underlyingproduct')
    new_lines = remove_column(csv_lines=new_lines, col_name='currencycode')
    new_lines = remove_column(csv_lines=new_lines, col_name='volume')
    for l in new_lines:
        print(l, end='')
