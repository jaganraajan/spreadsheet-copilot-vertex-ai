# Development Guide

This guide is for developers who want to contribute to or extend the Spreadsheet Copilot project.

## Project Architecture

### Directory Structure

```
spreadsheet-copilot-vertex-ai/
├── app/                        # FastAPI application
│   ├── __init__.py            # Package init
│   ├── main.py                # FastAPI app and endpoints
│   ├── schemas.py             # Pydantic models (ActionPlan, etc.)
│   ├── gemini_service.py      # Google Gemini AI integration
│   └── tools.py               # Tool implementations (stubs)
├── templates/                  # Flask HTML templates
│   ├── base.html              # Base template with navigation
│   ├── index.html             # Home page with upload
│   ├── preview.html           # CSV preview page
│   ├── analyze.html           # Analysis configuration page
│   ├── results.html           # Analysis results display
│   └── diff.html              # Diff view (placeholder)
├── samples/                    # Sample CSV files
├── uploads/                    # User uploaded files
├── preview_ui.py              # Flask preview application
├── requirements.txt           # Python dependencies
├── test_api.py                # Unit tests
├── .env.example               # Environment variables template
├── .gitignore                 # Git ignore rules
└── README.md                  # Main documentation
```

## Technology Stack

### Backend
- **FastAPI**: Modern, fast web framework with automatic API documentation
- **Pydantic**: Data validation using Python type hints
- **Pandas**: Data manipulation and analysis
- **Google Generative AI**: Gemini model integration
- **Uvicorn**: ASGI server for FastAPI

### Frontend
- **Flask**: Lightweight web application for UI
- **Bootstrap 5**: CSS framework for responsive design
- **Vanilla JavaScript**: Client-side interactions

## Development Setup

### 1. Clone and Setup

```bash
git clone https://github.com/jaganraajan/spreadsheet-copilot-vertex-ai.git
cd spreadsheet-copilot-vertex-ai
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 2. Install Development Dependencies

```bash
pip install pytest pytest-asyncio httpx black flake8 mypy
```

### 3. Configure Environment

```bash
cp .env.example .env
# Edit .env and add your GOOGLE_API_KEY
```

## Key Components

### 1. FastAPI Application (`app/main.py`)

The main API server with endpoints for:
- CSV file upload
- File listing and management
- AI analysis via Gemini
- Tool execution
- Sample file loading

**Adding a new endpoint:**

```python
@app.post("/your-endpoint")
async def your_endpoint(param: str = Form(...)):
    """Your endpoint description."""
    # Implementation
    return {"result": "data"}
```

### 2. Pydantic Schemas (`app/schemas.py`)

Data validation models using Pydantic.

**Adding a new schema:**

```python
class YourSchema(BaseModel):
    """Your schema description."""
    field1: str = Field(..., description="Field description")
    field2: Optional[int] = Field(None, description="Optional field")
```

### 3. Gemini Service (`app/gemini_service.py`)

Integration with Google Gemini AI model.

**Key methods:**
- `analyze_spreadsheet()`: Main analysis entry point
- `_create_data_summary()`: Generate data summary
- `_build_prompt()`: Build AI prompt
- `_parse_response()`: Parse AI response into ActionPlan

**Customizing the prompt:**

Edit the `_build_prompt()` method to change how the AI analyzes data.

### 4. Tool Stubs (`app/tools.py`)

Currently contains stub implementations. To make tools functional:

```python
def apply_formula(column: str, formula: str, target_column: str = None, description: str = ""):
    """Apply formula implementation."""
    # 1. Load the CSV file from uploads
    # 2. Apply the formula using pandas
    # 3. Save the result
    # 4. Return the modified data
    pass
```

**Tool registry:**

Tools are registered in the `TOOLS` dictionary for easy access:

```python
TOOLS = {
    "apply_formula": apply_formula,
    "create_pivot": create_pivot,
    "conditional_format": conditional_format,
    "your_new_tool": your_new_tool  # Add new tools here
}
```

### 5. Flask UI (`preview_ui.py`)

Web interface for visualizing data and results.

**Adding a new page:**

1. Add route in `preview_ui.py`:
```python
@app.route("/your-page/<filename>")
def your_page(filename):
    return render_template("your_page.html", filename=filename)
```

2. Create template in `templates/your_page.html`:
```html
{% extends "base.html" %}
{% block content %}
<!-- Your content -->
{% endblock %}
```

## Testing

### Running Tests

```bash
# Run all tests
pytest test_api.py -v

# Run specific test class
pytest test_api.py::TestAPIEndpoints -v

# Run with coverage
pip install pytest-cov
pytest test_api.py --cov=app --cov-report=html
```

### Writing Tests

Add tests to `test_api.py`:

```python
def test_your_feature(self):
    """Test your feature."""
    response = client.get("/your-endpoint")
    assert response.status_code == 200
    assert "expected_key" in response.json()
```

## Code Style

### Formatting

Use Black for code formatting:

```bash
black app/ preview_ui.py test_api.py
```

### Linting

Use Flake8 for linting:

```bash
flake8 app/ preview_ui.py --max-line-length=100
```

### Type Checking

Use mypy for type checking:

```bash
mypy app/ --ignore-missing-imports
```

## Common Development Tasks

### Adding a New Tool

1. Define the tool function in `app/tools.py`:
```python
def your_new_tool(param1: str, param2: int) -> Dict[str, Any]:
    """Your tool description."""
    return {
        "tool": "your_new_tool",
        "status": "stub",
        "parameters": {"param1": param1, "param2": param2}
    }
```

2. Add to the TOOLS registry:
```python
TOOLS = {
    # ...existing tools...
    "your_new_tool": your_new_tool
}
```

3. Update the tool list in `app/main.py`:
```python
@app.get("/tools")
async def list_tools():
    return {
        "tools": [
            # ...existing tools...
            {"name": "your_new_tool", "description": "Your tool description"}
        ]
    }
```

### Implementing Tool Execution

Currently, tools return stub responses. To implement actual execution:

1. Accept a DataFrame as input or load from file
2. Perform the operation using pandas
3. Save the result
4. Return the modified data

Example:
```python
import pandas as pd

def apply_formula(file_path: str, column: str, formula: str, **kwargs):
    # Load data
    df = pd.read_csv(file_path)
    
    # Apply formula (simplified example)
    if formula.startswith("=SUM"):
        result = df[column].sum()
    
    # Add result column
    df[f"{column}_result"] = result
    
    # Save
    output_path = file_path.replace(".csv", "_modified.csv")
    df.to_csv(output_path, index=False)
    
    return {
        "tool": "apply_formula",
        "status": "success",
        "output_file": output_path
    }
```

### Enhancing the AI Prompt

Modify `app/gemini_service.py` to improve AI analysis:

1. Add more data context in `_create_data_summary()`
2. Provide more specific tool examples in `_build_prompt()`
3. Add few-shot examples for better results
4. Fine-tune the response parsing in `_parse_response()`

### Adding File Format Support

To support Excel or other formats:

1. Update file upload validation in `app/main.py`
2. Add appropriate library (e.g., `openpyxl` for Excel)
3. Update file reading logic in `gemini_service.py`

```python
# Example: Excel support
if file_path.endswith('.xlsx'):
    df = pd.read_excel(file_path)
else:
    df = pd.read_csv(file_path)
```

## API Documentation

FastAPI automatically generates API documentation:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## Deployment

### Production Considerations

1. **Security:**
   - Add authentication (JWT, OAuth, etc.)
   - Validate file sizes and types
   - Sanitize file names
   - Rate limiting

2. **Performance:**
   - Use production ASGI server (gunicorn + uvicorn)
   - Add caching for analysis results
   - Implement background tasks for long operations

3. **Configuration:**
   - Use environment-specific configs
   - Secret management (not in .env)
   - Proper logging

### Docker Deployment

Create a `Dockerfile`:

```dockerfile
FROM python:3.11-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

Build and run:
```bash
docker build -t spreadsheet-copilot .
docker run -p 8000:8000 -e GOOGLE_API_KEY=your_key spreadsheet-copilot
```

## Troubleshooting

### Common Issues

1. **Import errors:** Make sure virtual environment is activated
2. **API key errors:** Verify GOOGLE_API_KEY is set correctly
3. **Port conflicts:** Change port in commands
4. **File not found:** Check file paths and working directory

## Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/your-feature`
3. Make changes and test
4. Format code: `black .`
5. Commit: `git commit -m "Add your feature"`
6. Push: `git push origin feature/your-feature`
7. Create Pull Request

## Resources

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [Pydantic Documentation](https://docs.pydantic.dev/)
- [Google AI Documentation](https://ai.google.dev/docs)
- [Pandas Documentation](https://pandas.pydata.org/docs/)
- [Flask Documentation](https://flask.palletsprojects.com/)
