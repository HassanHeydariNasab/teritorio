var r = new RestClient('http://127.0.0.1:8080', {contentType: 'json'});
//var r = new RestClient('http://blokado-altajceloj.rhcloud.com', {contentType: 'json'});
r.res('subskribi')
function subskribi(){
  var nomo = document.getElementById("nomo").value
  var pasvorto = document.getElementById("pasvorto").value
  var pasvorto2 = document.getElementById("pasvorto2").value
  if(pasvorto != pasvorto2){
    alert('گذرواژهٔ انتخابی را در هر دو بخش یکسان وارد کنید.')
  }
  else{
    r.subskribi(nomo+"/"+pasvorto).get().then(function(k){
      if(!k){
        alert('این نام‌کاربری قبلاً ثبت شده است.')
      }
      else{
        alert('ثبت‌نام شدید! اکنون وارد شوید.')
        window.location = 'ensaluti.html'
      }
    })
  }
}