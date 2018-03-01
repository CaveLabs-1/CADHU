$(document).ready(function() {
    $('.dataTable').DataTable({
      dom: 'Bfrtip',
        buttons: [
            'excel', 'pdf'
        ]
    });
} );
