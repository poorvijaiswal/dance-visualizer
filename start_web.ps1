Write-Host "=== Dance Visualizer Web Interface ===" -ForegroundColor Green

# Check if we're in the right directory
if (-not (Test-Path "web_interface.py")) {
    Write-Host "Error: web_interface.py not found!" -ForegroundColor Red
    Write-Host "Make sure you're in the dance_visualiser directory" -ForegroundColor Yellow
    exit 1
}

# Activate virtual environment if it exists
if (Test-Path "venv\Scripts\Activate.ps1") {
    Write-Host "Activating virtual environment..." -ForegroundColor Yellow
    & "venv\Scripts\Activate.ps1"
}

# Check if Streamlit is installed
try {
    python -c "import streamlit" 2>$null
    Write-Host "Streamlit found!" -ForegroundColor Green
} catch {
    Write-Host "Installing Streamlit..." -ForegroundColor Yellow
    pip install streamlit
}

# Check for available ports
$port = 8501
$portInUse = Get-NetTCPConnection -LocalPort $port -ErrorAction SilentlyContinue
if ($portInUse) {
    Write-Host "Port 8501 is in use, trying 8502..." -ForegroundColor Yellow
    $port = 8502
}

Write-Host "Starting Streamlit server on port $port..." -ForegroundColor Cyan
Write-Host "Open your browser to: http://localhost:$port" -ForegroundColor Green
Write-Host "Press Ctrl+C to stop the server" -ForegroundColor Gray

# Start Streamlit
streamlit run web_interface.py --server.port $port --server.address localhost
