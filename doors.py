#!/usr/bin/python
from gpiozero import Button
from signal import pause
import boto3
import logging
import socket
from logging.handlers import SysLogHandler

class ContextFilter(logging.Filter):
  hostname = socket.gethostname()

  def filter(self, record):
    record.hostname = ContextFilter.hostname
    return True

logger = logging.getLogger()
logger.setLevel(logging.INFO)

f = ContextFilter()
logger.addFilter(f)

syslog = SysLogHandler(address=('SYSLOGHOST', 514))
formatter = logging.Formatter('%(asctime)s ALARMHOST  homealarm: %(message)s', datefmt='%b %d %H:%M:%S')

syslog.setFormatter(formatter)
logger.addHandler(syslog)


def doorOpen(door, alert=False):
	print door+" opened"
	logger.info(door+" opened")
	if alert:
	        sendMessage("ALERT: "+door+" opened")

   
def doorClose(door, alert=False):
	print door+" closed"
        logger.info(door+" closed")
	if alert:
		sendMessage("ALERT: "+door+" closed")

def sendMessage(message):
	client = boto3.client('sns')
	response = client.publish(
    		TopicArn='ARN',    
    		Message=message
	)
	#print("Response: {}".format(response))	

sliding_door = Button(2)
front_door = Button(3)
basement_door = Button(4)
#when_pressed it is closed, open on release
sliding_door.when_pressed = lambda: doorClose("sliding_door") 
sliding_door.when_released = lambda: doorOpen("sliding_door")
front_door.when_pressed = lambda: doorClose("front_door")
front_door.when_released = lambda: doorOpen("front_door")
basement_door.when_pressed = lambda: doorClose("basement_door")
basement_door.when_released = lambda: doorOpen("basement_door", alert=True)

pause()
