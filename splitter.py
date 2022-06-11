import csv
import os
import shutil
import sys


x_key = "/vpulse"
y1_key = "/I9/pl"
y2_key = "/I10/pl"

# state -> vdc -> []value
v_data = dict()
i9_data = dict()
i10_data = dict()
involved = {x_key: v_data, y1_key: i9_data, y2_key: i10_data}


def is_float(s: str) -> bool:
    try:
        float(s)
        return True
    except:
        return False


def gen_path(base: str, state: int, vdc: int, cycle: int) -> str:
    return os.path.join(base, "state_{}".format(state), "vdc_{}".format(vdc), "cycle_{}".format(cycle), "data.csv")


def split_key(key: str) -> (str, int, int):
    parts = key.split()
    if parts[0] not in involved:
        return None
    return parts[0], int(parts[2]), float(parts[4])


def add_to_datas(tp: str, state: int, vdc: int, value: float):
    data = involved[tp]
    if state not in data:
        data[state] = dict()
    state_data = data[state]
    if vdc not in state_data:
        state_data[vdc] = list()
    state_data[vdc].append(value)


def is_float(s: str) -> bool:
    try:
        float(s)
        return True
    except:
        return False


def process_row(row: dict[str]):
    for k, v in row.items():
        v = str(v)
        if not is_float(v):
            # invalid data or blank in the table
            continue
        info = split_key(k)
        if not info:
            continue
        add_to_datas(*info, float(v))


def process_data(path: str):
    with open(path, "r") as csvfile:
        reader = csv.DictReader(csvfile, quoting=csv.QUOTE_MINIMAL)
        for row in reader:
            process_row(row)


def check_length():
    for state, vdc_map in v_data.items():
        for vdc, value_list in vdc_map.items():
            if len(i9_data[state][vdc]) != len(value_list):
                raise RuntimeError("mismatch data length in `state={}, vdc={}' between vpulse and i9 ({}!={})".format(state, vdc, len(value_list), len(i9_data[state][vdc])))
            if len(i10_data[state][vdc]) != len(value_list):
                raise RuntimeError("mismatch data length in `state={}, vdc={}' between vpulse and i10 ({}!={})".format(state, vdc, len(value_list), len(i10_data[state][vdc])))


def split_cycle(state: int, vdc: float) -> list[int]:
    v_list, i9_list, i10_list = v_data[state][vdc], i9_data[state][vdc], i10_data[state][vdc]
    non_zero_flag = False
    cycle_start_idx = [0]
    for idx in range(len(v_list)):
        if v_list[idx] or i9_list[idx] or i10_list[idx]:
            non_zero_flag = True
            continue
        if non_zero_flag:
            cycle_start_idx.append(idx)
            non_zero_flag = False
    return cycle_start_idx


def save(base_dir: str):
    for state, vdc_map in v_data.items():
        for vdc, values in vdc_map.items():
            cycle_range = split_cycle(state, vdc)
            for i in range(len(cycle_range)-1):
                start, end = cycle_range[i], cycle_range[i+1]
                path = gen_path(base_dir, state, vdc, i+1)
                dir = os.path.dirname(path)
                if os.path.exists(dir):
                    shutil.rmtree(dir)
                os.makedirs(os.path.dirname(path))
                with open(path, "w", newline="") as csvfile:
                    fieldnames = [x_key, y1_key, y2_key]
                    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                    writer.writeheader()
                    for j in range(start, end):
                        writer.writerow({x_key: values[j], y1_key: i9_data[state][vdc][j], y2_key: i10_data[state][vdc][j]})


if __name__ == "__main__":
    process_data(sys.argv[1])
    check_length()
    save(sys.argv[2])
