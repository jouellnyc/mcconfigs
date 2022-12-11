from machine import Pin, SPI

from .ili9341 import Display, color565
from .xglcd_font import XglcdFont

from .config import case, wires
from mlbapp.version import version

spi = SPI(2, baudrate=51200000, sck=Pin(18), mosi=Pin(23))

if case == "sideways":

    #sideways case:
    #https://github.com/jouellnyc/MLB-ESP32/blob/main/images/orange.png
    
    if wires == "right":
        #This is for when the wires are on the right of the sideways case
        display = Display(spi, dc=Pin(2), cs=Pin(15), rst=Pin(4), width=320, height=240, rotation=270)
    elif wires == "left":
        #This is for when the wires are on the left of the sideways case
        display = Display(spi, dc=Pin(2), cs=Pin(15), rst=Pin(4), width=320, height=240, rotation=90)
    def draw_outline_box():
        display.draw_vline(0,   0, 239, white)
        display.draw_vline(319, 0, 239, white)
        display.draw_hline(0,   0, 319, white)
        display.draw_hline(0,  40, 319, white)
        display.draw_hline(0, 239, 319, white)
    def clear_fill():
        display.clear()
        display.fill_rectangle(0,0, 319,239, drk_grn)
    print("HW:",case, wires)
    
elif case == "upright":

    if wires == "top":
        #This is for when the wires are on the top  of the upright case
        display = Display(spi, dc=Pin(2), cs=Pin(15), rst=Pin(4), width=240, height=320, rotation=0)
    elif wires == "bottom":
        #This is for when the wires are on the top  of the upright case
        display = Display(spi, dc=Pin(2), cs=Pin(15), rst=Pin(4), width=240, height=320, rotation=180)

    #upright case:
    #https://github.com/jouellnyc/MLB-ESP32/blob/main/images/side_view_black.jpg
    def draw_outline_box():
        display.draw_vline(0, 0, 319, white)
        display.draw_vline(239, 0, 319, white)
        display.draw_hline(0, 0, 239, white)
        display.draw_hline(0,  40, 239, white)
        display.draw_hline(0, 319, 239, white)
    def clear_fill():
        display.clear()
        display.fill_rectangle(0,0, 239,319, drk_grn)
    print("HW:",case, wires)

white=color565(255,255,255)
drk_grn=color565(50,100,30)
sm_font  = XglcdFont('../fonts/arial_23_24.c', 23, 24)

def print_setup(boot_stage):
    clear_fill()    
    draw_outline_box()
    display.draw_text(5, 8,  f"{boot_stage}"      , sm_font, white, drk_grn)
    display.draw_text(5, 65, 'MLB Kiosk'          , sm_font, white, drk_grn)
    display.draw_text(5, 105, f"Version {version}" , sm_font, white, drk_grn)

red=color565(255, 0, 0)
black=color565(0, 0, 0)

score_font  = XglcdFont('../fonts/sb_21_27.c', 21, 27)
date_font   = XglcdFont('../fonts/arial_32_31.c', 32, 31)

if __name__ == "__main__":
    display.draw_text(0, 66, 'Espresso Dolce', score_font, drk_grn)   