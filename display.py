from machine import Pin, SPI
import framebuf
import math
import time

DC = 8
RST = 12
MOSI = 11
SCK = 10
CS = 9

class OLED_1inch3(framebuf.FrameBuffer):
    def __init__(self):
        self.width = 128
        self.height = 64
        
        self.cs = Pin(CS, Pin.OUT)
        self.rst = Pin(RST, Pin.OUT)
        
        self.cs(1)
        self.spi = SPI(1)
        self.spi = SPI(1,2000_000)
        self.spi = SPI(1,20000_000,polarity=0, phase=0,sck=Pin(SCK),mosi=Pin(MOSI),miso=None)
        self.dc = Pin(DC,Pin.OUT)
        self.dc(1)
        self.buffer = bytearray(self.height * self.width // 8)
        super().__init__(self.buffer, self.width, self.height, framebuf.MONO_HMSB)
        self.init_display()
        
        self.white = 0xffff
        self.black = 0x0000
        
    def write_cmd(self, cmd):
        self.cs(1)
        self.dc(0)
        self.cs(0)
        self.spi.write(bytearray([cmd]))
        self.cs(1)
        
    def write_data(self, buf):
        self.cs(1)
        self.dc(1)
        self.cs(0)
        self.spi.write(bytearray([buf]))
        self.cs(1)

    def init_display(self):
        self.rst(1)
        time.sleep(0.001)
        self.rst(0)
        time.sleep(0.01)
        self.rst(1)

        cmds = [
            0xAE, 0x00, 0x10, 0xB0, 0xdc, 0x00, 0x81, 0x6f, 0x21,
            0xa0, 0xc0, 0xa4, 0xa6, 0xa8, 0x3f, 0xd3, 0x60, 0xd5,
            0x41, 0xd9, 0x22, 0xdb, 0x35, 0xad, 0x8a, 0xAF
        ]
        for cmd in cmds:
            self.write_cmd(cmd)

    def show(self):
        self.write_cmd(0xb0)
        for page in range(0,64):
            self.column = 63 - page              
            self.write_cmd(0x00 + (self.column & 0x0f))
            self.write_cmd(0x10 + (self.column >> 4))
            for num in range(0,16):
                self.write_data(self.buffer[page*16+num])

oled = OLED_1inch3()
        
def activate_screensaver():
    oled.fill(0x0000)
    oled.show()

def clear_display():    
    oled.fill(0x0000)
    oled.show()
    
    oled.text("POWER OFF", 27, 29, oled.white)
    oled.show()
    
    time.sleep(2)
    
    oled.fill(0x0000)
    oled.show()
    
def display_message(message, x_value):
    oled.fill(0x0000)
    oled.show()
    
    time.sleep(0.5)
    oled.text(message, x_value, 29, oled.white)
    oled.show()
    
def restart_display():    
    oled.fill(0x0000)
    oled.show()
    
    time.sleep(0.5)
    print("Restarting ...")
    oled.text("Restarting ...", 12, 29, oled.white)
    oled.show()
    
    time.sleep(1)
    
    oled.fill(0x0000)
    oled.show()
    
def show_time(hour, minute, second):
    hour_0 = hour % 10
    hour_1 = math.floor(hour / 10)
    minute_0 = minute % 10
    minute_1 = math.floor(minute / 10)
    second_0 = second % 10
    second_1 = math.floor(second / 10)
    print(f"{hour_1}{hour_0}:{minute_1}{minute_0}:{second_1}{second_0}")

    if hour_1 == 0:
        oled.fill_rect(3, 16, 4, 14, oled.white)
    if hour_1 == 0 or hour_1 == 1:
        oled.fill_rect(15, 34, 4, 14, oled.white)
    if hour_1 == 0 or hour_1 == 2:
        oled.fill_rect(7, 12, 8, 4, oled.white)
        oled.fill_rect(3, 34, 4, 14, oled.white)
        oled.fill_rect(7, 48, 8, 4, oled.white)
    if hour_1 == 0 or hour_1 == 1 or hour_1 == 2:
        oled.fill_rect(15, 16, 4, 14, oled.white)
    if hour_1 == 2:
        oled.fill_rect(7, 30, 8, 4, oled.white)

    if hour_0 in [0, 2, 3, 5, 6, 7, 8, 9]:
        oled.fill_rect(27, 12, 8, 4, oled.white)
    if hour_0 in [0, 4, 5, 6, 8, 9]:
        oled.fill_rect(23, 16, 4, 14, oled.white)
    if hour_0 in [0, 1, 2, 3, 4, 7, 8, 9]:
        oled.fill_rect(35, 16, 4, 14, oled.white)
    if hour_0 in [2, 3, 4, 5, 6, 8, 9]:
        oled.fill_rect(27, 30, 8, 4, oled.white)
    if hour_0 in [0, 2, 6, 8]:
        oled.fill_rect(23, 34, 4, 14, oled.white)
    if hour_0 in [0, 1, 3, 4, 5, 6, 7, 8, 9]:
        oled.fill_rect(35, 34, 4, 14, oled.white)
    if hour_0 in [0, 2, 3, 5, 6, 8, 9]:
        oled.fill_rect(27, 48, 8, 4, oled.white)

    oled.fill_rect(43, 29, 4, 4, oled.white)
    oled.fill_rect(43, 35, 4, 4, oled.white)

    if minute_1 in [0, 2, 3, 5, 6, 7, 8, 9]:
        oled.fill_rect(55, 12, 8, 4, oled.white)
    if minute_1 in [0, 4, 5, 6, 8, 9]:
        oled.fill_rect(51, 16, 4, 14, oled.white)
    if minute_1 in [0, 1, 2, 3, 4, 7, 8, 9]:
        oled.fill_rect(63, 16, 4, 14, oled.white)
    if minute_1 in [2, 3, 4, 5, 6, 8, 9]:
        oled.fill_rect(55, 30, 8, 4, oled.white)
    if minute_1 in [0, 2, 6, 8]:
        oled.fill_rect(51, 34, 4, 14, oled.white)
    if minute_1 in [0, 1, 3, 4, 5, 6, 7, 8, 9]:
        oled.fill_rect(63, 34, 4, 14, oled.white)
    if minute_1 in [0, 2, 3, 5, 6, 8, 9]:
        oled.fill_rect(55, 48, 8, 4, oled.white)

    if minute_0 in [0, 2, 3, 5, 6, 7, 8, 9]:
        oled.fill_rect(75, 12, 8, 4, oled.white)
    if minute_0 in [0, 4, 5, 6, 8, 9]:
        oled.fill_rect(71, 16, 4, 14, oled.white)
    if minute_0 in [0, 1, 2, 3, 4, 7, 8, 9]:
        oled.fill_rect(83, 16, 4, 14, oled.white)
    if minute_0 in [2, 3, 4, 5, 6, 8, 9]:
        oled.fill_rect(75, 30, 8, 4, oled.white)
    if minute_0 in [0, 2, 6, 8]:
        oled.fill_rect(71, 34, 4, 14, oled.white)
    if minute_0 in [0, 1, 3, 4, 5, 6, 7, 8, 9]:
        oled.fill_rect(83, 34, 4, 14, oled.white)
    if minute_0 in [0, 2, 3, 5, 6, 8, 9]:
        oled.fill_rect(75, 48, 8, 4, oled.white)

    if second_1 in [0, 2, 3, 5, 6, 7, 8, 9]:
        oled.fill_rect(97, 24, 6, 4, oled.white)
    if second_1 in [0, 4, 5, 6, 8, 9]:
        oled.fill_rect(93, 28, 4, 8, oled.white)
    if second_1 in [0, 1, 2, 3, 4, 7, 8, 9]:
        oled.fill_rect(103, 28, 4, 8, oled.white)
    if second_1 in [2, 3, 4, 5, 6, 8, 9]:
        oled.fill_rect(97, 36, 6, 4, oled.white)
    if second_1 in [0, 2, 6, 8]:
        oled.fill_rect(93, 40, 4, 8, oled.white)
    if second_1 in [0, 1, 3, 4, 5, 6, 7, 8, 9]:
        oled.fill_rect(103, 40, 4, 8, oled.white)
    if second_1 in [0, 2, 3, 5, 6, 8, 9]:
        oled.fill_rect(97, 48, 6, 4, oled.white)

    if second_0 in [0, 2, 3, 5, 6, 7, 8, 9]:
        oled.fill_rect(115, 24, 6, 4, oled.white)
    if second_0 in [0, 4, 5, 6, 8, 9]:
        oled.fill_rect(111, 28, 4, 8, oled.white)
    if second_0 in [0, 1, 2, 3, 4, 7, 8, 9]:
        oled.fill_rect(121, 28, 4, 8, oled.white)
    if second_0 in [2, 3, 4, 5, 6, 8, 9]:
        oled.fill_rect(115, 36, 6, 4, oled.white)
    if second_0 in [0, 2, 6, 8]:
        oled.fill_rect(111, 40, 4, 8, oled.white)
    if second_0 in [0, 1, 3, 4, 5, 6, 7, 8, 9]:
        oled.fill_rect(121, 40, 4, 8, oled.white)
    if second_0 in [0, 2, 3, 5, 6, 8, 9]:
        oled.fill_rect(115, 48, 6, 4, oled.white)
    
def show_time_and_date(hour, minute, second, year, month, day):
    time_string = f"{hour:02}:{minute:02}:{second:02}"
    print(time_string)
    oled.text("Time:", 10, 10, oled.white)
    oled.text(time_string, 10, 20, oled.white)
    
    date_string = f"{day:02}.{month:02}.{year}"
    print(date_string)
    oled.text("Date:", 10, 35, oled.white)
    oled.text(date_string, 10, 45, oled.white)

def start_display():
    oled.fill(0x0000)
    oled.show()
    
    x_end = 0
    while x_end <= 63:
        oled.line(0, 0, 127, x_end, oled.white)
        oled.show()
        x_end += 8

    x_start = 0
    while x_start <= 63:
        oled.line(0, x_start, 127, 63, oled.white)
        oled.show()
        x_start += 8
    
    oled.line(0, 63, 0, 0, oled.white)
    oled.show()
    
    oled.line(0, 0, 127, 0, oled.white)
    oled.show()
    
    oled.line(127, 0, 127, 63, oled.white)
    oled.show()
    
    oled.line(127, 63, 0, 63, oled.white)
    oled.show()

    y_end = 63
    while y_end >= 0:
        oled.line(0, 63, 127, y_end, oled.white)
        oled.show()
        y_end -= 8

    y_start = 63
    while y_start >= 0:
        oled.line(127, 0, 0, y_start, oled.white)
        oled.show()
        y_start -= 8
        
    y = 0
    while y <= 63:
        oled.fill_rect(0, y, 127, y+4, oled.white)
        oled.show()
        y += 4
        
    oled.text("Hello World!", 16, 29, oled.black)
    oled.show()

def update_display(hour, minute, second, year, month, day, display_mode):
    start_time = time.ticks_ms()

    oled.fill(0x0000)
    
    if display_mode == 0:
        show_time(hour, minute, second)
    else:
        show_time_and_date(hour, minute, second, year, month, day)

    oled.show()

    end_time = time.ticks_ms()
    print(f"Updating Display took: {end_time - start_time} ms")
