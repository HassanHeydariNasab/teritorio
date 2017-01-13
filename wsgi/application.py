#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os, json, re, bcrypt, datetime, time
from peewee import *
from playhouse.pool import *
from bottle import Bottle, request, response, hook
from urllib.parse import urlparse
from urllib.request import urlopen
from random import sample, randrange, randint, choice

if 'OPENSHIFT_DATA_DIR' in os.environ:
    #db = SqliteDatabase(os.environ['OPENSHIFT_DATA_DIR']+'datumaro.db')
    #url = urlparse(os.environ.get('OPENSHIFT_MYSQL_DB_URL'))
    url = urlparse(os.environ.get('OPENSHIFT_POSTGRESQL_DB_URL'))
    #db = PooledMySQLDatabase(os.environ['OPENSHIFT_APP_NAME'], host=url.hostname, port=url.port, user=url.username, passwd=url.password)
    db = PooledPostgresqlDatabase(os.environ['OPENSHIFT_APP_NAME'], host=url.hostname, port=url.port, user=url.username, password=url.password)
else:
    db = PooledSqliteDatabase('datumaro.db')

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
    oro = IntegerField(default=7)
    class Meta:
        database = db

class Parto(Model):
    x = IntegerField()
    y = IntegerField()
    uzanto = ForeignKeyField(Uzanto, default=1)
    minajxo = IntegerField(default=0)
    materialo = CharField(default='nenia')
    nivelo = IntegerField(default=1)
    class Meta:
        database = db

class UzantoVidPunkto(Model):
    uzanto = ForeignKeyField(Uzanto)
    parto = ForeignKeyField(Parto, default=1)
    class Meta:
        database = db

class Ordo(Model):
    uzanto = ForeignKeyField(Uzanto)
    jxetono = CharField()
    sku = CharField()
    uzita = BooleanField(default=False)
    class Meta:
        database = db

#db.connect()
#db.create_tables([Ordo])

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
    
def najbaraj_partoj(x, y, uzanto=False, profundo=1):
    if not uzanto:
        return Parto.select().where( (Parto.x <= x+profundo) & (Parto.x >= x-profundo) & (Parto.y <= y+profundo) & (Parto.y >= y-profundo) & ~((Parto.x == x) & (Parto.y == y)) )
    else:
        return Parto.select().where( (Parto.x <= x+profundo) & (Parto.x >= x-profundo) & (Parto.y <= y+profundo) & (Parto.y >= y-profundo) & ~((Parto.x == x) & (Parto.y == y)) & (Parto.uzanto == uzanto) )
        

@app.route('/')
def index():
    return "<b>cxefa</b> pagxo"

@app.route("/testo")
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
        UzantoVidPunkto.create(uzanto=uzanto, parto=1275)
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
    mapo = dict([(str(parto.x)+':'+str(parto.y), {'nomo':parto.uzanto.nomo, 'nivelo':parto.nivelo, 'minajxo':parto.minajxo, 'materialo':parto.materialo}) for parto in partoj])
    minejoj = Parto.select().where((Parto.minajxo > 0) & (Parto.uzanto == uzanto.id))
    gajnanto = 7
    orogajnanto = 0
    for minejo in minejoj:
        if minejo.materialo == 'argxento':
            gajnanto += minejo.nivelo
        elif minejo.materialo == 'oro':
            orogajnanto += minejo.nivelo
    mapo.update({'uzanto':uzanto.nomo, 'mono':uzanto.mono, 'oro':uzanto.oro, 'gajnanto':gajnanto, 'orogajnanto':orogajnanto})
    return json.dumps(mapo)

@app.route('/vidpunkto/<seanco>')
def vidpunkto(seanco):
    response.content_type = "application/json; charset=utf-8"
    try:
        vidpunkto = UzantoVidPunkto.select().join(Uzanto).where(Uzanto.seanco == seanco).get().parto
        return json.dumps({'x':str(vidpunkto.x),'y':str(vidpunkto.y)})
    except UzantoVidPunkto.DoesNotExist:
        return json.dumps(False)

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
    partoj = najbaraj_partoj(parto.x, parto.y)
    partoj_uzanto = najbaraj_partoj(parto.x, parto.y, uzanto)
    #plibonigado:
    if parto.uzanto == uzanto and uzanto.mono >= 1:
        if najbaraj_partoj(parto.x, parto.y, uzanto, 2).count() == 24:
            Parto.update(nivelo=Parto.nivelo+4).where(Parto.x == x, Parto.y == y).execute()
            informo = 'ارتقای حصاری دولایه'
        elif partoj_uzanto.count() == 8:
            Parto.update(nivelo=Parto.nivelo+2).where(Parto.x == x, Parto.y == y).execute()
            informo = 'ارتقای حصاری'
        else:
            Parto.update(nivelo=Parto.nivelo+1).where(Parto.x == x, Parto.y == y).execute()
            informo = 'ارتقای معمولی'
        Uzanto.update(mono=Uzanto.mono-1).where(Uzanto.seanco == seanco).execute()
        return json.dumps({'rezulto':True, 'pagita':1, 'informo':informo})
    #blokado de aliuloj:
    elif parto.uzanto != uzanto and parto.uzanto.id != 1 and partoj_uzanto.count() == 8 and uzanto.mono >= parto.nivelo/2+1:
        Parto.update(uzanto=uzanto).where(Parto.x == x, Parto.y == y).execute()
        Uzanto.update(mono=Uzanto.mono-parto.nivelo/2-1).where(Uzanto.seanco == seanco).execute()
        return json.dumps({'rezulto':True, 'pagita':int(parto.nivelo/2+1), 'informo':'حملهٔ محاصره‌ای'})
    #kolumna atakado:
    elif parto.uzanto != uzanto and parto.uzanto.id != 1 and ( Parto.select().where(((Parto.x < parto.x) & (Parto.x > parto.x - 4) & (Parto.y == y)) & (Parto.uzanto == uzanto)).count() == 3 or Parto.select().where( ((Parto.y > parto.y) & (Parto.y < parto.y + 4) & (Parto.x == x)) & (Parto.uzanto == uzanto) ).count() == 3 or Parto.select().where( ((Parto.y < parto.y) & (Parto.y > parto.y - 4) & (Parto.x == x)) & (Parto.uzanto == uzanto) ).count() == 3 or Parto.select().where( ((Parto.x > parto.x) & (Parto.x < parto.x + 4) & (Parto.y == y)) & (Parto.uzanto == uzanto)).count() == 3 ) and uzanto.mono >= (parto.nivelo/2)+1:
        Parto.update(uzanto=uzanto, nivelo=(Parto.nivelo/2)+1).where(Parto.x == x, Parto.y == y).execute()
        Uzanto.update(mono=Uzanto.mono-parto.nivelo/4-1).where(Uzanto.seanco == seanco).execute()
        return json.dumps({'rezulto':True, 'pagita':int(parto.nivelo/4+1), 'informo':'حملهٔ ستونی'})
    #blokado de naturo:
    elif parto.uzanto.id == 1 and partoj_uzanto.count() == 8 and uzanto.mono >= 1:
        Parto.update(uzanto=uzanto, nivelo=7).where(Parto.x == x, Parto.y == y).execute()
        Uzanto.update(mono=Uzanto.mono-2).where(Uzanto.seanco == seanco).execute()
        return json.dumps({'rezulto':True, 'pagita':2, 'informo':'تصرف محاصره‌ای'})
    #simpla gajnado de naturo:
    elif parto.uzanto.id == 1 and partoj_uzanto.count() >= 1 and uzanto.mono >= 1:
        Parto.update(uzanto=uzanto).where(Parto.x == x, Parto.y == y).execute()
        Uzanto.update(mono=Uzanto.mono-1).where(Uzanto.seanco == seanco).execute()
        return json.dumps({'rezulto':True, 'pagita':1, 'informo':'تصرف معمولی'})
    #simpla atakado:
    elif parto.uzanto != uzanto and parto.uzanto.id != 1 and partoj_uzanto.count() >= 1 and uzanto.mono >= parto.nivelo+2:
        Parto.update(uzanto=uzanto, nivelo=(Parto.nivelo/2)+1).where(Parto.x == x, Parto.y == y).execute()
        Uzanto.update(mono=Uzanto.mono-parto.nivelo-2).where(Uzanto.seanco == seanco).execute()
        return json.dumps({'rezulto':True, 'pagita':parto.nivelo+2, 'informo':'حملهٔ معمولی'})
    #unua domo:
    elif parto.uzanto.id == 1 and Parto.select().where(Parto.uzanto_id == uzanto.id).count() == 0 and uzanto.mono >= 1:
        Parto.update(uzanto=uzanto).where(Parto.id == parto.id).execute()
        Uzanto.update(mono=Uzanto.mono-1).where(Uzanto.id == uzanto.id).execute()
        return json.dumps({'rezulto':True, 'pagita':1, 'informo':'نخستین خانه'})
    else:
        return json.dumps(False)

@app.route("/eksplodi/<seanco>/<x>/<y>")
def eksplodi(seanco, x, y):
    response.content_type = "application/json; charset=utf-8"
    uzanto = Uzanto.get(Uzanto.seanco == seanco)
    try:
        parto = Parto.get(Parto.x == x, Parto.y == y, Parto.uzanto == uzanto)
    except Parto.DoesNotExist:
        return json.dumps(False)
    x = int(x)
    y = int(y)
    np = najbaraj_partoj(x, y, 1)
    npc = np.count()
    if npc > 5:
        npc = 5
    if parto.nivelo >= 2:
        Parto.update(uzanto=1, nivelo=1).where(Parto.x == x, Parto.y == y).execute()
        Parto.update(nivelo=Parto.nivelo/5+1).where(najbaraj_partoj(x, y)).execute()
        Parto.update(materialo='argxento', minajxo=Parto.minajxo+40).where((Parto.id << sample(list(np), randrange(npc))) & ~(Parto.materialo >> 'oro')).execute()
        if randint(0, 1) == 1:
            print(11111111)
            Parto.update(materialo='oro', minajxo=Parto.minajxo+40).where((Parto.id == choice(np).id) & ~(Parto.materialo >> 'argxento')).execute()
        return json.dumps({'rezulto':True, 'pagita':0, 'informo':'انفجار'})
    else:
        return json.dumps(False)

@app.route('/ordo/<seanco>/<ordoj>')
def ordo(seanco, ordoj):
    response.content_type = "application/json; charset=utf-8"
    uzanto = Uzanto.get(Uzanto.seanco == seanco)
    ordoj = ordoj.split(',')
    for ordo in ordoj:
        ordo = ordo.split('-')
        try:
            jxetono = ordo[0]
            sku = ordo[1]
        except IndexError:
            break;
        #PORFARI kontrolu la ordon per Bazar
        '''
        respondo = json.loads(str(urlopen('https://pardakht.cafebazaar.ir/devapi/v2/api/validate/<package_name>/inapp/<product_id>/purchases/<purchase_token>/').read())[2:-1])
        try:
            respondo['purchaseState'] == 0
        except KeyError:
            print(respondo['error']+' --> '+respondo['error_description'])
        '''
        Uzanto.update(mono = Uzanto.mono + int(sku[6:])).where(Uzanto.seanco == seanco).execute()
        
    return json.dumps(True)
    
@app.route("/konverti/<seanco>/<oro>")
def konverti(seanco, oro):
    response.content_type = "application/json; charset=utf-8"
    uzanto = Uzanto.get(Uzanto.seanco == seanco)
    oro = int(oro)
    if uzanto.oro < oro or oro <= 0:
        return json.dumps(False)
    else:
        Uzanto.update(mono=Uzanto.mono+oro*100, oro=Uzanto.oro-oro).where(Uzanto.seanco == seanco).execute()
        return json.dumps(True)
