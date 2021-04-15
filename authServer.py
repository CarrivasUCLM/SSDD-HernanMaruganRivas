#!/usr/bin/env python3
#-*- conding: utf-8 -*-

import sys
import Ice
import IceStorm
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
    def get_topic_manager(self):
        key = 'IceStorm.TopicManager.Proxy'
        proxy = self.communicator().propertyToProxy(key)
        if proxy is None:
            print("property {} not set".format(key))
            return None

        print("Using IceStorm in: '%s'" % key)
        return IceStorm.TopicManagerPrx.checkedCast(proxy)

    def run(self, argv):
        topic_mgr = self.get_topic_manager()
        if not topic_mgr:
            print('Invalid proxy')
            return 2

        topic_name = "IceFlixTopic"
        try:
            topic = topic_mgr.retrieve(topic_name)
        except IceStorm.NoSuchTopic:
            print("no such topic found, creating")
            topic = topic_mgr.create(topic_name)

        publisher = topic.getPublisher()
        iceflix = IceFlix.MainPrx.uncheckedCast(publisher)

        print("Te mando pallá una cosilla")
        
        iceflix.getAuthenticator()
        return 0

server = Server()
sys.exit(server.main(sys.argv))