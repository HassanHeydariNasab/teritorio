if(window.location.toString().match(/android/)){
  //var r = new RestClient('http://10.0.2.2:8080', {contentType: 'json'});
  var r = new RestClient('http://blokado-altajceloj.rhcloud.com', {contentType: 'json'});
}
else{
  var r = new RestClient('http://127.0.0.1:8080', {contentType: 'json'});
  //var r = new RestClient('http://blokado-altajceloj.rhcloud.com', {contentType: 'json'});
}
r.res('mapo')
r.res('vidpunkto')
r.res('konstrui')
r.res('eksplodi')
r.res('defendi')
r.res('ordo')
r.res('konverti')

var mm
var cl = console.log
var supru = document.getElementById('supru')
var malsupru = document.getElementById('malsupru')
var dekstru = document.getElementById('dekstru')
var maldekstru = document.getElementById('maldekstru')

function montri(msg){
  var informo = document.getElementById('informo')
  informo.innerHTML = msg
  informo.style.display = 'initial'
  setTimeout( function(){informo.style.display = 'none'}, 2000 );
}

function prompti(msg){
  var prompto = document.getElementById('prompto')
  prompto.innerHTML = msg
  prompto.style.display = 'initial'
  prompto.className = 'montri'
}
function kasxi_prompton(){
  var prompto = document.getElementById('prompto')
  prompto.className = 'kasxi'
  setTimeout( function(){prompto.style.display = 'none'}, 1000 );
}
function iri(){
  prompti('<div id="iri">'+
          '<div id="poz">'+
          '<label for="x">x:</label>'+
          '<input name="x" id="x" type="number" />'+
          '<label for="x">y:</label>'+
          '<input name="y" id="y" type="number" />'+
          '</div>'+
          '<div id="iru" onclick="iru()">برو</div><div id="fermu" onclick="kasxi_prompton()">بستن</div>'+
          '</div>')
}
function montri_konverton(){
  prompti('<div class="rtl">'
          + '<div class="titlo">تبدیل هر بلوک طلایی به ۱۰۰ نقره‌ای</div>'+
          '<label for="oro" class="ora">طلای مصرفی:</label>'
          + '</div>'+
          '<input name="oro" id="oro" type="number" />'+
          '<div id="iru" onclick="konvertu()">تبدیل</div><div id="fermu" onclick="kasxi_prompton()">بستن</div>'+
           '')
}
function konvertu(){
  r.konverti(window.localStorage.getItem('seanco')+'/'+document.getElementById('oro').value).get().then(function(k){
    r.mapo(window.localStorage.getItem('seanco')+'/'+x+'/'+y).get().then(function(m){
        xs = x
        ys = y
        mm = m
        mapi(m)
      })
    kasxi_prompton()
    if(k){
      montri('تبدیل با موفقیت انجام شد.')
    }
    else if(!k){
      montri('تبدیل انجام نشد.')
    }
  })
}
aktivi_konstruadon()
function aktivi_konstruadon(){
  window.localStorage.setItem('ago', 'konstruado')
  var konstruado = document.getElementById('konstruado')
  var eksplodado = document.getElementById('eksplodado')
  var defendado = document.getElementById('defendado')
  konstruado.style.backgroundColor = '#FFB300'
  konstruado.style.color = '#212121'
  eksplodado.style.backgroundColor = ''
  eksplodado.style.color = '#fff'
  defendado.style.backgroundColor = ''
  defendado.style.color = '#fff'
}
function aktivi_eksplodadon(){
  window.localStorage.setItem('ago', 'eksplodado')
  var konstruado = document.getElementById('konstruado')
  var eksplodado = document.getElementById('eksplodado')
  var defendado = document.getElementById('defendado')
  eksplodado.style.backgroundColor = '#FFB300'
  eksplodado.style.color = '#212121'
  konstruado.style.backgroundColor = ''
  konstruado.style.color = '#fff'
  defendado.style.backgroundColor = ''
  defendado.style.color = '#fff'
}
function aktivi_defendadon(){
  window.localStorage.setItem('ago', 'defendado')
  var konstruado = document.getElementById('konstruado')
  var eksplodado = document.getElementById('eksplodado')
  var defendado = document.getElementById('defendado')
  defendado.style.backgroundColor = '#FFB300'
  defendado.style.color = '#212121'
  eksplodado.style.backgroundColor = ''
  eksplodado.style.color = '#fff'
  konstruado.style.backgroundColor = ''
  konstruado.style.color = '#fff'
}
function persa(cifero){
  return cifero.replace(/0/g, "۰").replace(/1/g, "۱").replace(/2/g, "۲").replace(/3/g, "۳").replace(/4/g, "۴").replace(/5/g, "۵").replace(/6/g, "۶").replace(/7/g, "۷").replace(/8/g, "۸").replace(/9/g, "۹")
}
function listi_acxeteblojn(){
  prompti('<div class="acxetebla" onclick="Android.acxeti_dialogo(\'blokoj100\')">۱۰۰ بلوک</div><div class="acxetebla" onclick="Android.acxeti_dialogo(\'blokoj200\')">۲۰۰ بلوک</div><div class="acxetebla" onclick="Android.acxeti_dialogo(\'blokoj500\')">۵۰۰ بلوک</div><div class="acxetebla" onklick="Android.acxeti_dialogo(\'blokoj1000\')">۱۰۰۰ بلوک</div><div id="fermu" onclick="kasxi_prompton()">بستن</div>')
}
function sendi_ordojn(){
  r.ordo(window.localStorage.getItem('seanco')+'/'+window.localStorage.getItem('ordoj')).get().then(function(k){
    if(k){
      window.localStorage.setItem('ordoj', '');
      window.location.reload()
    }
  })
}
//x esatas por nuna x
var x, y
//xs estas por lasta x ke la mapo elsxutigxis
var xs, ys
x = window.localStorage.getItem('x')
y = window.localStorage.getItem('y')
var seanco = window.localStorage.getItem('seanco')
if (!(seanco)){
  window.location = 'ensaluti.html'
}
window.addEventListener('load', function(){
  r.vidpunkto(window.localStorage.getItem('seanco')).get().then(function(vidpunkto){
    if(!vidpunkto){window.location = 'ensaluti.html'}
    else{
      x = vidpunkto['x']
      y = vidpunkto['y']
      window.localStorage.setItem('x', x)
      window.localStorage.setItem('y', y)
      r.mapo(window.localStorage.getItem('seanco')+'/'+x+'/'+y).get().then(function(m){
        xs = x
        ys = y
        mm = m
        mapi(m)
      })
    }
  })
})

function iru(){
  //xp: provizora x
  var xp = document.getElementById('x').value
  var yp = document.getElementById('y').value
  if(xp && yp){
  r.mapo(window.localStorage.getItem('seanco')+'/'+xp+'/'+yp).get().then(function(m){
    xs = xp
    ys = yp
    x = xp
    y = yp
    window.localStorage.setItem('x', x)
    window.localStorage.setItem('y', y)
    mm = m
    mapi(m)
  })
}
}


supru.addEventListener('click', function(){
  x = window.localStorage.getItem('x')
  y = window.localStorage.getItem('y')
  if(Math.abs(+x-xs) > 3 || Math.abs(+y-ys) > 3){
    r.mapo(window.localStorage.getItem('seanco')+'/'+x+'/'+(+y-1).toString()).get().then(function(m){
      y = +y-1
      window.localStorage.setItem('y', y)
      xs = x
      ys = y
      mm = m
      mapi(m)
    })
  }
  else{
    y = +y-1
    window.localStorage.setItem('y', y)
    mapi(mm)
  }
})
malsupru.addEventListener('click', function(){
  x = window.localStorage.getItem('x')
  y = window.localStorage.getItem('y')
  if(Math.abs(+x-xs) > 3 || Math.abs(+y-ys) > 3){
    r.mapo(window.localStorage.getItem('seanco')+'/'+x+'/'+(+y+1).toString()).get().then(function(m){
      y = +y+1
      window.localStorage.setItem('y', y)
      xs = x
      ys = y
      mm = m
      mapi(m)
    })
  }
  else{
    y = +y+1
    window.localStorage.setItem('y', y)
    mapi(mm)
  }
})

dekstru.addEventListener('click', function(){
  x = window.localStorage.getItem('x')
  y = window.localStorage.getItem('y')
  if(Math.abs(+x-xs) > 3 || Math.abs(+y-ys) > 3){
    r.mapo(window.localStorage.getItem('seanco')+'/'+(+x+1).toString()+'/'+y).get().then(function(m){
      x = +x+1
      window.localStorage.setItem('x', x)
      xs = x
      ys = y
      mm = m
      mapi(m)
    })
  }
  else{
    x = +x+1
    window.localStorage.setItem('x', x)
    mapi(mm)
  }
})

maldekstru.addEventListener('click', function(){
  x = window.localStorage.getItem('x')
  y = window.localStorage.getItem('y')
  if(Math.abs(+x-xs) > 3 || Math.abs(+y-ys) > 3){
    r.mapo(window.localStorage.getItem('seanco')+'/'+(+x-1).toString()+'/'+y).get().then(function(m){
      x = +x-1
      window.localStorage.setItem('x', x)
      xs = x
      ys = y
      mm = m
      mapi(m)
    })
  }
  else{
    x = +x-1
    window.localStorage.setItem('x', x)
    mapi(mm)
  }
})

function mapi(mapo){
  x = window.localStorage.getItem('x')
  y = window.localStorage.getItem('y')
  var m = document.getElementById('mapo')
  var informoj = document.getElementById('informoj')
  var t = ''
  var nomo, uzanto, koloro, nivelo, minajxo, materialo
  uzanto = mapo['uzanto']
  for (j=+y-2;j<=+y+2;j++){
    t += '<tr>'
    for (i=+x-2;i<=+x+2;i++){
      try{
        nomo = mapo[i+':'+j]['nomo']
      }
      catch(e){
        nomo = 'neniu'
      }
      try{
        nivelo = mapo[i+':'+j]['nivelo']
      }
      catch(e){
        nivelo = ''
      }
      try{
        minajxo = mapo[i+':'+j]['minajxo']
      }
      catch(e){
        minajxo = ''
      }
      try{
        materialo = mapo[i+':'+j]['materialo']
      }
      catch(e){
        materialo = ''
      }
      if(minajxo == 0 || !minajxo || materialo == 'nenia' || !materialo){
        minajxo = '&nbsp;'
      }
      else if(materialo == 'argxento'){
        minajxo = '<div class="argxenta_minajxo">&rlm;'+persa(minajxo.toString())+' بلوک'+'</div>'
      }
      else if(materialo == 'oro'){
        minajxo = '<div class="ora_minajxo">&rlm;'+persa(minajxo.toString())+' بلوک'+'</div>'
      }
      if (nomo == uzanto){
        koloro = 'nigra'
      }
      else if(nomo == 'naturo'){
        koloro = 'natura'
        nomo = 'طبیعت'
      }
      else if(nomo == 'neniu'){
        koloro = 'neniu'
        nomo = '&nbsp;'
      }
      else{
        koloro = 'griza'
      }
      if(nivelo){nivelo = 'سطح ' + persa(nivelo.toString())}else{nivelo = '&nbsp;'}
      t+='<td'+' id="'+i.toString()+'_'+j.toString()+'" class="'+koloro+'" onclick=agi('+i.toString()+','+j.toString()+') >'+nomo+'<br>'+persa(i.toString())+':'+persa(j.toString())+'<br>'+nivelo+'<br>'+minajxo+'</td>'
    }
    t += '</tr>'
  }
  m.innerHTML = t
  informoj.innerHTML = persa(mapo['mono'].toString()) +' بلوک نقره‌ای / روزانه '+ persa(mapo['gajnanto'].toString()) + ' بلوک نقره‌ای / ' + '<a href="javascript:listi_acxeteblojn()">خرید</a>' + '<br>' + persa(mapo['oro'].toString())+' بلوک طلایی / روزانه '+ persa(mapo['orogajnanto'].toString()) + ' بلوک طلایی'+' / <a href="javascript:montri_konverton()">تبدیل</a>'
}
function agi(i, j){
  var ago = window.localStorage.getItem('ago')
  if (!(ago)){
    window.localStorage.setItem('ago', 'konstruado')
    ago = 'konstruado'
  }
  if(ago == 'konstruado'){
    konstrui(i, j)
  }
  else if(ago == 'eksplodado'){
    eksplodi(i, j)
  }
  else if(ago == 'defendado'){
    defendi(i, j)
  }
}
function konstrui(i, j){
  var k = confirm('مطمئنی می‌خوای بسازیش؟')
  if (k){
    r.konstrui(window.localStorage.getItem('seanco')+'/'+i.toString()+'/'+j.toString()).get().then(function(respondo){
      if(respondo['rezulto']){
        montri(respondo['informo']+'<br>'+'با هزینهٔ '+persa(respondo['pagita'].toString())+' بلوک')
      }
      else{
        alert('ساخته نشد!')
      }
      r.mapo(window.localStorage.getItem('seanco')+'/'+x+'/'+y).get().then(function(m){
        xs = x
        ys = y
        mm = m
        mapi(m)
      })
    })
  }
}
function eksplodi(i, j){
  var k = confirm('مطمئنی می‌خوای منفجرش کنی؟')
  if (k){
    r.eksplodi(window.localStorage.getItem('seanco')+'/'+i.toString()+'/'+j.toString()).get().then(function(respondo){
      if(respondo['rezulto']){
        montri(respondo['informo']+'<br>'+'با هزینهٔ '+persa(respondo['pagita'].toString())+' بلوک')
      }
      else{
        alert('منفجر نشد!')
      }
      r.mapo(window.localStorage.getItem('seanco')+'/'+x+'/'+y).get().then(function(m){
        xs = x
        ys = y
        mm = m
        mapi(m)
      })
    })
  }
}