// Get the modal elements
var registerModal = document.getElementById("registerModal");
var loginModal = document.getElementById("loginModal");
var createProjectModal = document.getElementById("createProjectModal");

// Get the buttons to open modals
var openRegisterModalBtn = document.getElementById("openRegisterModalBtn");
var openLoginModalBtn = document.getElementById("openLoginModalBtn");
var openCreateProjectModalBtn = document.getElementById(
  "openCreateProjectModalBtn"
);

// Get the <span> elements to close modals
var closeRegisterModal = document.getElementById("closeRegisterModal");
var closeLoginModal = document.getElementById("closeLoginModal");
var closeCreateProjectModal = document.getElementById(
  "closeCreateProjectModal"
);

// Open modals when buttons are clicked
openRegisterModalBtn.onclick = function () {
  registerModal.style.display = "block";
};
openLoginModalBtn.onclick = function () {
  loginModal.style.display = "block";
};
openCreateProjectModalBtn.onclick = function () {
  createProjectModal.style.display = "block";
};

// Close modals when the close button is clicked
closeRegisterModal.onclick = function () {
  registerModal.style.display = "none";
};
closeLoginModal.onclick = function () {
  loginModal.style.display = "none";
};
closeCreateProjectModal.onclick = function () {
  createProjectModal.style.display = "none";
};

// Close modals when clicking outside of the modal content
window.onclick = function (event) {
  if (event.target === registerModal) {
    registerModal.style.display = "none";
  }
  if (event.target === loginModal) {
    loginModal.style.display = "none";
  }
  if (event.target === createProjectModal) {
    createProjectModal.style.display = "none";
  }
};

// Register User function
function registerUser(event) {
  event.preventDefault();

  var email = document.getElementById("registerEmail").value;
  var password = document.getElementById("registerPassword").value;

  var myHeaders = new Headers();
  myHeaders.append("Content-Type", "application/json");

  var raw = JSON.stringify({
    email: email,
    password: password,
  });

  var requestOptions = {
    method: "POST",
    headers: myHeaders,
    body: raw,
    redirect: "follow",
  };

  fetch("http://localhost:5000/register", requestOptions)
    .then((response) => response.json())
    .then((result) => {
      document.getElementById("registerResponse").innerText =
        "Registration successful!";
      setTimeout(() => (registerModal.style.display = "none"), 2000);
    })
    .catch((error) => {
      document.getElementById("registerResponse").innerText = "Error: " + error;
    });
}

// Login User function
function loginUser(event) {
  event.preventDefault();

  var email = document.getElementById("loginEmail").value;
  var password = document.getElementById("loginPassword").value;

  var myHeaders = new Headers();
  myHeaders.append("Content-Type", "application/json");

  var raw = JSON.stringify({
    email: email,
    password: password,
  });

  var requestOptions = {
    method: "POST",
    headers: myHeaders,
    body: raw,
    redirect: "follow",
  };

  fetch("http://localhost:5000/login", requestOptions)
    .then((response) => response.json())
    .then((result) => {
      document.getElementById("loginResponse").innerText = "Login successful!";
      setTimeout(() => (loginModal.style.display = "none"), 2000);
    })
    .catch((error) => {
      document.getElementById("loginResponse").innerText = "Error: " + error;
    });
}

// Create Project function
function createProject(event) {
  event.preventDefault();

  var name = document.getElementById("projectName").value;
  var url = document.getElementById("projectUrl").value;
  var customerId = document.getElementById("customerId").value;

  var myHeaders = new Headers();
  myHeaders.append("Content-Type", "application/json");

  var raw = JSON.stringify({
    name: name,
    url: url,
    customerId: customerId,
  });

  var requestOptions = {
    method: "POST",
    headers: myHeaders,
    body: raw,
    redirect: "follow",
  };

  fetch("http://localhost:5000/project", requestOptions)
    .then((response) => response.json())
    .then((result) => {
      document.getElementById("createProjectResponse").innerText =
        "Project created successfully!";
      setTimeout(() => (createProjectModal.style.display = "none"), 2000);
    })
    .catch((error) => {
      document.getElementById("createProjectResponse").innerText =
        "Error: " + error;
    });
}
