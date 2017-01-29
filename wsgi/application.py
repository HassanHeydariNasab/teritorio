#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os, json, re, bcrypt, datetime, time
from peewee import *
from playhouse.pool import *
from bottle import Bottle, request, response, hook
from urllib.parse import urlparse
from urllib.request import urlopen
from random import sample, randrange, randint, choice
from collections import Counter

if 'OPENSHIFT_DATA_DIR' in os.environ:
    #db = SqliteDatabase(os.environ['OPENSHIFT_DATA_DIR']+'datumaro.db')
    #url = urlparse(os.environ.get('OPENSHIFT_MYSQL_DB_URL'))
    url = urlparse(os.environ.get('OPENSHIFT_POSTGRESQL_DB_URL'))
    #db = PooledMySQLDatabase(os.environ['OPENSHIFT_APP_NAME'], host=url.hostname, port=url.port, user=url.username, passwd=url.password)
    db = PooledPostgresqlDatabase(os.environ['OPENSHIFT_APP_NAME'], host=url.hostname, port=url.port, user=url.username, password=url.password)
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
    murita = BooleanField(default=False)
    orita = BooleanField(default=False)
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
        
#tttu:
class Tu(Model):
    uzantoO = ForeignKeyField(Uzanto, related_name='tu_o')
    uzantoX = ForeignKeyField(Uzanto, related_name='tu_x')
    tabulo = CharField()
    vico = ForeignKeyField(Uzanto)
    lastaIndekso = IntegerField(default=-1)
    venkulo = ForeignKeyField(Uzanto, related_name='tu_venkajxo')
    donita = BooleanField(default=False)
    class Meta:
        database = db
    
#db.connect()
#db.create_tables([Tu])

def get_hashed_password(plain_text_password):
    # Hash a password for the first time
    #   (Using bcrypt, the salt is saved into the hash itself)
    return bcrypt.hashpw(plain_text_password, bcrypt.gensalt())

def check_password(plain_text_password, hashed_password):
    # Check hased password. Useing bcrypt, the salt is saved into the hash itself
    return bcrypt.checkpw(plain_text_password, hashed_password)

def anstatauxigi(cxeno, indekso, signo):
    listo = list(cxeno)
    listo[indekso] = signo
    return ''.join(listo)

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
    
def najbaraj_partoj(x, y, uzanto=False, profundo=1, inkludita_muro=False):
    if not uzanto:
        if not inkludita_muro:
            return Parto.select().where( (Parto.x <= x+profundo) & (Parto.x >= x-profundo) & (Parto.y <= y+profundo) & (Parto.y >= y-profundo) & ~((Parto.x == x) & (Parto.y == y)) & ~(Parto.murita == True) )
        else:
            return Parto.select().where( (Parto.x <= x+profundo) & (Parto.x >= x-profundo) & (Parto.y <= y+profundo) & (Parto.y >= y-profundo) & ~((Parto.x == x) & (Parto.y == y)) )
    else:
        if not inkludita_muro:
            return Parto.select().where( (Parto.x <= x+profundo) & (Parto.x >= x-profundo) & (Parto.y <= y+profundo) & (Parto.y >= y-profundo) & ~((Parto.x == x) & (Parto.y == y)) & (Parto.uzanto == uzanto) & ~(Parto.murita == True))
        else:
            return Parto.select().where( (Parto.x <= x+profundo) & (Parto.x >= x-profundo) & (Parto.y <= y+profundo) & (Parto.y >= y-profundo) & ~((Parto.x == x) & (Parto.y == y)) & (Parto.uzanto == uzanto) )
        

@app.route('/')
def index():
    return "<b>cxefa</b> pagxo"

@app.route("/testo")
def testo():
    response.content_type = "application/json; charset=utf-8"
    return json.dumps("test!")

@app.route("/subskribi/<nomo>/<pasvorto>")
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

@app.route("/ensaluti/<nomo>/<pasvorto>")
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
    mapo = dict([(str(parto.x)+':'+str(parto.y), {'nomo':parto.uzanto.nomo, 'nivelo':parto.nivelo, 'minajxo':parto.minajxo, 'materialo':parto.materialo, 'murita':parto.murita, 'orita':parto.orita}) for parto in partoj])
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
#PORFARI forigxu dividilojn
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
    najbaraj_partoj_uzanto = najbaraj_partoj(parto.x, parto.y, uzanto)
    #Muro:
    if parto.murita:
        #plibonigado:
        if parto.uzanto == uzanto and uzanto.mono >= 1:
            Parto.update(nivelo=Parto.nivelo+7).where(Parto.id == parto.id).execute()
            Uzanto.update(mono=Uzanto.mono-1).where(Uzanto.seanco == seanco).execute()
            informo = 'ارتقای دیوار'
            return json.dumps({'rezulto':True, 'pagita':1, 'informo':informo})
        #simpla atakado:
        elif parto.uzanto != uzanto and parto.uzanto.id != 1 and najbaraj_partoj_uzanto.count() >= 1 and uzanto.mono >= parto.nivelo and sum([_.nivelo for _ in najbaraj_partoj_uzanto]) > parto.nivelo:
            Parto.update(uzanto=uzanto, nivelo=1, murita=False, materialo='nenia', minajxo=0).where(Parto.id == parto.id).execute()
            Uzanto.update(mono=Uzanto.mono-parto.nivelo).where(Uzanto.seanco == seanco).execute()
            return json.dumps({'rezulto':True, 'pagita':parto.nivelo, 'informo':'تخریب دیوار'})
        else:
            return json.dumps(False)
    else:
        #plibonigado:
        if parto.uzanto == uzanto and uzanto.mono >= 1:
            if najbaraj_partoj(parto.x, parto.y, uzanto, 2).count() == 24:
                Parto.update(nivelo=Parto.nivelo+4).where(Parto.id == parto.id).execute()
                informo = 'ارتقای حصاری دولایه'
            elif najbaraj_partoj_uzanto.count() == 8:
                Parto.update(nivelo=Parto.nivelo+2).where(Parto.id == parto.id).execute()
                informo = 'ارتقای حصاری'
            else:
                Parto.update(nivelo=Parto.nivelo+1).where(Parto.id == parto.id).execute()
                informo = 'ارتقای معمولی'
            Uzanto.update(mono=Uzanto.mono-1).where(Uzanto.seanco == seanco).execute()
            return json.dumps({'rezulto':True, 'pagita':1, 'informo':informo})
        #blokado de aliuloj:
        elif parto.uzanto != uzanto and parto.uzanto.id != 1 and najbaraj_partoj_uzanto.count() == 8 and uzanto.mono >= parto.nivelo/2+1 and sum([_.nivelo for _ in najbaraj_partoj_uzanto]) > parto.nivelo:
            Parto.update(uzanto=uzanto).where(Parto.id == parto.id).execute()
            if parto.orita:
                Uzanto.update(mono=Uzanto.mono-parto.nivelo/2-1, oro=Uzanto.oro+1).where(Uzanto.seanco == seanco).execute()
            else:
                Uzanto.update(mono=Uzanto.mono-parto.nivelo/2-1).where(Uzanto.seanco == seanco).execute()
            return json.dumps({'rezulto':True, 'pagita':int(parto.nivelo/2+1), 'informo':'حملهٔ محاصره‌ای'})
        #kolumna atakado:
        elif parto.uzanto != uzanto and parto.uzanto.id != 1 and ( Parto.select().where(((Parto.x < parto.x) & (Parto.x > parto.x - 4) & (Parto.y == y)) & (Parto.uzanto == uzanto)).count() == 3 or Parto.select().where( ((Parto.y > parto.y) & (Parto.y < parto.y + 4) & (Parto.x == x)) & (Parto.uzanto == uzanto) ).count() == 3 or Parto.select().where( ((Parto.y < parto.y) & (Parto.y > parto.y - 4) & (Parto.x == x)) & (Parto.uzanto == uzanto) ).count() == 3 or Parto.select().where( ((Parto.x > parto.x) & (Parto.x < parto.x + 4) & (Parto.y == y)) & (Parto.uzanto == uzanto)).count() == 3 ) and sum([_.nivelo for _ in najbaraj_partoj_uzanto]) > parto.nivelo and uzanto.mono >= (parto.nivelo/2)+1:
            Parto.update(uzanto=uzanto, nivelo=(Parto.nivelo/2)+1).where(Parto.id == parto.id).execute()
            if parto.orita:
                Uzanto.update(mono=Uzanto.mono-parto.nivelo/4-1, oro=Uzanto.oro+1).where(Uzanto.seanco == seanco).execute()
            else:
                Uzanto.update(mono=Uzanto.mono-parto.nivelo/4-1).where(Uzanto.seanco == seanco).execute()
            return json.dumps({'rezulto':True, 'pagita':int(parto.nivelo/4+1), 'informo':'حملهٔ ستونی'})
        #blokado de naturo:
        elif parto.uzanto.id == 1 and najbaraj_partoj_uzanto.count() == 8 and uzanto.mono >= 2:
            Parto.update(uzanto=uzanto, nivelo=7).where(Parto.id == parto.id).execute()
            Uzanto.update(mono=Uzanto.mono-2).where(Uzanto.seanco == seanco).execute()
            return json.dumps({'rezulto':True, 'pagita':2, 'informo':'تصرف محاصره‌ای'})
        #simpla gajnado de naturo:
        elif parto.uzanto.id == 1 and najbaraj_partoj_uzanto.count() >= 1 and uzanto.mono >= 1:
            Parto.update(uzanto=uzanto).where(Parto.id == parto.id).execute()
            Uzanto.update(mono=Uzanto.mono-1).where(Uzanto.seanco == seanco).execute()
            return json.dumps({'rezulto':True, 'pagita':1, 'informo':'تصرف معمولی'})
        #simpla atakado:
        elif parto.uzanto != uzanto and parto.uzanto.id != 1 and najbaraj_partoj_uzanto.count() >= 1 and uzanto.mono >= parto.nivelo and sum([_.nivelo for _ in najbaraj_partoj_uzanto]) > parto.nivelo:
            Parto.update(uzanto=uzanto, nivelo=(Parto.nivelo/2)+1).where(Parto.id == parto.id).execute()
            if parto.orita:
                Uzanto.update(mono=Uzanto.mono-parto.nivelo, oro=Uzanto.oro+1).where(Uzanto.seanco == seanco).execute()
            else:
                Uzanto.update(mono=Uzanto.mono-parto.nivelo).where(Uzanto.seanco == seanco).execute()
            return json.dumps({'rezulto':True, 'pagita':parto.nivelo, 'informo':'حملهٔ معمولی'})
        #unua domo:
        elif parto.nivelo == 1 and Parto.select().where(Parto.uzanto_id == uzanto.id).count() == 0 and uzanto.mono >= 1:
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
        parto = Parto.get(Parto.x == x, Parto.y == y, Parto.uzanto == uzanto, Parto.nivelo >= 7)
    except Parto.DoesNotExist:
        return json.dumps(False)
    x = int(x)
    y = int(y)
    najbaraj_partoj_naturo = najbaraj_partoj(x, y, 1)
    npc = najbaraj_partoj_naturo.count()
    if npc > 5:
        npc = 5
    Parto.update(uzanto=1, nivelo=1, murita=False, orita=False).where(Parto.id == parto.id).execute()
    npj = najbaraj_partoj(x, y)
    npjm = najbaraj_partoj(x, y, inkludita_muro=True)
    Parto.update(nivelo=Parto.nivelo-4).where(Parto.id << npj).execute()
    Parto.update(nivelo=Parto.nivelo-3).where(Parto.id << npjm).execute()
    for p in npjm:
        if p.nivelo < 1:
            p.nivelo = 1
            p.uzanto = 1
            p.murita = False
            p.orita = False
            p.save()
    if not parto.murita:
        Parto.update(materialo='argxento', minajxo=Parto.minajxo+7).where((Parto.id << sample(list(najbaraj_partoj_naturo), randrange(npc))) & ~(Parto.materialo == "oro")).execute()
        if randint(0, 3) == 1:
            Parto.update(materialo='oro', minajxo=Parto.minajxo+3).where((Parto.id == choice(najbaraj_partoj_naturo).id) & ~(Parto.materialo == "argxento")).execute()
    return json.dumps({'rezulto':True, 'pagita':0, 'informo':'انفجار'})

@app.route("/defendi/<seanco>/<x>/<y>")
def defendi(seanco, x, y):
    response.content_type = "application/json; charset=utf-8"
    uzanto = Uzanto.get(Uzanto.seanco == seanco)
    try:
        parto = Parto.get(Parto.x == x, Parto.y == y, Parto.uzanto == uzanto, Parto.nivelo >= 3, Parto.murita == False, Parto.orita == False)
    except Parto.DoesNotExist:
        return json.dumps(False)
    parto.murita = True
    parto.materialo = 'nenia'
    parto.minajxo = 0
    parto.save()
    return json.dumps({'rezulto':True, 'pagita':0, 'informo':'ساخت دیوار'})

@app.route("/origi/<seanco>/<x>/<y>")
def origi(seanco, x, y):
    response.content_type = "application/json; charset=utf-8"
    uzanto = Uzanto.get(Uzanto.seanco == seanco)
    if uzanto.oro < 1:
        return json.dumps(False)
    try:
        parto = Parto.get(Parto.x == x, Parto.y == y, Parto.uzanto == uzanto, Parto.nivelo >= 21, Parto.murita == False, Parto.orita == False)
    except Parto.DoesNotExist:
        return json.dumps(False)
    parto.orita = True
    parto.materialo = 'nenia'
    parto.minajxo = 0
    parto.save()
    uzanto.oro -= 1
    uzanto.save()
    return json.dumps({'rezulto':True, 'pagita':1, 'informo':'خانهٔ طلایی'})

@app.route("/statistiko/<seanco>")
def statistiko(seanco):
    response.content_type = "application/json; charset=utf-8"
    uzanto = Uzanto.get(Uzanto.seanco == seanco)
    argxentaj = Parto.select().where(Parto.uzanto == uzanto.id, Parto.orita == False).count()
    oraj = Parto.select().where(Parto.uzanto == uzanto.id, Parto.orita == True).count()
    muroj = Parto.select().where(Parto.uzanto == uzanto.id, Parto.murita == True).count()
    if uzanto.nomo == 'hsn6':
        uzantoj = Uzanto.select().count()
        return json.dumps({'argxentaj':argxentaj, 'oraj':oraj, 'muroj':muroj, 'uzantoj':uzantoj})
    else:
        return json.dumps({'argxentaj':argxentaj, 'oraj':oraj, 'muroj':muroj})

@app.route("/rango/<seanco>")
def rango(seanco):
    response.content_type = "application/json; charset=utf-8"
    uzanto = Uzanto.get(Uzanto.seanco == seanco)
    uzantoj = Uzanto.select().join(Parto).where(Parto.orita == True)
    uzantoj_ripetitaj = Counter(uzantoj).most_common()
    sep_unuaj = {}
    for (uzanto_ripetita, i) in zip(uzantoj_ripetitaj[:7], range(0,7)):
        sep_unuaj[str(i)] = (uzanto_ripetita[0].nomo, str(uzanto_ripetita[1]))
    return json.dumps(sep_unuaj)

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
    
#TTTU:
@app.route("/konverti/<seanco>/<oro>")
def konverti(seanco, oro):
    response.content_type = "application/json; charset=utf-8"
    uzanto = Uzanto.get(Uzanto.seanco == seanco)
    oro = int(oro)
    if uzanto.oro < oro or oro <= 0:
        return json.dumps(False)
    else:
        Uzanto.update(mono=Uzanto.mono+oro*40, oro=Uzanto.oro-oro).where(Uzanto.seanco == seanco).execute()
        return json.dumps(True)

@app.route('/rekomenci/<seanco>')
def rekomenci(seanco):
    response.content_type = "application/json; charset=utf-8"
    uzanto = Uzanto.get(Uzanto.seanco == seanco)
    naturo = Uzanto.get(Uzanto.id == 1)
    try:
        #atenda uzanto:
        tttu = Tu.get(Tu.uzantoX == naturo, Tu.uzantoO != uzanto)
        #rezignigi uzanton je aliaj ludoj:
        #PORFARI premiu al oponanto
        Tu.update(venkulo=Tu.uzantoO).where(Tu.uzantoX == uzanto)
        Tu.update(venkulo=Tu.uzantoX).where(Tu.uzantoO == uzanto, Tu.uzantoX != naturo)
        #anstatauxigi naturon per uzanto:
        tttu.uzantoX = uzanto
        tttu.vico = tttu.uzantoO
        tttu.save()
    except Tu.DoesNotExist:
        try:
            tttu = Tu.get(Tu.uzantoX == naturo, Tu.uzantoO == uzanto)
        except Tu.DoesNotExist:
            tttu = Tu.create(uzantoO=uzanto, uzantoX=naturo, tabulo=81*'e', vico=naturo, venkulo=naturo)
    return json.dumps(True)

@app.route('/tabulo/<seanco>')
def tabulo(seanco):
    response.content_type = "application/json; charset=utf-8"
    uzanto = Uzanto.get(Uzanto.seanco == seanco)
    naturo = Uzanto.get(Uzanto.id == 1)
    try:
        #kuranta ludo inter du uzantoj:
        tttu = Tu.get((Tu.uzantoX != naturo) & ((Tu.uzantoO == uzanto) | (Tu.uzantoX == uzanto)) & (Tu.venkulo == naturo))
    except Tu.DoesNotExist:
        try:
            #finita ludo:
            tttu = Tu.get((Tu.uzantoX != naturo) & ((Tu.uzantoO == uzanto) | (Tu.uzantoX == uzanto)) & (Tu.venkulo != naturo))
        except Tu.DoesNotExist:
            try:
                #atenda uzanto:
                tttu = Tu.get(Tu.uzantoX == naturo, Tu.uzantoO == uzanto)
            except Tu.DoesNotExist:
                #preta por nova ludo:
                return json.dumps(False)
    tb = tttu.tabulo
    T = dict([(str(i//9), tb[i:i+9]) for i in range(0, len(tb), 9)])
    #nun T estas tiel: {'0':'oeexxxeeoe', '1':'eeeoxeoxe', ..., '8':'eoxeoxoxo'}
    for I, t in T.items():
        if t[0:3] == 'xxx' or t[3:6] == 'xxx' or t[6:9] == 'xxx' or t[0::3] == 'xxx' or t[1::3] == 'xxx' or t[2::3] == 'xxx' or t[0]+t[4]+t[8] == 'xxx' or t[2]+t[4]+t[6] == 'xxx':
            T[I] = {'t': T[I], 'S': 'X'}
        elif t[0:3] == 'ooo' or t[3:6] == 'ooo' or t[6:9] == 'ooo' or t[0::3] == 'ooo' or t[1::3] == 'ooo' or t[2::3] == 'ooo' or t[0]+t[4]+t[8] == 'ooo' or t[2]+t[4]+t[6] == 'ooo':
            T[I] = {'t': T[I], 'S': 'O'}
        else:
            T[I] = {'t': T[I], 'S': 'E'}
    #nun T estas tiel: {'0':{'t':'oeexxxeeoe', 'S': 'X'}, '1':{'t':'eoeoxeoxe', 'S':'E'}, ...}
    #kontroli se la ludo havas venkulo:
    S = ''
    for I in range(0,9):
        S += T[str(I)]['S']
    if tttu.venkulo != naturo:
        venkulo = tttu.venkulo  
    elif S[0:3] == 'XXX' or S[3:6] == 'XXX' or S[6:9] == 'XXX' or S[0::3] == 'XXX' or S[1::3] == 'XXX' or S[2::3] == 'XXX' or S[0]+S[4]+S[8] == 'XXX' or S[2]+S[4]+S[6] == 'XXX':
        venkulo = tttu.uzantoX
    elif S[0:3] == 'OOO' or S[3:6] == 'OOO' or S[6:9] == 'OOO' or S[0::3] == 'OOO' or S[1::3] == 'OOO' or S[2::3] == 'OOO' or S[0]+S[4]+S[8] == 'OOO' or S[2]+S[4]+S[6] == 'OOO':
        venkulo = tttu.uzantoO
    else:
        venkulo = naturo
    if tttu.venkulo == uzanto and not tttu.donita:
        tttu.update(donita=True).execute()
        partoj = Parto.select().where((Parto.minajxo > 0) & (Parto.uzanto == uzanto))
        for parto in partoj:
            if parto.materialo == 'argxento':
                uzanto.mono += parto.nivelo
            elif parto.materialo == 'oro':
                uzanto.oro += parto.nivelo
            parto.minajxo -= parto.nivelo
            if parto.minajxo < 0:
                parto.minajxo = 0
            parto.save()
            if uzanto.oro > 40:
                uzanto.oro = 40
            uzanto.save()
    if uzanto == tttu.uzantoO:
        xo = 'o'
        oponanto = tttu.uzantoX
    elif uzanto == tttu.uzantoX:
        xo = 'x'
        oponanto = tttu.uzantoO
    return json.dumps({'Tabulo':T,'uzantoO':tttu.uzantoO.nomo, 'uzantoX':tttu.uzantoX.nomo, 'vico':tttu.vico.nomo, 'lastaIndekso':tttu.lastaIndekso, 'uzanto':uzanto.nomo, 'xo':xo, 'oponanto':oponanto.nomo, 'venkulo':venkulo.nomo})

@app.route('/agi/<seanco>/<I>/<i>')
def agi(seanco, I, i):
    response.content_type = "application/json; charset=utf-8"
    uzanto = Uzanto.get(Uzanto.seanco == seanco)
    naturo = Uzanto.get(Uzanto.id == 1)
    I = int(I)
    i = int(i)
    try:
        tttu = Tu.get((Tu.uzantoX != naturo) & ((Tu.uzantoO == uzanto) | (Tu.uzantoX == uzanto)) & (Tu.venkulo == naturo))
    except Tu.DoesNotExist:
        return json.dumps('لطفاً منتظر بمانید تا بازیکن دیگری به بازی بپیوندد.')
    if tttu.lastaIndekso != I and tttu.lastaIndekso != -1:
        return json.dumps('senpermesa movo '+str(I)+':'+str(i))
    if tttu.vico != uzanto or tttu.vico == naturo:
        return json.dumps('ne estas via vico')
    tb = tttu.tabulo
    if tb[I*9+i] == 'e':
        if uzanto == tttu.uzantoO:
            tb = anstatauxigi(tb, I*9+i, 'o')
        elif uzanto == tttu.uzantoX:
            tb = anstatauxigi(tb, I*9+i, 'x')
    else:
        return json.dumps('ne estas malplena')
    tttu.tabulo = tb
    tttu.save()
    T = dict([(str(_//9), tb[_:_+9]) for _ in range(0, len(tb), 9)])
    #nun T estas tiel: {'0':'oeexxxeeoe', '1':'eeeoxeoxe', ..., '8':'eoxeoxoxo'}
    for I, t in T.items():
        if t[0:3] == 'xxx' or t[3:6] == 'xxx' or t[6:9] == 'xxx' or t[0::3] == 'xxx' or t[1::3] == 'xxx' or t[2::3] == 'xxx' or t[0]+t[4]+t[8] == 'xxx' or t[2]+t[4]+t[6] == 'xxx':
            T[I] = {'t': T[I], 'S': 'X'}
        elif t[0:3] == 'ooo' or t[3:6] == 'ooo' or t[6:9] == 'ooo' or t[0::3] == 'ooo' or t[1::3] == 'ooo' or t[2::3] == 'ooo' or t[0]+t[4]+t[8] == 'ooo' or t[2]+t[4]+t[6] == 'ooo':
            T[I] = {'t': T[I], 'S': 'O'}
        else:
            T[I] = {'t': T[I], 'S': 'E'}
    #nun T estas tiel: {'0':{'t':'oeexxxeeoe', 'S': 'X'}, '1':{'t':'eoeoxeoxe', 'S':'E'}, ...}
    #kontroli se la ludo havas venkulo:
    S = ''
    for I in range(0,9):
        S += T[str(I)]['S']
        
    if S[0:3] == 'XXX' or S[3:6] == 'XXX' or S[6:9] == 'XXX' or S[0::3] == 'XXX' or S[1::3] == 'XXX' or S[2::3] == 'XXX' or S[0]+S[4]+S[8] == 'XXX' or S[2]+S[4]+S[6] == 'XXX':
        tttu.venkulo = tttu.uzantoX
    elif S[0:3] == 'OOO' or S[3:6] == 'OOO' or S[6:9] == 'OOO' or S[0::3] == 'OOO' or S[1::3] == 'OOO' or S[2::3] == 'OOO' or S[0]+S[4]+S[8] == 'OOO' or S[2]+S[4]+S[6] == 'OOO':
        tttu.venkulo = tttu.uzantoO
    if T[str(i)]['S'] == 'E':
        tttu.lastaIndekso = i
    else:
        tttu.lastaIndekso = -1
    if tttu.vico == tttu.uzantoO:
        tttu.vico = tttu.uzantoX
    elif tttu.vico == tttu.uzantoX:
        tttu.vico = tttu.uzantoO
    tttu.save()
    if uzanto == tttu.uzantoO:
        xo = 'o'
        oponanto = tttu.uzantoX
    elif uzanto == tttu.uzantoX:
        xo = 'x'
        oponanto = tttu.uzantoO
    return json.dumps({'Tabulo':T, 'uzantoO':tttu.uzantoO.nomo, 'uzantoX':tttu.uzantoX.nomo, 'vico':tttu.vico.nomo, 'lastaIndekso':tttu.lastaIndekso, 'uzanto':uzanto.nomo, 'xo':xo, 'oponanto':oponanto.nomo, 'venkulo':tttu.venkulo.nomo})

@app.route('/rezigni/<seanco>')
def rezigni(seanco):
    response.content_type = "application/json; charset=utf-8"
    uzanto = Uzanto.get(Uzanto.seanco == seanco)
    naturo = Uzanto.get(Uzanto.id == 1)
    try:
        tttu = Tu.get((Tu.uzantoX != naturo) & ((Tu.uzantoO == uzanto) | (Tu.uzantoX == uzanto)) & (Tu.venkulo == naturo))
    except Tu.DoesNotExist:
        return json.dumps(False)
    if tttu.uzantoO == uzanto:
        tttu.venkulo = tttu.uzantoX
        partoj = Parto.select().where((Parto.minajxo > 0) & (Parto.uzanto == tttu.uzantoX))
    elif tttu.uzantoX == uzanto:
        tttu.venkulo = tttu.uzantoO
        partoj = Parto.select().where((Parto.minajxo > 0) & (Parto.uzanto == tttu.uzantoO))
    for parto in partoj:
        if parto.materialo == 'argxento':
            uzanto.mono += parto.nivelo
        elif parto.materialo == 'oro':
            uzanto.oro += parto.nivelo
        parto.minajxo -= parto.nivelo
        if parto.minajxo < 0:
            parto.minajxo = 0
        parto.save()
    if uzanto.oro > 40:
        uzanto.oro = 40
    uzanto.save()
    tb = tttu.tabulo
    T = dict([(str(_//9), tb[_:_+9]) for _ in range(0, len(tb), 9)])
    if uzanto == tttu.uzantoO:
        xo = 'o'
        oponanto = tttu.uzantoX
    elif uzanto == tttu.uzantoX:
        xo = 'x'
        oponanto = tttu.uzantoO
    tttu.save()
    print(tttu.venkulo.nomo)
    tttu = Tu.get((Tu.uzantoX != naturo) & ((Tu.uzantoO == uzanto) | (Tu.uzantoX == uzanto)) & (Tu.venkulo != naturo))
    print(tttu.venkulo.nomo)
    return json.dumps({'Tabulo':T,'uzantoO':tttu.uzantoO.nomo, 'uzantoX':tttu.uzantoX.nomo, 'vico':tttu.vico.nomo, 'lastaIndekso':tttu.lastaIndekso, 'uzanto':uzanto.nomo, 'xo':xo, 'oponanto':oponanto.nomo, 'venkulo':tttu.venkulo.nomo})
