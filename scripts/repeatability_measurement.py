#! /usr/bin/env python3
import numpy as np
import argparse
import pprint
import sys

# import plotly.graph_objects as go
# from plotly.subplots import make_subplots

pp = pprint.PrettyPrinter(indent=2)
# import pandas as pd


def file_parser(filename, column=0):
    raw_data = []
    with open(filename, "r") as f:
        for line in f:
            try:
                val = float(line.strip().split(",")[column])
                raw_data.append(val)
            except Exception as e:
                print(e, file=sys.stderr)
    average = sum(raw_data) / len(raw_data)
    summit_list = []
    cut_data = [0 if x < average else x for x in raw_data]
    temp_list = [0]
    index = 0
    while True:
        if index >= len(cut_data):
            break
        if cut_data[index] == 0:
            max_val = max(temp_list)
            temp_list = [0]
            if max_val != 0:
                summit_list.append(max_val)
        else:
            temp_list.append(cut_data[index])
        index = index + 1
    return summit_list


def SimpleMovingAverage(point_list, window_size=100):
    statistics_list = []
    index = 0
    while True:
        if index + window_size > len(point_list):
            break
        current_point = np.array(point_list[index : index + window_size])
        mean = round(np.mean(current_point), 6)
        variance = round(np.var(current_point), 6)
        standard_deviation = round(np.std(current_point), 6)
        statistics_list.append([mean, variance, standard_deviation])
        index = index + 1
    return statistics_list


def main():
    parser = argparse.ArgumentParser(description="merge two csv files.")
    parser.add_argument(
        "csv_highspeed",
        metavar="csv_highspeed",
        type=str,
        help="csv_highspeed file name",
    )
    parser.add_argument(
        "csv_rowspeed", metavar="csv_rowspeed", type=str, help="csv_rowspeed  file name"
    )
    args = parser.parse_args()

    X_values_128_highspeed = file_parser(args.csv_highspeed, column=0)
    Y_values_128_highspeed = file_parser(args.csv_highspeed, column=1)
    X_length = len(X_values_128_highspeed)
    Y_length = len(Y_values_128_highspeed)
    mijikai_hou_128_highspeed = min(X_length, Y_length)
    X_values_128_highspeed = X_values_128_highspeed[0:mijikai_hou_128_highspeed]
    Y_values_128_highspeed = Y_values_128_highspeed[0:mijikai_hou_128_highspeed]

    X_values_rowspeed = file_parser(args.csv_rowspeed, column=2)
    Y_values_rowspeed = file_parser(args.csv_rowspeed, column=3)
    X_length = len(X_values_rowspeed)
    Y_length = len(Y_values_rowspeed)
    mijikai_hou_rowspeed = min(X_length, Y_length)
    X_values_rowspeed = X_values_rowspeed[0:mijikai_hou_rowspeed]
    Y_values_rowspeed = Y_values_rowspeed[0:mijikai_hou_rowspeed]

    X_values_128_highspeed = np.round(np.array(X_values_128_highspeed), 6)
    X_values_128_highspeed = X_values_128_highspeed - np.mean(X_values_128_highspeed)
    X_values_128_highspeed = np.round(X_values_128_highspeed, 6)

    Y_values_128_highspeed = np.round(np.array(Y_values_128_highspeed), 6)
    Y_values_128_highspeed = Y_values_128_highspeed - np.mean(Y_values_128_highspeed)
    Y_values_128_highspeed = np.round(Y_values_128_highspeed, 6)

    X_values_rowspeed = np.round(np.array(X_values_rowspeed), 6)
    X_values_rowspeed = X_values_rowspeed - np.mean(X_values_rowspeed)
    X_values_rowspeed = np.round(X_values_rowspeed, 6)

    Y_values_rowspeed = np.round(np.array(Y_values_rowspeed), 6)
    Y_values_rowspeed = Y_values_rowspeed - np.mean(Y_values_rowspeed)
    Y_values_rowspeed = np.round(Y_values_rowspeed, 6)

    print("speed_axis\tvalue")
    for i in range(len(X_values_128_highspeed)):
        print("High_X\t", X_values_128_highspeed[i])
        print("High_Y\t", Y_values_128_highspeed[i])
    for i in range(len(X_values_rowspeed)):
        print("Row_X\t", X_values_rowspeed[i])
        print("Row_Y\t", Y_values_rowspeed[i])


if __name__ == "__main__":
    main()
