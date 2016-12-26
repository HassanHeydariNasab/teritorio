#!/usr/bin/env python
# -*- coding: utf-8 -*-

from peewee import *
from application import Uzanto, Parto, UzantoVidPunkto, db

db.connect()

Uzanto.update(mono=Uzanto.mono+10).where(Uzanto.id != 1).execute()

partoj = Parto.select().where((Parto.minajxo > 0) & (Parto.uzanto != 1))
for parto in partoj:
    Uzanto.update(mono=Uzanto.mono+parto.nivelo).where(Uzanto.id == parto.uzanto.id).execute()
    parto.minajxo -= parto.nivelo
    if parto.minajxo < 0:
        parto.minajxo = 0
    parto.save()

db.close()
