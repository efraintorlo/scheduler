SHELL := /bin/bash
#-----------------------------------------------
#    __  __       _         __ _ _
#   |  \/  | __ _| | _____ / _(_) | ___
#   | |\/| |/ _  | |/ / _ \ |_| | |/ _ \
#   | |  | | (_| |   <  __/  _| | |  __/
#   |_|  |_|\__,_|_|\_\___|_| |_|_|\___|
#
#-----------------------------------------------
#         Makefile for PROJECT
#-----------------------------------------------
#	Author:      elchinot7
#	Email:       efraazu@gmail.com
#	Github:      https://github.com/elchinot7
#	Description: INFO
#-----------------------------------------------

EXECUTABLE ?= spotify


default:
	python scheduler.py -e $(EXECUTABLE)

help:
	python scheduler.py -h

