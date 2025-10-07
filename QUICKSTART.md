# Quick Start Guide

This guide will help you get started with the Spreadsheet Copilot in less than 5 minutes.

## Prerequisites

- Python 3.8 or higher
- Google AI API key ([Get one here](https://makersuite.google.com/app/apikey))

## Step 1: Setup Environment

```bash
# Clone the repository (if not already done)
git clone https://github.com/jaganraajan/spreadsheet-copilot-vertex-ai.git
cd spreadsheet-copilot-vertex-ai

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

## Step 2: Configure API Key

```bash
# Copy the example environment file
cp .env.example .env

# Edit .env and add your Google AI API key
# GOOGLE_API_KEY=your_actual_api_key_here
```

Or set it directly:
```bash
export GOOGLE_API_KEY="your_actual_api_key_here"
```

## Step 3: Start the Servers

### Option A: Using the convenience scripts

**Terminal 1 - FastAPI Server:**
```bash
./run_api.sh
```

**Terminal 2 - Flask UI:**
```bash
./run_ui.sh
```

### Option B: Manual start

**Terminal 1 - FastAPI Server:**
```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

**Terminal 2 - Flask UI:**
```bash
python preview_ui.py
```

## Step 4: Use the Application

1. **Open the Web UI:**
   - Navigate to http://localhost:5000 in your browser

2. **Load a Sample File:**
   - Click "Load" next to any sample file (e.g., sales_data.csv)
   - Or upload your own CSV file

3. **Preview the Data:**
   - Click "Preview" to see the data structure and statistics

4. **Analyze with AI:**
   - Click "Analyze" to get AI-powered recommendations
   - Optionally provide a custom prompt for specific analysis
   - Click "Run Analysis" to get action plan from Gemini AI

5. **Review Results:**
   - See the detailed analysis, recommended actions, and priorities
   - Execute tool stubs to see their structure

## API Quick Reference

### Upload a CSV
```bash
curl -X POST -F "file=@your_file.csv" http://localhost:8000/upload
```

### Analyze a File
```bash
curl -X POST \
  -F "filename=sales_data.csv" \
  -F "prompt=Analyze sales trends" \
  http://localhost:8000/analyze
```

### Execute a Tool
```bash
curl -X POST \
  -F "tool_name=apply_formula" \
  -F 'parameters={"column":"Sales","formula":"=SUM(Sales)"}' \
  http://localhost:8000/execute-tool
```

### List Files
```bash
curl http://localhost:8000/files
```

### Load Sample
```bash
curl -X POST -F "filename=sales_data.csv" http://localhost:8000/load-sample
```

## Explore API Documentation

Visit http://localhost:8000/docs for interactive API documentation powered by Swagger UI.

## Sample Files Included

- **sales_data.csv**: Sales transactions by product, category, and region
- **employee_data.csv**: Employee information with departments and salaries
- **inventory.csv**: Product inventory with reorder levels

## Troubleshooting

### Issue: "GOOGLE_API_KEY environment variable is not set"
**Solution:** Make sure you've created a `.env` file with your API key or exported it in your shell.

### Issue: Port already in use
**Solution:** Change the port in the run commands:
- FastAPI: `uvicorn app.main:app --reload --port 8001`
- Flask: Edit `preview_ui.py` and change `port=5000` to `port=5001`

### Issue: Module not found
**Solution:** Make sure you've activated the virtual environment and installed dependencies:
```bash
source venv/bin/activate
pip install -r requirements.txt
```

## Next Steps

- Implement actual tool execution logic in `app/tools.py`
- Customize the AI prompt in `app/gemini_service.py`
- Add authentication and user management
- Deploy to production with proper WSGI/ASGI servers

## Need Help?

- Check the [README.md](README.md) for detailed documentation
- Review API docs at http://localhost:8000/docs
- File an issue on GitHub
