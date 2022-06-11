import csv
import os
import sys
from typing import Union
import matplotlib.pyplot as plt

x_key = "/vpulse"
y1_key = "/I9/pl"
y2_key = "/I10/pl"


def gen_path(base: str, state: int, vdc: float, cycle: int) -> str:
    return os.path.join(base, "state_{}".format(state), "vdc_{}".format(vdc), "cycle_{}".format(cycle), "data.csv")


def read_data(path: str) -> Union[list, list, list]:
    xl, y1l, y2l = list(), list(), list()
    with open(path) as csvfile:
        reader = csv.DictReader(csvfile, quoting=csv.QUOTE_MINIMAL)
        for row in reader:
            xl.append(float(row[x_key]))
            y1l.append(float(row[y1_key]))
            y2l.append(float(row[y2_key]))
    return xl, y1l, y2l


def plot(base_dir: str, state: int, vdc: float, cycle: int):
    print(base_dir, state, vdc, cycle)
    path = gen_path(base_dir, state, vdc, cycle)
    print(path)
    xl, y1l, y2l = read_data(path)
    fig, ax = plt.subplots(figsize=(8, 8))
    # ax.data(xl, y1l)
    ax.plot(xl, y1l, "ro", label="state={},vdc={},{}".format(state, vdc, y1_key))
    ax.plot(xl, y2l, "b+", label="state={},vdc={},{}".format(state, vdc, y2_key))
    ax.set_xlabel("vpulse (V)")
    ax.set_ylabel("I (A)")
    ax.set_title("cycle={}".format(cycle))
    ax.legend()
    plt.show()


if __name__ == "__main__":
    plot(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4])
