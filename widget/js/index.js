async function indexNow() {
  const customer_name = localStorage.getItem("customer_name");
  const project_name = localStorage.getItem("project_name");
  const email = localStorage.getItem("email");

  // const backendUrl = "http://localhost:5000";
  const backendUrl = "https://simpy-ai.onrender.com";

  // Check for missing credentials
  if (!customer_name || !project_name || !email) {
    alert(
      "Missing customer name, project name, or email. Please provide all details."
    );
    return;
  }

  // Show spinner and disable button
  Spinner();
  Spinner.show();
  $("#indexButton").prop("disabled", true);

  try {
    // Make the POST request to backend
    const response = await fetch(`${backendUrl}/index`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        customer_name: customer_name,
        project_name: project_name,
        email: email,
      }),
    });

    // Check for non-200 responses
    if (!response.ok) {
      throw new Error(`Server error: ${response.statusText}`);
    }

    const data = await response.text();

    // Hide spinner and enable button
    Spinner.hide();
    $("#indexButton").prop("disabled", false);

    // Show success message
    alert(data);
  } catch (err) {
    // Handle errors: server issues, network issues, etc.
    console.error("Request failed", err);
    Spinner.hide();
    $("#indexButton").prop("disabled", false);
    alert(`Error: ${err.message || "An unexpected error occurred."}`);
  }
}
