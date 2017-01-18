#!/usr/bin/env python
# -*- coding: utf-8 -*-

from peewee import *
from application import Uzanto, Parto, UzantoVidPunkto, db

db.connect()

Uzanto.update(mono=Uzanto.mono+7).where(Uzanto.id != 1).execute()

partoj = Parto.select().where((Parto.minajxo > 0) & (Parto.uzanto != 1))
for parto in partoj:
    if parto.materialo == 'argxento':
        Uzanto.update(mono=Uzanto.mono+parto.nivelo).where(Uzanto.id == parto.uzanto.id).execute()
    elif parto.materialo == 'oro':
        Uzanto.update(oro=Uzanto.oro+parto.nivelo).where(Uzanto.id == parto.uzanto.id).execute()
    parto.minajxo -= parto.nivelo
    if parto.minajxo < 0:
        parto.minajxo = 0
    parto.save()

Uzanto.update(oro=40).where(Uzanto.oro > 40).execute()

db.close()
