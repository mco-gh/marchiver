// Popup script for Marchiver extension

// Function to update a result element
function updateResult(elementId, message, isSuccess = true) {
  const resultElement = document.getElementById(elementId);
  resultElement.textContent = message;
  resultElement.className = isSuccess ? 'result success' : 'result error';
}

// Function to format a response for display
function formatResponse(response) {
  return JSON.stringify(response, null, 2);
}

// Set up ping button
document.getElementById('pingBtn').addEventListener('click', function() {
  updateResult('pingResult', 'Checking extension status...');
  
  chrome.runtime.sendMessage({ action: 'ping' }, function(response) {
    if (chrome.runtime.lastError) {
      updateResult('pingResult', 'Error: ' + chrome.runtime.lastError.message, false);
      return;
    }
    
    if (response && response.success) {
      updateResult('pingResult', 'Extension is active and working properly.\n\nResponse: ' + formatResponse(response));
    } else {
      updateResult('pingResult', 'Extension responded but with an error.\n\nResponse: ' + formatResponse(response), false);
    }
  });
});

// Set up save button
document.getElementById('saveBtn').addEventListener('click', function() {
  updateResult('actionResult', 'Saving current page...');
  
  // Get the active tab
  chrome.tabs.query({ active: true, currentWindow: true }, function(tabs) {
    if (!tabs || tabs.length === 0) {
      updateResult('actionResult', 'Error: No active tab found', false);
      return;
    }
    
    const activeTab = tabs[0];
    
    // Send a message to the background script
    chrome.runtime.sendMessage(
      { action: 'savePage', url: activeTab.url, summarize: false },
      function(response) {
        if (chrome.runtime.lastError) {
          updateResult('actionResult', 'Error: ' + chrome.runtime.lastError.message, false);
          return;
        }
        
        if (response && response.success) {
          updateResult('actionResult', 'Page saved successfully.\n\nResponse: ' + formatResponse(response));
        } else {
          updateResult('actionResult', 'Error saving page.\n\nResponse: ' + formatResponse(response), false);
        }
      }
    );
  });
});

// Set up summarize button
document.getElementById('summarizeBtn').addEventListener('click', function() {
  updateResult('actionResult', 'Summarizing current page...');
  
  // Get the active tab
  chrome.tabs.query({ active: true, currentWindow: true }, function(tabs) {
    if (!tabs || tabs.length === 0) {
      updateResult('actionResult', 'Error: No active tab found', false);
      return;
    }
    
    const activeTab = tabs[0];
    
    // Send a message to the background script
    chrome.runtime.sendMessage(
      { action: 'summarizePage', url: activeTab.url },
      function(response) {
        if (chrome.runtime.lastError) {
          updateResult('actionResult', 'Error: ' + chrome.runtime.lastError.message, false);
          return;
        }
        
        if (response && response.success) {
          updateResult('actionResult', 'Page summarized successfully.\n\nResponse: ' + formatResponse(response));
        } else {
          updateResult('actionResult', 'Error summarizing page.\n\nResponse: ' + formatResponse(response), false);
        }
      }
    );
  });
});

// Set up check API button
document.getElementById('checkApiBtn').addEventListener('click', function() {
  updateResult('apiResult', 'Checking API connection...');
  
  chrome.runtime.sendMessage({ action: 'getApiEndpoint' }, function(response) {
    if (chrome.runtime.lastError) {
      updateResult('apiResult', 'Error: ' + chrome.runtime.lastError.message, false);
      return;
    }
    
    if (!response || !response.success || !response.apiEndpoint) {
      updateResult('apiResult', 'Error getting API endpoint.\n\nResponse: ' + formatResponse(response), false);
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
        updateResult('apiResult', 'API connection successful.\n\nEndpoint: ' + response.apiEndpoint + '\n\nResponse: ' + formatResponse(data));
      })
      .catch(error => {
        updateResult('apiResult', 'Error connecting to API: ' + error.message + '\n\nEndpoint: ' + response.apiEndpoint, false);
      });
  });
});

// Initialize
document.addEventListener('DOMContentLoaded', function() {
  // Clear result areas
  document.getElementById('pingResult').textContent = '';
  document.getElementById('actionResult').textContent = '';
  document.getElementById('apiResult').textContent = '';
  
  // Set version info
  const manifest = chrome.runtime.getManifest();
  document.getElementById('versionInfo').textContent = 'v' + manifest.version;
});
