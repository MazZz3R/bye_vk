#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Nikita Seleznev, 2018
import platform
import sys

PACKAGE_NAME = 'Bye, VK'
PACKAGE_SUFFIX = '-PyInstaller' if hasattr(sys, '_MEIPASS') else platform.system()
VERSION = '0.1.4a8' + PACKAGE_SUFFIX
