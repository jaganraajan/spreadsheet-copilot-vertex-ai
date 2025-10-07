"""
Simple tests for the FastAPI application.

To run these tests:
1. Install test dependencies: pip install pytest pytest-asyncio httpx
2. Run tests: pytest test_api.py -v
"""

import pytest
from fastapi.testclient import TestClient
from pathlib import Path
import json

from app.main import app
from app.tools import apply_formula, create_pivot, conditional_format


client = TestClient(app)


class TestAPIEndpoints:
    """Test API endpoints."""
    
    def test_root(self):
        """Test root endpoint."""
        response = client.get("/")
        assert response.status_code == 200
        data = response.json()
        assert "message" in data
        assert "Spreadsheet Copilot" in data["message"]
    
    def test_list_tools(self):
        """Test tools listing endpoint."""
        response = client.get("/tools")
        assert response.status_code == 200
        data = response.json()
        assert "tools" in data
        assert len(data["tools"]) == 3
        tool_names = [tool["name"] for tool in data["tools"]]
        assert "apply_formula" in tool_names
        assert "create_pivot" in tool_names
        assert "conditional_format" in tool_names
    
    def test_list_samples(self):
        """Test samples listing endpoint."""
        response = client.get("/samples")
        assert response.status_code == 200
        data = response.json()
        assert "samples" in data
        # Should have at least the sample files we created
        assert len(data["samples"]) >= 3
    
    def test_list_files_empty(self):
        """Test files listing when no files uploaded."""
        response = client.get("/files")
        assert response.status_code == 200
        data = response.json()
        assert "files" in data
        assert isinstance(data["files"], list)


class TestTools:
    """Test tool stubs."""
    
    def test_apply_formula(self):
        """Test apply_formula tool stub."""
        result = apply_formula(
            column="Sales",
            formula="=SUM(A:A)",
            description="Calculate total"
        )
        assert result["tool"] == "apply_formula"
        assert result["status"] == "stub"
        assert "parameters" in result
        assert result["parameters"]["column"] == "Sales"
        assert result["parameters"]["formula"] == "=SUM(A:A)"
    
    def test_create_pivot(self):
        """Test create_pivot tool stub."""
        result = create_pivot(
            index_columns=["Region"],
            value_column="Sales",
            aggregation="sum"
        )
        assert result["tool"] == "create_pivot"
        assert result["status"] == "stub"
        assert "parameters" in result
        assert result["parameters"]["index_columns"] == ["Region"]
        assert result["parameters"]["aggregation"] == "sum"
    
    def test_conditional_format(self):
        """Test conditional_format tool stub."""
        result = conditional_format(
            column="Quantity",
            condition=">100",
            format_style={"color": "red"},
            description="Highlight high values"
        )
        assert result["tool"] == "conditional_format"
        assert result["status"] == "stub"
        assert "parameters" in result
        assert result["parameters"]["column"] == "Quantity"
        assert result["parameters"]["condition"] == ">100"


class TestSchemas:
    """Test Pydantic schemas."""
    
    def test_action_plan_schema(self):
        """Test ActionPlan schema validation."""
        from app.schemas import ActionPlan, ToolCall
        
        tool_call = ToolCall(
            tool_name="apply_formula",
            parameters={"column": "Sales", "formula": "=SUM(A:A)"},
            reasoning="Calculate totals"
        )
        
        action_plan = ActionPlan(
            analysis="Test analysis",
            recommended_actions=[tool_call],
            summary="Test summary",
            priority="high"
        )
        
        assert action_plan.analysis == "Test analysis"
        assert len(action_plan.recommended_actions) == 1
        assert action_plan.priority == "high"
    
    def test_tool_call_schema(self):
        """Test ToolCall schema validation."""
        from app.schemas import ToolCall
        
        tool_call = ToolCall(
            tool_name="create_pivot",
            parameters={"index": "Region"},
            reasoning="Summarize by region"
        )
        
        assert tool_call.tool_name == "create_pivot"
        assert tool_call.parameters["index"] == "Region"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
