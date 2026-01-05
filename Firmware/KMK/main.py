from kb import Keyboard
from kmk.keys import KC
from kmk.modules.macros import Press, Release, Tap, Macros

import board
import busio
import usb_cdc
import neopixel
import adafruit_ssd1306
import time

keyboard = Keyboard()

macros = Macros()
keyboard.modules.append(macros)

i2c = busio.I2C(board.SCL, board.SDA)
oled = adafruit_ssd1306.SSD1306_I2C(128, 32, i2c)

pixel = neopixel.NeoPixel(board.NEOPIXEL, 1, brightness=0.3)

oled_mode = 0

def toggle_oled_mode():
    global oled_mode
    oled_mode = (oled_mode + 1) % 2


keyboard.keymap = [
    [
        KC.MIC_MUTE,
        KC.MUTE,
        KC.MEDIA_PLAY_PAUSE, 
        KC.Macro(            
            Press(KC.LGUI),
            Press(KC.LSHIFT),
            Tap(KC.S),
            Release(KC.LSHIFT),
            Release(KC.LGUI),
        ),
        KC.MACRO(toggle_oled_mode),  
        KC.LOCK,
    ]
]


def set_led(temp):
    if temp < 50:
        pixel[0] = (0, 255, 0)
    elif temp < 70:
        pixel[0] = (255, 165, 0)
    else:
        pixel[0] = (255, 0, 0)


last_update = 0
cpu = ram = temp = 0.0

def poll_pc():
    global cpu, ram, temp, last_update

    if usb_cdc.data.in_waiting:
        try:
            line = usb_cdc.data.readline().decode().strip()
            parts = dict(p.split(":") for p in line.split(";"))
            cpu = float(parts["CPU"])
            ram = float(parts["RAM"])
            temp = float(parts["TEMP"])
            set_led(temp)
        except:
            pass

    if time.monotonic() - last_update > 0.1:
        last_update = time.monotonic()
        oled.fill(0)

        if oled_mode == 0:
            oled.text("SYSTEM", 0, 0)
            oled.text(f"CPU {cpu:.0f}%", 0, 12)
            oled.text(f"RAM {ram:.0f}%", 64, 12)
            oled.text(f"TEMP {temp:.1f}C", 0, 22)
        else:
            t = time.localtime()
            oled.text("CLOCK", 0, 0)
            oled.text(f"{t.tm_hour:02}:{t.tm_min:02}:{t.tm_sec:02}", 0, 14)

        oled.show()

keyboard.before_matrix_scan = poll_pc

if __name__ == "__main__":
    keyboard.go()
