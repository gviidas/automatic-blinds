import wifimgr  # importing wifimgr.py library
import utime
import ntptime
from webpage import web_page
import re
from machine import Timer, RTC

from DRV8825 import StepperMotor
from voltmeter import get_bat_vol
from dayinfo import DayInfo

try:
    import usocket as socket
except:
    import socket

#connecting to Wifi
wlan = wifimgr.do_connect()
print("ESP OK")
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(('', 80))
s.listen(5)

# Setting stepper mode, Pins, and delay in us
s1 = StepperMotor(dir_pin=21,
                  step_pin=22,
                  enable_pin=23,
                  stepperMIN=0,
                  stepperMAX=4000,
                  stepperPos=0,
                  delay=500)

def set_current_time(event):
    '''Setting current time, from internet server'''
    ntptime.server = ('lt.pool.ntp.org') #setting server
    ntptime.settime() #setting current time from server
    t = utime.mktime(utime.localtime())+(2*3600) #getting epoch time in seconds from 2000.01.01.0.0 and adding 3600*2 secs fot GTM+2
    timelist = list(utime.localtime(t))  #converting local time to a list to edit elements
    timelist.insert(3,timelist[6]) #at index 3 adding element 6, to change format for RTC
    timelist.pop(7) #removing 7th element to make format for RTC
    CT = RTC()
    CT.datetime(timelist) #setting curent RTC time to CCC list

set_current_time(True)
auto_update_time = Timer(1) 
auto_update_time.init(period=3600*1000, mode=Timer.PERIODIC ,callback=set_current_time) #creating timer to update time everyhour


def check_auto_blinds(event):
    '''Checking if blinds in good position set by auto button'''
    global srs_min #using sunrise variable
    global sns_min #using sunset variable 
    
    Day = DayInfo()
    minute_now = Day.time_now()[1]
    print ('checking auto blinds: sunrise minute:{}, sunset minute: {}, minutes_now:{}'.format(srs_min,sns_min,minute_now))
    if srs_min <= minute_now <= sns_min: #if minutes at the moment is between srs_min and sns_min, blinds should be opened.
        if s1.stepperPos == s1.stepperMAX:
            print("opened already")
            pass
        else:
            s1.blinds_open()
    else:
        if s1.stepperPos == s1.stepperMIN:
            print("closed already")
            pass
        else:
            s1.blinds_close()
    return print('ok')

while True:
    try:
        conn, addr = s.accept()
        conn.settimeout(3.0)
        print('Got a connection from %s' % str(addr))
        request = conn.recv(1024)
        conn.settimeout(None)

        Day = DayInfo() #getting day info from DayInfo class
        srs = Day.sunrise()[0] #updating sunrise info
        sns = Day.sunset()[0] #updating sunset info
        current_date = Day.date_now() #updating current date
        current_time = Day.time_now()[0] #updating current time
        minute_now = Day.time_now()[1] #updating current minute of the day

        # look if there are our gets in request url
        request = str(request)
        print('Content = %s' % request)
        look_blinds_open = request.find("/?blindsOpen")
        look_blinds_close = request.find("/?blindsClose")
        look_blinds_value = request.find("/?blindsValue")
        look_blinds_AutoAPI = request.find("/?blindsAutoAPI")
        look_blinds_AutoOFF = request.find("/?blindsAutoOFF")
        look_blinds_AutoINPUT = request.find("/?blindsAutoINPUT")

        if int(look_blinds_open) == 6:  # look if it find ?/blindsOpen in 6 character
            s1.blinds_open()
        elif int(look_blinds_close) == 6: # look if it find ?/blindsClose in 6 character
            s1.blinds_close()
        elif int(look_blinds_value) == 6: # look if it find /?blindsValue in 6 character
            reqValue = request[19:25]  # filter elements from reqValue
            reqValue = int(re.sub('[^0-9]', '', reqValue))  # filter numbers from reqValue
            s1.blinds_control(reqValue)
        elif int(look_blinds_AutoAPI) == 6: # look if it find /?blindsAutoAPI in 6 character
            srs_min = Day.sunrise()[1]
            sns_min = Day.sunset()[1]

            auto_timer = Timer(0) #make interuptions timer to check autoblinds function
            auto_timer.init(period=30*1000, 
                            mode=Timer.PERIODIC,
                            callback=check_auto_blinds)
        elif int(look_blinds_AutoOFF) == 6: # look if it find /?blindsAutoOFF in 6 character
            try:
                auto_timer.deinit()
            except:
                pass

        elif int(look_blinds_AutoINPUT) == 6: # look if it find /?blindsAutoINPUT in 6 character
            srs_set = request[23:28]  # filter elements from srs_set in request string
            srs_set = srs_set.split(":", 2)  # split into numbers
            srs_min = int(srs_set[0]) * 60 + int(srs_set[1]) #turn srs_set into minutes of the day

            sns_set = request[29:34]  # filter elements from sns_set in request string
            sns_set = sns_set.split(":", 2)  # split into numbers
            sns_min = int(sns_set[0]) * 60 + int(sns_set[1]) #turn sns_set into minutes of the day

            auto_timer = Timer(0) #make interuptions timer to check autoblinds function
            auto_timer.init(period=30*1000,
                            mode=Timer.PERIODIC,
                            callback=check_auto_blinds)

        else:
            pass

        batteryVol = get_bat_vol()  # function from voltmeter.py
        stepperPos = s1.stepperPos  # gets current stepper position from DRV8825.py class StepperMotor
        response = web_page(stepperPos, batteryVol, current_date, current_time, srs, sns)
        conn.send('HTTP/1.1 200 OK\n')
        conn.send('Content-Type: text/html\n')
        conn.send('Connection: close\n\n')
        conn.sendall(response)
        conn.close()
    except OSError as e:
        conn.close()
        print('Connection closed')
