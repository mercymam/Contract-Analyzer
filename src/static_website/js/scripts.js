console.log("Script loaded.");

// Handle the form POST request
document.getElementById("uploadForm").addEventListener("submit", function(e) {
  e.preventDefault();

  const fileInput = document.getElementById("document");
  const file = fileInput.files[0];

  if (!file) {
    alert("Please select a file before submitting.");
    return;
  }

  const formData = new FormData();
  formData.append("contract", file);

  fetch("https://httpbin.org/post", {
    method: "POST",
    body: formData
  })
  .then(response => response.json())
  .then(data => {
    console.log("POST response:", data);
    alert("File uploaded successfully (test). Now checking status in 3 seconds...");

    // Wait 3 seconds then do GET request
    setTimeout(() => {
      fetch("https://httpbin.org/get")
        .then(response => response.json())
        .then(getData => {
          console.log("GET response:", getData);
          alert("GET request completed. Check console for details.");
        })
        .catch(error => {
          console.error("Error with GET request:", error);
          alert("Error making GET request.");
        });
    }, 3000);

  })
  .catch(error => {
    console.error("Error uploading:", error);
    alert("Error uploading the file.");
  });
});
