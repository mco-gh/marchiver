// Constants
const API_BASE_URL = 'http://localhost:8000/api';

// Initialize extension
chrome.runtime.onInstalled.addListener(() => {
  // Create context menu items
  chrome.contextMenus.create({
    id: 'savePage',
    title: 'Save page to Marchiver',
    contexts: ['page']
  });
  
  chrome.contextMenus.create({
    id: 'summarizePage',
    title: 'Summarize and save page',
    contexts: ['page']
  });
});

// Listen for messages from content script or popup
chrome.runtime.onMessage.addListener((message, sender, sendResponse) => {
  // Handle ping action for extension detection
  if (message.action === 'ping') {
    sendResponse({ success: true, message: 'Marchiver extension is active' });
    return false; // No async response needed
  }

  // Handle getApiEndpoint action
  if (message.action === 'getApiEndpoint') {
    sendResponse({ 
      success: true, 
      apiEndpoint: API_BASE_URL 
    });
    return false; // No async response needed
  }

  // Handle savePage action
  if (message.action === 'savePage') {
    // Build the URL with query parameters
    const fetchUrl = new URL(`${API_BASE_URL}/web/fetch`);
    fetchUrl.searchParams.append('url', message.url);
    fetchUrl.searchParams.append('save', 'true');
    fetchUrl.searchParams.append('summarize', message.summarize ? 'true' : 'false');
    
    // Make API call to save the page
    fetch(fetchUrl, {
      method: 'POST'
    })
    .then(response => {
      if (!response.ok) {
        throw new Error(`API returned status ${response.status}`);
      }
      return response.json();
    })
    .then(data => {
      sendResponse({
        success: true,
        document: data
      });
    })
    .catch(error => {
      sendResponse({
        success: false,
        error: error.message
      });
    });
    
    return true; // Async response needed
  }
  
  // Handle summarizePage action
  if (message.action === 'summarizePage') {
    // Build the URL with query parameters
    const fetchUrl = new URL(`${API_BASE_URL}/web/fetch`);
    fetchUrl.searchParams.append('url', message.url);
    fetchUrl.searchParams.append('save', 'true');
    fetchUrl.searchParams.append('summarize', 'true');
    
    // Make API call to summarize the page
    fetch(fetchUrl, {
      method: 'POST'
    })
    .then(response => {
      if (!response.ok) {
        throw new Error(`API returned status ${response.status}`);
      }
      return response.json();
    })
    .then(data => {
      sendResponse({
        success: true,
        document: data
      });
    })
    .catch(error => {
      sendResponse({
        success: false,
        error: error.message
      });
    });
    
    return true; // Async response needed
  }
  
  // Handle search action
  if (message.action === 'search') {
    const query = message.query || '';
    const semantic = message.semantic || false;
    const limit = message.limit || 10;
    const offset = message.offset || 0;
    
    // Build the search URL with query parameters
    const searchUrl = new URL(`${API_BASE_URL}/documents`);
    if (query) {
      searchUrl.searchParams.append('query', query);
      searchUrl.searchParams.append('semantic', semantic);
    }
    searchUrl.searchParams.append('limit', limit);
    searchUrl.searchParams.append('offset', offset);
    
    // Make API call to search documents
    fetch(searchUrl)
      .then(response => {
        if (!response.ok) {
          throw new Error(`API returned status ${response.status}`);
        }
        return response.json();
      })
      .then(data => {
        sendResponse({
          success: true,
          results: data
        });
      })
      .catch(error => {
        sendResponse({
          success: false,
          error: error.message
        });
      });
    
    return true; // Async response needed
  }
  
  // If we get here, we didn't handle the message
  sendResponse({ success: false, error: 'Unhandled message action: ' + message.action });
  return false;
});

// Handle context menu clicks
chrome.contextMenus.onClicked.addListener((info, tab) => {
  const url = info.pageUrl;
  
  switch (info.menuItemId) {
    case 'savePage':
      // Show initial notification
      chrome.notifications.create({
        type: 'basic',
        iconUrl: '/images/icon128.png',
        title: 'Marchiver',
        message: 'Saving page to Marchiver...'
      });
      
      // Build the URL with query parameters
      const fetchUrl = new URL(`${API_BASE_URL}/web/fetch`);
      fetchUrl.searchParams.append('url', url);
      fetchUrl.searchParams.append('save', 'true');
      fetchUrl.searchParams.append('summarize', 'true'); // Changed to include summarization
      
      // Make API call to save the page
      fetch(fetchUrl, {
        method: 'POST'
      })
      .then(response => {
        if (!response.ok) {
          throw new Error(`API returned status ${response.status}`);
        }
        return response.json();
      })
      .then(data => {
        // Show success notification with summary info if available
        let message = 'Page saved successfully!';
        if (data && data.summary) {
          message = 'Page saved with summary!';
        }
        
        chrome.notifications.create({
          type: 'basic',
          iconUrl: '/images/icon128.png',
          title: 'Marchiver',
          message: message
        });
      })
      .catch(error => {
        // Show error notification
        chrome.notifications.create({
          type: 'basic',
          iconUrl: '/images/icon128.png',
          title: 'Marchiver',
          message: `Error saving page: ${error.message}`
        });
      });
      break;
      
    case 'summarizePage':
      // Show initial notification
      chrome.notifications.create({
        type: 'basic',
        iconUrl: '/images/icon128.png',
        title: 'Marchiver',
        message: 'Summarizing page...'
      });
      
      // Build the URL with query parameters
      const summarizeUrl = new URL(`${API_BASE_URL}/web/fetch`);
      summarizeUrl.searchParams.append('url', url);
      summarizeUrl.searchParams.append('save', 'true');
      summarizeUrl.searchParams.append('summarize', 'true');
      
      // Make API call to summarize the page
      fetch(summarizeUrl, {
        method: 'POST'
      })
      .then(response => {
        if (!response.ok) {
          throw new Error(`API returned status ${response.status}`);
        }
        return response.json();
      })
      .then(data => {
        // Show success notification
        chrome.notifications.create({
          type: 'basic',
          iconUrl: '/images/icon128.png',
          title: 'Marchiver',
          message: 'Page summarized and saved successfully!'
        });
      })
      .catch(error => {
        // Show error notification
        chrome.notifications.create({
          type: 'basic',
          iconUrl: '/images/icon128.png',
          title: 'Marchiver',
          message: `Error summarizing page: ${error.message}`
        });
      });
      break;
  }
});
