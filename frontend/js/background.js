// Constants
const API_BASE_URL = 'http://localhost:8000/api';

// Initialize extension
chrome.runtime.onInstalled.addListener(async () => {
  console.log('Marchiver extension installed');
  
  // Set default settings
  const settings = await loadSettings();
  
  // Check if API is reachable
  try {
    const response = await fetch(`${settings.apiEndpoint}/health`);
    if (response.ok) {
      console.log('Connected to Marchiver API');
    } else {
      console.warn('API connection error. Check settings.');
    }
  } catch (error) {
    console.warn('API connection error:', error);
  }
});

// Listen for messages from content script or popup
chrome.runtime.onMessage.addListener((message, sender, sendResponse) => {
  if (message.action === 'savePage') {
    savePage(message.url, message.summarize)
      .then(result => sendResponse(result))
      .catch(error => sendResponse({ success: false, error: error.message }));
    return true; // Indicates async response
  }
  
  if (message.action === 'summarizePage') {
    summarizePage(message.url)
      .then(result => sendResponse(result))
      .catch(error => sendResponse({ success: false, error: error.message }));
    return true; // Indicates async response
  }
  
  if (message.action === 'search') {
    search(message.query, message.semantic, message.limit)
      .then(result => sendResponse(result))
      .catch(error => sendResponse({ success: false, error: error.message }));
    return true; // Indicates async response
  }
});

// Save a page
async function savePage(url, summarize = false) {
  try {
    // Get settings
    const settings = await loadSettings();
    const apiUrl = `${settings.apiEndpoint || API_BASE_URL}/web/fetch`;
    
    // Save the page
    const response = await fetch(apiUrl, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        url: url,
        save: true,
        summarize: summarize || settings.autoSummarize !== false,
      }),
    });
    
    if (!response.ok) {
      throw new Error(`API error: ${response.status}`);
    }
    
    const data = await response.json();
    
    return {
      success: true,
      document: data
    };
  } catch (error) {
    console.error('Error saving page:', error);
    throw error;
  }
}

// Summarize a page
async function summarizePage(url) {
  try {
    // Get settings
    const settings = await loadSettings();
    const apiUrl = `${settings.apiEndpoint || API_BASE_URL}/web/fetch`;
    
    // Fetch and summarize the page
    const response = await fetch(apiUrl, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        url: url,
        save: true,
        summarize: true,
      }),
    });
    
    if (!response.ok) {
      throw new Error(`API error: ${response.status}`);
    }
    
    const data = await response.json();
    
    return {
      success: true,
      document: data
    };
  } catch (error) {
    console.error('Error summarizing page:', error);
    throw error;
  }
}

// Search documents
async function search(query, semantic = false, limit = 10) {
  try {
    // Get settings
    const settings = await loadSettings();
    
    // Build API URL
    const apiUrl = `${settings.apiEndpoint || API_BASE_URL}/documents?query=${encodeURIComponent(query)}&semantic=${semantic}&limit=${limit}`;
    
    // Perform search
    const response = await fetch(apiUrl);
    
    if (!response.ok) {
      throw new Error(`API error: ${response.status}`);
    }
    
    const results = await response.json();
    
    return {
      success: true,
      results: results
    };
  } catch (error) {
    console.error('Error searching:', error);
    throw error;
  }
}

// Load settings from storage
async function loadSettings() {
  return new Promise((resolve) => {
    chrome.storage.sync.get({
      apiEndpoint: API_BASE_URL,
      apiKey: '',
      embeddingModel: 'gemini',
      showRelatedDocs: true,
      showProximityScore: true,
      maxResults: 10,
      autoSummarize: true,
      cacheExpiration: 30
    }, (items) => {
      resolve(items);
    });
  });
}

// Context menu setup
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
  
  chrome.contextMenus.create({
    id: 'saveLink',
    title: 'Save link to Marchiver',
    contexts: ['link']
  });
  
  chrome.contextMenus.create({
    id: 'summarizeLink',
    title: 'Summarize and save link',
    contexts: ['link']
  });
  
  chrome.contextMenus.create({
    id: 'searchSelection',
    title: 'Search Marchiver for "%s"',
    contexts: ['selection']
  });
});

// Handle context menu clicks
chrome.contextMenus.onClicked.addListener((info, tab) => {
  switch (info.menuItemId) {
    case 'savePage':
      savePage(tab.url, false)
        .then(result => {
          if (result.success) {
            chrome.tabs.create({
              url: `document.html?id=${result.document.id}`
            });
          }
        })
        .catch(error => console.error('Error saving page:', error));
      break;
      
    case 'summarizePage':
      summarizePage(tab.url)
        .then(result => {
          if (result.success) {
            chrome.tabs.create({
              url: `document.html?id=${result.document.id}`
            });
          }
        })
        .catch(error => console.error('Error summarizing page:', error));
      break;
      
    case 'saveLink':
      savePage(info.linkUrl, false)
        .then(result => {
          if (result.success) {
            chrome.tabs.create({
              url: `document.html?id=${result.document.id}`
            });
          }
        })
        .catch(error => console.error('Error saving link:', error));
      break;
      
    case 'summarizeLink':
      summarizePage(info.linkUrl)
        .then(result => {
          if (result.success) {
            chrome.tabs.create({
              url: `document.html?id=${result.document.id}`
            });
          }
        })
        .catch(error => console.error('Error summarizing link:', error));
      break;
      
    case 'searchSelection':
      chrome.tabs.create({
        url: `popup.html?search=${encodeURIComponent(info.selectionText)}`
      });
      break;
  }
});
