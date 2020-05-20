function indexNow() {
    Spinner();
    Spinner.show();
    $("#indexButton").prop('disabled', true);
    $.ajax({
        url: "http://localhost:5000/index",
        type: "POST",
        success: function (data) {
            Spinner.hide();
            $("#indexButton").prop('disabled', false);
            alert(data)
        },
        error: function () {
            alert("error");
        }
    });
}