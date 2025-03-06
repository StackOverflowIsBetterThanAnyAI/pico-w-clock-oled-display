# pico-w-clock-display

Enter your WiFi credentials in the `lib/env.py` file.

As soon as the `Pico` is plugged in, it connects to the specified WiFi Access Point.

Then, it fetches the current time, disconnects from the WiFi and updates the time every second.

Every 24h the time is synchronized again by reconnecting to the Access Point.
