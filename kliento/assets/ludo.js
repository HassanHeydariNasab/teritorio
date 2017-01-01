//var r = new RestClient('http://127.0.0.1:8080', {contentType: 'json'});
var r = new RestClient('http://blokado-altajceloj.rhcloud.com', {contentType: 'json'});
//var r = new RestClient('http://10.0.2.2:8080', {contentType: 'json'});
r.res('mapo')
r.res('vidpunkto')
r.res('konstrui')
r.res('ordo')

var mm
var cl = console.log
var supru = document.getElementById('supru')
var malsupru = document.getElementById('malsupru')
var dekstru = document.getElementById('dekstru')
var maldekstru = document.getElementById('maldekstru')

function persa(cifero){
  return cifero.replace(/0/g, "۰").replace(/1/g, "۱").replace(/2/g, "۲").replace(/3/g, "۳").replace(/4/g, "۴").replace(/5/g, "۵").replace(/6/g, "۶").replace(/7/g, "۷").replace(/8/g, "۸").replace(/9/g, "۹")
}
function listi_acxeteblojn(){
  var informoj = document.getElementById('informoj')
  var iri = document.getElementById('iri')
  window.localStorage.setItem('inforomoj', informoj.innerHTML)
  iri.style.display = 'none'
  informoj.style.height = 'calc(20vh - 1px)'
  informoj.innerHTML = '<a href="javascript:Android.acxeti_dialogo(\'blokoj100\')">۱۰۰ بلوک</a>&nbsp;/&nbsp;<a href="javascript:Android.acxeti_dialogo(\'blokoj200\')">۲۰۰ بلوک</a>&nbsp;/&nbsp;<a href="javascript:Android.acxeti_dialogo(\'blokoj500\')">۵۰۰ بلوک</a>&nbsp;/&nbsp;<a href="javascript:Android.acxeti_dialogo(\'blokoj1000\')">۱۰۰۰ بلوک</a><br><a href="javascript:mallisti_acxeteblojn()">بازگشت</a>'
}
function mallisti_acxeteblojn(){
  var informoj = document.getElementById('informoj')
  var iri = document.getElementById('iri')
  informoj.innerHTML = window.localStorage.getItem('inforomoj')
  iri.style.display = ''
  informoj.style.height = 'calc(10vh - 1px)'
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

function bloki(mapo, x, y){
  return mapo[x+':'+y]['nomo']
}
function mapi(mapo){
  x = window.localStorage.getItem('x')
  y = window.localStorage.getItem('y')
  var m = document.getElementById('mapo')
  var informoj = document.getElementById('informoj')
  var t = ''
  var nomo, uzanto, koloro, nivelo, minajxo
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
      if(minajxo == 0 || !minajxo){minajxo = '&nbsp;'}else{minajxo = '&rlm;'+persa(minajxo.toString())+' بلوک'}
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
      t+='<td'+' id="'+i.toString()+'_'+j.toString()+'" class="'+koloro+'" onclick=konstrui('+i.toString()+','+j.toString()+') >'+nomo+'<br>'+persa(i.toString())+':'+persa(j.toString())+'<br>'+nivelo+'<br>'+minajxo+'</td>'
    }
    t += '</tr>'
  }
  m.innerHTML = t
  informoj.innerHTML = persa(mapo['mono'].toString()) +' بلوک موجودی / روزانه '+ persa(mapo['gajnanto'].toString()) + ' بلوک / ' + '<a href="javascript:listi_acxeteblojn()">خرید</a>'
}

function konstrui(i, j){
  var k = confirm('مطمئنی می‌خوای بسازیش؟')
  if (k){
    r.konstrui(window.localStorage.getItem('seanco')+'/'+i.toString()+'/'+j.toString()).get().then(function(farita){
      if(farita){
        alert('با موفقیت ساخته شد.')
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