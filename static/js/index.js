// Configuration
const API_BASE_URL = '';
let currentResults = null;
let currentStep = 0;
let isPlaying = false;
let playInterval = null;
let speed = 500; // ms per step

// DOM Elements
const algorithmForm = document.getElementById('algorithmForm');
const screen = document.getElementById('screen');
const loading = document.getElementById('loading');
const errorMessage = document.getElementById('errorMessage');
const stepNavigation = document.getElementById('stepNavigation');
const prevStepBtn = document.getElementById('prevStep');
const nextStepBtn = document.getElementById('nextStep');
const playPauseBtn = document.getElementById('playPause');
const currentStepSpan = document.getElementById('currentStep');
const totalStepsSpan = document.getElementById('totalSteps');
const comparisonChartCanvas = document.getElementById('comparisonChart');
const randomBtn = document.getElementById('randomBtn');
const speedSelect = document.getElementById('speed');

// Initialize
document.addEventListener('DOMContentLoaded', () => {
    // Setup algorithm selection
    setupAlgorithmSelection();
    
    // Setup event listeners
    setupEventListeners();
    
    // Load algorithm info
    loadAlgorithmInfo();
});

function setupAlgorithmSelection() {
    const algorithmOptions = document.querySelectorAll('.algorithm-option');
    algorithmOptions.forEach(option => {
        option.addEventListener('click', () => {
            option.classList.toggle('selected');
        });
    });
}

function setupEventListeners() {
    // Form submission
    algorithmForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        await runAlgorithms();
    });
    
    // Random button
    randomBtn.addEventListener('click', generateRandomInput);
    
    // Sample inputs
    document.querySelectorAll('.sample-btn').forEach(btn => {
        btn.addEventListener('click', () => {
            const refString = btn.getAttribute('data-input');
            const frames = btn.getAttribute('data-frames');
            document.getElementById('referenceString').value = refString;
            document.getElementById('frames').value = frames;
        });
    });
    
    // Step navigation
    prevStepBtn.addEventListener('click', () => changeStep(-1));
    nextStepBtn.addEventListener('click', () => changeStep(1));
    playPauseBtn.addEventListener('click', togglePlay);
    
    // Speed selection
    speedSelect.addEventListener('change', updateSpeed);
}

// Function to display the graph in screen-1
function displayComparisonGraph(graphBase64) {
    const screen1 = document.getElementById('screen-1');
    const graphPlaceholder = document.getElementById('graph-placeholder');
    const graphImage = document.getElementById('comparison-graph');
    
    if (graphBase64) {
        // Show graph image
        graphImage.src = `data:image/png;base64,${graphBase64}`;
        graphImage.style.display = 'block';
        graphPlaceholder.style.display = 'none';
        
        // Add download button
        addDownloadButton(graphBase64);
    } else {
        // Show placeholder
        graphImage.style.display = 'none';
        graphPlaceholder.style.display = 'block';
        graphPlaceholder.innerHTML = '<p>Could not generate graph. Running algorithms...</p>';
    }
}

// Function to add download button for graph
function addDownloadButton(graphBase64) {
    let existingBtn = document.getElementById('download-graph-btn');
    if (existingBtn) {
        existingBtn.remove();
    }
    
    const downloadBtn = document.createElement('button');
    downloadBtn.id = 'download-graph-btn';
    downloadBtn.className = 'btn';
    downloadBtn.innerHTML = '<i class="fas fa-download"></i> Download Graph';
    downloadBtn.style.marginTop = '15px';
    
    downloadBtn.addEventListener('click', () => {
        // Create download link
        const link = document.createElement('a');
        link.href = `data:image/png;base64,${graphBase64}`;
        link.download = 'page_fault_comparison.png';
        link.click();
    });
    
    document.getElementById('screen-1').appendChild(downloadBtn);
}

async function runAlgorithms() {
    // Get form data
    const frames = parseInt(document.getElementById('frames').value);
    const referenceString = document.getElementById('referenceString').value;
    
    // Get selected algorithms
    const selectedAlgorithms = [];
    document.querySelectorAll('.algorithm-option.selected').forEach(option => {
        selectedAlgorithms.push(option.getAttribute('data-algo'));
    });
    
    if (selectedAlgorithms.length === 0) {
        showError('Please select at least one algorithm');
        return;
    }
    
    // Validate input
    if (!referenceString.trim()) {
        showError('Please enter a reference string');
        return;
    }
    
    // Show loading
    showLoading(true);
    hideError();
    
    try {
        // Call API
        const response = await fetch(`${API_BASE_URL}/api/calculate`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                frames: frames,
                reference_string: referenceString,
                algorithms: selectedAlgorithms
            })
        });
        
        console.log("Response status:", response.status); // Add this
        const data = await response.json();
        console.log("API Response:", data); // Add this to see what's returned
        
        if (data.error) {
            showError(data.error);
            return;
        }
        
        // Store results
        currentResults = data.results;
        
        // Display results
        displayResults(data);

        if (data.graph) {
            displayComparisonGraph(data.graph);
        }
        
        // Setup step navigation
        setupStepNavigation(data.total_pages);
        
    } catch (error) {
        showError('Failed to connect to server: ' + error.message);
    } finally {
        showLoading(false);
    }
}

// Function to display detailed results
function displayResults(data) {
    screen.innerHTML = '';
    
    // Display input summary
    const inputSummary = document.createElement('div');
    inputSummary.className = 'input-summary';
    inputSummary.innerHTML = `
        <h3><i class="fas fa-info-circle"></i> Input Summary</h3>
        <div class="summary-box">
            <p><strong>Reference String:</strong> ${data.input.reference_string}</p>
            <p><strong>Number of Frames:</strong> ${data.input.frames}</p>
            <p><strong>Total Pages:</strong> ${data.input.total_pages}</p>
        </div>
    `;
    screen.appendChild(inputSummary);
    
    // Display algorithm results
    for (const [algoName, algoData] of Object.entries(data.results)) {
        const algoSection = createAlgorithmSection(algoName, algoData);
        screen.appendChild(algoSection);
    }
    
    // Display step-by-step data if available
    if (data.step_by_step) {
        displayStepByStep(data.step_by_step);
    }
}

function createAlgorithmSection(algoName, algoData) {
    const section = document.createElement('div');
    section.className = 'algorithm-result';

    const header = document.createElement('h3');
    header.innerHTML = `<i class="fas fa-project-diagram"></i> ${algoData.name} Results`;
    section.appendChild(header);

    // --- SAFEGUARD: Ensure history exists ---
    const history = algoData.history || []; 

    // Statistics
    const statsBox = document.createElement('div');
    statsBox.className = 'stats-box';
    statsBox.innerHTML = `
        <div class="stat-item">
            <div class="stat-label">Page Faults</div>
            <div class="stat-value">${algoData.page_faults || 0}</div>
        </div>
        <div class="stat-item">
            <div class="stat-label">Fault Rate</div>
            <div class="stat-value">${((algoData.page_fault_rate || 0) * 100).toFixed(1)}%</div>
        </div>
        <div class="stat-item">
            <div class="stat-label">Pages</div>
            <div class="stat-value">${history.length}</div>
        </div>
    `;
    section.appendChild(statsBox);

    // Page table
    const pageTableSection = document.createElement('div');
    pageTableSection.className = 'page-table';
    pageTableSection.innerHTML = '<h4>Step-by-Step Page Table</h4>';

    const table = document.createElement('table');

    // Create header row
    const headerRow = document.createElement('tr');
    headerRow.innerHTML = '<th>Step</th><th>Page</th>';
    // Parse frames safely
    const frameCount = parseInt(document.getElementById('frames').value) || 3;
    
    for (let i = 0; i < frameCount; i++) {
        headerRow.innerHTML += `<th>Frame ${i + 1}</th>`;
    }
    headerRow.innerHTML += '<th>Fault</th><th>Replaced</th>';
    table.appendChild(headerRow);

    // Create data rows
    history.forEach((step, index) => {
        const row = document.createElement('tr');
        row.innerHTML = `
            <td>${index + 1}</td>
            <td><strong>${step.page}</strong></td>
        `;

        // --- SAFEGUARD: Ensure memory exists ---
        const memory = step.memory || [];

        // Frame cells
        for (let i = 0; i < frameCount; i++) {
            if (i < memory.length) {
                row.innerHTML += `<td>${memory[i]}</td>`;
            } else {
                row.innerHTML += '<td>-</td>';
            }
        }

        // Fault and replaced cells
        const faultCell = step.fault ?
            `<td class="page-fault"><i class="fas fa-times"></i> Fault</td>` :
            `<td class="page-hit"><i class="fas fa-check"></i> Hit</td>`;

        const replacedCell = step.replaced ?
            `<td><i class="fas fa-exchange-alt"></i> ${step.replaced}</td>` :
            '<td>-</td>';

        row.innerHTML += faultCell + replacedCell;
        table.appendChild(row);
    });

    pageTableSection.appendChild(table);
    section.appendChild(pageTableSection);

    return section;
}

// Function to display step-by-step data
function displayStepByStep(stepData) {
    const stepSection = document.createElement('div');
    stepSection.className = 'step-by-step-section';
    stepSection.innerHTML = '<h3><i class="fas fa-list-ol"></i> Step-by-Step Execution</h3>';
    
    // Create tabs for each algorithm
    const tabsContainer = document.createElement('div');
    tabsContainer.className = 'algorithm-tabs';
    
    const contentContainer = document.createElement('div');
    contentContainer.className = 'algorithm-tabs-content';
    
    for (const [algoName, algoData] of Object.entries(stepData)) {
        // Create tab button
        const tabButton = document.createElement('button');
        tabButton.className = 'tab-button';
        tabButton.textContent = algoName.toUpperCase();
        tabButton.addEventListener('click', (e) => showAlgorithmSteps(algoName, algoData, e.target));
        tabsContainer.appendChild(tabButton);
        
        // Create content pane
        const contentPane = document.createElement('div');
        contentPane.className = 'tab-pane';
        contentPane.id = `pane-${algoName}`;
        contentPane.style.display = 'none';
        contentContainer.appendChild(contentPane);
    }
    
    stepSection.appendChild(tabsContainer);
    stepSection.appendChild(contentContainer);
    screen.appendChild(stepSection);
    
    // Show first algorithm by default
    const firstAlgo = Object.keys(stepData)[0];
    if (firstAlgo) {
        showAlgorithmSteps(firstAlgo, stepData[firstAlgo]);
        document.querySelector('.tab-button').classList.add('active');
    }
}

function showAlgorithmSteps(algoName, algoData, clickedBtn = null) {
    const paneId = `pane-${algoName}`;
    const pane = document.getElementById(paneId);
    
    if (!pane) return;
    
    // Hide all panes
    document.querySelectorAll('.tab-pane').forEach(p => p.style.display = 'none');
    document.querySelectorAll('.tab-button').forEach(b => b.classList.remove('active'));
    
    // Show selected pane
    pane.style.display = 'block';
    if (clickedBtn) {
        clickedBtn.classList.add('active');
    }
    
    // Create step table
    pane.innerHTML = `
        <h4>${algoName.toUpperCase()} - Step-by-Step</h4>
        <div class="step-table-container">
            <table class="step-table">
                <thead>
                    <tr>
                        <th>Step</th>
                        <th>Page</th>
                        <th>Frames</th>
                        <th>Status</th>
                        <th>Action</th>
                    </tr>
                </thead>
                <tbody id="step-table-${algoName}">
                    <!-- Steps will be populated here -->
                </tbody>
            </table>
        </div>
    `;
    
    // If we have actual step data, populate it
    // For now, show a message
    const tbody = document.getElementById(`step-table-${algoName}`);
    tbody.innerHTML = `
        <tr>
            <td colspan="5" style="text-align: center; padding: 20px;">
                <p>Detailed step-by-step data would be shown here.</p>
                <p>Each step shows the page being accessed, the state of frames, 
                and whether it was a hit or fault.</p>
            </td>
        </tr>
    `;
}

function displayComparisonChart(chartUrl) {
    // Remove existing chart if any
    const existingChart = Chart.getChart('comparisonChart');
    if (existingChart) {
        existingChart.destroy();
    }
    
    // Create new chart
    const ctx = comparisonChartCanvas.getContext('2d');
}

function setupStepNavigation(totalSteps) {
    stepNavigation.style.display = 'flex';
    currentStep = 0;
    totalStepsSpan.textContent = totalSteps;
    updateStepControls();
}

function changeStep(delta) {
    if (!currentResults) return;
    
    const totalSteps = parseInt(totalStepsSpan.textContent);
    const newStep = currentStep + delta;
    
    if (newStep >= 0 && newStep < totalSteps) {
        currentStep = newStep;
        currentStepSpan.textContent = currentStep + 1;
        updateStepControls();
        highlightCurrentStep();
    }
}

function togglePlay() {
    if (!currentResults) return;
    
    if (isPlaying) {
        // Pause
        clearInterval(playInterval);
        playPauseBtn.innerHTML = '<i class="fas fa-play"></i> Play';
        isPlaying = false;
    } else {
        // Play
        playPauseBtn.innerHTML = '<i class="fas fa-pause"></i> Pause';
        isPlaying = true;
        
        const totalSteps = parseInt(totalStepsSpan.textContent);
        playInterval = setInterval(() => {
            if (currentStep < totalSteps - 1) {
                changeStep(1);
            } else {
                togglePlay();
            }
        }, speed);
    }
}

function updateStepControls() {
    const totalSteps = parseInt(totalStepsSpan.textContent);
    prevStepBtn.disabled = currentStep === 0;
    nextStepBtn.disabled = currentStep === totalSteps - 1;
}

function highlightCurrentStep() {
    // Highlight current step in all tables
    document.querySelectorAll('.page-table table tr').forEach((row, index) => {
        row.classList.remove('current-step-row');
        if (index === currentStep + 1) { // +1 for header row
            row.classList.add('current-step-row');
            row.style.backgroundColor = '#e3f2fd';
        }
    });
}

async function generateRandomInput() {
    showLoading(true);
    
    try {
        const response = await fetch(`${API_BASE_URL}/api/random?length=15`);
        const data = await response.json();
        
        document.getElementById('referenceString').value = data.reference_string;
        document.getElementById('frames').value = data.frames;
    } catch (error) {
        showError('Failed to generate random input');
    } finally {
        showLoading(false);
    }
}

async function loadAlgorithmInfo() {
    try {
        const response = await fetch(`${API_BASE_URL}/api/algorithms`);
        const data = await response.json();
        
        console.log('Algorithm info loaded:', data);
    } catch (error) {
        console.warn('Could not load algorithm info:', error);
    }
}

function updateSpeed() {
    const speedValue = speedSelect.value;
    switch(speedValue) {
        case 'fast': speed = 300; break;
        case 'medium': speed = 500; break;
        case 'slow': speed = 1000; break;
    }
    
    // Update interval if playing
    if (isPlaying) {
        clearInterval(playInterval);
        playInterval = setInterval(() => {
            if (currentStep < parseInt(totalStepsSpan.textContent) - 1) {
                changeStep(1);
            } else {
                togglePlay();
            }
        }, speed);
    }
}

// Utility functions
function showLoading(show) {
    loading.classList.toggle('active', show);
}

function showError(message) {
    errorMessage.textContent = message;
    errorMessage.classList.add('active');
}

function hideError() {
    errorMessage.classList.remove('active');
}

// Keyboard shortcuts
document.addEventListener('keydown', (e) => {
    if (!currentResults) return;
    
    switch(e.key) {
        case 'ArrowLeft':
            if (!prevStepBtn.disabled) changeStep(-1);
            break;
        case 'ArrowRight':
            if (!nextStepBtn.disabled) changeStep(1);
            break;
        case ' ':
            e.preventDefault();
            togglePlay();
            break;
    }
});