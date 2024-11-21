import connect
import initialize_time
import machine
import time

led = machine.Pin('LED', machine.Pin.OUT)

led_on = False

def fetch_time():
    connect.connect_to_wifi()
    time_data = initialize_time.get_time_from_api()
    connect.disconnect_wifi()
    return time_data

def main():
    global led_on
    try:
        time_data = fetch_time()
        
        if None in time_data:
            raise ValueError("Time has no correct values.")
        
        current_hour, current_minute, current_second, current_year, current_month, current_day = time_data
        
        while True:
            led.off() if led_on else led.on()
            time.sleep(1)
            current_second += 1
            
            if current_second >= 60:
                current_second = 0
                current_minute += 1
                
            if current_minute >= 60:
                current_minute = 0
                current_hour += 1
                
            if current_hour >= 24:
                current_hour = 0
                current_day += 1
                
            if (current_day > 28 and current_month == 2 and not is_leap_year(current_year)) or (current_day > 29 and current_month == 2 and  is_leap_year(current_year)) or (current_day > 30 and current_month in [4, 6, 9, 11]) or (current_day > 31 and current_month in [1, 3, 5, 7, 8, 10, 12]):
                current_day = 1
                current_month += 1
                
            if current_month >= 12:
                current_month = 1
                current_year += 1
            
            time_data = current_hour, current_minute, current_second, current_year, current_month, current_day
                          
            print(time_data)
            
            if current_second == 0:
                try:
                    led.off()
                    fetch_start = time.time()
                    time_data = fetch_time()
                    fetch_duration = time.time() - fetch_start
                    
                    print(fetch_duration)
                
                    if None not in time_data:
                        print("Synchronizing successful.")
                        current_hour, current_minute, current_second, current_year, current_month, current_day = time_data
                    else:
                        print("Synchronizing unsuccessful.")
                        current_second += int(fetch_duration)

                except Exception as e:
                    print(f"Error fetching new time: {e}")
            
            led_on = not led_on
        
    except ValueError as ve:
        print(f"Error fetching the current time. Please check your connection or the API.")
        
    except KeyboardInterrupt:
        led.off()
        print("Program has been terminated by the user.")
        
    except Exception as e:
        print(f"An unexpected error has occured: {e}")
        
def is_leap_year(year):
    return (year % 4 == 0) and (year % 100 != 0 or year % 400 == 0)
    
if __name__ == "__main__":
    main()
    
