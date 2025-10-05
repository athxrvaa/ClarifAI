<<<<<<< HEAD
// extension/content.js

const observer = new MutationObserver((mutations, obs) => {
    const target = findTargetElement();
    if (target && !document.getElementById('sustainability-widget-clarifai')) {
        injectWidget(target);
        // We don't disconnect, as some sites might re-render the area.
    }
});

observer.observe(document.body, { childList: true, subtree: true });

function findTargetElement() {
    const allButtons = document.querySelectorAll('button');
    for (const button of allButtons) {
        const buttonText = button.textContent.trim().toUpperCase();
        if (buttonText === 'BUY NOW' || buttonText === 'ADD TO CART') {
            const container = button.closest('div, li'); // Find a reasonable parent
            return container ? container.parentElement : null;
        }
    }
    return null;
}

function injectWidget(target) {
    const widget = document.createElement('div');
    widget.id = 'sustainability-widget-clarifai';
    widget.innerHTML = `
        <div class="clarifai-header">
            <img src="${chrome.runtime.getURL("icon48.png")}" class="clarifai-logo" />
            Sustainability Score
        </div>
        <div class="clarifai-body">
            <div class="clarifai-score-container" id="clarifai-score-container">
                <div class="clarifai-score" id="clarifai-score">--</div>
                <div class="clarifai-loader" id="clarifai-loader" style="display:none;"></div>
            </div>
            <div class="clarifai-info">
                <p class="clarifai-summary" id="clarifai-summary">Click to Analyze</p>
                <p class="clarifai-error" id="clarifai-error" style="display:none;"></p>
                <a class="clarifai-details-toggle" id="clarifai-details-toggle" style="display:none;">Show Details</a>
            </div>
        </div>
        <div class="clarifai-details-panel" id="clarifai-details-panel"></div>
    `;
    
    target.insertAdjacentElement('beforebegin', widget);

    widget.addEventListener('click', () => {
        const scoreEl = document.getElementById('clarifai-score');
        const loaderEl = document.getElementById('clarifai-loader');
        if (scoreEl.textContent !== '--' || loaderEl.style.display === 'block') {
            return;
        }
        document.getElementById('clarifai-summary').style.display = 'none';
        loaderEl.style.display = 'block';
        scoreEl.style.display = 'none';
        
        chrome.runtime.sendMessage({ action: "analyzePage", url: window.location.href });
    });
}

chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {
    if (request.action === "updateWidget") {
        updateWidgetUI(request.data);
    } else if (request.action === "widgetError") {
        displayWidgetError(request.message);
    }
});

function updateWidgetUI(data) {
    const scoreEl = document.getElementById('clarifai-score');
    const scoreContainerEl = document.getElementById('clarifai-score-container');
    const loaderEl = document.getElementById('clarifai-loader');
    const summaryEl = document.getElementById('clarifai-summary');
    const detailsToggleEl = document.getElementById('clarifai-details-toggle');
    const detailsPanelEl = document.getElementById('clarifai-details-panel');

    if (!scoreEl) return;

    // --- Update Main Display ---
    loaderEl.style.display = 'none';
    scoreEl.style.display = 'block';
    summaryEl.style.display = 'block';
    detailsToggleEl.style.display = 'block';

    const results = data.analysis_results;
    const score = results.final_score;
    const breakdown = results.breakdown;

    scoreEl.textContent = score;
    summaryEl.textContent = breakdown.end_of_life_advice;
    
    // --- Set Colors Based on Score ---
    let scoreColor = '#7f8c8d'; // Default grey
    if (score >= 75) scoreColor = '#27ae60'; // Green
    else if (score >= 50) scoreColor = '#f39c12'; // Yellow
    else scoreColor = '#e74c3c'; // Red
    scoreContainerEl.style.borderColor = scoreColor;
    scoreEl.style.color = scoreColor;

    // --- Populate the Hidden Details Panel ---
    detailsPanelEl.innerHTML = `
        <div class="clarifai-detail-item">
            <span class="clarifai-detail-label">Carbon (Material):</span>
            <span class="clarifai-detail-value">${breakdown.material_carbon_footprint_kgCO2} kg CO₂</span>
        </div>
        <div class="clarifai-detail-item">
            <span class="clarifai-detail-label">Carbon (Transport):</span>
            <span class="clarifai-detail-value">${breakdown.transportation_carbon_footprint_kgCO2} kg CO₂</span>
        </div>
        <div class="clarifai-detail-item">
            <span class="clarifai-detail-label">Water Usage:</span>
            <span class="clarifai-detail-value">${breakdown.material_water_usage_L} L</span>
        </div>
        <div class="clarifai-detail-item">
            <span class="clarifai-detail-label">End of Life Score:</span>
            <span class="clarifai-detail-value">${breakdown.end_of_life_score} / 100</span>
        </div>
        <div class="clarifai-detail-item">
            <span class="clarifai-detail-label">Origin:</span>
            <span class="clarifai-detail-value">${breakdown.manufacturing_location_factor}</span>
        </div>
    `;

    // --- Add Click Listener for the "Show/Hide Details" Toggle ---
    let detailsVisible = false;
    detailsToggleEl.onclick = () => {
        detailsVisible = !detailsVisible;
        detailsPanelEl.style.display = detailsVisible ? 'block' : 'none';
        detailsToggleEl.textContent = detailsVisible ? 'Hide Details' : 'Show Details';
    };
}

function displayWidgetError(message) {
    const loaderEl = document.getElementById('clarifai-loader');
    const errorEl = document.getElementById('clarifai-error');
    const summaryEl = document.getElementById('clarifai-summary');
    const scoreEl = document.getElementById('clarifai-score');

    if (!loaderEl || !errorEl) return;

    loaderEl.style.display = 'none';
    scoreEl.style.display = 'none';
    summaryEl.style.display = 'none';
    errorEl.style.display = 'block';
    errorEl.textContent = `Error: ${message}`;
=======
// extension/content.js

const observer = new MutationObserver((mutations, obs) => {
    const target = findTargetElement();
    if (target && !document.getElementById('sustainability-widget-clarifai')) {
        injectWidget(target);
        // We don't disconnect, as some sites might re-render the area.
    }
});

observer.observe(document.body, { childList: true, subtree: true });

function findTargetElement() {
    const allButtons = document.querySelectorAll('button');
    for (const button of allButtons) {
        const buttonText = button.textContent.trim().toUpperCase();
        if (buttonText === 'BUY NOW' || buttonText === 'ADD TO CART') {
            const container = button.closest('div, li'); // Find a reasonable parent
            return container ? container.parentElement : null;
        }
    }
    return null;
}

function injectWidget(target) {
    const widget = document.createElement('div');
    widget.id = 'sustainability-widget-clarifai';
    widget.innerHTML = `
        <div class="clarifai-header">
            <img src="${chrome.runtime.getURL("icon48.png")}" class="clarifai-logo" />
            Sustainability Score
        </div>
        <div class="clarifai-body">
            <div class="clarifai-score-container" id="clarifai-score-container">
                <div class="clarifai-score" id="clarifai-score">--</div>
                <div class="clarifai-loader" id="clarifai-loader" style="display:none;"></div>
            </div>
            <div class="clarifai-info">
                <p class="clarifai-summary" id="clarifai-summary">Click to Analyze</p>
                <p class="clarifai-error" id="clarifai-error" style="display:none;"></p>
                <a class="clarifai-details-toggle" id="clarifai-details-toggle" style="display:none;">Show Details</a>
            </div>
        </div>
        <div class="clarifai-details-panel" id="clarifai-details-panel"></div>
    `;
    
    target.insertAdjacentElement('beforebegin', widget);

    widget.addEventListener('click', () => {
        const scoreEl = document.getElementById('clarifai-score');
        const loaderEl = document.getElementById('clarifai-loader');
        if (scoreEl.textContent !== '--' || loaderEl.style.display === 'block') {
            return;
        }
        document.getElementById('clarifai-summary').style.display = 'none';
        loaderEl.style.display = 'block';
        scoreEl.style.display = 'none';
        
        chrome.runtime.sendMessage({ action: "analyzePage", url: window.location.href });
    });
}

chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {
    if (request.action === "updateWidget") {
        updateWidgetUI(request.data);
    } else if (request.action === "widgetError") {
        displayWidgetError(request.message);
    }
});

function updateWidgetUI(data) {
    const scoreEl = document.getElementById('clarifai-score');
    const scoreContainerEl = document.getElementById('clarifai-score-container');
    const loaderEl = document.getElementById('clarifai-loader');
    const summaryEl = document.getElementById('clarifai-summary');
    const detailsToggleEl = document.getElementById('clarifai-details-toggle');
    const detailsPanelEl = document.getElementById('clarifai-details-panel');

    if (!scoreEl) return;

    // --- Update Main Display ---
    loaderEl.style.display = 'none';
    scoreEl.style.display = 'block';
    summaryEl.style.display = 'block';
    detailsToggleEl.style.display = 'block';

    const results = data.analysis_results;
    const score = results.final_score;
    const breakdown = results.breakdown;

    scoreEl.textContent = score;
    summaryEl.textContent = breakdown.end_of_life_advice;
    
    // --- Set Colors Based on Score ---
    let scoreColor = '#7f8c8d'; // Default grey
    if (score >= 75) scoreColor = '#27ae60'; // Green
    else if (score >= 50) scoreColor = '#f39c12'; // Yellow
    else scoreColor = '#e74c3c'; // Red
    scoreContainerEl.style.borderColor = scoreColor;
    scoreEl.style.color = scoreColor;

    // --- Populate the Hidden Details Panel ---
    detailsPanelEl.innerHTML = `
        <div class="clarifai-detail-item">
            <span class="clarifai-detail-label">Carbon (Material):</span>
            <span class="clarifai-detail-value">${breakdown.material_carbon_footprint_kgCO2} kg CO₂</span>
        </div>
        <div class="clarifai-detail-item">
            <span class="clarifai-detail-label">Carbon (Transport):</span>
            <span class="clarifai-detail-value">${breakdown.transportation_carbon_footprint_kgCO2} kg CO₂</span>
        </div>
        <div class="clarifai-detail-item">
            <span class="clarifai-detail-label">Water Usage:</span>
            <span class="clarifai-detail-value">${breakdown.material_water_usage_L} L</span>
        </div>
        <div class="clarifai-detail-item">
            <span class="clarifai-detail-label">End of Life Score:</span>
            <span class="clarifai-detail-value">${breakdown.end_of_life_score} / 100</span>
        </div>
        <div class="clarifai-detail-item">
            <span class="clarifai-detail-label">Origin:</span>
            <span class="clarifai-detail-value">${breakdown.manufacturing_location_factor}</span>
        </div>
    `;

    // --- Add Click Listener for the "Show/Hide Details" Toggle ---
    let detailsVisible = false;
    detailsToggleEl.onclick = () => {
        detailsVisible = !detailsVisible;
        detailsPanelEl.style.display = detailsVisible ? 'block' : 'none';
        detailsToggleEl.textContent = detailsVisible ? 'Hide Details' : 'Show Details';
    };
}

function displayWidgetError(message) {
    const loaderEl = document.getElementById('clarifai-loader');
    const errorEl = document.getElementById('clarifai-error');
    const summaryEl = document.getElementById('clarifai-summary');
    const scoreEl = document.getElementById('clarifai-score');

    if (!loaderEl || !errorEl) return;

    loaderEl.style.display = 'none';
    scoreEl.style.display = 'none';
    summaryEl.style.display = 'none';
    errorEl.style.display = 'block';
    errorEl.textContent = `Error: ${message}`;
>>>>>>> 2ae3776 (Initial commit for deployment)
}