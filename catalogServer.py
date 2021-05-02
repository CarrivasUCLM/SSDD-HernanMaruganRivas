#!/usr/bin/env python3
#-*- conding: utf-8 -*-

import sys
import Ice
import IceStorm
Ice.loadSlice('iceflix.ice')

import IceFlix

class MediaCatalogI(IceFlix.MediaCatalog):
    def getTile(self, id):
        return 0
    
    def getTilesByName(self, name, exact):
        return True

    def getTilesByTags(self, tags, includeAllTags):
        return 0

    def renameTile(self, id, name, authentication):
        return 0

    def addTags(self, id, tags, authentication):
        return 0
    
    def removeTags(self, id, tags, authentication):
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

        topic_name = "ServiceAvailability"
        try:
            topic = topic_mgr.retrieve(topic_name)
        except IceStorm.NoSuchTopic:
            print("no such topic found, creating")
            topic = topic_mgr.create(topic_name)

        publisher = topic.getPublisher()
        iceflix = IceFlix.MainPrx.uncheckedCast(publisher)


        topic_media = "MediaAnnouncements"
        try:
            topic = topic_mgr.retrieve(topic_media)
        except IceStorm.NoSuchTopic:
            print("no such topic found, creating")
            topic = topic_mgr.create(topic_media)

        publisher = topic.getPublisher()
        iceflix = IceFlix.MainPrx.uncheckedCast(publisher)

        iceflix.getCatalogService()
        return 0


server = Server()
sys.exit(server.main(sys.argv))