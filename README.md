# Spreadsheet Copilot with Google Gemini AI

AI-powered spreadsheet analysis tool using FastAPI and Google Gemini AI. Upload CSV files, get intelligent analysis, and receive actionable recommendations for data transformations.

## Features

- 📊 **CSV Upload**: Upload and manage CSV files through a REST API
- 🤖 **AI Analysis**: Leverage Google Gemini AI for intelligent spreadsheet analysis
- 🛠️ **Tool Stubs**: Ready-to-implement functions for:
  - `apply_formula`: Apply formulas and calculations
  - `create_pivot`: Generate pivot tables
  - `conditional_format`: Apply conditional formatting rules
- 🎨 **Preview UI**: Flask-based web interface for file management and visualization
- 📁 **Sample Data**: One-click loader for sample CSV files
- 🔄 **Diff View**: Compare original vs transformed data (coming soon)

## Project Structure

```
.
├── app/
│   ├── __init__.py
│   ├── main.py              # FastAPI application
│   ├── schemas.py           # Pydantic schemas (ActionPlan, etc.)
│   ├── gemini_service.py    # Google Gemini AI integration
│   └── tools.py             # Tool stubs (apply_formula, etc.)
├── templates/               # Flask HTML templates
│   ├── base.html
│   ├── index.html
│   ├── preview.html
│   ├── analyze.html
│   ├── results.html
│   └── diff.html
├── samples/                 # Sample CSV files
│   ├── sales_data.csv
│   ├── employee_data.csv
│   └── inventory.csv
├── uploads/                 # Uploaded CSV files
├── preview_ui.py            # Flask preview UI application
└── requirements.txt         # Python dependencies
```

## Setup

### Prerequisites

- Python 3.8+
- Google AI API Key (for Gemini)

### Installation

1. Clone the repository:
```bash
git clone https://github.com/jaganraajan/spreadsheet-copilot-vertex-ai.git
cd spreadsheet-copilot-vertex-ai
```

2. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Set up environment variables:
```bash
# Create a .env file in the root directory
echo "GOOGLE_API_KEY=your_api_key_here" > .env
```

Get your Google AI API key from: https://makersuite.google.com/app/apikey

## Usage

### Option 1: Using Docker (Recommended)

The easiest way to run both servers:

```bash
# Make sure GOOGLE_API_KEY is in your .env file
docker-compose up
```

This will start both the FastAPI server (port 8000) and Flask UI (port 5000).

### Option 2: Using Convenience Scripts

**Terminal 1 - FastAPI Server:**
```bash
./run_api.sh
```

**Terminal 2 - Flask UI:**
```bash
./run_ui.sh
```

### Option 3: Manual Start

**Terminal 1 - FastAPI Server:**
```bash
# Start the FastAPI server
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

The API will be available at:
- API: http://localhost:8000
- Interactive API Docs: http://localhost:8000/docs
- Alternative API Docs: http://localhost:8000/redoc

**Terminal 2 - Preview UI:**
```bash
python preview_ui.py
```

The web UI will be available at: http://localhost:5000

### Using the Application

1. **Upload a CSV file**:
   - Via UI: Go to http://localhost:5000 and use the upload form
   - Via API: POST to http://localhost:8000/upload

2. **Load sample data**:
   - Click "Load" next to any sample file in the UI
   - Or use the `/load-sample` endpoint

3. **Analyze a file**:
   - Click "Analyze" next to a file in the UI
   - Or POST to `/analyze` with filename and optional prompt

4. **View results**:
   - See AI-generated analysis and recommended actions
   - Execute tool stubs to see their structure

## API Endpoints

### Core Endpoints

- `GET /` - API information
- `POST /upload` - Upload a CSV file
- `POST /analyze` - Analyze a CSV with Gemini AI
- `POST /execute-tool` - Execute a tool stub
- `GET /files` - List uploaded files
- `GET /samples` - List sample files
- `POST /load-sample` - Load a sample file to uploads
- `GET /download/{filename}` - Download a file
- `GET /tools` - List available tools

### Example: Upload and Analyze

```bash
# Upload a file
curl -X POST "http://localhost:8000/upload" \
  -F "file=@sales_data.csv"

# Analyze it
curl -X POST "http://localhost:8000/analyze" \
  -F "filename=sales_data.csv" \
  -F "prompt=Focus on sales trends by region"
```

## Response Schema: ActionPlan

The Gemini AI returns structured responses following the `ActionPlan` schema:

```python
{
    "analysis": "Detailed analysis of the spreadsheet",
    "recommended_actions": [
        {
            "tool_name": "apply_formula",
            "parameters": {"column": "Sales", "formula": "=SUM(Sales)"},
            "reasoning": "Calculate total sales"
        }
    ],
    "summary": "Brief summary of recommendations",
    "priority": "high"  # or "medium", "low"
}
```

## Tool Stubs

### apply_formula
Apply formulas to spreadsheet columns.

```python
apply_formula(
    column="Sales",
    formula="=A1*1.1",
    target_column="Sales_With_Tax",
    description="Add 10% tax"
)
```

### create_pivot
Create pivot tables for data summarization.

```python
create_pivot(
    index_columns=["Region", "Product"],
    value_column="Sales",
    aggregation="sum"
)
```

### conditional_format
Apply conditional formatting rules.

```python
conditional_format(
    column="Quantity",
    condition="<30",
    format_style={"color": "red", "background": "yellow"},
    description="Highlight low stock items"
)
```

## Development

### Running Tests

```bash
# Install dev dependencies
pip install pytest pytest-asyncio httpx

# Run tests (when implemented)
pytest
```

### Code Style

The project follows standard Python conventions. Format code with:

```bash
pip install black
black .
```

## Technologies Used

- **FastAPI**: Modern, fast web framework for building APIs
- **Flask**: Lightweight web application for the preview UI
- **Google Generative AI**: Gemini AI model for intelligent analysis
- **Pandas**: Data manipulation and analysis
- **Pydantic**: Data validation and settings management
- **Uvicorn**: ASGI server for FastAPI

## Future Enhancements

- [ ] Implement actual tool execution (currently stubs)
- [ ] Add diff view with before/after comparison
- [ ] Support for Excel files (.xlsx)
- [ ] Real-time collaboration features
- [ ] Export analysis reports
- [ ] Advanced visualization options
- [ ] User authentication and file management

## License

MIT License

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.