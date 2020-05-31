


function indexNow() {

    const customer_name = localStorage.getItem("customer_name");
    const project_name = localStorage.getItem("project_name");
    const email = localStorage.getItem("email");

    Spinner();
    Spinner.show();
    $("#indexButton").prop('disabled', true);
    if (customer_name != "" && project_name != "" && email != "") {
        $.ajax({
            url: "http://localhost:5000/index",
            type: "POST",
            data: JSON.stringify({ customer_name: customer_name, project_name: project_name, email: email }),
            contentType: "application/json; charset=utf-8",
            success: function (data) {
                Spinner.hide();
                $("#indexButton").prop('disabled', false);
                alert(data)
            },
            error: function (err) {
                console.log(err)
                alert("error");
            }
        });
    } else {
        console.log("empty credentials to send")
    }




}