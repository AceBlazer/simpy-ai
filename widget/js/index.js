


function indexNow() {

    const customer_name = localStorage.getItem("customer_name");
    const project_name = localStorage.getItem("project_name");
    const email = localStorage.getItem("email");

    const backendUrl="https://simpy-backend.herokuapp.com";
    //const backendUrl="http://localhost:5000";

    Spinner();
    Spinner.show();
    $("#indexButton").prop('disabled', true);
    if (customer_name != "" && project_name != "" && email != "") {
        $.ajax({
            url: backendUrl+"/index",
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