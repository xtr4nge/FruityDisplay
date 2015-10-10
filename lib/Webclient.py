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

import requests
from requests import session

requests.packages.urllib3.disable_warnings() # DISABLE SSL CHECK WARNINGS

class Webclient:

    def __init__(self, server, token):
        
        self.global_webserver = server
        self.path = "/modules/api/includes/ws_action.php"
        self.s = requests.session()
        self.token = token

    def login(self):

        payload = {
            'action': 'login',
            'token': self.token
        }
        
        self.s = requests.session()
        self.s.get(self.global_webserver, verify=False) # DISABLE SSL CHECK
        self.s.post(self.global_webserver + '/login.php', data=payload)

    def loginCheck(self):
                
        response = self.s.get(self.global_webserver + '/login_check.php')
        #print response.headers
        #print ":" + response.text
        
        if response.text != "":
            self.login()
        
        if response.text != "":
            print "Ah, Ah, Ah! You didn't say the magic word!"
            sys.exit()
        
        return True
        
    def submitPost(self, data):
        response = self.s.post(self.global_webserver + data)
        #print response.headers
        #print "debug: " + response.text
        return response.json
    
        if response.text == "":
            return True
        else:
            return False
    
    def submitGet(self, data):
        response = self.s.get(self.global_webserver + self.path + "?" + data)
        #print response.headers
        #print "debug: " + response.text
        #print response.json

        return response