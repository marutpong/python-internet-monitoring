import internetMonitor
import mqttMonitor

if __name__ == '__main__':
    internet_checking_ins = internetMonitor.InternetMonitor()
    mqtt_monitor_ins = mqttMonitor.MqttMonitor()
