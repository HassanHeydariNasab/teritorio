if(window.location.toString().match(/android/)){
  //var r = new RestClient('http://10.0.2.2:8080', {contentType: 'json'});
  var r = new RestClient('http://blokado-altajceloj.rhcloud.com', {contentType: 'json'});
}
else{
  var r = new RestClient('http://127.0.0.1:8080', {contentType: 'json'});
  //var r = new RestClient('http://blokado-altajceloj.rhcloud.com', {contentType: 'json'});
}

var cl = console.log
var finita = true

r.res('rekomenci')
r.res('tabulo')
r.res('agi')
r.res('rezigni')

var T = document.getElementsByClassName('T')
var informoj = document.getElementById('informoj')
var rekomencu = document.getElementById('rekomencu')
var rezignu = document.getElementById('rezignu')

function reveni(){
  window.location = 'ludo.html'
}

window.addEventListener('load', function(){
  if(finita){
      finita = false
      if(!finita){
        r.tabulo(window.localStorage.getItem('seanco')).get().then(function(k){
          if(!k){
            rezignu.style.display = 'none'
            rekomencu.style.display = ''
          }
          else{
            rezignu.style.display = ''
            rekomencu.style.display = 'none'
            mapi(k)
          }
        })
      }
      setInterval(function(){
        if(!finita){
          r.tabulo(window.localStorage.getItem('seanco')).get().then(function(k){
            if(!k){
              rezignu.style.display = 'none'
              rekomencu.style.display = ''
            }
            else{
              rezignu.style.display = ''
              rekomencu.style.display = 'none'
              mapi(k)
            }
          })
        }
      },3000)
  }
})

function agi(I, i){
  if(!finita){
    r.agi(window.localStorage.getItem('seanco')+'/'+I.toString()+'/'+i.toString()).get().then(function(k){
      if (typeof(k) == 'string'){
        alert(k)
      }
      else{
        mapi(k)
      }
    })
  }
}
function ijIndekso(i, j){
  return i+3*j
}
function mapi(k){
  var mapo = k['Tabulo']
  var uzanto = k['uzanto']
  var vico = k['vico']
  var lastaIndekso = k['lastaIndekso']
  for(i=0;i<T.length;i++){
    T[i.toString()].className = 'T'
  }
  if(k['venkulo'] != 'naturo'){
    informoj.innerHTML = 'شما('+k['uzanto']+') علیه '+k['oponanto']+'<br>'+'نشانهٔ شما: '+k['xo']+' &nbsp; پیروز: '+k['venkulo']
    rezignu.style.display = 'none'
    rekomencu.style.display = ''
  }
  else if(k['venkulo'] == 'naturo'){
    informoj.innerHTML = 'شما('+k['uzanto']+') علیه '+k['oponanto']+'<br>'+'نشانهٔ شما: '+k['xo']+' &nbsp; نوبت: '+vico
    rezignu.style.display = ''
    rekomencu.style.display = 'none'
  }
  if(k['uzantoX'] == 'naturo'){
    informoj.innerHTML = 'در انتظار یک بازیکن دیگر…'
    rezignu.style.display = 'none'
    rekomencu.style.display = 'none'
  }
  /*else if(k['uzantoX'] != 'naturo' && k['venkulo'] == 'naturo'){
    rezignu.style.display = ''
    rekomencu.style.display = ''
  }*/
  var t = ''
  var koloro = 'e'
  for (I=0;I<=8;I++){
    t=''
    for (j=0;j<=2;j++){
      t += '<tr>'
      for (i=0;i<=2;i++){
        if(mapo[I.toString()]['S'] == 'O'){
          T[I.toString()].className = ' T O'
          koloro = 'o'
        }
        else if(mapo[I.toString()]['S'] == 'X'){
          T[I.toString()].className = ' T X'
        }
        t+='<td'+' id="'+i.toString()+'_'+j.toString()+'" class="'+mapo[I.toString()]['t'][ijIndekso(i, j)]+'" onclick=agi('+I.toString()+','+ijIndekso(i, j)+') ></td>'
      }
      t += '</tr>'
    }
    T[I.toString()].innerHTML = t
  }
  if(lastaIndekso == -1 && vico == uzanto){
    for(i=0;i<T.length;i++){
      T[i.toString()].className += ' aktiva'
    }
  }
  else if(lastaIndekso == -1){
    for(i=0;i<T.length;i++){
      T[i.toString()].className += ' aktiva_por_aliulo'
    }
  }
  else if(vico == uzanto){
    T[lastaIndekso.toString()].className += ' aktiva'
  }
  else if(vico != uzanto){
    T[lastaIndekso.toString()].className += ' aktiva_por_aliulo'
  }
  if(k['venkulo'] != 'naturo'){
    for(i=0;i<T.length;i++){
      T[i.toString()].className = T[i.toString()].className.replace('aktiva','').replace('aktiva_por_aliulo','')
    }
  }
  if(k['venkulo'] == k['uzanto']){
  }
  else{
  }
}

function rezigni(){
  r.rezigni(window.localStorage.getItem('seanco')).get().then(function(k){
    cl(k)
    for(i=0;i<T.length;i++){
      T[i.toString()].className = T[i.toString()].className.replace('aktiva','').replace('aktiva_por_aliulo','')
    }
    informoj.innerHTML = 'شما('+k['uzanto']+') علیه '+k['oponanto']+'<br>'+'نشانهٔ شما: '+k['xo']+' &nbsp; پیروز: '+k['venkulo']
  })
  //finita = true
  //rezignu.style.display = 'none'
  //rekomencu.style.display = ''
}
function rekomenci(){
  r.rekomenci(window.localStorage.getItem('seanco')).get().then(function(){
    finita = false
    informoj.innerHTML = 'در انتظار یک بازیکن دیگر…'
    rezignu.style.display = 'none'
    rekomencu.style.display = 'none'
  })
}
