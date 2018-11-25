import io
import logging
import os
import sys
import time
from datetime import datetime
from subprocess import call
from time import sleep
from fnmatch import fnmatch

sys.path.append(os.path.join(os.path.dirname(os.path.realpath(__file__)), './vendored/'))

# import boto3

import greengrasssdk
s3client = greengrasssdk.client("s3")


logger = logging.getLogger()
logger.setLevel(logging.INFO)

logger.info('Initializing Camera/handler')

OS_PATH_PICS = "/home/ggc_user"
S3_BUCKET_NAME = 'smart-garden-images'
INTERVAL = 600 # seconds -> 10 min

serial = ""
def __init__(self):
    global serial   
    serial = getserial()

def getserial():
    logger.info('getserial called')
    # Extract serial from cpuinfo file
    cpuserial = "0000000000000000"
    try:
        f = open('/proc/cpuinfo','r')
        for line in f:
            if line[0:6]=='Serial':
                cpuserial = line[10:26]
        f.close()
    except:
        cpuserial = "ERROR000000000"
    return cpuserial   

def capture_image():
    """
    Captures image from RPi Camera
    """
    delete_content()
    logger.info('Invoked function capture_image()')
    logger.info(os.path.dirname(os.path.realpath(__file__)))
    call(os.path.dirname(os.path.realpath(__file__)) + "/webcam.sh")
    sleep(1)
    for file in os.listdir(OS_PATH_PICS):
        if fnmatch(file, "*.jpg"):
            logger.log(file)
            s3client.upload_file(os.path.join(OS_PATH_PICS, file), S3_BUCKET_NAME, "{}_{}".format(serial,file))
    sleep(5)
    delete_content()

def delete_content():
    for the_file in os.listdir(OS_PATH_PICS):
        file_path = os.path.join(OS_PATH_PICS, the_file)
        try:
            if os.path.isfile(file_path):
                os.unlink(file_path)
        except Exception as e:
            print(e)
#----

#        cv2.imwrite('/usr/plantwatering/img_001.jpg', frame)

    # capture = cv.CaptureFromCAM(0)
    # cv.SetCaptureProperty(capture, cv.CV_CAP_PROP_FRAME_HEIGHT, my_height)
    # cv.SetCaptureProperty(capture, cv.CV_CAP_PROP_FRAME_WIDTH, my_width)
    # cv.SetCaptureProperty(capture, cv.CV_CAP_PROP_FORMAT, cv.IPL_DEPTH_32F)

    # img = cv.QueryFrame(capture)


    # image_stream = io.BytesIO()
    # camera = PiCamera()

    # camera.start_preview()
    # time.sleep(2) # camera warm-up time
    # camera.capture(image_stream, 'jpeg')

#----

    # file_name = '{}.jpg'.format(datetime.now().isoformat().replace(':', ''))

    # logger.info('Image captured, transferring to s3://{}/{}'.format(
    #     S3_BUCKET_NAME,
    #     file_name,
    # ))

    # s3 = boto3.client('s3')
    
    # s3.upload_fileobj("", S3_BUCKET_NAME, file_name)

    # return


def start():
    while True:
        capture_image()
        time.sleep(INTERVAL)

start()

def pinned_handler():
    """
    Mock function to run pinned lambda
    """
    pass