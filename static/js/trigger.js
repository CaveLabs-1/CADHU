$('whatsapp').click( function(e) {
  e.preventDefault();
  https://api.whatsapp.com/send?phone=
  return false;
} );

function whatsapp(celular){
  window.open("https://api.whatsapp.com/send?phone=" + celular,"_blank")
}
