<<<<<<< HEAD
// extension/background.js
chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {
    // Check if the message is for analyzing the page
    if (request.action === "analyzePage") {
        const apiUrl = 'http://127.0.0.1:8000/assess';

        console.log("Background script received URL:", request.url);

        fetch(apiUrl, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ url: request.url })
        })
        .then(response => {
            if (!response.ok) {
                // If response is not ok, parse the error detail
                return response.json().then(err => { throw new Error(err.detail || 'API Error'); });
            }
            return response.json();
        })
        .then(data => {
            console.log("Data received from API:", data);
            // Send the successful result back to the content script in the active tab
            chrome.tabs.query({ active: true, currentWindow: true }, function(tabs) {
                if (tabs[0]) {
                    chrome.tabs.sendMessage(tabs[0].id, { action: "updateWidget", data: data });
                }
            });
        })
        .catch(error => {
            console.error("Error fetching analysis:", error);
            // Send an error message back to the content script
            chrome.tabs.query({ active: true, currentWindow: true }, function(tabs) {
                if (tabs[0]) {
                    chrome.tabs.sendMessage(tabs[0].id, { action: "widgetError", message: error.message });
                }
            });
        });

        return true; // Important for asynchronous sendResponse
    }
=======
// extension/background.js
chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {
    // Check if the message is for analyzing the page
    if (request.action === "analyzePage") {
        const apiUrl = 'http://127.0.0.1:8000/assess';

        console.log("Background script received URL:", request.url);

        fetch(apiUrl, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ url: request.url })
        })
        .then(response => {
            if (!response.ok) {
                // If response is not ok, parse the error detail
                return response.json().then(err => { throw new Error(err.detail || 'API Error'); });
            }
            return response.json();
        })
        .then(data => {
            console.log("Data received from API:", data);
            // Send the successful result back to the content script in the active tab
            chrome.tabs.query({ active: true, currentWindow: true }, function(tabs) {
                if (tabs[0]) {
                    chrome.tabs.sendMessage(tabs[0].id, { action: "updateWidget", data: data });
                }
            });
        })
        .catch(error => {
            console.error("Error fetching analysis:", error);
            // Send an error message back to the content script
            chrome.tabs.query({ active: true, currentWindow: true }, function(tabs) {
                if (tabs[0]) {
                    chrome.tabs.sendMessage(tabs[0].id, { action: "widgetError", message: error.message });
                }
            });
        });

        return true; // Important for asynchronous sendResponse
    }
>>>>>>> 2ae3776 (Initial commit for deployment)
});