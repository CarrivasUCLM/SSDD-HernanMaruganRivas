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
        print("New media service:'{}'".format(id))
        self.addService(service, self.listaMedia)