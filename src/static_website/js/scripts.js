console.log("Script loaded.");

// Utility to generate a random contract_id
function generateContractId() {
  return 'contract_' + Date.now() + '_' + Math.floor(Math.random() * 10000);
}

document.getElementById("uploadForm").addEventListener("submit", function(e) {
  e.preventDefault();

  const fileInput = document.getElementById("document");
  const file = fileInput.files[0];

  if (!file) {
    alert("Please select a file before submitting.");
    return;
  }

  // Generate a unique contract_id
  const contractId = generateContractId();
  console.log("Generated contract_id:", contractId);

  // Store the ID in sessionStorage
  sessionStorage.setItem("currentContractId", contractId);

  const formData = new FormData();
  formData.append("contract", file);
  formData.append("contract_id", contractId); // Use contract_id in POST

  fetch("https://httpbin.org/post", {
    method: "POST",
    body: formData
  })
  .then(response => response.json())
  .then(data => {
    console.log("POST response:", data);
    alert(`File uploaded successfully.\nAssigned contract_id: ${contractId}\nChecking status in 3 seconds...`);

    // Wait 3 seconds then do GET request
    setTimeout(() => {
      const storedId = sessionStorage.getItem("currentContractId");

      fetch(`https://httpbin.org/get?contract_id=${encodeURIComponent(storedId)}`)
        .then(response => response.json())
        .then(getData => {
          console.log("GET response:", getData);
          alert(`GET request completed for contract_id: ${storedId}\nCheck console for details.`);
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
