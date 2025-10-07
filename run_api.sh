#!/bin/bash
# Start the FastAPI server

echo "Starting FastAPI Spreadsheet Copilot API..."
echo "API will be available at: http://localhost:8000"
echo "API Docs: http://localhost:8000/docs"
echo ""

uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
