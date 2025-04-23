// Constants
const API_BASE_URL = 'http://localhost:8000/api';

// DOM Elements
const apiEndpointInput = document.getElementById('apiEndpoint');
const apiKeyInput = document.getElementById('apiKey');
const embeddingModelSelect = document.getElementById('embeddingModel');
const showRelatedDocsCheckbox = document.getElementById('showRelatedDocs');
const showProximityScoreCheckbox = document.getElementById('showProximityScore');
const maxResultsInput = document.getElementById('maxResults');
const autoSummarizeCheckbox = document.getElementById('autoSummarize');
const cacheExpirationInput = document.getElementById('cacheExpiration');
const saveBtn = document.getElementById('saveBtn');
const resetBtn = document.getElementById('resetBtn');
const statusElement = document.getElementById('status');

// Event Listeners
document.addEventListener('DOMContentLoaded', loadOptions);
saveBtn.addEventListener('click', saveOptions);
resetBtn.addEventListener('click', resetOptions);

// Load options from storage
function loadOptions() {
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
    apiEndpointInput.value = items.apiEndpoint;
    apiKeyInput.value = items.apiKey;
    embeddingModelSelect.value = items.embeddingModel;
    showRelatedDocsCheckbox.checked = items.showRelatedDocs;
    showProximityScoreCheckbox.checked = items.showProximityScore;
    maxResultsInput.value = items.maxResults;
    autoSummarizeCheckbox.checked = items.autoSummarize;
    cacheExpirationInput.value = items.cacheExpiration;
  });
}

// Save options to storage
function saveOptions() {
  const settings = {
    apiEndpoint: apiEndpointInput.value.trim() || API_BASE_URL,
    apiKey: apiKeyInput.value.trim(),
    embeddingModel: embeddingModelSelect.value,
    showRelatedDocs: showRelatedDocsCheckbox.checked,
    showProximityScore: showProximityScoreCheckbox.checked,
    maxResults: parseInt(maxResultsInput.value) || 10,
    autoSummarize: autoSummarizeCheckbox.checked,
    cacheExpiration: parseInt(cacheExpirationInput.value) || 30
  };
  
  chrome.storage.sync.set(settings, () => {
    showStatus('Settings saved successfully!', 'success');
    
    // Test API connection
    testApiConnection(settings.apiEndpoint);
  });
}

// Reset options to defaults
function resetOptions() {
  apiEndpointInput.value = API_BASE_URL;
  apiKeyInput.value = '';
  embeddingModelSelect.value = 'gemini';
  showRelatedDocsCheckbox.checked = true;
  showProximityScoreCheckbox.checked = true;
  maxResultsInput.value = 10;
  autoSummarizeCheckbox.checked = true;
  cacheExpirationInput.value = 30;
  
  showStatus('Settings reset to defaults. Click Save to apply.', 'info');
}

// Test API connection
async function testApiConnection(apiEndpoint) {
  try {
    const response = await fetch(`${apiEndpoint}/health`);
    
    if (response.ok) {
      showStatus('API connection successful!', 'success');
    } else {
      showStatus(`API connection error: ${response.status} ${response.statusText}`, 'error');
    }
  } catch (error) {
    showStatus(`API connection error: ${error.message}`, 'error');
  }
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
