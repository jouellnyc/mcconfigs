""" The whole point of this file is to serve as an  abstraction/proxy such """
""" the all the app runner needs to do is import one variable: 'display'   """

""" All Devices  Need These """
from machine import Pin, SPI
#Color Picker - not specific to devices but handy here
from .ili9341 import color565

from bbapp.version import version
from .config import case, wires, screen

white=color565(255,255,255)
drk_grn=color565(50,100,30)
red=color565(255, 0, 0)
black=color565(0, 0, 0)

""" Break Down of Individual Personalities                """

""" All ili9341's seem to have the same SCK/MOSI settings """
""" But dc, cs, rst seem to vary                          """
    
if screen == 'lilygo_ili9341_2_4':
    
    from .lily_go_2_4_inch import dc, cs, rst
    
elif screen == 'ili9341':
    
    from .esp32_oled_2_8_inch import dc, cs, rst


if 'ili' in screen:

    from .ili9341 import Display
    from .xglcd_font import XglcdFont
    
    spi = SPI(2, baudrate=51200000, sck=Pin(18), mosi=Pin(23))
    """Unleash the bigger fonts for the large screens """
    sm_font     = XglcdFont('../fonts/arial_23_24.c', 23, 24)
    score_font  = XglcdFont('../fonts/sb_21_27.c', 21, 27)
    date_font   = XglcdFont('../fonts/arial_32_31.c', 32, 31)
    
    if case == "sideways":

        v13 = 239 ; v21 = 319 ; h13 = 319 ; h23 = 319 ; h32 = 239 ; h33 = 319
        
        """ Sideways case: https://github.com/jouellnyc/BB-ESP32-KIOSK/blob/main/images/orange.png """
        #This is for when the wires are on the right of the sideways case
        
        if wires == "right":

            width=320; height=240; rotation=270

        elif wires == "left":
            
            #This is for when the wires are on the left of the sideways case
            width=320; height=240; rotation=90

    elif case == "upright":
        
        v13 = 319 ; v21 = 239 ; h13 = 239 ; h23 = 239 ; h32 = 319 ; h33 = 239
        """ Use the small font if upright so it fits """
        date_font=sm_font
    
        """ Upright case: https://github.com/jouellnyc/BB-ESP32-KIOSK/blob/main/images/side_view_black.jpg """
        if wires == "top":
            #This is for when the wires are on the top  of the upright case
            width=240; height=320; rotation=0
        elif wires == "bottom":
            #This is for when the wires are on the top  of the upright case
            width=240; height=320; rotation=180
            
    display = Display(spi, dc=Pin(dc), cs=Pin(cs), rst=Pin(rst), width=width, height=height, rotation=rotation)
    
    def draw_outline_box():
        display.draw_vline(0,   0, v13, white)
        display.draw_vline(v21, 0, 239, white)
        display.draw_hline(h13, 0, 319, white)
        display.draw_hline(0,  40, h23, white)
        display.draw_hline(0, h33, h32, white)
        
    def clear_fill():
        display.clear()
        display.fill_rectangle(0,0, h23, h32, drk_grn)        
            
    """ Each clear_fill() is unique per angle/'wires' """
    def print_setup(boot_stage):
        clear_fill()    
        draw_outline_box()
        display.draw_text(5, 8,  f"{boot_stage}"       , sm_font, white, drk_grn)
        display.draw_text(5, 65, 'BB Kiosk'            , sm_font, white, drk_grn)
        display.draw_text(5, 105, f"Version {version}" , sm_font, white, drk_grn)
        
    display.draw_outline_box = draw_outline_box
    display.clear_fill       = clear_fill
    display.print_setup      = print_setup
    display.white            = white
    display.drk_grn          = drk_grn
    display.red              = red
    display.black            = black
    display.sm_font          = sm_font
    display.score_font       = score_font
    display.date_font        = date_font
    
elif screen == "lilygo_watch":

    from .lilygo_watch_1_54_inch import dc, cs, backlight, font, axp202c, st7789, rotation, TFA, BFA
    
    class Watch:
        
        """ Since the ili9341 screen were supported first, in order to support a """
        """ unified interface and the lilygo watch we need to make the watch     """
        """ function calls behave like the ili9341 driver                        """
        
        def __init__(self):
            self.font    = font
            self.red     = red
            self.black   = black
            self.drk_grn = drk_grn
            self.white   = white  
            """ Only one font used on the tiny watch Screen ... """
            self.sm_font    = font
            self.score_font = font
            self.date_font  = font
            self.tft        = self.tft_config(rotation=rotation)
            self.tft.init()
            
        def tft_config(self, rotation=0, buffer_size=0, options=0):
            axp = axp202c.PMU()
            axp.enablePower(axp202c.AXP202_LDO2)
            return st7789.ST7789(
                SPI(1, baudrate=32000000, sck=Pin(18, Pin.OUT), mosi=Pin(19, Pin.OUT)),
                240, 240, cs=Pin(cs, Pin.OUT),dc=Pin(dc, Pin.OUT),backlight=Pin(backlight, Pin.OUT),
                rotation=rotation, options=options, buffer_size=buffer_size)

        def draw_text(self, startx, starty, text, font, fg_text, bg_text):
            self.tft.text(font, text, startx, starty, st7789.WHITE, drk_grn)

        def draw_outline_box(self):
            self.tft.hline(  0,   0, 239, self.white)
            self.tft.hline(  0, 239, 239, self.white)
            self.tft.hline(  0,  50, 239, self.white)
            self.tft.vline(  0,   0, 239, self.white)
            self.tft.vline(  0, 239, 239, self.white)

        def clear_fill(self):
            self.tft.fill(self.drk_grn)

        def print_setup(self, boot_stage):
            self.clear_fill()
            self.draw_outline_box()
            self.tft.text(self.sm_font, f"{boot_stage}"      , 5,   8, self.white, self.drk_grn)
            self.tft.text(self.sm_font, f"BB Kiosk"          , 5,  65, self.white, self.drk_grn)
            self.tft.text(self.sm_font, f"Version {version}" , 5, 105, self.white, self.drk_grn)
    
    display = Watch()
    
