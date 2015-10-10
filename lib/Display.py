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

from configobj import ConfigObj

class Display:
    def __init__(self, item):
        self.item = item
        self.itemUD = 0
        self.msg = ""
        self.subItem = False
        
        self.modules = []
        self.menu = []
        self.config = ConfigObj("init.conf")

    # UPDATE MODULES
    def update_modules(self, modules):
        self.modules = modules

    # CREATE MENU
    def load_home(self):
        load_array = ["empty",""]
        return load_array
    
    def load_status(self, modules):
        load_array = []
        counter = 0
        load_array.append(["empty",""])
        for item in modules:
            counter = counter + 1
            load_array.append([item.upper(), "screenYN("+str(counter)+")", item.lower(), "setModuleAction"])
        return load_array
    
    def load_modules(self, modules):
        load_array = []
        counter = 0
        load_array.append(["empty",""])
        for item in modules:
            counter = counter + 1
            load_array.append([item.upper(), "screenYN("+str(counter)+")", item.lower(), "setModuleAction"])
        return load_array
    
    def load_config(self):
        load_array = [
                        ["empty",""],
                        ["Internet","getInterface()","i_internet","WSsetInterface"],
                        ["Wireless","getInterface()","i_wireless","WSsetInterface"],
                        ["Monitor","getInterface()","i_monitor","WSsetInterface"]
                    ]
        return load_array
    
    def load_services(self):
        load_array = [
                        ["empty",""],
                        ["Nginx","serviceAction(1)","nginx","serviceAction"],
                        ["SSH","serviceAction(2)","ssh","serviceAction"]
                    ]
        return load_array
    
    def load_commands(self):
        load_array = []
        counter = 0
        load_array.append(["empty",""])
        for item, v in self.config['commands'].iteritems():
            theCommand = v.split("||")
            counter = counter + 1
            load_array.append([theCommand[0].upper(), "screenCommands("+str(counter)+")", theCommand[1], "-"])
        return load_array
    
    def load_exit(self):
        load_array = [["empty","exit()"]]
        return load_array
    
    def load_about(self):
        load_array = [["empty","screenAbout()"]]
        return load_array
    
    def create_menu(self):
        self.menu = []
        self.menu.append(["FruityWiFi",self.load_home()])
        if self.config["SCREEN_MODULES"] == "True" or self.config["SCREEN_MODULES"] == "true":
            self.menu.append(["Modules", self.load_modules(self.modules)])
        if self.config["SCREEN_COMMANDS"] == "True" or self.config["SCREEN_COMMANDS"] == "true":
            self.menu.append(["Commands", self.load_commands()])
        #self.menu.append(["Status", self.load_status(self.modules)]) # [TO BE IMPLEMENTED]
        #self.menu.append(["Config", self.load_config()]) # [TO BE IMPLEMENTED]
        #self.menu.append(["Services", self.load_services()]) # [TO BE IMPLEMENTED]
        self.menu.append(["About", self.load_about()])
        self.menu.append(["Exit", self.load_exit()])

    def addScreen(self, newScreen):
        self.menu.append(newScreen)

    # SET KEYPAD
    def right(self):
        #lcd.noBlink()
        if (self.subItem == True):
            self.subItem = False
        else:
            self.itemUD = 0
            if self.item >= (len(self.menu) - 1) : #EX 5
                self.item = 1
            else:
                self.item += 1

    def left(self):
        #lcd.noBlink()
        if (self.subItem == True):
            self.subItem = False
        else:
            self.itemUD = 0
            if self.item <= 1:
                self.item = (len(self.menu) - 1) #EX 5
            else:
                self.item -= 1

    def down(self):
        if self.itemUD >= (len(self.menu[self.item][1]) - 1): #EX 2:
            self.itemUD = 0
        else:
            self.itemUD += 1

    def up(self):
        if self.itemUD <= 0:
            self.itemUD = (len(self.menu[self.item][1]) - 1) #EX 5
        else:
            self.itemUD -= 1

    def select(self):
        test();

    def show(self):
        if self.itemUD == 0:
            self.msg = str(self.menu[self.item][self.itemUD])
            return self.msg
        else:
            s1 = str(self.menu[self.item][0])
            s2 = str(self.itemUD) + ". " + str(self.menu[self.item][1][self.itemUD][0])
            s2len = len(self.menu[self.item][1])
            self.msg = s1+"\n"+s2
            return self.msg
            
