window.addEventListener('DOMContentLoaded', function () {

    //const backendUrl="https://simpy-backend.herokuapp.com";
    const backendUrl="http://localhost:5000";

    //load shop infos (custoer name, project name) to send later in requests
    if (window.location.href.indexOf("C:/")>=0) {
        localStorage.setItem("window_url", "https://www.go-jasser.com/index.php?fcbid=1f2f5f4s4gd4fg4d6fg4f4dg5d3g4d3f5g4d435g4d3g45/") 
    } else {
        localStorage.setItem("window_url", window.location.hostname) 
    }
    
    $.ajax({
        url: backendUrl+"/shop-info",
        type: "GET",
        data: { url: localStorage.getItem("window_url") },
        dataType: "json",
        contentType: "application/json; charset=utf-8",
        success: function (data) {
            localStorage.setItem("customer_name", data["customer_name"]);
            localStorage.setItem("project_name", data["project_name"]);
            localStorage.setItem("email", data["email"]);
        },
        error: function (e) {
            console.log(e)
        }
    });



    var global;
    var image = document.querySelector('#image');
    var result = document.querySelector('#result');
    var minAspectRatio = 0.5;
    var maxAspectRatio = 1.5;

    $('#modal').on('shown.bs.modal', function () {
        var cropper = new Cropper(image, {

            ready: function () {
                var cropper = this.cropper;
                var containerData = cropper.getContainerData();
                var cropBoxData = cropper.getCropBoxData();
                var aspectRatio = cropBoxData.width / cropBoxData.height;
                var newCropBoxWidth;

                if (aspectRatio < minAspectRatio || aspectRatio > maxAspectRatio) {
                    newCropBoxWidth = cropBoxData.height * ((minAspectRatio + maxAspectRatio) / 2);

                    cropper.setCropBoxData({
                        left: (containerData.width - newCropBoxWidth) / 2,
                        width: newCropBoxWidth
                    });
                }
            },
            cropmove: function () {
                var cropper = this.cropper;
                var cropBoxData = cropper.getCropBoxData();
                var aspectRatio = cropBoxData.width / cropBoxData.height;

                if (aspectRatio < minAspectRatio) {
                    cropper.setCropBoxData({
                        width: cropBoxData.height * minAspectRatio
                    });
                } else if (aspectRatio > maxAspectRatio) {
                    cropper.setCropBoxData({
                        width: cropBoxData.height * maxAspectRatio
                    });
                }
                global = cropper;
            },
            cropend: function () {
                //juste pr tester c à supprimer
                var image = new Image();

                image.src = cropper.getCroppedCanvas().toDataURL('image/jpeg');
                //result.appendChild(image);

            },
        });
    }).on('hidden.bs.modal', function () {
        //console.log("IMAGE TO WORK WITH: " + global.getCroppedCanvas().toDataURL('image/jpeg'));
        $.ajax({
            url: backendUrl+"/search",
            type: "POST",
            data: JSON.stringify({ image: global.getCroppedCanvas().toDataURL('image/jpeg'), customer_name: localStorage.getItem("customer_name") , project_name: localStorage.getItem("project_name") }),
            dataType: "json",
            contentType: "application/json; charset=utf-8",
            success: function (data) {
                $('#resContainer').empty();
                console.log(data.similars)
                $('#modalRes').modal('show');
                if (data.similars.length > 0) {
                    //similars found
                    for (let i in data.similars) {
                        var img = $('<img id="$' + i.toString() + '">');
                        img.css("height", "200px");
                        img.css("width", "auto");
                        img.css("margin", "10px");
                        img.css("cursor", "pointer");
                        img.css("border-radius", "2px");
                        img.attr('src', data.similars[i].image.toString());
                        img.appendTo('#resContainer');
                    }
                } else {
                    //no similars found
                    var img = $('<img src="./img/notfound.png" width="200px">');
                    var label = $('<label> Sorry, no similars found ! </label>');
                    label.css("display", "block");
                    img.appendTo('#resContainer');
                    label.appendTo('#resContainer');
                }
                global = null;
            },
            error: function () {
                $('#resContainer').empty();
                $('#modalRes').modal('show');
                //var img = new Image();
                var img = $('<img src="./img/error.png" width="200px">');
                var label = $('<label> Sorry, something went wrong ! </label>');
                label.css("display", "block");
                img.appendTo('#resContainer');
                label.appendTo('#resContainer');
                global = null;
            }
        });
        global.destroy();
    });


});




function help() {
    console.log("helppppp")
    var p1 = $("<p id='h1'> This is a widget that can be added to any e-commerce website to help merchants by providing \"similar images search of a product\" to their customers in order to increase sales and store efficiency. </p>")
    var p2 = $("<p id='h2'> It is all designed and developed by Jasser Saanoun (saanoun.jasser21@gmail.com). </p>")
    if ($("#h1").length) {
        //nothing
    } else {
        p1.insertBefore('#drop-region')
        p2.insertBefore('#drop-region')
    }
}