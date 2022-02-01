import network

essid = 'DIR-615-19a3'
password = '40304458'

def do_connect():
    wlan = network.WLAN(network.STA_IF)    # create station interface
    wlan.active(True)                      # activate the interface
    if not wlan.isconnected():
        print('connecting to network...')
        wlan.connect(essid, password)
        while not wlan.isconnected():
            print('not connected')
            pass
    print('connected')    
    print('network config:', wlan.ifconfig())

