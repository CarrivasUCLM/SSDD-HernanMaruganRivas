#!/usr/bin/env python3
#-*- conding: utf-8 -*-

import sys
import Ice
Ice.loadSlice('iceflix.ice')

import IceFlix
import IceStorm


class MainI(IceFlix.Main):
    def getAuthenticator(self, current=None):
        print("Este es el authenticator")
        sys.stdout.flush()
        

    def getCatalogService(self, current=None):
        print("Y este es el catálogo")
        sys.stdout.flush()


class ServiceAvailabilityI(IceFlix.ServiceAvailability):

    def catalogService(self, service, id):
        return 0

    def authenticationService(self, service, id):
        return 0

    def mediaService(self, service, id):
        return 0
        

    
class Server(Ice.Application):

    def get_topic_manager(self):
        key = 'IceStorm.TopicManager.Proxy'
        proxy = self.communicator().propertyToProxy(key)
        if proxy is None:
            print("property '{}' not set".format(key))
            return None

        print("Using IceStorm in: '%s'" % key)
        return IceStorm.TopicManagerPrx.checkedCast(proxy)

    def run(self, argv):
        topic_mgr = self.get_topic_manager()
        if not topic_mgr:
            print("Invalid proxy")
            return 2

        ic = self.communicator()
        servant = MainI()
        adapter = ic.createObjectAdapter("MainAdapter")
        subscriber = adapter.addWithUUID(servant)

        topic_name = "IceFlixTopic"
        qos = {}
        try:
            topic = topic_mgr.retrieve(topic_name)
        except IceStorm.NoSuchTopic:
            topic = topic_mgr.create(topic_name)

        topic.subscribeAndGetPublisher(qos, subscriber)
        print("Waiting events... '{}'".format(subscriber))

        adapter.activate()
        self.shutdownOnInterrupt()
        ic.waitForShutdown()

        topic.unsubscribe(subscriber)

        return 0
    


server = Server()
sys.exit(server.main(sys.argv))