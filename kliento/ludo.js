var r = new RestClient('http://127.0.0.1:8080', {contentType: 'json'});
//var r = new RestClient('http://blokado-altajceloj.rhcloud.com', {contentType: 'json'});
r.res('mapo')
r.res('vidpunkto')
r.res('konstrui')

var mm
var cl = console.log
var supru = document.getElementById('supru')
var malsupru = document.getElementById('malsupru')
var dekstru = document.getElementById('dekstru')
var maldekstru = document.getElementById('maldekstru')

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
  })
})

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
      if (nomo == uzanto){
        koloro = 'nigra'
      }
      else if(nomo == 'naturo'){
        koloro = 'natura'
      }
      else if(nomo == 'neniu'){
        koloro = 'neniu'
      }
      else{
        koloro = 'griza'
      }
      t+='<td'+' id="'+i.toString()+'_'+j.toString()+'" class="'+koloro+'" onclick=konstrui('+i.toString()+','+j.toString()+') >'+nomo+'<br>'+i.toString()+', '+j.toString()+'<br>'+nivelo+'<br>'+minajxo+'</td>'
    }
    t += '</tr>'
  }
  m.innerHTML = t
  informoj.innerHTML = mapo['mono'] +'  '+ mapo['gajnanto']
}

function konstrui(i, j){
  var k = confirm('مطمئنی می‌خوای بسازیش؟')
  if (k){
    r.konstrui(window.localStorage.getItem('seanco')+'/'+i.toString()+'/'+j.toString()).get().then(function(farita){
      alert(farita)
      r.mapo(window.localStorage.getItem('seanco')+'/'+x+'/'+y).get().then(function(m){
        xs = x
        ys = y
        mm = m
        mapi(m)
      })
    })
  }
}