#!/usr/bin/env python3
#-*- conding: utf-8 -*-

import uuid
import os.path
import sys
import Ice
import IceStorm
import iceevents
Ice.loadSlice('iceflix.ice')
import IceFlix

class StreamControllerI(IceFlix.StreamController):

    def getSDP(self, authenticacion, port, current=None):
        return 0
    
    def getSyncTopic(self, current=None):
        return 0
    
    def refreshAuthentication (self, authenticacion, current = None):
        return 0

    def stop(self, current=None):
        return 0


class StreamerSyncI(IceFlix.StreamerSync):
    def requestAuthentication(self, current = None):
        return 0
    
class StreamProviderI(IceFlix.StreamProvider):

    def __init__(self):
        self._id_= str(uuid.uuid4())

    def getStream(self, id, authentication):
        return 0
    
    def isAvailable(self, id):
        return 0
    
    def reannounceMedia(self):
        return 0

class StreamAnnouncesI(IceFlix.StreamAnnounces):
    def newMedia(self, id, initialName, providerId, current = None):
        return 0


class ServiceAvailabilityI(IceFlix.ServiceAvailability):
    def __init__(self):
        self.listaCatalog = []
        self.listaAuth=[]
        self.listaMedia=[]

    def addService(self, service, lista, current=None):
        lista.append(service)
        print(lista)
    
    def removeById(self, id, lista, current=None):
        _id=format(id)
        self.lista.remove(_id)

    def catalogService(self, service, id, current=None):
        print("New catalog service: '{}'".format(id))
        self.addService(service, self.listaCatalog)
 
    def authenticationService(self, service, id, current=None):
        print("New authentication service:'{}'".format(id))
        self.addService(service, self.listaAuth)

    def mediaService(self, service, id, current=None):
        print("New media service:'{}'".format(id)+ "'{}'".format(service))
        _id_=format(id)
        self.listaMedia.append([service,_id_])
        "print(self.listaMedia)"

class Server(Ice.Application):

    def run(self, argv):

        '''Publisher'''
        event = iceevents.IceEvents(self.communicator())
        topic_manager = event.get_topic_manager()
        topic = event.get_topic('ServiceAvailability')
        publisher = event.get_publisher('ServiceAvailability')
        publisher_services = IceFlix.ServiceAvailabilityPrx.uncheckedCast(publisher)
        

        '''Subscriber'''
        eventSubscriber = iceevents.IceEvents(self.communicator())
        broker = eventSubscriber.communicator()
        topic_manager = eventSubscriber.get_topic_manager()
        servant = ServiceAvailabilityI()
        adapter=broker.createObjectAdapter("IceFlixAdapter")
        proxy_subscriber = adapter.addWithUUID(servant)
        eventSubscriber.subscribe('ServiceAvailability', proxy_subscriber)


        "Comunicacion directa"
        adapter.activate()
        broker2 = self.communicator()
        stream_provider = StreamProviderI()
        adapter2 = broker2.createObjectAdapter("MediaAdapter")
        proxy=adapter.addWithUUID(stream_provider)
        publisher_services.mediaService(IceFlix.StreamProviderPrx.checkedCast(proxy), stream_provider._id_)
        print("Waiting events... '{}'".format(proxy))
        topic.getPublisher()
        
        broker.waitForShutdown()
        topic.unsubscribe(proxy)

        return 0

server = Server()
sys.exit(server.main(sys.argv))
