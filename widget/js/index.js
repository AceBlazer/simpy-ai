


function indexNow() {

    var customer_name = "";
    var project_name = "";
    var email = "";
    var window_url = "";


    //load shop infos (custoer name, project name) to send later in requests
    if (window.location.href.indexOf("C:/") >= 0) {
        window_url = "https://www.go-jasser.com/index.php?fcbid=1f2f5f4s4gd4fg4d6fg4f4dg5d3g4d3f5g4d435g4d3g45/"
    } else {
        window_url = window.location.href
    }
    $.ajax({
        url: "http://localhost:5000/shop-info",
        type: "GET",
        data: { url: window_url },
        contentType: "application/json; charset=utf-8",
        success: function (data) {
            customer_name = data["customer_name"];
            project_name = data["project_name"];
            email = data["email"];
            //actual work
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
        },
        error: function (e) {
            console.log(e)
        }
    });



}