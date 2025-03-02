// DOM elements where files are dropped and previewed
const dropRegion = document.getElementById("drop-region");
const imagePreviewRegion = document.getElementById("image-preview");

// Open file selector when drop region is clicked
const fakeInput = document.createElement("input");
fakeInput.type = "file";
fakeInput.accept = "image/*";
fakeInput.multiple = false;

dropRegion.addEventListener("click", () => fakeInput.click());

fakeInput.addEventListener("change", function () {
  const files = fakeInput.files;
  handleFiles(files);
});

// Prevent default behavior for drag events
function preventDefault(e) {
  e.preventDefault();
  e.stopPropagation();
}

// Attach prevent default listeners for drag events
["dragenter", "dragleave", "dragover", "drop"].forEach((event) => {
  dropRegion.addEventListener(event, preventDefault, false);
});

// Handle image drop
function handleDrop(e) {
  const dt = e.dataTransfer;
  const files = dt.files;

  if (files.length) {
    handleFiles(files);
  } else {
    // Check for image URL if no files were dropped
    const html = dt.getData("text/html");
    const match = html && /\bsrc="?([^"\s]+)"?\s*/.exec(html);
    const url = match && match[1];

    if (url) {
      uploadImageFromURL(url);
    }
  }
}

dropRegion.addEventListener("drop", handleDrop, false);

// Upload image from URL if dragged from external source
function uploadImageFromURL(url) {
  const img = new Image();
  const canvas = document.createElement("canvas");
  const ctx = canvas.getContext("2d");

  img.onload = function () {
    canvas.width = this.naturalWidth;
    canvas.height = this.naturalHeight;
    ctx.drawImage(this, 0, 0);
    canvas.toBlob(function (blob) {
      handleFiles([blob]);
    }, "image/png");
  };

  img.onerror = function () {
    alert("Error in uploading image from URL.");
  };

  img.crossOrigin = ""; // Handle cross-origin images
  img.src = url;
}

// Handle file(s) selected or dropped
function handleFiles(files) {
  const image = files[files.length - 1];

  if (validateImage(image)) {
    previewAndUploadImage(image);
  }
}

// Validate the image file (type and size)
function validateImage(image) {
  const validTypes = ["image/jpeg", "image/png", "image/gif"];
  const maxSizeInBytes = 10e6; // 10MB

  if (!validTypes.includes(image.type)) {
    alert("Invalid File Type. Please upload a JPEG, PNG, or GIF image.");
    return false;
  }

  if (image.size > maxSizeInBytes) {
    alert("File too large. Please upload an image smaller than 10MB.");
    return false;
  }

  return true;
}

// Preview and upload the image after validation
function previewAndUploadImage(image) {
  const imgView = document.createElement("div");
  imgView.className = "image-view";
  imagePreviewRegion.appendChild(imgView);

  const img = document.createElement("img");
  imgView.appendChild(img);

  const overlay = document.createElement("div");
  overlay.className = "overlay";
  imgView.appendChild(overlay);

  const reader = new FileReader();
  reader.onload = function (e) {
    img.src = e.target.result;
  };

  reader.onerror = function () {
    alert("Error reading the image file.");
  };

  reader.readAsDataURL(image);

  document.getElementById("image").src = URL.createObjectURL(image);

  // Hide the upload modal and show the crop modal
  $("#uploadModal").modal("hide");
  $("#modal").modal("show");
}
