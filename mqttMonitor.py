#!/usr/bin/python
####################################
# File name: mqttMonitor.py        #
# Author: Marutpong Chailangka     #
# Python Version: 2.7              #
####################################

import socket
from socket import AF_INET, SOCK_STREAM, SOCK_DGRAM
import time
from threading import Thread
import psutil

try:
    import RPi.GPIO as GPIO
    is_gpio_imported = True
except:
    is_gpio_imported = False

class MqttMonitor(Thread):

    def __init__(self, pin=25, interval_secs=5):
        Thread.__init__(self)
        # Pin Definitons:
        self.ledpin_status = pin
        self.interval_secs = interval_secs

        self.is_connected = False
        self.server_host = 'multidemo.nellehliving.com'
        self.server_ip = '159.65.137.98'
        self.is_set_server_ip = False

        self.setup_GPIO()
        self.turn_led_status_off()
        self.start()

    def setup_GPIO(self):
        if is_gpio_imported is False:
            return
        # Pin Setup:
        # GPIO.cleanup()
        GPIO.setmode(GPIO.BCM) # Broadcom pin-numbering scheme
        GPIO.setup(self.ledpin_status, GPIO.OUT) # LED pin set as output

    def turn_led_status_on(self):
        print "MQTT \t Status connected"
        if is_gpio_imported is False:
            return
        GPIO.output(self.ledpin_status, GPIO.LOW)

    def turn_led_status_off(self):
        print "MQTT \t Status not connected"
        if is_gpio_imported is False:
            return
        GPIO.output(self.ledpin_status, GPIO.HIGH)

    def is_mqtt_connected(self):
        for c in psutil.net_connections(kind='inet'):
            if c.raddr:
                raddr = "%s:%s" % (c.raddr)
                (remote_ip, remote_port) = c.raddr
                if self.server_ip in raddr and c.status == 'ESTABLISHED':
                    return True
        return False

    def set_server_ip(self):
        print "MQTT \t Query Server IP Address"
        try:
            ip_addr = socket.gethostbyname(self.server_host)
            print "MQTT \t Server IP Address is %s" % ip_addr
            self.is_set_server_ip = True
            return ip_addr
        except:
            pass

    def run(self):
        while 1:
            time.sleep(self.interval_secs)

            if self.is_set_server_ip is False:
                self.set_server_ip()

            try:
                self.is_connected = self.is_mqtt_connected()
            except:
                print "MQTT \t ----------- Error -------------"
                self.turn_led_status_off()
                continue

            if self.is_connected:
                self.turn_led_status_on()
            else:
                self.turn_led_status_off()

if __name__ == '__main__':
    mqtt_monitor_ins = MqttMonitor()
