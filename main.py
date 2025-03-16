import connect
import initialize_time
import machine
import time

from display import clear_display, restart_display, start_display, toggle_screensaver, update_display

led = machine.Pin('LED', machine.Pin.OUT)

keyA = machine.Pin(15, machine.Pin.IN, machine.Pin.PULL_UP)
keyB = machine.Pin(17, machine.Pin.IN, machine.Pin.PULL_UP)

display_on = True
led_on = False

def fetch_time():
    try:
        start_display()
        connect.connect_to_wifi()
        time_data = initialize_time.get_time_from_api()
        connect.disconnect_wifi()
        return time_data
    
    except KeyboardInterrupt:
        print("Program has been terminated by the user.")
        clear_display()

def main():
    global led_on, display_on
    
    try:
        time_data = fetch_time()
        
        if None in time_data:
            raise ValueError("Time has no correct values.")
        
        current_hour, current_minute, current_second, current_year, current_month, current_day = time_data
        
        last_time = time.ticks_ms()
        
        while True:
            if keyA.value() == 0:
                restart_display()
                machine.reset()
            
            if keyB.value() == 0:
                led.off()
                toggle_screensaver(display_on)
                display_on = not display_on
            
            now = time.ticks_ms()
            elapsed = time.ticks_diff(now, last_time)
            
            if elapsed >= 1000:
                last_time = now
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
                
                if (current_day > 28 and current_month == 2 and not is_leap_year(current_year)) or \
                   (current_day > 29 and current_month == 2 and is_leap_year(current_year)) or \
                   (current_day > 30 and current_month in [4, 6, 9, 11]) or \
                   (current_day > 31 and current_month in [1, 3, 5, 7, 8, 10, 12]):
                    current_day = 1
                    current_month += 1
                
                if current_month >= 13:
                    current_month = 1
                    current_year += 1
                
                time_data = current_hour, current_minute, current_second, current_year, current_month, current_day
                
                update_display(current_hour, current_minute, current_second, current_year, current_month, current_day, display_on)
                
                if display_on:
                    led_on = not led_on
                    led.value(led_on)
            
            if current_hour == 0 and current_minute == 0 and current_second == 0:
                try:
                    fetch_start = time.ticks_ms()
                    time_data = fetch_time()
                    fetch_duration = time.ticks_diff(time.ticks_ms(), fetch_start) / 1000.0
                    
                    if None not in time_data:
                        print("Synchronizing successful.")
                        current_hour, current_minute, current_second, current_year, current_month, current_day = time_data
                    else:
                        print("Synchronizing unsuccessful.")
                        current_second += int(fetch_duration)

                except Exception as e:
                    print(f"Error fetching new time: {e}")              

    except ValueError as ve:
        led.off()
        print(f"Error fetching the current time. Please check your connection or the API: {ve}")
        clear_display()
        
    except KeyboardInterrupt:
        led.off()
        print("Program has been terminated by the user.")
        clear_display()
        
    except Exception as e:
        led.off()
        print(f"An unexpected error has occurred: {e}")
        clear_display()
        
def is_leap_year(year):
    return (year % 4 == 0) and (year % 100 != 0 or year % 400 == 0)
    
if __name__ == "__main__":
    main()
