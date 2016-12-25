#!/usr/bin/env python
# -*- coding: utf-8 -*-
import datetime, time
from peewee import *
from application import Uzanto, Parto, UzantoVidPunkto

Uzanto.update(mono=Uzanto.mono+1).where(Uzanto.id != 1).execute()

partoj = Parto.select().where(Parto.minajxo > 0)
for parto in partoj:
    Uzanto.update(mono=Uzanto.mono+parto.nivelo).where(Uzanto.id == parto.uzanto.id).execute()
    parto.minajxo -= parto.nivelo
    parto.save()
