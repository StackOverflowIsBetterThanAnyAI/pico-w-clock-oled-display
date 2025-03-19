# Pico W Clock OLED Display

## You need:

* [Raspberry Pi Pico WH](https://www.berrybase.de/en/raspberry-pi-pico-wh-rp2040-wlan-mikrocontroller-board-mit-headern)

* [Pico OLED 1.3 Display](https://www.berrybase.de/en/1.3-64-128-oled-display-modul-fuer-raspberry-pi-pico)

  * used in SPI mode
 
  * 1.3" 64×128 px
 
  * SH1107

## Installation Guide:

Flash your Pico with [MicroPython](https://www.raspberrypi.com/documentation/microcontrollers/micropython.html).

Enter your WiFi credentials in the [`lib/env.py`](https://github.com/StackOverflowIsBetterThanAnyAI/pico-w-clock-oled-display/blob/main/lib/env.py) file.

```
SSID = "SSID"
PASSWORD = "WIFI_PASSWORD"
```

<br/>

As soon as the `Pico` is plugged in, it connects to the specified WiFi Access Point.

Then, it fetches the current time from an open API, disconnects from the WiFi and updates the time every second.

The default time zone is equal to Europe/Berlin, but it can easily be changed in the [`initialize_time.py`](https://github.com/StackOverflowIsBetterThanAnyAI/pico-w-clock-oled-display/blob/main/initialize_time.py) file by referring to [the official docs](https://timeapi.io/swagger/index.html).

```
response = urequests.get("https://timeapi.io/api/time/current/zone?timeZone=Europe%2FBerlin")
```

<br/>

The default time format is `hh:mm:ss`, and the corresponding date format is `DD.MM.YYYY`, which can be modified in the [`display.py`](https://github.com/StackOverflowIsBetterThanAnyAI/pico-w-clock-oled-display/blob/main/display.py) file.

```
time_string = f"{hour:02}:{minute:02}:{second:02}"
date_string = f"{day:02}.{month:02}.{year}"
```

<br/>

Every new day at 00:00:00 (can be edited in the [`main.py`](https://github.com/StackOverflowIsBetterThanAnyAI/pico-w-clock-oled-display/blob/main/main.py) file), the time is synchronized again by reconnecting to the Access Point, if it is available.

```
if current_hour == 0 and current_minute == 0 and current_second == 0:
```

<br/>

By pressing `KEY0`, the program is restarted, pressing `KEY1` leads to clearing the screen. The content reappears after pressing `KEY1` once again.

Holding down `KEY0` for five seconds will shutdown the `Pico` safely.
