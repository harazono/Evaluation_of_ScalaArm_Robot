#! /usr/bin/env python3

import cv2
import time
import numpy as np
import sys
import pprint
pp = pprint.PrettyPrinter(indent=2)
import argparse

def detect_color_in_HSV_range(img, hsv_min, hsv_max):
	hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
	mask       = cv2.inRange(hsv, hsv_min, hsv_max)
	masked_img = cv2.bitwise_and(img, img, mask     = mask)
	return mask, masked_img

def concat_tile(im_list_2d):
	return cv2.vconcat([cv2.hconcat(im_list_h) for im_list_h in im_list_2d])


def detect_center_of_mark(img):#<class 'numpy.ndarray'>
	im_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
	threshold = 50
	ret, img_thresh = cv2.threshold(im_gray, threshold, 255, cv2.THRESH_BINARY)
	img_blur = cv2.blur(img_thresh, (3, 4))
	contours, hierarchy = cv2.findContours(img_blur, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
	if len(contours) != 0:
		cnt = max(contours, key=cv2.contourArea)
		M = cv2.moments(cnt)
		#print(M)
		cx = int(M['m10']/M['m00'])
		cy = int(M['m01']/M['m00'])
		return cx, cy
	else:
		return 0, 0


def main():
	parser = argparse.ArgumentParser(description = "Dobotの動作を見て、幾何分布に従う失敗確率を見積もるための統計を出すスクリプト")
	parser.add_argument("input", metavar = "MP4", type = str, help = "input mp4 file")
	parser.add_argument("-o",    metavar = "output_filename_prefix", type = str, default = "result", help = "output file name prefix (default = result)")
	args = parser.parse_args()


	input_filename  = args.input
	output_filename = args.o
	cap_file = cv2.VideoCapture(input_filename)
	frame_rate = cap_file.get(cv2.CAP_PROP_FPS)

	print(f"input file name: {input_filename}\topen: {cap_file.isOpened()}")
	"""
	動画を１フレームごとに処理する。
	
	"""
	print(f"CAP_PROP_FRAME_WIDTH  : {cap_file.get(cv2.CAP_PROP_FRAME_WIDTH)}")
	print(f"CAP_PROP_FRAME_HEIGHT : {cap_file.get(cv2.CAP_PROP_FRAME_HEIGHT)}")
	print(f"CAP_PROP_FPS          : {cap_file.get(cv2.CAP_PROP_FPS)}")
	print(f"CAP_PROP_FRAME_COUNT  : {cap_file.get(cv2.CAP_PROP_FRAME_COUNT)}")
	print(f"CAP_PROP_POS_FRAMES   : {cap_file.get(cv2.CAP_PROP_POS_FRAMES)}")
	print(f"CAP_PROP_POS_MSEC     : {cap_file.get(cv2.CAP_PROP_POS_MSEC)}")


	#bgrLower = np.array([0, 255, 255])    # 抽出する色の下限(BGR)
	#bgrUpper = np.array([255, 255, 255])    # 抽出する色の上限(BGR)
	#bgrLower = np.array([  0,   0,   0])    # 抽出する色の下限(BGR)
	#bgrUpper = np.array([255, 255, 255])    # 抽出する色の上限(BGR)


	#height, width = 1920, 1080
	height = int(cap_file.get(cv2.CAP_PROP_FRAME_HEIGHT))
	width  = int(cap_file.get(cv2.CAP_PROP_FRAME_WIDTH))
	half_height = int(height/2)
	half_width  = int(width/2)
	half_size = (half_width, half_height)
	print(f"half_size: {half_size}")
	fmt = cv2.VideoWriter_fourcc('m', 'p', '4', 'v') # ファイル形式(ここではmp4)
	writer = cv2.VideoWriter(output_filename + "_movie.mp4", fmt, 10, half_size) # ライター作成

	distance_list = ["frame, distance"]
	distance_output_filename = output_filename + "_distance.csv"
	distance_writer = open(distance_output_filename, "w")

	mask_hsv_blue   = {"min": np.array([70, 90,  0]), "max": np.array([150,255,255])}
	#mask_hsv_red    = {"min": np.array([0 , 150,  0]), "max": np.array([ 15,255,255])}
	mask_hsv_green  = {"min": np.array([45, 100,  0]), "max": np.array([ 70,255,255])}
	mask_hsv_yellow = {"min": np.array([25, 100, 100]), "max": np.array([ 30,255,255])}
	mask = np.zeros((height, width), dtype=np.uint8)
	mask[height//2:, width//2:] = 255
	green_circle_is_in_left_side_flag = False
	count_distance_flag = False


	ret, frame = cap_file.read()
	print("Proccecing")
	while ret:
		sec = round(cap_file.get(cv2.CAP_PROP_POS_FRAMES)/frame_rate)
		frame_count = round(cap_file.get(cv2.CAP_PROP_POS_FRAMES))
		print(f"Sec: {sec}/3600       \r", end = "", file = sys.stderr)
		if sec > 60 * 60:
			break


		frame_tiny     = cv2.resize(frame, dsize=half_size)
		extract_blue   = detect_color_in_HSV_range(frame_tiny, mask_hsv_blue["min"]  ,mask_hsv_blue["max"] )[1]
		extract_green  = detect_color_in_HSV_range(frame_tiny, mask_hsv_green["min"] ,mask_hsv_green["max"])[1]
		blue_center    = detect_center_of_mark(extract_blue)
		green_center   = detect_center_of_mark(extract_green)

		result = cv2.addWeighted(extract_blue, 1, extract_green, 1, 0)
		result = cv2.addWeighted(result, 1, frame_tiny, 0.6, 0)
		
		cv2.circle(result, blue_center,   5, (0, 0, 255), 3)
		cv2.circle(result, green_center,  5, (0, 0, 255), 3)

		if green_center[0] < half_width / 3:
			green_circle_is_in_left_side_flag = True
		else:
			green_circle_is_in_left_side_flag = False

		if green_circle_is_in_left_side_flag is False and count_distance_flag is True:
			count_distance_flag = False

		if green_circle_is_in_left_side_flag is True and count_distance_flag is False:			
			distance = blue_center[1]
			cv2.putText(result, str(distance), (100, 200), cv2.FONT_HERSHEY_PLAIN, 4, (255, 255, 255), 5, cv2.LINE_AA)
			cv2.putText(result, str(frame_count), (100, 100), cv2.FONT_HERSHEY_PLAIN, 4, (255, 255, 255), 5, cv2.LINE_AA)
			writer.write(result)
			distance_list.append(f"{frame_count}, {distance}")
			count_distance_flag = True
		else:
			writer.write(result)

		for i in range(int(frame_rate / 10)):
			ret, frame = cap_file.read()



	distance_writer.write("\n".join(distance_list))
	print("\nDone")
	writer.release()



if __name__ == '__main__':
	main()