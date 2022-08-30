#!/usr/bin/env python3

import cv2
import numpy as np
from configobj import ConfigObj
import logging
from time import sleep
from datetime import datetime

conf = ConfigObj("cctvread.ini")
logging.basicConfig(filename=conf['main']['logname'], format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.DEBUG)

logger = logging.getLogger('cctv-1')
logger.setLevel(logging.DEBUG)

logger.info('program starting')

while True:
	cap = cv2.VideoCapture(conf['main']['source'])
	if cap is None or not cap.isOpened():
		logger.error('Unable to open video source: %s' % (conf['main']['source']))
	else:
		v_fps = cap.get(cv2.CAP_PROP_FPS)
		v_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
		v_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
	
		logger.info('Camera source opened : %s with %d x %d @ %d fps' % (conf['main']['source'], v_height, v_width, v_fps))
		while True:
		#for i in range(20):
			ret, img = cap.read()
			if ret:
				fn = '%s/%s%s.jpg' % (conf['main']['output_path'], conf['main']['filename_prefix'], datetime.now().strftime("%Y%m%d%H%M%S%f"))
				cv2.imwrite(fn, img)
				logger.info('Image %s saved' % (fn))
				sleep(1)
				cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
			else:
				logger.error('Unable read video from source: %s' % (conf['main']['source']))
				break
		cap.release()
	sleep(20)

logger.info("program ending")