from machine import Pin, ADC
import time

#Set ADC pin
getVol = ADC(Pin(34))
'''
ADC.ATTN_0DB : the full range voltage: 0- 1.2V
ADC.ATTN_2_5DB : the full range voltage: 0- 1.5V
ADC.ATTN_6DB : the full range voltage: 0- 2.0V
ADC.ATTN_11DB : the full range voltage: 0-3.3V
'''
getVol.atten(ADC.ATTN_11DB)

'''
ADC.WIDTH_9BIT: range 0-511
ADC.WIDTH_10BIT: range 0-1023
ADC.WIDTH_11BIT: range 0-2047
ADC.WIDTH_12BIT: range 0-4095
'''
getVol.width(ADC.WIDTH_12BIT)

lastVol = [] #creating empty list of elements to reduce voltage peaks
for i in range(10):
    lastVol.append(i)
    
def get_bat_vol():
    for currentVol in range(len(lastVol)):
        lastVol[currentVol] = getVol.read()*8.05*0.000110*2  #3.3V = 4095 1 = 3.3/4095 *2because voltage split
        batteryVol = sum(lastVol) / len(lastVol) #getting average of last 5 voltages
        time.sleep_ms(10)
    batteryVol="{:.2f}".format(batteryVol)
    return batteryVol



