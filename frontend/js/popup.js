// Constants
const API_BASE_URL = 'http://localhost:8000/api';

// DOM Elements
const savePageBtn = document.getElementById('savePageBtn');
const summarizeBtn = document.getElementById('summarizeBtn');
const searchInput = document.getElementById('searchInput');
const semanticSearchCheckbox = document.getElementById('semanticSearch');
const searchBtn = document.getElementById('searchBtn');
const resultsContainer = document.getElementById('results');
const statusElement = document.getElementById('status');
const optionsBtn = document.getElementById('optionsBtn');

// Event Listeners
document.addEventListener('DOMContentLoaded', init);
savePageBtn.addEventListener('click', savePage);
summarizeBtn.addEventListener('click', summarizePage);
searchBtn.addEventListener('click', performSearch);
optionsBtn.addEventListener('click', openOptions);
searchInput.addEventListener('keypress', (e) => {
  if (e.key === 'Enter') {
    performSearch();
  }
});

// Initialization
async function init() {
  // Load settings
  const settings = await loadSettings();
  
  // Check if API is reachable
  try {
    const response = await fetch(`${settings.apiEndpoint || API_BASE_URL}/health`);
    if (response.ok) {
      showStatus('Connected to Marchiver API', 'success');
    } else {
      showStatus('API connection error. Check settings.', 'error');
    }
  } catch (error) {
    showStatus('API connection error. Check settings.', 'error');
  }
}

// Save current page
async function savePage() {
  showStatus('Saving page...');
  
  try {
    // Get current tab
    const [tab] = await chrome.tabs.query({ active: true, currentWindow: true });
    
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
        url: tab.url,
        save: true,
        summarize: settings.autoSummarize !== false,
      }),
    });
    
    if (!response.ok) {
      throw new Error(`API error: ${response.status}`);
    }
    
    const data = await response.json();
    
    showStatus('Page saved successfully!', 'success');
    
    // Show the saved document
    chrome.tabs.create({
      url: `document.html?id=${data.id}`
    });
    
  } catch (error) {
    console.error('Error saving page:', error);
    showStatus(`Error: ${error.message}`, 'error');
  }
}

// Summarize current page
async function summarizePage() {
  showStatus('Summarizing page...');
  
  try {
    // Get current tab
    const [tab] = await chrome.tabs.query({ active: true, currentWindow: true });
    
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
        url: tab.url,
        save: true,
        summarize: true,
      }),
    });
    
    if (!response.ok) {
      throw new Error(`API error: ${response.status}`);
    }
    
    const data = await response.json();
    
    showStatus('Page summarized and saved!', 'success');
    
    // Show the saved document
    chrome.tabs.create({
      url: `document.html?id=${data.id}`
    });
    
  } catch (error) {
    console.error('Error summarizing page:', error);
    showStatus(`Error: ${error.message}`, 'error');
  }
}

// Perform search
async function performSearch() {
  const query = searchInput.value.trim();
  
  if (!query) {
    showStatus('Please enter a search query', 'error');
    return;
  }
  
  showStatus('Searching...');
  resultsContainer.innerHTML = '';
  
  try {
    // Get settings
    const settings = await loadSettings();
    const useSemanticSearch = semanticSearchCheckbox.checked;
    const maxResults = settings.maxResults || 10;
    
    // Build API URL
    const apiUrl = `${settings.apiEndpoint || API_BASE_URL}/documents?query=${encodeURIComponent(query)}&semantic=${useSemanticSearch}&limit=${maxResults}`;
    
    // Perform search
    const response = await fetch(apiUrl);
    
    if (!response.ok) {
      throw new Error(`API error: ${response.status}`);
    }
    
    const results = await response.json();
    
    if (results.length === 0) {
      resultsContainer.innerHTML = '<div class="no-results">No results found</div>';
      showStatus('No results found', 'info');
    } else {
      displaySearchResults(results);
      showStatus(`Found ${results.length} results`, 'success');
    }
    
  } catch (error) {
    console.error('Error searching:', error);
    showStatus(`Error: ${error.message}`, 'error');
  }
}

// Display search results
function displaySearchResults(results) {
  resultsContainer.innerHTML = '';
  
  results.forEach(result => {
    const resultItem = document.createElement('div');
    resultItem.className = 'result-item';
    resultItem.dataset.id = result.id;
    
    const title = document.createElement('div');
    title.className = 'result-title';
    title.textContent = result.title;
    
    const url = document.createElement('div');
    url.className = 'result-url';
    url.textContent = result.url || 'No URL';
    
    const summary = document.createElement('div');
    summary.className = 'result-summary';
    summary.textContent = result.summary || result.content.substring(0, 150) + '...';
    
    resultItem.appendChild(title);
    resultItem.appendChild(url);
    resultItem.appendChild(summary);
    
    resultItem.addEventListener('click', () => {
      chrome.tabs.create({
        url: `document.html?id=${result.id}`
      });
    });
    
    resultsContainer.appendChild(resultItem);
  });
}

// Open options page
function openOptions() {
  chrome.runtime.openOptionsPage();
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

// Show status message
function showStatus(message, type = '') {
  statusElement.textContent = message;
  statusElement.className = 'status';
  
  if (type) {
    statusElement.classList.add(type);
  }
  
  // Clear status after 5 seconds if it's a success message
  if (type === 'success') {
    setTimeout(() => {
      statusElement.textContent = '';
      statusElement.className = 'status';
    }, 5000);
  }
}
