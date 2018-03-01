$(document).ready(function() {
    $('.dataTable').DataTable();
    $('.modal').modal();
    $('.datepicker').datepicker({
        format: 'yyyy-mm-dd',
        i18n: {
            today: 'Hoy',
            clear: 'Borrar',
            done: 'Ok',
            previousMonth: '‹',
            nextMonth: '›',
            months: [
                'Enero',
                'Febrero',
                'Marzo',
                'Abril',
                'Mayo',
                'Junio',
                'Julio',
                'Agosto',
                'Septiembre',
                'Octubre',
                'Noviembre',
                'Diciembre'
            ],
            monthsShort: [
                'Ene',
                'Feb',
                'Mar',
                'Abr',
                'May',
                'Jun',
                'Jul',
                'Ago',
                'Sep',
                'Oct',
                'Nov',
                'Dic'
            ],
            weekdays: [
                'Domingo',
                'Lunes',
                'Martes',
                'Miércoles',
                'Jueves',
                'Viernes',
                'Sábado'
            ],
            weekdaysShort: [
                'Dom',
                'Lun',
                'Mar',
                'Mie',
                'Jue',
                'Vie',
                'Sab'
            ],
            weekdaysAbbrev: ['D', 'L', 'M', 'Mi', 'J', 'V', 'S']
        }
    });
    $('.timepicker').timepicker({
        defaultTime: 'now',
        twelveHour: false,
        format: 'hh:mm:ss ',
        i18n: {
            clear: 'Borrar',
            cancel: 'Cancelar',
            done: 'Ok',
        }
    });
});

