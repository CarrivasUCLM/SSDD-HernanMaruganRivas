#!/usr/bin/make -f
# -*- mode:makefile -*-

run-mainserver:
	gnome-terminal -- bash -c \
	"./iceFlixServer.py --Ice.Config=IceFlixServer.config; bash"

run-authserver:
	gnome-terminal -- bash -c \
	"./authServer.py --Ice.Config=authServer.config; bash"


run-catalogserver:
	gnome-terminal -- bash -c \
	"./catalogServer.py --Ice.Config=catalogServer.config; bash"



run-icestorm:
	mkdir -p IceStorm/
	gnome-terminal -- bash -c \
	"icebox --Ice.Config=icebox.config; bash"