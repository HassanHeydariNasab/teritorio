#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os, json, re, bcrypt, datetime, time
from peewee import *
from bottle import Bottle, request, response, hook
from urllib.parse import urlparse

if 'OPENSHIFT_DATA_DIR' in os.environ:
    #db = SqliteDatabase(os.environ['OPENSHIFT_DATA_DIR']+'datumaro.db')
    url = urlparse(os.environ.get('OPENSHIFT_MYSQL_DB_URL'))
    db = MySQLDatabase(os.environ['OPENSHIFT_APP_NAME'], host=url.hostname, port=url.port, user=url.username, passwd=url.password)
else:
    db = SqliteDatabase('datumaro.db')

@hook('before_request')
def _connect_db():
    db.connect()

@hook('after_request')
def _close_db():
    if not db.is_closed():
        db.close()


class Uzanto(Model):
    nomo = CharField()
    pasvorto = CharField()
    seanco = CharField(max_length=32, null=True)
    mono = IntegerField(default=400)
    class Meta:
        database = db

class Parto(Model):
    x = IntegerField()
    y = IntegerField()
    uzanto = ForeignKeyField(Uzanto, default=1)
    minajxo = IntegerField(default=0)
    nivelo = IntegerField(default=1)
    kreota = DateTimeField(default=datetime.datetime.now())
    class Meta:
        database = db

class UzantoVidPunkto(Model):
    uzanto = ForeignKeyField(Uzanto)
    parto = ForeignKeyField(Parto, default=1)
    class Meta:
        database = db

#db.connect()
#db.create_tables([UzantoVidPunkto])

def get_hashed_password(plain_text_password):
    # Hash a password for the first time
    #   (Using bcrypt, the salt is saved into the hash itself)
    return bcrypt.hashpw(plain_text_password, bcrypt.gensalt())

def check_password(plain_text_password, hashed_password):
    # Check hased password. Useing bcrypt, the salt is saved into the hash itself
    return bcrypt.checkpw(plain_text_password, hashed_password)

def krei_mondon(x, y):
    for i in range(0, x):
        for j in range(0, y):
            Parto.create(x = i, y = j)
#krei_mondon(50,50)
application = Bottle()
app = application

def ensalutita(seanco):
    try:
        Uzanto.get(Uzanto.seanco == seanco)
        return True
    except Uzanto.DoesNotExist:
        return False
    
def najbaraj_partoj(x, y, uzanto):
    return Parto.select().where( (Parto.x <= x+1) & (Parto.x >= x-1) & (Parto.y <= y+1) & (Parto.y >= y-1) & ~((Parto.x == x) & (Parto.y == y)) & (Parto.uzanto == uzanto) )

@app.route('/')
def index():
    return "<b>cxefa</b> pagxo"

@app.get("/testo")
def testo():
    response.content_type = "application/json; charset=utf-8"
    return json.dumps("test!")

@app.get("/subskribi/<nomo>/<pasvorto>")
def subskribi(nomo, pasvorto):
    #PORFARI cxu retposxto/telefono devas konfirmigxi?
    response.content_type = "application/json; charset=utf-8"
    try:
        uzanto = Uzanto.get(Uzanto.nomo == nomo)
        return json.dumps(False)
    except Uzanto.DoesNotExist:
        uzanto = Uzanto(nomo=nomo, pasvorto=get_hashed_password(pasvorto))
        uzanto.save()
        UzantoVidPunkto.create(uzanto=uzanto, parto=1)
        return json.dumps(True)

@app.get("/ensaluti/<nomo>/<pasvorto>")
def ensaluti(nomo, pasvorto):
    response.content_type = "application/json; charset=utf-8"
    uzanto = Uzanto.get(Uzanto.nomo == nomo)
    if check_password(pasvorto, uzanto.pasvorto):
        from random import SystemRandom
        import string
        seanco = ''.join(SystemRandom().choice(string.ascii_uppercase + string.digits) for _ in range(32))
        uzanto.seanco = seanco
        uzanto.save()
        vidpunkto = UzantoVidPunkto.select().join(Uzanto).where(Uzanto.seanco == seanco).get()
        return json.dumps({'seanco': seanco, 'x': vidpunkto.parto.x, 'y': vidpunkto.parto.y})
    else:
        return json.dumps(False)

@app.route('/saluti/<seanco>')
def saluti(seanco):
    response.content_type = "application/json; charset=utf-8"
    return json.dumps("Saluton " + Uzanto.get(Uzanto.seanco == seanco).nomo)

@app.route('/mapo/<seanco>/<x>/<y>')
def mapo(seanco, x, y):
    response.content_type = "application/json; charset=utf-8"
    uzanto = Uzanto.get(Uzanto.seanco == seanco)
    x = int(x)
    y = int(y)
    if x > 48:
        x = 48
    if y > 48:
        y = 48
    if x < 1:
        x = 1
    if y < 1:
        y = 1
    vidparto = Parto.get(Parto.x == x, Parto.y == y)
    UzantoVidPunkto.update(parto=vidparto).where(UzantoVidPunkto.uzanto == uzanto).execute()
    partoj = Parto.select().where( (Parto.x < x+10) & (Parto.x > x-10) & (Parto.y < y+10) & (Parto.y > y-10) )
    mapo = dict([(str(parto.x)+':'+str(parto.y), {'nomo':parto.uzanto.nomo, 'kreota':time.mktime(parto.kreota.timetuple()), 'nivelo':parto.nivelo, 'minajxo':parto.minajxo}) for parto in partoj])
    mapo.update({'uzanto':uzanto.nomo, 'mono':uzanto.mono})
    return json.dumps(mapo)

@app.route('/vidpunkto/<seanco>')
def vidpunkto(seanco):
    response.content_type = "application/json; charset=utf-8"
    vidpunkto = UzantoVidPunkto.select().join(Uzanto).where(Uzanto.seanco == seanco).get().parto
    return json.dumps({'x':str(vidpunkto.x),'y':str(vidpunkto.y)})

@app.route('/konstrui/<seanco>/<x>/<y>')
def konstrui(seanco, x, y):
    response.content_type = "application/json; charset=utf-8"
    uzanto = Uzanto.get(Uzanto.seanco == seanco)
    x = int(x)
    y = int(y)
    try:
        parto = Parto.get(Parto.x == x, Parto.y == y)
    except Parto.DoesNotExist:
        return json.dumps(False)
    partoj = Parto.select().where( (Parto.x <= x+1) & (Parto.x >= x-1) & (Parto.y <= y+1) & (Parto.y >= y-1) & ~((Parto.x == x) & (Parto.y == y)) & (Parto.uzanto == uzanto) )
    if parto.uzanto.id == 1 and partoj.count() >= 1 and uzanto.mono >= 1:
        Parto.update(uzanto=uzanto).where(Parto.x == x, Parto.y == y).execute()
        Uzanto.update(mono=Uzanto.mono-1).where(Uzanto.seanco == seanco).execute()
        return json.dumps(True)
    elif parto.uzanto.id == 1 and Parto.select().join(Uzanto, on=(Uzanto.id == Parto.uzanto)).where(Parto.uzanto == uzanto).count() == 0 and uzanto.mono >= 1:
        Parto.update(uzanto=uzanto).where(Parto.x == x, Parto.y == y).execute()
        Uzanto.update(mono=Uzanto.mono-1).where(Uzanto.seanco == seanco).execute()
        return json.dumps(True)
    elif parto.uzanto == uzanto and uzanto.mono >= 1:
        Parto.update(nivelo=Parto.nivelo+1).where(Parto.x == x, Parto.y == y).execute()
        Uzanto.update(mono=Uzanto.mono-1).where(Uzanto.seanco == seanco).execute()
        return json.dumps(True)
    elif parto.uzanto != uzanto and parto.uzanto.id != 1 and partoj.count() >= 1:
        Parto.update(uzanto=uzanto, nivelo=(Parto.nivelo/2)+1).where(Parto.x == x, Parto.y == y).execute()
        Uzanto.update(mono=Uzanto.mono-parto.nivelo).where(Uzanto.seanco == seanco).execute()
        return json.dumps(True)
    else:
        return json.dumps(False)
