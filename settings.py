#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Nikita Seleznev, 2018
import platform
import sys

PACKAGE_NAME = 'Bye, VK'
PY_INSTALLER = hasattr(sys, '_MEIPASS')
CLIENT = 'PyInstaller' if PY_INSTALLER else platform.system()
VERSION = '0.2'
