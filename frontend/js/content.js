// Function to notify the page that the extension is active
function notifyPageExtensionActive() {
  // Dispatch custom event
  document.dispatchEvent(new CustomEvent('marchiver-extension-response'));
  
  // Use window.postMessage as a backup
  window.postMessage({
    type: 'MARCHIVER_EXTENSION_STATUS',
    status: 'active'
  }, window.location.origin);
}

// Main initialization
function init() {
  // Listen for messages from background script
  chrome.runtime.onMessage.addListener((message, sender, sendResponse) => {
    if (message.action === 'getPageContent') {
      const content = getPageContent();
      sendResponse({ success: true, content });
    }
    
    return false; // No async response
  });

  // Add keyboard shortcut listener
  document.addEventListener('keydown', handleKeyDown);
  
  // Add custom event listeners for test page
  setupTestPageEventListeners();
  
  // Send a message to the background script to confirm the extension is working
  chrome.runtime.sendMessage({ action: 'ping' }, function(response) {
    // Notify the page that the extension is active
    notifyPageExtensionActive();
  });
  
  // Set up a periodic notification to ensure the page gets the message
  setTimeout(notifyPageExtensionActive, 500);
}

// Set up event listeners for the test page
function setupTestPageEventListeners() {
  // Listen for ping event to check if extension is active
  document.addEventListener('marchiver-extension-ping', function(event) {
    // Respond to let the test page know the extension is active
    notifyPageExtensionActive();
    
    // Also send a message to the background script
    chrome.runtime.sendMessage({ action: 'ping' });
  });
  
  // Listen for save page event
  document.addEventListener('marchiver-save-page', function(event) {
    const detail = event.detail || {};
    chrome.runtime.sendMessage(
      { action: 'savePage', url: detail.url || window.location.href, summarize: detail.summarize || false },
      (response) => {
        // Send response back to the test page
        window.dispatchEvent(new CustomEvent('marchiver-save-page-response', {
          detail: response || { success: false, error: 'No response from extension' }
        }));
        
        showNotification(response && response.success ? 
          'Page saved to Marchiver' : 
          'Error saving page', 
          !(response && response.success));
      }
    );
  });
  
  // Listen for summarize page event
  document.addEventListener('marchiver-summarize-page', function(event) {
    const detail = event.detail || {};
    chrome.runtime.sendMessage(
      { action: 'summarizePage', url: detail.url || window.location.href },
      (response) => {
        // Send response back to the test page
        window.dispatchEvent(new CustomEvent('marchiver-summarize-page-response', {
          detail: response || { success: false, error: 'No response from extension' }
        }));
        
        showNotification(response && response.success ? 
          'Page summarized and saved to Marchiver' : 
          'Error summarizing page', 
          !(response && response.success));
      }
    );
  });
  
  // Listen for search event
  document.addEventListener('marchiver-search', function(event) {
    const detail = event.detail || {};
    chrome.runtime.sendMessage(
      { action: 'search', query: detail.query || 'test', semantic: detail.semantic !== undefined ? detail.semantic : true, limit: detail.limit || 5 },
      (response) => {
        // Send response back to the test page
        window.dispatchEvent(new CustomEvent('marchiver-search-response', {
          detail: response || { success: false, error: 'No response from extension' }
        }));
      }
    );
  });
  
  // Listen for API check event
  document.addEventListener('marchiver-check-api', function() {
    chrome.runtime.sendMessage({ action: 'getApiEndpoint' }, function(response) {
      if (response && response.apiEndpoint) {
        const apiUrl = response.apiEndpoint + '/health';
        
        // Make a fetch request to the API
        fetch(apiUrl)
          .then(response => {
            if (response.ok) {
              return response.json();
            }
            throw new Error('API returned status ' + response.status);
          })
          .then(data => {
            // Send success response back to the test page
            window.dispatchEvent(new CustomEvent('marchiver-check-api-response', {
              detail: { 
                success: true, 
                apiUrl: response.apiEndpoint,
                data: data 
              }
            }));
          })
          .catch(error => {
            // Send error response back to the test page
            window.dispatchEvent(new CustomEvent('marchiver-check-api-response', {
              detail: { 
                success: false, 
                error: error.message 
              }
            }));
          });
      } else {
        // Send error response back to the test page
        window.dispatchEvent(new CustomEvent('marchiver-check-api-response', {
          detail: { 
            success: false, 
            error: 'Failed to get API endpoint from extension' 
          }
        }));
      }
    });
  });
}

// Handle keyboard shortcuts
function handleKeyDown(event) {
  // Alt+S to save page
  if (event.altKey && event.key === 's') {
    savePage();
  }
  
  // Alt+M to summarize page
  if (event.altKey && event.key === 'm') {
    summarizePage();
  }
}

// Save the current page
function savePage() {
  chrome.runtime.sendMessage(
    { action: 'savePage', url: window.location.href, summarize: false },
    (response) => {
      showNotification(response && response.success ? 
        'Page saved to Marchiver' : 
        'Error saving page', 
        !(response && response.success));
    }
  );
}

// Summarize the current page
function summarizePage() {
  chrome.runtime.sendMessage(
    { action: 'summarizePage', url: window.location.href },
    (response) => {
      showNotification(response && response.success ? 
        'Page summarized and saved to Marchiver' : 
        'Error summarizing page', 
        !(response && response.success));
    }
  );
}

// Get page content
function getPageContent() {
  return {
    title: document.title,
    url: window.location.href,
    content: document.body.innerText,
    html: document.documentElement.outerHTML
  };
}

// Show notification
function showNotification(message, isError = false) {
  const notification = document.createElement('div');
  notification.className = 'marchiver-notification';
  notification.textContent = message;
  
  // Style the notification
  notification.style.cssText = `
    position: fixed;
    top: 20px;
    right: 20px;
    z-index: 9999;
    background-color: ${isError ? '#f44336' : '#4caf50'};
    color: white;
    border-radius: 4px;
    padding: 12px 20px;
    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    font-size: 14px;
    box-shadow: 0 2px 10px rgba(0, 0, 0, 0.2);
    opacity: 0;
    transition: opacity 0.3s ease-in-out;
  `;
  
  // Add notification to page
  document.body.appendChild(notification);
  
  // Fade in
  setTimeout(() => {
    notification.style.opacity = '1';
  }, 10);
  
  // Auto-remove after 3 seconds
  setTimeout(() => {
    notification.style.opacity = '0';
    setTimeout(() => {
      if (notification.parentNode) {
        notification.parentNode.removeChild(notification);
      }
    }, 300);
  }, 3000);
}

// Initialize the content script
init();
