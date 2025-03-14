# Pico W Clock OLED Display

## You need:

* [Raspberry Pi Pico WH](https://www.berrybase.de/en/raspberry-pi-pico-wh-rp2040-wlan-mikrocontroller-board-mit-headern)

* [Pico OLED 1.3 Display](https://www.berrybase.de/en/1.3-64-128-oled-display-modul-fuer-raspberry-pi-pico)

## Installation Guide:

Flash your Pico with [MicroPython](https://www.raspberrypi.com/documentation/microcontrollers/micropython.html).

Enter your WiFi credentials in the `lib/env.py` file.

As soon as the `Pico` is plugged in, it connects to the specified WiFi Access Point.

Then, it fetches the current time, disconnects from the WiFi and updates the time every second.

Every new day, the time is synchronized again by reconnecting to the Access Point, if it is available.
