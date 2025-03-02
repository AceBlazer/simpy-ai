window.addEventListener("DOMContentLoaded", function () {
  // const backendUrl = "http://localhost:5000";
  const backendUrl = "https://simpy-ai.onrender.com";

  // Load shop info (customer name, project name) to send later in requests
  try {
    if (
      window.location.href.indexOf("C:/") >= 0 ||
      window.location.href.indexOf("D:/") >= 0
    ) {
      localStorage.setItem(
        "window_url",
        "https://www.go-jasser.com/index.php?fcbid=1f2f5f4s4gd4fg4d6fg4f4dg5d3g4d3f5g4d435g4d3g45/"
      );
    } else {
      localStorage.setItem("window_url", window.location.hostname);
    }
  } catch (e) {
    console.error("LocalStorage is not available:", e);
  }

  $.ajax({
    url: backendUrl + "/shop-info",
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
      console.log(e);
    },
  });

  var global;
  var image = document.querySelector("#image");
  var result = document.querySelector("#result");
  var minAspectRatio = 0.5;
  var maxAspectRatio = 1.5;
  var minCropBoxSize = 100; // Minimum crop box size
  var maxCropBoxSize = 800; // Maximum crop box size

  // Cropper initialization when the modal is shown
  $("#modal")
    .on("shown.bs.modal", function () {
      if (image) {
        var cropper = new Cropper(image, {
          ready: function () {
            var cropper = this.cropper;
            var containerData = cropper.getContainerData();
            var cropBoxData = cropper.getCropBoxData();
            var aspectRatio = cropBoxData.width / cropBoxData.height;
            var newCropBoxWidth;

            if (aspectRatio < minAspectRatio || aspectRatio > maxAspectRatio) {
              newCropBoxWidth =
                cropBoxData.height * ((minAspectRatio + maxAspectRatio) / 2);

              cropper.setCropBoxData({
                left: (containerData.width - newCropBoxWidth) / 2,
                width: newCropBoxWidth,
              });
            }
          },
          cropmove: function () {
            var cropper = this.cropper;
            var cropBoxData = cropper.getCropBoxData();
            var aspectRatio = cropBoxData.width / cropBoxData.height;

            if (aspectRatio < minAspectRatio) {
              cropper.setCropBoxData({
                width: cropBoxData.height * minAspectRatio,
              });
            } else if (aspectRatio > maxAspectRatio) {
              cropper.setCropBoxData({
                width: cropBoxData.height * maxAspectRatio,
              });
            }
            global = cropper;
          },
          cropend: function () {
            var image = new Image();
            image.src = cropper.getCroppedCanvas().toDataURL("image/jpeg");
          },
        });
      } else {
        console.error("Image element is missing!");
      }
    })
    .on("hidden.bs.modal", function () {
      if (global) {
        sendImageToBackend(
          global.getCroppedCanvas().toDataURL("image/jpeg"),
          localStorage.getItem("customer_name"),
          localStorage.getItem("project_name")
        )
          .done(function (data) {
            $("#resContainer").empty();
            console.log(data.similars);
            $("#modalRes").modal("show");
            if (data.similars.length > 0) {
              for (let i in data.similars) {
                var img = $('<img id="$' + i.toString() + '">');
                img.css("height", "200px");
                img.css("width", "auto");
                img.css("margin", "10px");
                img.css("cursor", "pointer");
                img.css("border-radius", "2px");
                img.attr("src", data.similars[i].image.toString());
                img.appendTo("#resContainer");
              }
            } else {
              var img = $('<img src="./img/notfound.png" width="200px">');
              var label = $("<label> Sorry, no similars found! </label>");
              label.css("display", "block");
              img.appendTo("#resContainer");
              label.appendTo("#resContainer");
            }
            global = null;
          })
          .fail(function () {
            $("#resContainer").empty();
            $("#modalRes").modal("show");
            var img = $('<img src="./img/error.png" width="200px">');
            var label = $("<label> Sorry, something went wrong! </label>");
            label.css("display", "block");
            img.appendTo("#resContainer");
            label.appendTo("#resContainer");
            global = null;
          });
        global.destroy();
        global = null; // Explicitly clear global
      }
    });

  // Function to send image to backend
  function sendImageToBackend(croppedImageData, customerName, projectName) {
    return $.ajax({
      url: backendUrl + "/search",
      type: "POST",
      data: JSON.stringify({
        image: croppedImageData,
        customer_name: customerName,
        project_name: projectName,
      }),
      dataType: "json",
      contentType: "application/json; charset=utf-8",
    });
  }

  // Help function
  function help() {
    if (!$("#h1").length && !$("#h2").length) {
      var p1 = $(
        "<p id='h1'> This is a widget that can be added to any e-commerce website... </p>"
      );
      var p2 = $(
        "<p id='h2'> Designed and developed by Jasser Saanoun (saanoun.jasser21@gmail.com). </p>"
      );
      p1.insertBefore("#drop-region");
      p2.insertBefore("#drop-region");
    }
  }
});
