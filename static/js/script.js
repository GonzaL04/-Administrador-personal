document.addEventListener('DOMContentLoaded', function() {
    var myModal = document.getElementById('myModal');
    var myInput = document.getElementById('myInput');

    if (myModal) {
        myModal.addEventListener('shown.bs.modal', function() {
            myInput.focus();
        });
    }
});