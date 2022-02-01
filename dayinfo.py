import utime
import urequests as requests


class DayInfo:
    '''
    From API getting current day information as sunrise and sunset times. 
    '''
    def __init__(self):

        self.day_info_string = requests.get('https://api.sunrise-sunset.org/json?lat=54.66322912081811&lng=25.2686010635021=today')
        self.day_info_json = self.day_info_string.json()
        self.srs =0
        self.srs_min =0
        self.sns =0
        self.sns_min =0
        self.loctime = utime.localtime()
        self.current_date =0
        self.current_time =0
        self.minutes_now =0

    def sunrise(self):
            
        self.srsGTM0 = self.day_info_json['results']['sunrise']  # sunrise info from json file
        srs_split = self.srsGTM0.split(":", 2)  # split info into numbers 
        self.srs_min = (int(srs_split[0])+2) * 60 + int(srs_split[1])  # count in which minute of the day
        self.srs = ('{}:{}'.format(int(srs_split[0])+2, srs_split[1]))
        return (self.srs, self.srs_min)

    def sunset(self):
        
        self.snsGTM0 = self.day_info_json['results']['sunset']  # sunset info from json file
        sns_split = self.snsGTM0.split(":", 2)  # split info into numbers
        self.sns_min = (int(sns_split[0])+2) * 60 + int(sns_split[1])+12*60  # count in which minute of the day
        self.sns = ('{}:{}'.format(int(sns_split[0])+2, sns_split[1]))
        return (self.sns, self.sns_min)

    def date_now(self):
        
        self.current_date = ('{:02d}-{:02d}-{:02d} '.format(self.loctime[0], self.loctime[1], self.loctime[2]))
        return self.current_date #getting YEAR , MONTH and DAY from current time string
    
    def time_now(self):
        self.current_time = ('{:02d}:{:02d}:{:02d} '.format(self.loctime[3], self.loctime[4], self.loctime[5]))
        minute_split = self.current_time.split(":",2) #split into numbers
        self.minutes_now = int(minute_split[0])*60+int(minute_split[1])
        
        return (self.current_time, self.minutes_now) #returning current time in string and minutes 
    

    def get_var(self):
        '''
        self.sunrise()
        self.sunset()
        self.date_now()
        self.time_now()
        self.minute_now()
        '''
        return (self.srs, self.srs_min, self.sns, self.sns_min, self.current_date, self.current_time, self.minutes_now)