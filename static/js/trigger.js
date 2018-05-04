function whatsapp(celular){
  window.open("https://api.whatsapp.com/send?phone=" + celular,"_blank")
}

// function validarMontoPago(){
//   // $('#nuevo_pago').submit();
//   console.log($("input[value='monto']"));
//   console.log($("#monto_maximo").val());
// }

$(document).ready(function() {
  $('#nuevo_pago').on('submit', function(e){

    console.log($("#monto").val());
    console.log($("#monto_maximo").val());

    if (Number($("#monto").val()) > Number($("#monto_maximo").val())) {
      M.toast({html: 'El monto supera el total del grupo inscrito.'})
    } else {
      return;
    }

    e.preventDefault();
  });

  $('#forma_grupo').on('submit', function(e){


    var inicio = new Date($("#id_fecha_inicio").val());
    var fin = new Date($("#id_fecha_fin").val());

    if (inicio > fin) {
      M.toast({html: 'La fecha de fin es antes que la de inicio.'})
    } else {
      return;
    }

    e.preventDefault();
  });
});
