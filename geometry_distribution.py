#! /usr/bin/env python3

import numpy as np
import sys
import pprint
pp = pprint.PrettyPrinter(indent=2)
import argparse


def main():
	parser = argparse.ArgumentParser(description = "headerが'frame, distance'となっているCSVファイルから、フタ閉めに失敗する確率を見積もる")
	parser.add_argument("input", metavar = "csv", type = str, help = "input csv file")
	#parser.add_argument("-o",    metavar = "output_filename_prefix", type = str, default = "result", help = "output file name prefix (default = result)")
	args = parser.parse_args()
	distances = []
	with open(args.input, "r") as f:
		for line in f:
			line = line.strip()
			if len(line) == 0 or line[0] == "#" or line[0] == "f":
				continue
			line = line.split(",")
			if len(line)!= 2:
				print("invalid line:", line)
				sys.exit(1)
			frame, distance = line
			frame = int(frame)
			distance = int(distance)
			distances.append(distance)
	distances = np.array(distances)
	threshold = (np.max(distances) + np.min(distances))/2
	if np.max(distances) - np.min(distances) < 5:
		threshold = np.min(distances) - 1


	geo_dist = []
	temp_cnt = 1
	for i in range(len(distances)):
		if i >= 100:
			break
		if distances[i] > threshold:
			temp_cnt = temp_cnt + 1
		else:
			geo_dist.append(temp_cnt)
			temp_cnt = 1

	if geo_dist == []:
		number_of_attempts_before_failure = len(distances)
	else:
		number_of_attempts_before_failure = round(np.mean(np.array(geo_dist)), 3)
	#print(f"{args.input}\t{np.max(distances)}\t{np.min(distances)}\t{threshold}\t{len(distances)}\t{len(geo_dist)}\t{number_of_attempts_before_failure}\t{round(1/number_of_attempts_before_failure, 3)}")
	print("file name\ttotal number of attempts\taverage of number of attempts before failure\t逆数")
	print(f"{args.input}\t{len(distances)}\t{len(geo_dist)}\t{number_of_attempts_before_failure}\t{round(1/number_of_attempts_before_failure, 3)}")
	"""
	print("success/failure(_/x):", end = "")
	for i in range(len(distances)):
		if i >= 100:
			break
		if distances[i] > threshold:
			print("_", end = "")
		else:
			print("x", end = "")
	print()

	"""


if __name__ == "__main__":
	main()