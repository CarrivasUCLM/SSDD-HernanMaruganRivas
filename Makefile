#!/usr/bin/make -f
# -*- mode:makefile -*-

all:
	$(MAKE) run-icestorm
	$(MAKE) run-mainserver &
	$(MAKE) run-authserver &
	$(MAKE) run-catalogserver &
	$(MAKE) run-mediaserver

run-mainserver:
	./iceFlixServer.py --Ice.Config=IceFlixServer.config

run-authserver:
	./auth_server.py --Ice.Config=authServer.config users.json


run-catalogserver:
	./catalogServer.py --Ice.Config=catalogServer.config

run-mediaserver:
	./mediaServer.py --Ice.Config=mediaServer.config media.json

run-icestorm:
	mkdir -p IceStorm/
	gnome-terminal -- bash -c \
	"icebox --Ice.Config=icebox.config; bash"