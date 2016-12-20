var r = new RestClient('http://127.0.0.1:8080', {contentType: 'json'});
r.res('ensaluti')
function ensaluti(){
  var nomo = document.getElementById("nomo").value
  var pasvorto = document.getElementById("pasvorto").value
  r.ensaluti(nomo+"/"+pasvorto).get().then(function(k){
    if(!k){
      alert("نام‌کاربری و گذرواژه مطابق نیستند!")
    }
    else{
      window.localStorage.setItem('seanco', k['seanco'])
      window.localStorage.setItem('x', k['x'])
      window.localStorage.setItem('y', k['y'])
      window.location = 'ludo.html'
      }
  })
}