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

  // Sanitize filename
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
      //alert(`File uploaded successfully.\nAssigned contract_id: ${contractId}\nChecking status shortly...`);

      //show label
      showLabel();
      // Show and start progress bar
      startProgressBar();

      // Start repeated GET attempts
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
      if (getData.statusCode === 404) {
        const elapsed = Date.now() - startTime;
        if (elapsed > 300000) { // 5 minutes
          completeProgressBar();
          alert(`File too large or processing failed after 5 minutes.`);
          displaySummary("File too large or no summary available.");
        } else {
          console.log(`Status 404. Retrying in 60 seconds...`);
          setTimeout(() => attemptGet(contractId, attemptNumber + 1, startTime), 60000);
        }
      } else {
        completeProgressBar();
        console.log("data", getData)
        displaySummary(JSON.stringify(getData, null, 2));
        //alert(`Response retrieved successfully for contract_id: ${contractId}`);
      }
    })
    .catch(error => {
      console.error(`Error with GET request on attempt ${attemptNumber}:`, error);
      const elapsed = Date.now() - startTime;
      if (elapsed > 300000) {
        completeProgressBar();
        alert(`File too large or processing failed after 5 minutes.`);
        displaySummary("File too large or no summary available.");
      } else {
        console.log(`Retrying after error in 60 seconds...`);
        setTimeout(() => attemptGet(contractId, attemptNumber + 1, startTime), 60000);
      }
    });
}

function showLabel(){
    const labelContainer = document.getElementById("labelContainer");
    // Hide the form
    labelContainer.style.display = "block";

}
// Progress bar simulation logic
let progressInterval;
function startProgressBar() {
  const container = document.getElementById("progressContainer");
  const bar = document.getElementById("progressBar");
  const form = document.getElementById("uploadForm");

  // Hide the form
  form.style.display = "none";

  // Show progress container and reset bar width
  container.style.display = "block";
  bar.style.width = "0%";

  let progress = 0;
  progressInterval = setInterval(() => {
    if (progress < 95) {
      progress += 15;  // Increase by 15% every 8 seconds
      if (progress > 95) progress = 95; // Cap at 95%
      bar.style.width = progress + "%";
    }
  }, 8000);
}

function completeProgressBar() {
  clearInterval(progressInterval);
  const bar = document.getElementById("progressBar");
  const container = document.getElementById("progressContainer");
  const form = document.getElementById("uploadForm");
  const labelContainer = document.getElementById("labelContainer");


  // Fill the progress bar to 100%
  bar.style.width = "100%";

  // Hide the progress bar container
  container.style.display = "none";

  // Hide label container
  labelContainer.style.display = "none";

  // Reset the form inputs before showing
  form.reset();
  
  // Show the upload form again
  form.style.display = "inline-flex";
  
}


// // Display summary text in the page (add a div with id="summary" in your HTML)
// function displaySummary(text) {
//   let summaryDiv = document.getElementById("summary");
//   if (!summaryDiv) {
//     summaryDiv = document.createElement("div");
//     summaryDiv.id = "summary";
//     document.body.appendChild(summaryDiv);
//   }

//   // Convert markdown to HTML and set innerHTML inside a markdown-body div
//   // const htmlContent = `<div class=\"markdown-body\">${text}</div>`;
//   summaryDiv.innerHTML = htmlContent;
// }

function displaySummary(text) {
  let summaryDiv = document.getElementById("summary");
  if (!summaryDiv) {
    summaryDiv = document.createElement("div");
    summaryDiv.id = "summary";
    document.body.appendChild(summaryDiv);
  }

  // Unescape newlines and remove extra quotes if present
  let cleanText = text.replace(/\\n/g, '\n').replace(/^"|"$/g, '');

  // Convert markdown to HTML using marked.js
  const htmlContent = `<div class="markdown-body">${marked.parse(cleanText)}</div>`;
  summaryDiv.innerHTML = htmlContent;
}