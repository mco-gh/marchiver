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
    // Mock successful response
    sendResponse({
      success: true,
      document: {
        id: 'mock-doc-' + Date.now(),
        url: message.url,
        title: 'Saved page: ' + message.url,
        summary: message.summarize ? 'This is a mock summary' : null
      }
    });
    return false; // No async response needed
  }
  
  // Handle summarizePage action
  if (message.action === 'summarizePage') {
    // Mock successful response
    sendResponse({
      success: true,
      document: {
        id: 'mock-doc-' + Date.now(),
        url: message.url,
        title: 'Summarized page: ' + message.url,
        summary: 'This is a mock summary for ' + message.url
      }
    });
    return false; // No async response needed
  }
  
  // Handle search action
  if (message.action === 'search') {
    // Mock successful response
    sendResponse({
      success: true,
      results: [
        { id: 'mock-result-1', title: 'Mock Result 1', url: 'http://example.com/1' },
        { id: 'mock-result-2', title: 'Mock Result 2', url: 'http://example.com/2' }
      ]
    });
    return false; // No async response needed
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
      // Handle save page action
      // Show a notification
      chrome.notifications.create({
        type: 'basic',
        iconUrl: '/images/icon128.png',
        title: 'Marchiver',
        message: 'Saving page to Marchiver...'
      });
      
      // Mock successful save
      setTimeout(() => {
        chrome.notifications.create({
          type: 'basic',
          iconUrl: '/images/icon128.png',
          title: 'Marchiver',
          message: 'Page saved successfully!'
        });
      }, 1000);
      break;
      
    case 'summarizePage':
      // Handle summarize page action
      // Show a notification
      chrome.notifications.create({
        type: 'basic',
        iconUrl: '/images/icon128.png',
        title: 'Marchiver',
        message: 'Summarizing page...'
      });
      
      // Mock successful summarization
      setTimeout(() => {
        chrome.notifications.create({
          type: 'basic',
          iconUrl: '/images/icon128.png',
          title: 'Marchiver',
          message: 'Page summarized and saved successfully!'
        });
      }, 2000);
      break;
  }
});
