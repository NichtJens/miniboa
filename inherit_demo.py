#!/usr/bin/env python
#------------------------------------------------------------------------------
#   inherit_demo.py
#   adapted from
#   handler_demo.py
#   Copyright 2009 Jim Storch
#   Licensed under the Apache License, Version 2.0 (the "License"); you may
#   not use this file except in compliance with the License. You may obtain a
#   copy of the License at http://www.apache.org/licenses/LICENSE-2.0
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#   WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#   License for the specific language governing permissions and limitations
#   under the License.
#------------------------------------------------------------------------------

"""
Example of inheriting from miniboa's TelnetServer.
"""

import miniboa


class MyServer(miniboa.TelnetServer):

    def __init__(self, *args, **kwargs):
        super(MyServer, self).__init__(*args, **kwargs)

        self.CLIENTS = []


    def on_connect(self, client):
        """
        Example on_connect handler.
        """
        client.send('You connected from %s\n' % client.addrport())
        if self.CLIENTS:
            client.send('Also connected are:\n')
            for neighbor in self.CLIENTS:
                client.send('%s\n' % neighbor.addrport())
        else:
            client.send('Sadly, you are alone.\n')
        self.CLIENTS.append(client)


    def on_disconnect(self, client):
        """
        Example on_disconnect handler.
        """
        self.CLIENTS.remove(client)



if __name__ == '__main__':
    MyServer().run()

