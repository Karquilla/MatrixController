import time
import neopixel

from utils import *
matrix = None
display = matrix_startup()
animPlayer = anim_player.AnimPlayer(matrixportal)
startup_anim(animPlayer,1)

data = ""
command = 0
sub_command = ""
setup = False
menu_setup = False
timer = Timer()

timeStart = time.time()
firstGet = False
loops = 3
while True:
    timeCurr = time.time()
    timeDiff = timeCurr - timeStart
    if (timeDiff >= 5):
        change = False
        curr_data = get_data()
        if curr_data != data or curr_data != 'none':
            data = curr_data
            #print(data)
            change = True
            if data[0] == '$':
                command,sub_command = data.split(' ',1)
                command = get_menu(command)
        timeStart = time.time()
            
                
    #print(command, " sub ", sub_command)
    
    if command == -1:
        display.set_text("shutting down..")
        time.sleep(2) 
        sys.exit(0)
    elif command == 0:
        if menu_setup == False:
            display.set_text("$quit $timer\n$text_display\n$stop_watch")
            menu_setup = True
    elif command == 1:
        display.setup_text()
        led_sign(display,sub_command)
    elif command == 2:
        stop_watch(display, data)
    elif command == 3:
        timer.start_timer(display=display,seconds=sub_command)
        timer.timer_running(display,sub_command)
    elif command == 4:
        startup_anim(animPlayer,anim = sub_command,loops = loops)

    matrixportal.display.refresh()
    
 
# [x]---fix anim player to take file name and number of loops to be played
# [x]---add commands to start anim player
# [x]---add anim player to main loop
# [x]---anim.run no longer indefinite, can remove ifs from setup
# []---add sub command for loops
# []---
# []---
# []---