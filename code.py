import time
import neopixel
from utils import *
matrix = None
display = matrix_startup()

data = ""
command = 0
sub_command = ""
setup = False
menu_setup = False
timer = Timer()

while True: 
    change = False
    curr_data = get_data()
    if curr_data != data:
        data = curr_data
        #print(data)
        change = True
        if data[0] == '$':
            command,sub_command = data.split(' ',1)
            command = get_menu(command)
            
                
    #print(command, " sub ", sub_command)
     
    if command == -1:
        display.set_text("shutting down..")
        time.sleep(2)
        sys.exit(0)
    elif command == 0:
        if menu_setup == False:
            display.set_text(
                "$quit $timer\n$text_display\n$stop_watch"
            )
            menu_setup = True
    elif command == 1:
        led_sign(display,sub_command)
    elif command == 2:
        stop_watch(display, data)
    elif command == 3:
        timer.start_timer(display=display,seconds=sub_command)
        timer.timer_running(display,sub_command)

    matrixportal.display.refresh()
    
 
