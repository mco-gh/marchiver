// Constants
const MARCHIVER_BADGE_ID = 'marchiver-badge';

// State
let isBadgeVisible = false;

// Initialize
init();

// Main initialization
function init() {
  // Listen for messages from background script
  chrome.runtime.onMessage.addListener((message, sender, sendResponse) => {
    if (message.action === 'showBadge') {
      showBadge();
      sendResponse({ success: true });
    }
    
    if (message.action === 'hideBadge') {
      hideBadge();
      sendResponse({ success: true });
    }
    
    if (message.action === 'getPageContent') {
      const content = getPageContent();
      sendResponse({ success: true, content });
    }
  });
  
  // Add keyboard shortcut listener
  document.addEventListener('keydown', handleKeyDown);
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
      if (response && response.success) {
        showNotification('Page saved to Marchiver');
      } else {
        showNotification('Error saving page', true);
      }
    }
  );
}

// Summarize the current page
function summarizePage() {
  chrome.runtime.sendMessage(
    { action: 'summarizePage', url: window.location.href },
    (response) => {
      if (response && response.success) {
        showNotification('Page summarized and saved to Marchiver');
      } else {
        showNotification('Error summarizing page', true);
      }
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

// Show notification badge
function showBadge() {
  if (isBadgeVisible) return;
  
  const badge = document.createElement('div');
  badge.id = MARCHIVER_BADGE_ID;
  badge.innerHTML = `
    <div class="marchiver-badge-content">
      <img src="${chrome.runtime.getURL('images/icon48.png')}" alt="Marchiver" class="marchiver-badge-icon">
      <div class="marchiver-badge-text">Saved to Marchiver</div>
      <button class="marchiver-badge-close">×</button>
    </div>
  `;
  
  // Style the badge
  badge.style.cssText = `
    position: fixed;
    top: 20px;
    right: 20px;
    z-index: 9999;
    background-color: white;
    border-radius: 8px;
    box-shadow: 0 2px 10px rgba(0, 0, 0, 0.2);
    padding: 12px;
    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    font-size: 14px;
    transition: opacity 0.3s ease-in-out;
  `;
  
  // Style the content
  const content = badge.querySelector('.marchiver-badge-content');
  content.style.cssText = `
    display: flex;
    align-items: center;
    gap: 10px;
  `;
  
  // Style the icon
  const icon = badge.querySelector('.marchiver-badge-icon');
  icon.style.cssText = `
    width: 24px;
    height: 24px;
  `;
  
  // Style the text
  const text = badge.querySelector('.marchiver-badge-text');
  text.style.cssText = `
    color: #333;
    font-weight: 500;
  `;
  
  // Style the close button
  const closeBtn = badge.querySelector('.marchiver-badge-close');
  closeBtn.style.cssText = `
    background: none;
    border: none;
    color: #999;
    font-size: 20px;
    cursor: pointer;
    padding: 0;
    margin-left: 10px;
  `;
  
  // Add event listener to close button
  closeBtn.addEventListener('click', hideBadge);
  
  // Add badge to page
  document.body.appendChild(badge);
  isBadgeVisible = true;
  
  // Auto-hide after 5 seconds
  setTimeout(hideBadge, 5000);
}

// Hide notification badge
function hideBadge() {
  const badge = document.getElementById(MARCHIVER_BADGE_ID);
  if (badge) {
    badge.style.opacity = '0';
    setTimeout(() => {
      if (badge.parentNode) {
        badge.parentNode.removeChild(badge);
      }
      isBadgeVisible = false;
    }, 300);
  }
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
