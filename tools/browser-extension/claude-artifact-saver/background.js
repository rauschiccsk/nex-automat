/**
 * Claude Artifact Saver - Background Service Worker
 * Minimálna implementácia - zatiaľ nie je potrebná extra funkcionalita
 */

console.log('Claude Artifact Saver - Background service worker loaded');

// Listen for extension install/update
chrome.runtime.onInstalled.addListener((details) => {
    if (details.reason === 'install') {
        console.log('Claude Artifact Saver installed');
    } else if (details.reason === 'update') {
        console.log('Claude Artifact Saver updated to version', chrome.runtime.getManifest().version);
    }
});

// Keep service worker alive (optional)
chrome.runtime.onMessage.addListener((message, sender, sendResponse) => {
    if (message.type === 'ping') {
        sendResponse({ status: 'ok' });
    }
    return true;
});