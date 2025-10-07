"""Flask preview UI for spreadsheet copilot."""

import os
import json
import requests
from pathlib import Path

from flask import Flask, render_template, request, jsonify, redirect, url_for
import pandas as pd

app = Flask(__name__)

# Configuration
API_BASE_URL = os.getenv("API_BASE_URL", "http://localhost:8000")
UPLOAD_DIR = Path("uploads")


@app.route("/")
def index():
    """Main page showing file list and upload form."""
    return render_template("index.html")


@app.route("/files")
def get_files():
    """Get list of uploaded files."""
    try:
        response = requests.get(f"{API_BASE_URL}/files")
        return jsonify(response.json())
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/samples")
def get_samples():
    """Get list of sample files."""
    try:
        response = requests.get(f"{API_BASE_URL}/samples")
        return jsonify(response.json())
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/load-sample", methods=["POST"])
def load_sample():
    """Load a sample file."""
    filename = request.form.get("filename")
    try:
        response = requests.post(
            f"{API_BASE_URL}/load-sample",
            data={"filename": filename}
        )
        return jsonify(response.json())
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/preview/<filename>")
def preview_file(filename):
    """Preview a CSV file."""
    file_path = UPLOAD_DIR / filename
    
    if not file_path.exists():
        return "File not found", 404
    
    # Read CSV and convert to HTML
    df = pd.read_csv(file_path)
    
    # Get basic stats
    stats = {
        "rows": len(df),
        "columns": len(df.columns),
        "column_names": df.columns.tolist(),
        "missing_values": df.isnull().sum().to_dict()
    }
    
    return render_template(
        "preview.html",
        filename=filename,
        stats=stats,
        table=df.to_html(classes="table table-striped table-bordered", index=False),
        data_head=df.head(10).to_html(classes="table table-striped table-bordered", index=False)
    )


@app.route("/analyze/<filename>", methods=["GET", "POST"])
def analyze_file(filename):
    """Analyze a CSV file."""
    if request.method == "GET":
        return render_template("analyze.html", filename=filename)
    
    # POST: Run analysis
    prompt = request.form.get("prompt", "")
    
    try:
        response = requests.post(
            f"{API_BASE_URL}/analyze",
            data={"filename": filename, "prompt": prompt}
        )
        
        if response.status_code == 200:
            result = response.json()
            return render_template(
                "results.html",
                filename=filename,
                action_plan=result["action_plan"],
                raw_json=json.dumps(result, indent=2)
            )
        else:
            return f"Analysis failed: {response.text}", response.status_code
            
    except Exception as e:
        return f"Error: {str(e)}", 500


@app.route("/diff/<filename>")
def diff_view(filename):
    """Show diff view (before/after comparison)."""
    # This is a stub for now - would show original vs transformed data
    return render_template("diff.html", filename=filename)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
