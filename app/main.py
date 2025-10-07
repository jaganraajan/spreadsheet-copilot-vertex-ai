"""FastAPI application for spreadsheet copilot."""

import os
import shutil
from pathlib import Path
from typing import List

from fastapi import FastAPI, File, UploadFile, HTTPException, Form
from fastapi.responses import JSONResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware

from app.schemas import AnalysisRequest, AnalysisResponse
from app.gemini_service import GeminiService
from app.tools import execute_tool, TOOLS

# Initialize FastAPI app
app = FastAPI(
    title="Spreadsheet Copilot API",
    description="AI-powered spreadsheet analysis using Google Gemini",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Create uploads directory
UPLOAD_DIR = Path("uploads")
UPLOAD_DIR.mkdir(exist_ok=True)

SAMPLES_DIR = Path("samples")
SAMPLES_DIR.mkdir(exist_ok=True)

# Initialize Gemini service (will be created on demand to avoid init errors)
gemini_service = None


def get_gemini_service():
    """Get or create Gemini service instance."""
    global gemini_service
    if gemini_service is None:
        try:
            gemini_service = GeminiService()
        except ValueError as e:
            raise HTTPException(
                status_code=500,
                detail=f"Gemini service initialization failed: {str(e)}"
            )
    return gemini_service


@app.get("/")
async def root():
    """Root endpoint."""
    return {
        "message": "Spreadsheet Copilot API",
        "docs": "/docs",
        "preview_ui": "http://localhost:5000 (run preview_ui.py separately)"
    }


@app.post("/upload")
async def upload_csv(file: UploadFile = File(...)):
    """
    Upload a CSV file for analysis.
    
    Args:
        file: CSV file to upload
        
    Returns:
        Upload confirmation with filename
    """
    if not file.filename.endswith('.csv'):
        raise HTTPException(status_code=400, detail="Only CSV files are allowed")
    
    # Save file
    file_path = UPLOAD_DIR / file.filename
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    
    return {
        "filename": file.filename,
        "status": "uploaded",
        "path": str(file_path)
    }


@app.post("/analyze", response_model=AnalysisResponse)
async def analyze_spreadsheet(
    filename: str = Form(...),
    prompt: str = Form(None)
):
    """
    Analyze an uploaded CSV file using Gemini AI.
    
    Args:
        filename: Name of the uploaded CSV file
        prompt: Optional user prompt for specific analysis
        
    Returns:
        ActionPlan with recommended actions
    """
    file_path = UPLOAD_DIR / filename
    
    if not file_path.exists():
        raise HTTPException(status_code=404, detail=f"File {filename} not found")
    
    # Get Gemini service and analyze
    service = get_gemini_service()
    action_plan = service.analyze_spreadsheet(str(file_path), prompt)
    
    return AnalysisResponse(
        action_plan=action_plan,
        filename=filename,
        status="completed"
    )


@app.post("/execute-tool")
async def execute_tool_endpoint(tool_name: str = Form(...), parameters: str = Form(...)):
    """
    Execute a specific tool.
    
    Args:
        tool_name: Name of the tool to execute
        parameters: JSON string of tool parameters
        
    Returns:
        Tool execution result
    """
    import json
    
    if tool_name not in TOOLS:
        raise HTTPException(
            status_code=400,
            detail=f"Unknown tool: {tool_name}. Available: {list(TOOLS.keys())}"
        )
    
    try:
        params = json.loads(parameters)
    except json.JSONDecodeError:
        raise HTTPException(status_code=400, detail="Invalid JSON in parameters")
    
    result = execute_tool(tool_name, **params)
    return result


@app.get("/files")
async def list_files():
    """List all uploaded CSV files."""
    files = []
    for file_path in UPLOAD_DIR.glob("*.csv"):
        files.append({
            "filename": file_path.name,
            "size": file_path.stat().st_size,
            "path": str(file_path)
        })
    return {"files": files}


@app.get("/samples")
async def list_samples():
    """List all sample CSV files."""
    samples = []
    for file_path in SAMPLES_DIR.glob("*.csv"):
        samples.append({
            "filename": file_path.name,
            "size": file_path.stat().st_size,
            "path": str(file_path)
        })
    return {"samples": samples}


@app.post("/load-sample")
async def load_sample(filename: str = Form(...)):
    """
    Load a sample CSV file to uploads directory.
    
    Args:
        filename: Name of the sample file to load
        
    Returns:
        Load confirmation
    """
    sample_path = SAMPLES_DIR / filename
    
    if not sample_path.exists():
        raise HTTPException(status_code=404, detail=f"Sample {filename} not found")
    
    # Copy to uploads
    upload_path = UPLOAD_DIR / filename
    shutil.copy(sample_path, upload_path)
    
    return {
        "filename": filename,
        "status": "loaded",
        "message": f"Sample {filename} loaded to uploads"
    }


@app.get("/download/{filename}")
async def download_file(filename: str):
    """
    Download an uploaded CSV file.
    
    Args:
        filename: Name of the file to download
        
    Returns:
        File download response
    """
    file_path = UPLOAD_DIR / filename
    
    if not file_path.exists():
        raise HTTPException(status_code=404, detail=f"File {filename} not found")
    
    return FileResponse(file_path, filename=filename)


@app.get("/tools")
async def list_tools():
    """List available tools."""
    return {
        "tools": [
            {
                "name": "apply_formula",
                "description": "Apply formulas to columns"
            },
            {
                "name": "create_pivot",
                "description": "Create pivot tables"
            },
            {
                "name": "conditional_format",
                "description": "Apply conditional formatting"
            }
        ]
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
