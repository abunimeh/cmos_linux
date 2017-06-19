// detect IE and stop IE to use

var nav_ua = navigator.userAgent;
if (nav_ua.indexOf('Trident') > -1) {
  if(!window.location.origin){
      var rdt_url = window.location.protocol + '//' + window.location.host + '/page_error/' ;
  } else {
      var rdt_url = window.location.origin + '/page_error/';
  }
  window.location.href = rdt_url; 
}
