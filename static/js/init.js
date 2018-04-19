$(document).ready(function() {
  $('.dataTable').DataTable( {
      dom: "<'row no-margin'<'col s4'l><'col s4 center'B><'col s4'f>>" +
            "<'row'<'col s12'tr>>" +
            "<'row'<'col s6'i><'col s6'p>>",
      "lengthMenu": [[25, 50, 100, 500, 1000], [25, 50, 100, 500, 1000]],
      columnDefs: [ {
            targets: [ 0 ],
            orderData: [ 0, 1 ]
        }, {
            targets: [ 1 ],
            orderData: [ 1, 0 ]
        }, {
            targets: [ 4 ],
            orderData: [ 4, 0 ]
        } ],
      buttons: [
          {
              extend: 'excel',
              exportOptions: {
                  columns: ':visible'
              }
          },
          'colvis'
      ],
      columnDefs: [ {
          visible: false
      } ]
  } );

  $('.dataTableX').DataTable( {
      dom: "<'row'<'col s4'l><'col s4 center'B><'col s4'f>>" +
            "<'row'<'col s12'tr>>" +
            "<'row'<'col s6'i><'col s6'p>>",
      "scrollX": true,
      "lengthMenu": [[25, 50, 100, 500, 1000], [25, 50, 100, 500, 1000]],
      columnDefs: [ {
            targets: [ 0 ],
            orderData: [ 0, 1 ]
        }, {
            targets: [ 1 ],
            orderData: [ 1, 0 ]
        }, {
            targets: [ 4 ],
            orderData: [ 4, 0 ]
        } ],
      buttons: [
          {
              extend: 'excel',
              exportOptions: {
                  columns: ':visible'
              }
          },
          'colvis'
      ],
      columnDefs: [ {
          visible: false
      } ]
  } );

    $('.fixed-action-btn').floatingActionButton();

    //inicializa tabs
    $('.tabs').tabs();

    $('.sidenav').sidenav();
    // $(".button-collapse").sideNav();
    $('.tooltipped').tooltip({delay: 50});
    // $('.timepicker').timepicker();
    $('select').select();
    $('.modal').modal();
    $('.collapsible').collapsible();

    $('.datepicker').datepicker({
        format: 'yyyy-mm-dd',
        i18n: {
            today: 'Hoy',
            clear: 'Borrar',
            done: 'Ok',
            previousMonth: '‹',
            nextMonth: '›',
            months: ['Enero', 'Febrero', 'Marzo', 'Abril', 'Mayo', 'Junio', 'Julio', 'Agosto', 'Septiembre', 'Octubre', 'Noviembre', 'Diciembre'],
            monthsShort: [ 'Ene', 'Feb', 'Mar', 'Abr', 'May', 'Jun', 'Jul', 'Ago', 'Sep', 'Oct', 'Nov', 'Dic'],
            weekdays: [ 'Lunes', 'Martes', 'Miércoles', 'Jueves', 'Viernes', 'Sábado',  'Domingo' ],
            weekdaysShort: [ 'Lun', 'Mar', 'Mie', 'Jue', 'Vie', 'Sab', 'Dom' ],
            weekdaysAbbrev: [ 'L', 'M', 'Mi', 'J', 'V', 'S', 'D' ]
        }
    });
    $('.timepicker').timepicker({
        defaultTime: 'now',
        twelveHour: true,
        i18n: {
            clear: 'Borrar',
            cancel: 'Cancelar',
            done: 'Ok',
        }
    });
});


$('#sidenavBtn').on('click', function(){
  console.log("asd");
});
