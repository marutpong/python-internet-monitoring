#!/usr/bin/python
####################################
# File name: internetMonitor.py    #
# Author: Marutpong Chailangka     #
# Python Version: 2.7              #
####################################

from threading import Thread
import time
import urllib2

try:
    import RPi.GPIO as GPIO
    is_gpio_imported = True
except:
    is_gpio_imported = False

class InternetMonitor(Thread):

    def __init__(self, pin1=23, pin2=24, interval_secs=5):
        Thread.__init__(self)
        # Pin Definitons:
        self.ledpin_status_on = pin1
        self.ledpin_status_off = pin2
        self.interval_secs = interval_secs

        self.is_online = False
        self.checkingServer = 'http://google.com'

        self.setup_GPIO()
        self.turn_led_status_off()
        self.start()

    def setup_GPIO(self):
        if is_gpio_imported is False:
            return
        # Pin Setup:
        GPIO.cleanup() # cleanup all GPIO
        GPIO.setmode(GPIO.BCM) # Broadcom pin-numbering scheme
        GPIO.setup(self.ledpin_status_on, GPIO.OUT) # LED pin set as output
        GPIO.setup(self.ledpin_status_off, GPIO.OUT) # LED pin set as output

    def turn_led_status_on(self):
        print "Status \t connected"
        if is_gpio_imported is False:
            return
        GPIO.output(self.ledpin_status_off, GPIO.LOW)
        GPIO.output(self.ledpin_status_on, GPIO.HIGH)
    

    def turn_led_status_off(self):
        print "Status \t not connected"
        if is_gpio_imported is False:
            return
        GPIO.output(self.ledpin_status_off, GPIO.HIGH)
        GPIO.output(self.ledpin_status_on, GPIO.LOW)

    def turn_all_led_off(self):
        if is_gpio_imported is False:
            return
        GPIO.output(self.ledpin_status_off, GPIO.LOW)
        GPIO.output(self.ledpin_status_on, GPIO.LOW)

    def is_internet_on(self):
        for timeout in [1,5,10,15]:
            try:
                response=urllib2.urlopen(self.checkingServer,timeout=timeout)
                return True
            except:
                return False
        return False

    def run(self):
        while 1:
            time.sleep(self.interval_secs)

            try:
                self.is_online = self.is_internet_on()
            except:
                print "----------- Error -------------"
                self.turn_all_led_off()
                GPIO.cleanup() # cleanup all GPIO
                continue

            if self.is_online:
                self.turn_led_status_on()
            else:
                self.turn_led_status_off()

if __name__ == '__main__':
    internet_checking = InternetMonitor()
