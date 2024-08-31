import board
import busio
import sys
import displayio
import time
import random
import text_prompt as prompt
from os import getenv
from adafruit_esp32spi import adafruit_esp32spi_wifimanager
from digitalio import DigitalInOut
import adafruit_connection_manager
import adafruit_requests
from adafruit_esp32spi import adafruit_esp32spi
from adafruit_matrixportal.matrixportal import MatrixPortal
import terminalio
from adafruit_display_text import label

DATA_SOURCE = "https://io.adafruit.com/api/v2/Kyle_A/feeds/test-feed/data"
DATA_LOCATION = [0,"value"]

secrets = {
    "ssid": getenv("CIRCUITPY_WIFI_SSID"),
    "password": getenv("CIRCUITPY_WIFI_PASSWORD"),
    "aio_username": getenv("ADAFRUIT_AIO_USERNAME"),
    "aio_key": getenv("ADAFRUIT_AIO_KEY")
}

matrixportal = MatrixPortal(status_neopixel=board.NEOPIXEL, debug=False, url = DATA_SOURCE,
                headers={"X-AIO-Key": secrets["aio_key"]}, json_path = DATA_LOCATION)
time.sleep(2)

command_map = {
    "quit" : -1,
    "menu" : 0,
    "text_display" : 1,
    "stop_watch" : 2,
    "timer" : 3,
}

def get_menu(command):
    sel = command_map.get(command[1:])
    return sel

class text_display:
    def __init__(self,pos=(int(32/2),0),color = (0,50,0),scale = 1,scrolling = False,text="*****"):
        self.pos = pos
        self.color = color
        self.scale = scale
        self.scrolling = scrolling
        self.text = text
        self.display = matrixportal.display
        self.text_area = None

    def setup_text(self):
        self.text_area = label.Label(
        terminalio.FONT,
        text = self.text,
        color= prompt.hex_colors.get("violet"),  
        scale = int(self.scale),
        #x = self.pos[0]
        #scrolling = self.scrolling,
        #text_wrap = int(64/6)
        y = 6,
        line_spacing = .9
        )
        
        #self.text_area.x = int(64/2)
        #self.text_area.y = int(32/2)
        matrixportal.display.rotation = 180
       
        matrixportal.display.root_group = self.text_area

        #matrixportal.display.refresh()

    def set_color(self, color):
       self.text_area.color = color

    def set_text(self, text:str):
        self.text_area.text = text

class Timer:
    def __init__(self):
        self.start_seconds = 0
        self.running_seconds = 0
        self.running_seconds_old = 0
        self.start_time = None
        self.current_time = 0
        self.running = False
        self.paused = False
    
    def start_timer(self, display, seconds):
        if self.running == False:
            self.start_seconds = int(seconds)
            self.running_seconds_old = self.start_seconds
            self.start_time = time.time()
            display.set_text(seconds)
            self.running = True

    def timer_running(self, display,sub_c):
        if sub_c == "pause":
            self.running = False
        elif sub_c == "start":
            self.start_timer(display,self.running_seconds)

        if self.running and self.running_seconds_old != 0:
            self.current_time = time.time()
            diff = self.current_time - self.start_time
            self.running_seconds = self.start_seconds - diff
            if self.running_seconds != self.running_seconds_old:
                display.set_text(str(self.running_seconds))
                self.running_seconds_old = self.running_seconds
        elif self.running:
            display.set_text("Times up!")
            time.sleep(5)
            self.running = False

def matrix_startup():
    random.seed(time.time()*1000)
    matrix = text_display(text = random.choice(prompt.welcome))
    matrix.setup_text()
    matrixportal.display.refresh()

    time.sleep(3)
    
    return matrix

def get_data():
    if int(time.time() % 10) == 0:
        try:
            response = matrixportal.fetch()
            #print("Received data:", response)
            return response
        except Exception as e:
            error = "Error" + str(e)
            print(error)
    else: return "none"

def stop_watch(matrix, data):
    _timer = 0
    matrixportal.set_text(_timer)
    start_time = time.time()
    _timer_old = 0
    get_timer = 0
    while(data == "start"):
        curr_time = time.time()
        _timer = curr_time - start_time
        
        if (int(_timer) != int(_timer_old)):
            matrixportal.set_text(_timer)
            _timer_old = _timer
            get_timer += 1

        if get_timer == 2:
            data = get_data()
            get_timer = 0


def led_sign(matrix, sub_c):
    command, text = sub_c.split(' ', 1)
    if command == "text":
        if (matrix.text != text):
            matrix.text = text
            matrix.set_text(matrix.text)
    if command == "color":
        if (matrix.color != text):
            matrix.color = text
            matrix.set_color(prompt.hex_colors.get(matrix.color))
 
