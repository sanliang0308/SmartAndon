$(function () {
    var table = $('.jsDT-view').DataTable({
        dom: 'Brfltip',
        buttons: [
            'copy', 'csv', 'excel', 'pdf', 'print'
        ],
		responsive: true
    });
    $('#startDate, #endDate').change(function() {
        table.draw();
    } );
});