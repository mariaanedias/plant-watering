import sys
import os
import logging
sys.path.append(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'vendored/'))

logger = logging.getLogger()
logger.setLevel(logging.INFO)

import RPi.GPIO as GPIO
import greengrasssdk


logger.info('Initializing moistureHandler')   
logger.info('RPI info {}'.format(GPIO.RPI_INFO))

#setup io
channel = 17
GPIO.setmode(GPIO.BCM)
GPIO.setup(channel, GPIO.IN)

#setup greengrasssdk
iotData = greengrasssdk.client('iot-data')

NO_WATER = '{ "water_level": "0" }'
WATER = '{ "water_level": "1" }'

def publishNoWater():
    publishMoistureLevel(NO_WATER)

def publishWater():
    publishMoistureLevel(WATER)

def publishMoistureLevel(water_level):
    iotData.publish(topic='PlantWatering/MoistureLevel', payload=water_level )

def collect_moisture(channel):
    if GPIO.input(channel):
        logger.info('no water detected on channel {}'.format(channel))
        publishNoWater()
    else: 
        logger.info('water detected on channel {}'.format(channel))
        publishWater()

collect_moisture(channel)

GPIO.add_event_detect(channel, GPIO.BOTH)
GPIO.add_event_callback(channel, collect_moisture)

def pinned_handler(event, context):
    """
    Mock function for pinned/long-lived Lambda
    """         
    pass