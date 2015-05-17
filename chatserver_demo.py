#!/usr/bin/env python
#------------------------------------------------------------------------------
#   chatserver_demo.py
#   adapted from
#   chat_demo.py
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
Chat Room Demo for Miniboa.
"""

import miniboa


class ChatServer(miniboa.TelnetServer):

    def __init__(self, *args, **kwargs):
        super(ChatServer, self).__init__(*args, on_connect=self.on_connect, on_disconnect=self.on_disconnect, **kwargs)

        self.running = True
        self.idle_timeout = 300


#    @property
#    def client_count(self):
#        return super(ChatServer, self).client_count()


    @property
    def client_list(self):
        return super(ChatServer, self).client_list()


    def on_connect(self, client):
        """
        Sample on_connect function.
        Handles new connections.
        """
        c = client.addrport()
        print "++ Opened connection to %s" % c
        self.broadcast('%s joins the conversation.\n' % c)
        client.send("Welcome to the Chat Server, %s.\n" % c)


    def on_disconnect(self, client):
        """
        Sample on_disconnect function.
        Handles lost connections.
        """
        c = client.addrport()
        print "-- Lost connection to %s" % c
        self.broadcast('%s leaves the conversation.\n' % c)


    def kick_idle(self):
        """
        Looks for idle clients and disconnects them by setting active to False.
        """
        ## Who hasn't been typing?
        for client in self.client_list:
            if client.idle() > self.idle_timeout:
                print('-- Kicking idle lobby client from %s' % client.addrport())
                client.active = False


    def process_clients(self):
        """
        Check each client, if client.cmd_ready == True then there is a line of
        input available via client.get_command().
        """
        for client in self.client_list:
            if client.active and client.cmd_ready:
                ## If the client sends input echo it to the chat room
                self.chat(client)


    def broadcast(self, msg):
        """
        Send msg to every client.
        """
        for client in self.client_list:
            client.send(msg)

    

    def chat(self, client):
        """
        Echo whatever client types to everyone.
        """
        msg = client.get_command()
        print '%s says, "%s"' % (client.addrport(), msg)

        for guest in self.client_list:
            if guest != client:
                guest.send('%s says, %s\n' % (client.addrport(), msg))
            else:
                guest.send('You say, %s\n' % msg)

        cmd = msg.lower()
        ## bye = disconnect
        if cmd == 'bye':
            client.active = False
        ## shutdown == stop the server
        elif cmd == 'shutdown':
            self.running = False


#------------------------------------------------------------------------------
#       Main
#------------------------------------------------------------------------------

if __name__ == '__main__':
    ## Simple chat server to demonstrate connection handling via the
    ## async and telnet modules.

    ## Create a telnet server with a port, address,
    ## a function to call with new connections
    ## and one to call with lost connections.

    server = ChatServer(timeout = .05)
    print(">> Listening for connections on port %d.  CTRL-C to break." % server.port)

    ## Server Loop
    while server.running:
        server.poll()               ## Send, Recv, and look for new connections
        server.kick_idle()          ## Check for idle clients
        server.process_clients()    ## Check for client input

    print(">> Server shutdown.")

