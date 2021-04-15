#!/usr/bin/make -f
# -*- mode:makefile -*-



run-icestorm:
	mkdir -p IceStorm/
	gnome-terminal -- bash -c \
	"icebox --Ice.Config=icebox.config; bash"