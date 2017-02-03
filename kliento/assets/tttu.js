var r
if(window.location.toString().match(/android/)){
  //r = new RestClient('http://10.0.2.2:8080', {contentType: 'json'});
  r = new RestClient('http://blokado-altajceloj.rhcloud.com', {contentType: 'json'});
}
else{
  r = new RestClient('http://127.0.0.1:8080', {contentType: 'json'});
  //r = new RestClient('http://blokado-altajceloj.rhcloud.com', {contentType: 'json'});
}

var cl = console.log
var finita = true

r.res('tabuloj')
r.res('rekomenci')
r.res('tabulo')
r.res('agi')
r.res('rezigni')
r.res('nuligi')

var T = document.getElementsByClassName('T')
var informoj = document.getElementById('informoj')
var tempiloj = document.getElementById('tempiloj')
var tu = document.getElementById('tu')
var rekomencu = document.getElementById('rekomencu')
var rezignu = document.getElementById('rezignu')
var nuligu = document.getElementById('nuligu')

rezignu.style.display = 'none'
rekomencu.style.display = 'none'
nuligu.style.display = 'none'

function persa(cifero){
  return cifero.replace(/0/g, "۰").replace(/1/g, "۱").replace(/2/g, "۲").replace(/3/g, "۳").replace(/4/g, "۴").replace(/5/g, "۵").replace(/6/g, "۶").replace(/7/g, "۷").replace(/8/g, "۸").replace(/9/g, "۹")
}

function reveni(){
  window.location = 'ludo.html'
}
function preni_tabulojn(){
  var prenita = false
  r.tabuloj(window.localStorage.getItem('seanco')).get().then(function(k){
    if(!!k){
      //uzanto havas almenaux unu tabulon:
      var tuo = ''
      for(var t in k){
        if(k[t]['venkulo'] == 'naturo'){
          k[t]['venkulo'] = 'هیچ‌کس!'
        }
        if(k[t]['uzantoX'] == 'naturo'){
          k[t]['uzantoX'] = 'هیچ‌کس!'
        }
        if(k[t]['vico'] == 'naturo'){
          k[t]['vico'] = 'هیچ‌کس!'
        }
        tuo += '<option value="'+t+'" >'+persa(t)+' > '+k[t]['uzantoO'] + ' علیه ' + k[t]['uzantoX']+' | نوبت: '+k[t]['vico']+' | پیروز: '+k[t]['venkulo']+'</option>'
      }
      tu.innerHTML = tuo
      var oj = document.getElementsByTagName('option')
      if(!(window.localStorage.getItem('elektita') in k) || window.localStorage.getItem('elektita') == 'undefined'){
        window.localStorage.setItem('elektita', oj[0].value)
      }
      tu.value = window.localStorage.getItem('elektita')
      finita = false
      prenita = true
    }
    else{
      //uzanto ne havas tabulon:
      finita = true
      rezignu.style.display = 'none'
      rekomencu.style.display = ''
      nuligu.style.display = 'none'
      informoj.innerHTML = 'یک بازی جدید شروع کنید.'
      prenita = false
    }
  })
  return prenita
}
r.tabuloj(window.localStorage.getItem('seanco')).get().then(function(k){
  preni_tabulojn()
  if(!finita){
    r.tabulo(window.localStorage.getItem('seanco')+'/'+tu.value).get().then(function(k){
      if(!k){
        rezignu.style.display = 'none'
        rekomencu.style.display = ''
        nuligu.style.display = 'none'
      }
      else{
        rezignu.style.display = ''
        rekomencu.style.display = 'none'
        nuligu.style.display = 'none'
        mapi(k)
      }
    })
  }
  setInterval(function(){
    if(!finita){
      r.tabulo(window.localStorage.getItem('seanco')+'/'+tu.value).get().then(function(k){
        if(!k){
          rezignu.style.display = 'none'
          rekomencu.style.display = ''
          nuligu.style.display = 'none'
        }
        else{
          rezignu.style.display = ''
          rekomencu.style.display = 'none'
          if(k['oponanto'] == 'naturo'){
            nuligu.style.display = ''
          }
          else{
            nuligu.style.display = 'none'
          }
          mapi(k)
        }
      })
    }
  },3000)
})
tu.addEventListener('change', function(){
  window.localStorage.setItem('elektita', tu.value)
})
function agi(I, i){
  if(!finita){
    r.agi(window.localStorage.getItem('seanco')+'/'+tu.value+'/'+I.toString()+'/'+i.toString()).get().then(function(k){
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
  preni_tabulojn()
  var mapo = k['Tabulo']
  var uzanto = k['uzanto']
  var vico = k['vico']
  var lastaIndekso = k['lastaIndekso']
  if(k['venkulo'] == uzanto){
    k['venkulo'] = 'شما'
  }
  k['uzanto'] = 'شما'
  for(i=0;i<T.length;i++){
    T[i.toString()].className = 'T'
  }
  if(k['egalita']){
    finita = true
    informoj.innerHTML = k['uzanto']+' علیه '+k['oponanto']+'<br>'+'نشانهٔ شما: '+k['xo']+' &nbsp; مساوی!'
    rezignu.style.display = 'none'
    rekomencu.style.display = ''
    nuligu.style.display = 'none'
    tempiloj.innerHTML = '&rlm;O: '+persa((300-k['tempilo_uzantoO']).toString())+'s'+' | X: '+persa((300-k['tempilo_uzantoX']).toString())+'s'
  }
  else{
    if(k['venkulo'] != 'naturo'){
      finita = true
      informoj.innerHTML = k['uzanto']+' علیه '+k['oponanto']+'<br>'+'نشانهٔ شما: '+k['xo']+' &nbsp; پیروز: '+k['venkulo']
      rezignu.style.display = 'none'
      rekomencu.style.display = ''
      nuligu.style.display = 'none'
      tempiloj.innerHTML = '&rlm;O: '+persa((300-k['tempilo_uzantoO']).toString())+'s'+' | X: '+persa((300-k['tempilo_uzantoX']).toString())+'s'
    }
    else if(k['venkulo'] == 'naturo'){
      informoj.innerHTML = k['uzanto']+' علیه '+k['oponanto']+'<br>'+'نشانهٔ شما: '+k['xo']+' &nbsp; نوبت: '+vico
      rezignu.style.display = ''
      rekomencu.style.display = 'none'
      if(k['oponanto'] == 'naturo'){
        nuligu.style.display = ''
      }
      else{
        nuligu.style.display = 'none'
      }
      tempiloj.innerHTML = '&rlm;O: '+persa((300-k['tempilo_uzantoO']).toString())+'s'+' | X: '+persa((300-k['tempilo_uzantoX']).toString())+'s'
    }
  }
  if(k['uzantoX'] == 'naturo'){
    informoj.innerHTML = 'در انتظار یک بازیکن دیگر…'
    rezignu.style.display = 'none'
    rekomencu.style.display = 'none'
    nuligu.style.display = ''
    tempiloj.innerHTML = ''
  }
  var t = ''
  for (I=0;I<=8;I++){
    t=''
    for (j=0;j<=2;j++){
      t += '<tr>'
      for (i=0;i<=2;i++){
        if(mapo[I.toString()]['S'] == 'O'){
          T[I.toString()].className = ' T O'
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
    cl(1)
    for(I=0;I<T.length;I++){
      if(mapo[I.toString()]['S'] == 'E'){
        T[I.toString()].className += ' aktiva'
      }
    }
  }
  else if(lastaIndekso == -1){
    cl(2)
    for(I=0;I<T.length;I++){
      if(mapo[I.toString()]['S'] == 'E'){
        T[I.toString()].className += ' aktiva_por_aliulo'
      }
    }
  }
  else if((vico == uzanto) && (mapo[lastaIndekso.toString()]['S'] == 'E')){
    T[lastaIndekso.toString()].className += ' aktiva'
  }
  else if((vico != uzanto) && (mapo[lastaIndekso.toString()]['S'] == 'E')){
    T[lastaIndekso.toString()].className += ' aktiva_por_aliulo'
  }
  if((k['venkulo'] != 'naturo') || mapo['egalita']){
    for(i=0;i<T.length;i++){
      T[i.toString()].className = T[i.toString()].className.replace('aktiva','').replace('aktiva_por_aliulo','')
    }
  }
}

function rezigni(){
  r.rezigni(window.localStorage.getItem('seanco')+'/'+tu.value).get().then(function(k){
    window.localStorage.setItem('elektita', tu.value)
    for(i=0;i<T.length;i++){
      T[i.toString()].className = T[i.toString()].className.replace('aktiva','').replace('aktiva_por_aliulo','')
    }
  })
}

function rekomenci(){
  r.rekomenci(window.localStorage.getItem('seanco')).get().then(function(k){
    if(k['stato']){
      finita = false
      preni_tabulojn()
      informoj.innerHTML = 'در انتظار یک بازیکن دیگر…'
      rezignu.style.display = 'none'
      rekomencu.style.display = 'none'
      nuligu.style.display = ''
      window.localStorage.setItem('elektita', k['id'])
    }
  })
}

function nuligi(){
  r.nuligi(window.localStorage.getItem('seanco')+'/'+tu.value).get().then(function(k){
    if(preni_tabulojn()){
      var oj = document.getElementsByTagName('option')
      window.localStorage.setItem('elektita', oj[0].value)
      for(i=0;i<T.length;i++){
        T[i.toString()].className = T[i.toString()].className.replace('aktiva','').replace('aktiva_por_aliulo','')
      }
    }
    finita = false
  })
}