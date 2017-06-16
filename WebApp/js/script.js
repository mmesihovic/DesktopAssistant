$('#myModal').on('shown.bs.modal', function () {
  $('#myInput').focus()
})


var promptDelete = function(id) {
    var oke = confirm("Are you sure that you want to delete the reminder?");
    if(oke) {
        window.location= "api/deleteReminder.php?deleteKey="+id;
    }
}