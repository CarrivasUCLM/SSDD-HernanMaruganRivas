#!/usr/bin/env python3
#-*- conding: utf-8 -*-

import sys
import Ice
Ice.loadSlice('iceflix.ice')

import IceFlix

class AuthenticatorI(IceFlix.Authenticator):
    def refreshAuthorization(self, user, passwordHash):
        return 0
    
    def isAuthorized(self, authentication):
        return True

class TokenRevocationI(IceFlix.TokenRevocation):
    def revoke(self, authentication):
        return 0

class Server(Ice.Application):
    def run(self, argv):
        broker = self.communicator()
        servant = AuthenticatorI()

        adapter = broker.createObjectAdapter("AuthAdapter")
        proxy = adapter.add(servant, broker.stringToIdentity("auth"))

        print(proxy, flush=True)

        adapter.activate()
        self.shutdownOnInterrupt()
        broker.waitForShutdown()

        return 0


server = Server()
sys.exit(server.main(sys.argv))