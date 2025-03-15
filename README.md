# Pico W Clock OLED Display

## You need:

* [Raspberry Pi Pico WH](https://www.berrybase.de/en/raspberry-pi-pico-wh-rp2040-wlan-mikrocontroller-board-mit-headern)

* [Pico OLED 1.3 Display](https://www.berrybase.de/en/1.3-64-128-oled-display-modul-fuer-raspberry-pi-pico)

  * used in SPI mode

## Installation Guide:

Flash your Pico with [MicroPython](https://www.raspberrypi.com/documentation/microcontrollers/micropython.html).

Enter your WiFi credentials in the `lib/env.py` file.

As soon as the `Pico` is plugged in, it connects to the specified WiFi Access Point.

Then, it fetches the current time from an open API, disconnects from the WiFi and updates the time every second.

The default time zone is equal to Europe/Berlin, but it can easily be changed in the `initialize_time.py` file by referring to [the official docs](https://timeapi.io/swagger/index.html).

The default time format is `hh:mm:ss`, and the corresponding date format is `DD.MM.YYYY`, which can be modified in the `display.py` file.

Every new day at 00:00:00 (can be edited in the `main.py` file), the time is synchronized again by reconnecting to the Access Point, if it is available.

By pressing `KEY0`, the program is restarted, pressing `KEY1` leads to a termination of the process.

