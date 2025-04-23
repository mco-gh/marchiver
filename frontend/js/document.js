// Constants
const API_BASE_URL = 'http://localhost:8000/api';

// DOM Elements
const backBtn = document.getElementById('backBtn');
const documentTitle = document.getElementById('documentTitle');
const documentUrl = document.getElementById('documentUrl');
const documentDate = document.getElementById('documentDate');
const documentTags = document.getElementById('documentTags');
const contentTab = document.getElementById('contentTab');
const summaryTab = document.getElementById('summaryTab');
const contentPanel = document.getElementById('contentPanel');
const summaryPanel = document.getElementById('summaryPanel');
const documentContent = document.getElementById('documentContent');
const documentSummary = document.getElementById('documentSummary');
const relatedDocuments = document.getElementById('relatedDocuments');
const editBtn = document.getElementById('editBtn');
const editModal = document.getElementById('editModal');
const closeModalBtn = document.getElementById('closeModalBtn');
const editTitle = document.getElementById('editTitle');
const editTags = document.getElementById('editTags');
const editCategory = document.getElementById('editCategory');
const editSummary = document.getElementById('editSummary');
const saveEditBtn = document.getElementById('saveEditBtn');
const cancelEditBtn = document.getElementById('cancelEditBtn');
const statusElement = document.getElementById('status');

// State
let currentDocument = null;
let documentId = null;

// Event Listeners
document.addEventListener('DOMContentLoaded', init);
backBtn.addEventListener('click', goBack);
contentTab.addEventListener('click', () => switchTab('content'));
summaryTab.addEventListener('click', () => switchTab('summary'));
editBtn.addEventListener('click', openEditModal);
closeModalBtn.addEventListener('click', closeEditModal);
cancelEditBtn.addEventListener('click', closeEditModal);
saveEditBtn.addEventListener('click', saveDocumentChanges);

// Initialization
async function init() {
  // Get document ID from URL
  const urlParams = new URLSearchParams(window.location.search);
  documentId = urlParams.get('id');
  
  if (!documentId) {
    showStatus('No document ID provided', 'error');
    return;
  }
  
  // Load settings
  const settings = await loadSettings();
  
  // Load document
  await loadDocument(documentId, settings);
}

// Load document
async function loadDocument(id, settings) {
  showStatus('Loading document...');
  
  try {
    // Get document
    const apiUrl = `${settings.apiEndpoint || API_BASE_URL}/documents/${id}`;
    const response = await fetch(apiUrl);
    
    if (!response.ok) {
      throw new Error(`API error: ${response.status}`);
    }
    
    const document = await response.json();
    currentDocument = document;
    
    // Display document
    displayDocument(document);
    
    // Load related documents if enabled
    if (settings.showRelatedDocs) {
      loadRelatedDocuments(id, settings);
    }
    
    showStatus('Document loaded', 'success');
  } catch (error) {
    console.error('Error loading document:', error);
    showStatus(`Error: ${error.message}`, 'error');
  }
}

// Display document
function displayDocument(document) {
  // Set title
  documentTitle.textContent = document.title;
  document.title = `${document.title} - Marchiver`;
  
  // Set URL
  if (document.url) {
    documentUrl.textContent = document.url;
    documentUrl.href = document.url;
  } else {
    documentUrl.textContent = 'No URL';
    documentUrl.href = '#';
  }
  
  // Set date
  const date = new Date(document.date);
  documentDate.textContent = date.toLocaleString();
  
  // Set tags
  documentTags.innerHTML = '';
  if (document.tags && document.tags.length > 0) {
    document.tags.forEach(tag => {
      const tagElement = document.createElement('span');
      tagElement.className = 'tag';
      tagElement.textContent = tag;
      documentTags.appendChild(tagElement);
    });
  } else {
    const noTagsElement = document.createElement('span');
    noTagsElement.textContent = 'No tags';
    documentTags.appendChild(noTagsElement);
  }
  
  // Set content
  documentContent.textContent = document.content;
  
  // Set summary
  if (document.summary) {
    documentSummary.textContent = document.summary;
    summaryTab.style.display = 'block';
  } else {
    documentSummary.textContent = 'No summary available';
    summaryTab.style.display = 'none';
  }
}

// Load related documents
async function loadRelatedDocuments(id, settings) {
  try {
    // Get related documents
    const apiUrl = `${settings.apiEndpoint || API_BASE_URL}/documents/${id}/similar`;
    const response = await fetch(apiUrl);
    
    if (!response.ok) {
      throw new Error(`API error: ${response.status}`);
    }
    
    const documents = await response.json();
    
    // Display related documents
    displayRelatedDocuments(documents, settings.showProximityScore);
  } catch (error) {
    console.error('Error loading related documents:', error);
    relatedDocuments.innerHTML = '<div class="error">Failed to load related documents</div>';
  }
}

// Display related documents
function displayRelatedDocuments(documents, showProximityScore) {
  relatedDocuments.innerHTML = '';
  
  if (documents.length === 0) {
    relatedDocuments.innerHTML = '<div class="no-results">No related documents found</div>';
    return;
  }
  
  documents.forEach(doc => {
    const relatedItem = document.createElement('div');
    relatedItem.className = 'related-item';
    relatedItem.dataset.id = doc.id;
    
    const title = document.createElement('div');
    title.className = 'related-title';
    title.textContent = doc.title;
    
    const summary = document.createElement('div');
    summary.className = 'related-summary';
    summary.textContent = doc.summary || doc.content.substring(0, 150) + '...';
    
    relatedItem.appendChild(title);
    
    // Add proximity score if enabled
    if (showProximityScore && doc.score) {
      const score = document.createElement('div');
      score.className = 'related-score';
      score.textContent = `Similarity: ${Math.round(doc.score * 100)}%`;
      relatedItem.appendChild(score);
    }
    
    relatedItem.appendChild(summary);
    
    relatedItem.addEventListener('click', () => {
      window.location.href = `document.html?id=${doc.id}`;
    });
    
    relatedDocuments.appendChild(relatedItem);
  });
}

// Switch between content and summary tabs
function switchTab(tab) {
  if (tab === 'content') {
    contentTab.classList.add('active');
    summaryTab.classList.remove('active');
    contentPanel.classList.add('active');
    summaryPanel.classList.remove('active');
  } else {
    contentTab.classList.remove('active');
    summaryTab.classList.add('active');
    contentPanel.classList.remove('active');
    summaryPanel.classList.add('active');
  }
}

// Open edit modal
function openEditModal() {
  if (!currentDocument) return;
  
  // Populate form fields
  editTitle.value = currentDocument.title;
  editTags.value = currentDocument.tags ? currentDocument.tags.join(', ') : '';
  editCategory.value = currentDocument.category || '';
  editSummary.value = currentDocument.summary || '';
  
  // Show modal
  editModal.classList.add('active');
}

// Close edit modal
function closeEditModal() {
  editModal.classList.remove('active');
}

// Save document changes
async function saveDocumentChanges() {
  if (!currentDocument || !documentId) return;
  
  showStatus('Saving changes...');
  
  try {
    // Get settings
    const settings = await loadSettings();
    
    // Prepare update data
    const updateData = {
      title: editTitle.value.trim(),
      tags: editTags.value.split(',').map(tag => tag.trim()).filter(tag => tag),
      category: editCategory.value.trim(),
      summary: editSummary.value.trim()
    };
    
    // Update document
    const apiUrl = `${settings.apiEndpoint || API_BASE_URL}/documents/${documentId}`;
    const response = await fetch(apiUrl, {
      method: 'PUT',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(updateData),
    });
    
    if (!response.ok) {
      throw new Error(`API error: ${response.status}`);
    }
    
    const updatedDocument = await response.json();
    currentDocument = updatedDocument;
    
    // Update display
    displayDocument(updatedDocument);
    
    // Close modal
    closeEditModal();
    
    showStatus('Document updated successfully', 'success');
  } catch (error) {
    console.error('Error updating document:', error);
    showStatus(`Error: ${error.message}`, 'error');
  }
}

// Go back to previous page
function goBack() {
  window.history.back();
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
