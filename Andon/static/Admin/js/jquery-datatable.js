$(function () {
    $('.jsDT-view').DataTable({
        dom: 'Brfltip',
        buttons: [
            'copy', 'csv', 'excel', 'pdf', 'print'
        ],
		responsive: true
    });
});