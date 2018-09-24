#!/usr/bin/python
####################################
# File name: internetMonitor.py    #
# Author: Marutpong Chailangka     #
# Python Version: 2.7              #
####################################

import time
import urllib2
import RPi.GPIO as GPIO


class InternetMonitor(object):

    def __init__(self, pin1=23, pin2=24, interval_secs=2):
        # Pin Definitons:
        self.ledpin_status_on = pin1
        self.ledpin_status_off = pin2
        self.interval_secs = interval_secs
        self.is_online = False
        self.checkingServer = 'http://google.com'

        self.setup_GPIO()
        self.trig_led_status_off()
        self.interval_check()

    def setup_GPIO(self):
        # Pin Setup:
        GPIO.cleanup() # cleanup all GPIO
        GPIO.setmode(GPIO.BCM) # Broadcom pin-numbering scheme
        GPIO.setup(self.ledpin_status_on, GPIO.OUT) # LED pin set as output
        GPIO.setup(self.ledpin_status_off, GPIO.OUT) # LED pin set as output

    def trig_led_status_on(self):
        GPIO.output(self.ledpin_status_off, GPIO.LOW)
        GPIO.output(self.ledpin_status_on, GPIO.HIGH)
    

    def trig_led_status_off(self):
        GPIO.output(self.ledpin_status_off, GPIO.HIGH)
        GPIO.output(self.ledpin_status_on, GPIO.LOW)

    def trig_all_led_off(self):
        GPIO.output(self.ledpin_status_off, GPIO.LOW)
        GPIO.output(self.ledpin_status_on, GPIO.LOW)

    def internet_is_on(self):
        for timeout in [1,5,10,15]:
            try:
                response=urllib2.urlopen(self.checkingServer,timeout=timeout)
                return True
            except:
                return False
        return False

    def interval_check(self):
        try:
            while 1:
                time.sleep(self.interval_secs)
                self.is_online = self.internet_is_on()
                if self.is_online:
                    self.trig_led_status_on()
                else:
                    self.trig_led_status_off()

        except: # If there is any error:
            self.trig_all_led_off()
            GPIO.cleanup() # cleanup all GPIO
        print 'Terminating'

if __name__ == '__main__':
    internet_checking = InternetMonitor()
