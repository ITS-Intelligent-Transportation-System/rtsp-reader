#!/usr/bin/env python3

import cv2
import numpy as np
from configobj import ConfigObj
import logging
from time import sleep, time
from datetime import datetime
import argparse
#import daemon

save_lognum = -1

def do_log(log_num, logger, err_level, messages):
	global save_lognum
	if log_num == save_lognum:
		return
	else:
		save_lognum = log_num
		if err_level == "info":
			logger.info(messages)
		elif err_level == "debug":
			logger.debug(messages)
		elif err_level == "error":
			logger.error(messages)
		else:
			return

def parse_opt():
	parser = argparse.ArgumentParser()
	parser.add_argument('--config', type=str, required=True, help='config file of the CCTV')
	opt = parser.parse_args()
	return(opt)

def main(opt):
	conf = ConfigObj(opt.config)

	logging.basicConfig(filename=conf['main']['logname'], format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.DEBUG)
	logger = logging.getLogger(conf['main']['cctv_name'])
	logger.setLevel(logging.DEBUG)
	do_log(0, logger, "info", '=========== PROGRAM STARTING ==========')

	while True:
		cap = cv2.VideoCapture(conf['main']['source'])
		if cap is None or not cap.isOpened():
			do_log(1, logger, "error", 'Unable to open video source: %s' % (conf['main']['source']))
		else:
			v_fps = cap.get(cv2.CAP_PROP_FPS)
			v_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
			v_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
		
			do_log(2, logger, "info", 'Camera source opened : %s with %d x %d @ %d fps' % (conf['main']['source'], v_height, v_width, v_fps))

			fourcc = cv2.VideoWriter_fourcc(*'XVID')
			fn = '%s/%s-%s.avi' % (conf['main']['output_path'], conf['main']['cctv_name'], datetime.now().strftime("%Y%m%d%H%M%S"))
			out = cv2.VideoWriter(fn, fourcc, v_fps, (v_width,v_height))

			end = start = time()
			do_log(3, logger, "info", 'Starting record video %s' % (fn))
			while (end - start) <= float(conf['main']['video_length']):
				ret, img = cap.read()
				end = time()
				if ret:
					out.write(img)
					sleep(1 / v_fps)
				else:
					do_log(4, logger, "error", 'Unable read video from source: %s' % (conf['main']['source']))
					break
			out.release()
			cap.release()
			do_log(5, logger, "info", 'Ending record video %s' % (fn))

if __name__ == "__main__":
	opt = parse_opt()
	main(opt)
	do_log(255, logger, "info", "========== END-OF-PROGRAM ==========")