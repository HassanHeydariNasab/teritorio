#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os, json, re, bcrypt, datetime, time, sys
from peewee import *
from urllib.parse import urlparse
sys.path.append('../../../wsgi/')
from application import Uzanto, Parto, UzantoVidPunkto
Uzanto.update(mono=Uzanto.mono+1).where(Uzanto.id != 1).execute()
