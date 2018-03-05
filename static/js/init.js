$(document).ready(function() {
    $('.dataTable').DataTable();
    $('.sidenav').sidenav();
    $('.tooltipped').tooltip({delay: 50});
    $('.timepicker').timepicker();
    $('select').select();

    tomorrow = new Date(new Date().getTime() + 24 * 60 * 60 * 1000);

    $('.datepicker').datepicker({
      selectMonths: true, // Creates a dropdown to control month
      selectYears: 15, // Creates a dropdown of 15 years to control year,
      monthsFull: [ 'Enero', 'Febrero', 'Marzo', 'Abril', 'Mayo', 'Junio', 'Julio', 'Agosto', 'Septiembre', 'Octubre', 'Noviembre', 'Diciembre' ],
      monthsShort: [ 'Ene', 'Feb', 'Mar', 'Abr', 'May', 'Jun', 'Jul', 'Ags', 'Sep', 'Oct', 'Nov', 'Dec' ],
      weekdaysFull: [ 'Domingo', 'Lunes', 'Martes', 'Miércoles', 'Jueves', 'Viernes', 'Sábado' ],
      weekdaysShort: [ 'Domingo', 'Lunes', 'Martes', 'Miércoles', 'Jueves', 'Viernes', 'Sábado' ],
      weekdaysLetter: [ 'D', 'L', 'M', 'M', 'J', 'V', 'S' ],
      today: 'Hoy',
      clear: 'Cerrar',
      close: 'Ok',
      format: 'dd/mm/yyyy',
      formatSubmit: 'dd/mm/yyyy',
      min: tomorrow,
      closeOnSelect: false // Close upon selecting a date,
    });

    console.log('hola');


} );
