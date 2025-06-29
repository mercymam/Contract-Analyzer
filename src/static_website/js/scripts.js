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

  // Step 1: GET the upload URL
  fetch(presignedUrl)
    .then(response => response.json())
    .then(data => {
      console.log("GET presigned endpoint response:", data);

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
      attemptGet(contractId, 1, Date.now());
    })
    .catch(error => {
      console.error("Error during upload flow:", error);
      alert("Error uploading the file.");
    });
});

// Retry GET function with 5 min max duration
function attemptGet(contractId, attemptNumber, startTime) {
  if (!startTime) {
    startTime = Date.now();
  }

  console.log(`Attempt ${attemptNumber}: Fetching status for ${contractId}`);

  const statusUrl = `https://7ts7q7vvig.execute-api.eu-north-1.amazonaws.com/dev/status/${encodeURIComponent(contractId)}`;

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
      //console.log("GET response JSON:", getData);

      if (getData.statusCode === 404) {
        const elapsed = Date.now() - startTime;
        if (elapsed > 300000) { // 5 minutes
          alert(`File too large or processing failed after 5 minutes.`);
          displaySummary("File too large or no summary available.");
        } else {
          console.log(`Status 404. Retrying in 60 seconds (elapsed: ${Math.round(elapsed / 1000)} sec)...`);
          setTimeout(() => attemptGet(contractId, attemptNumber + 1, startTime), 60000);
        }
      } else {
        // Display successful result
        displaySummary(JSON.stringify(getData, null, 2));
        alert(`Response retrieved successfully for contract_id: ${contractId}`);
      }
    })
    .catch(error => {
      console.error(`Error with GET request on attempt ${attemptNumber}:`, error);

      const elapsed = Date.now() - startTime;
      if (elapsed > 300000) { // 5 minutes
        alert(`File too large or processing failed after 5 minutes.`);
        displaySummary("File too large or no summary available.");
      } else {
        console.log(`Retrying after error in 10 seconds (elapsed: ${Math.round(elapsed / 1000)} sec)...`);
        setTimeout(() => attemptGet(contractId, attemptNumber + 1, startTime), 10000);
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
