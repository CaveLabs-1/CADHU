$(document).ready(function() {
    $('.dataTable').DataTable({
      dom: 'Bfrtip',
        buttons: [
            'excel', 'pdf'
        ]
    });
} );

$(document).ready(function(){
    $('.fixed-action-btn').floatingActionButton();
});
