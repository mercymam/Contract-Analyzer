console.log("Script loaded.");

// Utility to generate a random 4-digit contract_id suffix
function generateContractId() {
  return Math.floor(1000 + Math.random() * 9000);
}

document.getElementById("uploadForm").addEventListener("submit", function(e) {
  e.preventDefault();

  const fileInput = document.getElementById("document");
  const file = fileInput.files[0];

  if (!file) {
    alert("Please select a file before submitting.");
    return;
  }

  // Sanitize filename (remove extension and non-alphanumerics, lowercase)
  const sanitizedFileName = file.name
    .replace(/\.[^/.]+$/, "")
    .replace(/[^a-zA-Z0-9]/g, "")
    .toLowerCase();

  const contractId = `${sanitizedFileName}_${generateContractId()}.pdf`;
  console.log("Generated contract_id:", contractId);
  const presignedUrl = `https://7ts7q7vvig.execute-api.eu-north-1.amazonaws.com/dev/generate-presigned-url/${encodeURIComponent(contractId)}`;

  sessionStorage.setItem("currentContractId", contractId);

  // Step 1: GET the upload URL (dummy simulation)
  fetch(presignedUrl)
    .then(response => response.json())
    .then(data => {
      console.log("GET presigned endpoint response:", data);

      // Step 2: PUT the file and contract_id to the presigned URL
      const presignedUrl = data;


       // Step 2: PUT the raw PDF file to the presigned URL
      return fetch(presignedUrl, {
        method: "PUT",
        headers: {
          "Content-Type": "application/pdf"
        },
        body: file
      });
    })
    .then(response => {
      if (!response.ok) {
        throw new Error(`Upload failed with status ${response.status}`);
      }

      console.log("PUT upload successful.");
      alert(`File uploaded successfully.\nAssigned contract_id: ${contractId}\nChecking status shortly...`);

      // Step 3: Start repeated GET attempts to fetch results
      attemptGet(contractId, 1);
    })
    .catch(error => {
      console.error("Error during upload flow:", error);
      alert("Error uploading the file.");
    });
});

// Retry GET function
function attemptGet(contractId, attemptNumber) {
  console.log(`Attempt ${attemptNumber}: Fetching status for ${contractId}`);

  const fileName = 8962;
  const statusUrl = `https://7ts7q7vvig.execute-api.eu-north-1.amazonaws.com/dev/status/${encodeURIComponent(fileName)}`;

  fetch(statusUrl)
    .then(response => {
      console.log(`HTTP status code: ${response.status}`);

      if (response.status === 200) {
        return response.json();
      } else {
        throw new Error(`Server returned status ${response.status}`);
      }
    })
    .then(getData => {
      console.log("GET response JSON:", getData);

      // Display the entire JSON as a string
      displaySummary(JSON.stringify(getData, null, 2));

      alert(`Response retrieved successfully for contract_id: ${contractId}`);
    })
    .catch(error => {
      console.error(`Error with GET request on attempt ${attemptNumber}:`, error);
      if (attemptNumber < 3) {
        setTimeout(() => attemptGet(contractId, attemptNumber + 1), 3000);
      } else {
        alert(`Sorry, no summary available for contract_id: ${contractId} after 3 attempts.`);
        displaySummary("No summary available.");
      }
    });
}
// Display summary text in the page (add a div with id="summary" in your HTML)
function displaySummary(text) {
  let summaryDiv = document.getElementById("summary");
  if (!summaryDiv) {
    summaryDiv = document.createElement("div");
    summaryDiv.id = "summary";
    summaryDiv.style.marginTop = "20px";
    summaryDiv.style.padding = "10px";
    summaryDiv.style.border = "1px solid #ccc";
    summaryDiv.style.backgroundColor = "#f4f4f4";
    summaryDiv.style.maxWidth = "600px";
    summaryDiv.style.margin = "20px auto";
    document.body.appendChild(summaryDiv);
  }
  summaryDiv.textContent = text;
}
