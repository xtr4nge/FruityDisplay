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

class lcd_debug:
    def __init__(self):
        self.OFF = True
        self.LEFT = False
        self.RIGHT = False
        self.UP = False
        self.DOWN = False
        self.SELECT = False
    
    def clear(self):
        print "debug (clear)"
        #os.system("clear")

    def message(self, var):
        print "debug (message): " + str(var)
        
    def backlight(self, var):
        print "debug (backlight): " + str(var)

    def noDisplay(self):
        print "debug (noDisplay)"
    
    def noBlink(self):
        print "debug (noBlink)"
    
    def buttonPressed(self, var):
        #print "debug (buttonPressed): " + str(var)
        pass
    
    def blink(self):
        #print "debug (blink)"
        pass
    
    def setCursor(self, var1, var2):
        #print "debug (setCursor): " + str(var1) + ", " + str(var2)
        pass
