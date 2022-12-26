from machine import Pin, SPI

from .ili9341 import Display, color565
from .xglcd_font import XglcdFont

from .config import case, wires, screen
from mlbapp.version import version

if screen == 'lilygo_ili9341_2_4':
    from .lily_go_2_4_inch import dc, cs, rst
elif screen == 'ili9341':
    from .esp32_oled_2_8_inch import dc, cs, rst
    

spi = SPI(2, baudrate=51200000, sck=Pin(18), mosi=Pin(23))

if case == "sideways":

    #The sideways case: https://github.com/jouellnyc/MLB-ESP32/blob/main/images/orange.png
    #This is for when the wires are on the right of the sideways case
    if wires == "right":
        width=320; height=240; rotation=270
    elif wires == "left":
    #This is for when the wires are on the left of the sideways case
        width=320; height=240; rotation=90
    
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
    
    #Upright case: https://github.com/jouellnyc/MLB-ESP32/blob/main/images/side_view_black.jpg
    if wires == "top":
        #This is for when the wires are on the top  of the upright case
        width=240; height=320; rotation=0
    elif wires == "bottom":
        #This is for when the wires are on the top  of the upright case
        width=240; height=320; rotation=180

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

display = Display(spi, dc=Pin(dc), cs=Pin(cs), rst=Pin(rst), width=width, height=height, rotation=rotation)
        
white=color565(255,255,255)
drk_grn=color565(50,100,30)
red=color565(255, 0, 0)
black=color565(0, 0, 0)

sm_font  = XglcdFont('../fonts/arial_23_24.c', 23, 24)
score_font  = XglcdFont('../fonts/sb_21_27.c', 21, 27)
date_font   = XglcdFont('../fonts/arial_32_31.c', 32, 31)

def print_setup(boot_stage):
    clear_fill()    
    draw_outline_box()
    display.draw_text(5, 8,  f"{boot_stage}"       , sm_font, white, drk_grn)
    display.draw_text(5, 65, 'MLB Kiosk'           , sm_font, white, drk_grn)
    display.draw_text(5, 105, f"Version {version}" , sm_font, white, drk_grn)

if __name__ == "__main__":
    display.draw_text(0, 66, 'Espresso Dolce', score_font, drk_grn)   
