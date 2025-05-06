// Popup script for Marchiver extension

// Function to format a response for display
function formatResponse(response) {
  return JSON.stringify(response, null, 2);
}

// Function to update a status indicator
function updateStatusIndicator(elementId, isSuccess) {
  const indicator = document.getElementById(elementId);
  indicator.innerHTML = isSuccess ? '✓' : '✗';
  indicator.className = isSuccess ? 'status-indicator check' : 'status-indicator cross';
}

// Function to show a loading spinner with optional message
function showSpinner(elementId, message = null) {
  const indicator = document.getElementById(elementId);
  indicator.innerHTML = '';
  const spinner = document.createElement('div');
  spinner.className = 'spinner';
  indicator.appendChild(spinner);
  
  // If a message is provided and it's the summarize indicator, update the result area
  if (message && elementId === 'summarizeIndicator') {
    document.getElementById('summaryResult').textContent = message;
  }
}

// Function to hide a spinner
function hideSpinner(elementId) {
  const indicator = document.getElementById(elementId);
  indicator.innerHTML = '';
}

// Function to display a summary in a user-friendly way
function displaySummary(response) {
  const resultElement = document.getElementById('summaryResult');
  
  // Clear previous content
  resultElement.innerHTML = '';
  resultElement.className = 'result success';
  
  if (response && response.document && response.document.summary) {
    // Create title element
    const titleElement = document.createElement('div');
    titleElement.className = 'summary-title';
    titleElement.textContent = response.document.title || 'Summary';
    resultElement.appendChild(titleElement);
    
    // Create summary content element
    const summaryElement = document.createElement('div');
    summaryElement.className = 'summary-content';
    summaryElement.textContent = response.document.summary;
    resultElement.appendChild(summaryElement);
    
    // Add metadata if available
    if (response.document.url) {
      const urlElement = document.createElement('div');
      urlElement.className = 'summary-url';
      urlElement.innerHTML = `<strong>Source:</strong> <a href="${response.document.url}" target="_blank">${response.document.url}</a>`;
      resultElement.appendChild(urlElement);
    }
    
    // Add document ID
    if (response.document.id) {
      const idElement = document.createElement('div');
      idElement.className = 'summary-id';
      idElement.innerHTML = `<strong>Document ID:</strong> ${response.document.id}`;
      resultElement.appendChild(idElement);
    }
  } else {
    // No summary available
    resultElement.textContent = 'No summary available in the response.';
  }
}

// Set up ping button
document.getElementById('pingBtn').addEventListener('click', function() {
  // Show loading spinner
  showSpinner('pingIndicator');
  
  chrome.runtime.sendMessage({ action: 'ping' }, function(response) {
    if (chrome.runtime.lastError) {
      updateStatusIndicator('pingIndicator', false);
      return;
    }
    
    updateStatusIndicator('pingIndicator', response && response.success);
  });
});

// Set up save button
document.getElementById('saveBtn').addEventListener('click', function() {
  // Show loading spinner with message
  showSpinner('saveIndicator');
  
  // Get the active tab
  chrome.tabs.query({ active: true, currentWindow: true }, function(tabs) {
    if (!tabs || tabs.length === 0) {
      updateStatusIndicator('saveIndicator', false);
      return;
    }
    
    const activeTab = tabs[0];
    
    // Update button text to show progress
    const saveBtn = document.getElementById('saveBtn');
    const originalText = saveBtn.textContent;
    saveBtn.textContent = 'Saving...';
    saveBtn.disabled = true;
    
    // Set a timeout to show additional feedback if it's taking a while
    const slowOperationTimeout = setTimeout(() => {
      saveBtn.textContent = 'Still saving (API calls in progress)...';
    }, 3000);
    
    // Send a message to the background script
    chrome.runtime.sendMessage(
      { action: 'savePage', url: activeTab.url, summarize: true },
      function(response) {
        // Clear the timeout
        clearTimeout(slowOperationTimeout);
        
        // Reset button
        saveBtn.textContent = originalText;
        saveBtn.disabled = false;
        
        if (chrome.runtime.lastError) {
          updateStatusIndicator('saveIndicator', false);
          return;
        }
        
        updateStatusIndicator('saveIndicator', response && response.success);
      }
    );
  });
});

// Set up summarize button
document.getElementById('summarizeBtn').addEventListener('click', function() {
  // Clear previous result and show loading indicators
  showSpinner('summarizeIndicator', 'Summarizing current page...');
  
  // Get the active tab
  chrome.tabs.query({ active: true, currentWindow: true }, function(tabs) {
    if (!tabs || tabs.length === 0) {
      document.getElementById('summaryResult').textContent = 'Error: No active tab found';
      document.getElementById('summaryResult').className = 'result error';
      updateStatusIndicator('summarizeIndicator', false);
      return;
    }
    
    const activeTab = tabs[0];
    
    // Update button text to show progress
    const summarizeBtn = document.getElementById('summarizeBtn');
    const originalText = summarizeBtn.textContent;
    summarizeBtn.textContent = 'Summarizing...';
    summarizeBtn.disabled = true;
    
    // Set a timeout to update the message if it's taking a while
    const slowOperationTimeout = setTimeout(() => {
      document.getElementById('summaryResult').textContent = 'Still summarizing... This may take a moment as we process the page content and generate a summary using AI.';
    }, 3000);
    
    // Send a message to the background script
    chrome.runtime.sendMessage(
      { action: 'summarizePage', url: activeTab.url },
      function(response) {
        // Clear the timeout
        clearTimeout(slowOperationTimeout);
        
        // Reset button
        summarizeBtn.textContent = originalText;
        summarizeBtn.disabled = false;
        
        if (chrome.runtime.lastError) {
          document.getElementById('summaryResult').textContent = 'Error: ' + chrome.runtime.lastError.message;
          document.getElementById('summaryResult').className = 'result error';
          updateStatusIndicator('summarizeIndicator', false);
          return;
        }
        
        if (response && response.success) {
          // Display the summary in a user-friendly way
          displaySummary(response);
          updateStatusIndicator('summarizeIndicator', true);
        } else {
          document.getElementById('summaryResult').textContent = 'Error summarizing page.';
          document.getElementById('summaryResult').className = 'result error';
          updateStatusIndicator('summarizeIndicator', false);
        }
      }
    );
  });
});

// Set up check API button
document.getElementById('checkApiBtn').addEventListener('click', function() {
  // Show loading spinner
  showSpinner('apiIndicator');
  
  chrome.runtime.sendMessage({ action: 'getApiEndpoint' }, function(response) {
    if (chrome.runtime.lastError) {
      updateStatusIndicator('apiIndicator', false);
      return;
    }
    
    if (!response || !response.success || !response.apiEndpoint) {
      updateStatusIndicator('apiIndicator', false);
      return;
    }
    
    const apiUrl = response.apiEndpoint + '/health';
    
    // Make a fetch request to the API
    fetch(apiUrl)
      .then(response => {
        if (!response.ok) {
          throw new Error('API returned status ' + response.status);
        }
        return response.json();
      })
      .then(data => {
        updateStatusIndicator('apiIndicator', true);
      })
      .catch(error => {
        updateStatusIndicator('apiIndicator', false);
      });
  });
});

// Initialize
document.addEventListener('DOMContentLoaded', function() {
  // Clear result areas
  document.getElementById('summaryResult').textContent = '';
  document.getElementById('pingIndicator').innerHTML = '';
  document.getElementById('apiIndicator').innerHTML = '';
  document.getElementById('saveIndicator').innerHTML = '';
  document.getElementById('summarizeIndicator').innerHTML = '';
  
  // Set version info
  const manifest = chrome.runtime.getManifest();
  document.getElementById('versionInfo').textContent = 'v' + manifest.version;
});
