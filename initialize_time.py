import urequests
import time
import machine

led = machine.Pin('LED', machine.Pin.OUT)

current_hour = 0
current_minute = 0
current_second = 0

current_year = 0
current_month = 0
current_day = 0

def get_time_from_api():
    global current_hour, current_minute, current_second, current_year, current_month, current_day
    led.on()
    try:
        print("Fetching current time ...")
        response = urequests.get("https://timeapi.io/api/time/current/zone?timeZone=Europe%2FBerlin")
        print(response.status_code)
        
        if response.status_code == 200:
            led.off()
            data = response.json()
            print(data)
            current_hour= data["hour"]
            current_minute = data["minute"]
            current_second =data["seconds"]
            
            current_year = data["year"]
            current_month = data["month"]
            current_day = data["day"]
    
            print(current_hour, current_minute, current_second, current_year, current_month, current_day)
            return current_hour, current_minute, current_second, current_year, current_month, current_day

    except:
        print("Error while fetching current time.")
        return None, None, None, None, None, None
