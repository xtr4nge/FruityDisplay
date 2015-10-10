#!/usr/bin/python
'''
    Copyright (C) 2013-2015 xtr4nge [_AT_] gmail.com

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.
'''

import os
import sys
import subprocess
from time import sleep
#from lib.Adafruit_CharLCDPlate import Adafruit_CharLCDPlate
from lib.Getch import *

from lib.Display import Display
from lib.Webclient import Webclient
from lib.lcd_debug import lcd_debug
from lib.Screen import *

import json

from configobj import ConfigObj

config = ConfigObj("init.conf")

if config["DEBUG"] == "True" or config["DEBUG"] == "true":
    DEBUG = True
else:
    DEBUG = False

__FIRMWARE__ = "1.0"
__FRUITYWIFI__ = "2.2"

# LOAD CONFIG FILE
prefix = config["PREFIX"]
server = config["api"]["server"]
token = config["api"]["token"]
white_list_status = config["white_list"]["status"]
white_list = config["white_list"]["modules"]
black_list_status = config["black_list"]["status"]
black_list = config["black_list"]["modules"]

white_list = white_list.split("|")
black_list = black_list.split("|")

if white_list_status == "True" or white_list_status == "true":
    white_list_status = True
else:
    white_list_status = False

if black_list_status == "True" or black_list_status == "true":
    black_list_status = True
else:
    black_list_status = False

# Message output
class bcolors:
    PURPLE = '\033[95m'
    CYAN = '\033[96m'
    DARKCYAN = '\033[36m'
    BLUE = '\033[94m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BOLD = '\033[1m'
    UNDERL = '\033[4m'
    ENDC = '\033[0m'
    
def show_error(message):
    print bcolors.RED + bcolors.BOLD + "[-] " + bcolors.ENDC + str(message)

def show_alert(message):
    print bcolors.YELLOW + bcolors.BOLD + "[!] " + bcolors.ENDC + str(message)

def show_msg(message):
    print bcolors.GREEN + bcolors.BOLD + "[+] " + bcolors.ENDC + str(message)

def show_info(message):
    print bcolors.BLUE + bcolors.BOLD + "[*] " + bcolors.ENDC + str(message)

# Show banner
def show_banner():

    banner = """
 ___         _ _      __      ___ ___ _   ___  _         _           
| __| _ _  _(_) |_ _  \ \    / (_) __(_) |   \(_)____ __| |__ _ _  _ 
| _| '_| || | |  _| || \ \/\/ /| | _|| | | |) | (_-< '_ \ / _` | || |
|_||_|  \_,_|_|\__|\_, |\_/\_/ |_|_| |_| |___/|_/__/ .__/_\__,_|\_, |
                   |__/                            |_|          |__/
             """

    print banner
    print "Site: " + bcolors.BOLD + "http://www.fruitywifi.com" + bcolors.ENDC
    print "Twitter: " + bcolors.BOLD + "@fruitywifi @xtr4nge" + bcolors.ENDC
    print

show_banner()

# START FRUITYWIFI SESSION [API]
show_info("Establishing session with FruityWiFi server...")
try:
    w = Webclient(server, token)
    w.login()
    w.loginCheck()
    show_msg("Session established. Have fun ;)")
    print 
except:
    sleep(1)
    show_error("The session cannot be established. Check the connection details.")
    print 
    sys.exit()

show_info("FruityDisplay v" + __FIRMWARE__)
print 

# LOAD MODULES
execute = "/module"
out =  w.submitGet("api=" + str(execute))

modules = []
for line in out.json():
    if white_list_status:
        if line in white_list:
            modules.append(line)
    else:
        modules.append(line)
        
    if black_list_status:
        if line in black_list and line in modules:
            modules.remove(line)
            #modules.pop()

# CALL API
def call_api(execute):
    out =  w.submitGet("api=" + str(execute))
    try:
        return out.json()
    except:
        pass

# LCD_DEBUG [class]

# Initialize the LCD plate.  Should auto-detect correct I2C bus.  If not,
# pass '0' for early 256 MB Model B boards or '1' for all later versions
if DEBUG == True:
    lcd = lcd_debug()
else:
    from lib.Adafruit_CharLCDPlate import Adafruit_CharLCDPlate
    lcd = Adafruit_CharLCDPlate()

# Clear display and show greeting, pause 1 sec
lcd.clear()


# DISPLAY
display = Display(0)
display.update_modules(modules)
display.create_menu()


# TEMPLATE TO ADD EXTRA SCREEN ---
newScreen = [
                ["empty",""],
                ["SUB-1","screenFunction(1)","SUB-1-COMMAND","-"],
                ["SUB-2","screenFunction(2)","SUB-2-COMMAND","-"]
            ]

#display.addScreen(["SCREEN-NAME", newScreen]) # UNCOMMMENT LINE TO ADD EXTRA SECTION
# END TEMPLATE -------------------

#displayON = "ON"

lcd.clear()
lcd.numlines=2
lcd.message(display.show())

# GENERAL MENU
def menu():
    
    lcd.noBlink()

    while True:
        sleep(0.1)
        k = "-"
        if DEBUG == True:
            k = getch()

        if k == 'x':
            sys.exit()
            break
        
        if lcd.buttonPressed(lcd.LEFT) or k == 'a':
            lcd.clear()
            display.left()
            lcd.message(display.show())
            sleep(0.5)

        if lcd.buttonPressed(lcd.RIGHT) or k == 'd':
            lcd.clear()
            display.right()
            lcd.message(display.show())
            sleep(0.5)

        if lcd.buttonPressed(lcd.UP) or k == 'w':
            lcd.clear()
            display.up()
            lcd.message(display.show())
            sleep(0.5)

        if lcd.buttonPressed(lcd.DOWN) or k == 's':
            lcd.clear()
            display.down()
            lcd.message(display.show())
            sleep(0.5)

        if lcd.buttonPressed(lcd.SELECT) or k == 'q':
            A=1
            itemLF = display.item
            itemUD = display.itemUD
            toExec = display.menu[itemLF][1][itemUD][1]
            if toExec != "":
                if DEBUG: print "eval: " + toExec
                eval(toExec)
            else:
                if DEBUG: print "empty..."
                pass
            
            sleep(0.5)

# SCREEN Y/N (MODULES)
def screenYN(i):
    
    display.subItem = True
    itemLF = display.item
    itemUD = display.itemUD
    
    lcd.clear()
    lcd.blink()
    lcd.setCursor(0,0)
    lcd.message(prefix + display.menu[itemLF][1][itemUD][0]) # NAME OF COMMAND TO EXEC [position 0 in array]
    lcd.setCursor(0,1)
    lcd.message("LOADING")
    
    xpos = 0
    set = str(getModuleStatus(display.menu[itemLF][1][itemUD][2]))
    temp = set
    
    if DEBUG: print display.menu[itemLF][1][itemUD][2]
    
    lcd.clear()
    lcd.blink()
    lcd.setCursor(0,0)
    lcd.message(prefix + display.menu[itemLF][1][itemUD][0]) # NAME OF COMMAND TO EXEC [position 0 in array]

    lcd.setCursor(12,1)
    lcd.message("["+set+"]*")
    lcd.setCursor(13,1)

    sleep(0.5)

    while True:
        sleep(0.1)
        k = '-'
        if DEBUG == True:
            k = getch()
        
        if lcd.buttonPressed(lcd.UP) or k == 'w':
            lcd.message("N")

            if set == "N":
                lcd.setCursor(15,1)
                lcd.message("*")
            else:
                lcd.setCursor(15,1)
                lcd.message(" ")

                lcd.setCursor(13,1)
                temp = "N"
                
            sleep(0.5)

        if lcd.buttonPressed(lcd.DOWN) or k == 's':
            lcd.message("Y")

            if set == "Y":
                lcd.setCursor(15,1)
                lcd.message("*")
            else:
                lcd.setCursor(15,1)
                lcd.message(" ")
                lcd.setCursor(13,1)
                temp = "Y"
            
            sleep(0.5)

        if lcd.buttonPressed(lcd.SELECT) or k == 'q':
            set = temp
            lcd.setCursor(15,1)
            lcd.message("*")
            
            lcd.setCursor(0,1)
            lcd.message("                ")
            lcd.setCursor(0,1)
            lcd.message("LOADING")
            
            if temp == "Y":
                v_action = "start"
            else:
                temp = "N"
                v_action = "stop"
                
            toExec = display.menu[itemLF][1][itemUD][3]+"('"+display.menu[itemLF][1][itemUD][2]+"','"+v_action+"')"

            if toExec != "":
                eval(toExec)
                if DEBUG: print "eval: " + toExec
            else:
                if DEBUG: print "empty..."
                pass
            
            # RESTORE SCREEN
            lcd.setCursor(0,1)
            lcd.message("                ")
            
            lcd.setCursor(12,1)
            lcd.message("["+str(temp)+"]*")
            lcd.setCursor(13,1)
            
            sleep(0.5)

        if lcd.buttonPressed(lcd.RIGHT) or k == 'd':
            if DEBUG: print "screenYN: out R"
            menu()
            break

        if lcd.buttonPressed(lcd.LEFT) or k == 'a':
            if DEBUG: print "screenYN: out L"
            menu()
            break

# SCREEN COMMANDS
def screenCommands(i):
    # LOAD SCREEN AFTER MENU SELECTION    
    display.subItem = True
    itemLF = display.item
    itemUD = display.itemUD
    xpos = 0
    
    lcd.clear()
    lcd.blink()
    lcd.setCursor(0,0)
    lcd.message(prefix + display.menu[itemLF][1][itemUD][0]) # NAME OF COMMAND TO EXEC [position 0 in array]
    
    lcd.setCursor(0,1)
    lcd.message("LOADING")
    
    # EXEC COMMAND
    out = str(execCommand(display.menu[itemLF][1][itemUD][2])) # COMMAND TO EXEC [position 2 in array]
    temp = out
    
    sleep(1)
    
    lcd.setCursor(0,1)
    lcd.message("                ")
    lcd.setCursor(0,1)
    lcd.message("DONE")
    
    sleep(1)
    
    # RESTORE MENU SCREEN
    lcd.clear()
    lcd.blink()
    lcd.setCursor(0,0)
    lcd.message("Commands\n" + str(i) + ". " + display.menu[itemLF][1][itemUD][0])

# SCREEN ABOUT
def screenAbout():
    
    lcd.clear()
    lcd.message("FruityWiFi v" + __FRUITYWIFI__ + "\nFirmware v"+ __FIRMWARE__)
    
    while True:
        sleep(0.1)
        k = "-"
        if DEBUG == True:
            k = getch()
        
        if lcd.buttonPressed(lcd.RIGHT) or k == 'd':
            if DEBUG: print "about: out R"
            menu()
            break

        if lcd.buttonPressed(lcd.LEFT) or k == 'a':
            if DEBUG: print "about: out L"
            menu()
            break

# SCREEN EXIT
def exit():
	print "Bye ;)"
	lcd.clear()
	lcd.message("See you soon.\nBye ;)")
	sleep(2)
	lcd.clear()
	lcd.message("FruityWiFi v" + __FRUITYWIFI__ + "\nFirmware v" + __FIRMWARE__)
	sleep(2)
	lcd.backlight(lcd.OFF)
	lcd.noDisplay()
	sys.exit()

# GET MODULE STATUS
def getModuleStatus(v_module):    
    if DEBUG: print "DEBUG (setModuleAction)"
    
    execute = "/module/" + v_module
    if DEBUG: print execute
    if DEBUG: print call_api(execute)
    
    result = call_api(execute)
    
    if result[0] == True:
        return "Y"
    else:
        return "N"

# SET MODULE [START|STOP]
def setModuleAction(v_module, v_action):
    if DEBUG: print "DEBUG (setModuleAction)"
    
    execute = "/module/" + v_module + "/" + v_action
    if DEBUG: print execute
    if DEBUG: print call_api(execute)
    result = call_api(execute)

    try:
        if result[0] == True:
            return "Y"
        else:
            return "N"    
    except:
        return "N"

def WSserviceAction(v_service, v_action):
    if DEBUG: print "DEBUG (WSserviceAction)"
    
    execute = "/module/" + v_service + "/" + v_action
    if DEBUG: print execute
    if DEBUG: print call_api(execute)
    
    result = call_api(execute)
    
    if result == True:
        return "Y"
    else:
        return "N"    

def getInterface():
    # TO BE IMPLEMENTED
    pass

def WSgetAllInterfaces():
    # TO BE IMPLEMENTED
    pass

def WSgetInterface(v_config):
    # TO BE IMPLEMENTED
    pass

def serviceAction(v_value):
    # TO BE IMPLEMENTED
    pass

def commandAction(v_value):
    # TO BE IMPLEMENTED
    pass
    
def execCommand(cmd):
    p = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True)
    (output, err) = p.communicate()

    return output.strip()

lcd.clear()
i = 0
lcd.message("LOADING\n")
while(i < 16):
	lcd.message(".")
	sleep(.1)
	i += 1

sleep(0.5)

lcd.clear()
lcd.message("FruityWiFi\nv" + __FRUITYWIFI__)

def main():
    try:
        menu()
        return 0
    except KeyboardInterrupt:
        print
        exit()
    except Exception, err:
        print 'Caught an exception'
        print "Error: " + str(err)
        exit()
        return 1

if __name__ == '__main__':
    sys.exit(main())
