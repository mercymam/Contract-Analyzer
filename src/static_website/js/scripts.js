console.log("Script loaded.");

// Utility to generate a random contract_id
function generateContractId() {
  return Math.floor(1000 + Math.random() * 9000); // 4-digit random number
}

document.getElementById("uploadForm").addEventListener("submit", function(e) {
  e.preventDefault();

  const fileInput = document.getElementById("document");
  const file = fileInput.files[0];

  if (!file) {
    alert("Please select a file before submitting.");
    return;
  }

  // Get sanitized filename (remove extension and non-alphanumerics)
  const sanitizedFileName = file.name
    .replace(/\.[^/.]+$/, "")      // remove extension
    .replace(/[^a-zA-Z0-9]/g, "")  // remove non-alphanumeric
    .toLowerCase();

  // Generate contract_id
  const contractId = `${sanitizedFileName}_${generateContractId()}`;
  console.log("Generated contract_id:", contractId);

  // Store in sessionStorage
  sessionStorage.setItem("currentContractId", contractId);

  const formData = new FormData();
  formData.append("contract", file);
  formData.append("contract_id", contractId);

  fetch("https://httpbin.org/post", {
    method: "POST",
    body: formData
  })
  .then(response => response.json())
  .then(data => {
    console.log("POST response:", data);
    alert(`File uploaded successfully.\nAssigned contract_id: ${contractId}\nChecking status shortly...`);

    // Start GET attempts
    attemptGet(contractId, 1);
  })
  .catch(error => {
    console.error("Error uploading:", error);
    alert("Error uploading the file.");
  });
});

// Function to attempt GET request with retries
function attemptGet(contractId, attemptNumber) {
  console.log(`Attempt ${attemptNumber}: Fetching summary for ${contractId}`);

  // Dummy summary variable
  const dummySummary = "This is a dummy summary of your contract. It contains placeholder text for demonstration.";

  fetch(`https://httpbin.org/get?contract_id=${encodeURIComponent(contractId)}`)
    .then(response => response.json())
    .then(getData => {
      console.log("GET response:", getData);
      // Display dummy summary
      document.getElementById("result").innerText =
        `Summary for contract_id ${contractId}:\n${dummySummary}`;
      alert(`Summary retrieved successfully for contract_id: ${contractId}`);
    })
    .catch(error => {
      console.error(`Error with GET request on attempt ${attemptNumber}:`, error);
      if (attemptNumber < 3) {
        // Retry after 3 seconds
        setTimeout(() => {
          attemptGet(contractId, attemptNumber + 1);
        }, 3000);
      } else {
        // All attempts failed
        document.getElementById("result").innerText =
          `Sorry, we could not retrieve a summary for contract_id ${contractId} after 3 attempts.`;
        alert(`Sorry, we could not retrieve a summary for contract_id: ${contractId} after 3 attempts.`);
      }
    });
}
