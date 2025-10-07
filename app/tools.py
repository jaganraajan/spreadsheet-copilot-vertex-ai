"""Tool stubs for spreadsheet operations."""

from typing import Dict, Any, List


def apply_formula(
    column: str,
    formula: str,
    target_column: str = None,
    description: str = ""
) -> Dict[str, Any]:
    """
    Apply a formula to a column in the spreadsheet.
    
    Args:
        column: Source column name
        formula: Formula to apply (e.g., "=SUM(A:A)", "=A1*1.1")
        target_column: Target column for the result (optional, defaults to new column)
        description: Description of what the formula does
        
    Returns:
        Dictionary with operation details
    """
    return {
        "tool": "apply_formula",
        "status": "stub",
        "parameters": {
            "column": column,
            "formula": formula,
            "target_column": target_column or f"{column}_formula",
            "description": description
        },
        "message": "Formula application stub - not yet implemented"
    }


def create_pivot(
    index_columns: List[str],
    value_column: str,
    aggregation: str = "sum",
    columns: List[str] = None
) -> Dict[str, Any]:
    """
    Create a pivot table from the spreadsheet data.
    
    Args:
        index_columns: Columns to use as pivot index
        value_column: Column to aggregate
        aggregation: Aggregation function (sum, mean, count, etc.)
        columns: Columns to pivot (optional)
        
    Returns:
        Dictionary with operation details
    """
    return {
        "tool": "create_pivot",
        "status": "stub",
        "parameters": {
            "index_columns": index_columns,
            "value_column": value_column,
            "aggregation": aggregation,
            "columns": columns or []
        },
        "message": "Pivot table creation stub - not yet implemented"
    }


def conditional_format(
    column: str,
    condition: str,
    format_style: Dict[str, str],
    description: str = ""
) -> Dict[str, Any]:
    """
    Apply conditional formatting to a column.
    
    Args:
        column: Column name to format
        condition: Condition expression (e.g., ">100", "=='Active'")
        format_style: Formatting styles (e.g., {"color": "red", "background": "yellow"})
        description: Description of the formatting rule
        
    Returns:
        Dictionary with operation details
    """
    return {
        "tool": "conditional_format",
        "status": "stub",
        "parameters": {
            "column": column,
            "condition": condition,
            "format_style": format_style,
            "description": description
        },
        "message": "Conditional formatting stub - not yet implemented"
    }


# Tool registry for easy access
TOOLS = {
    "apply_formula": apply_formula,
    "create_pivot": create_pivot,
    "conditional_format": conditional_format
}


def execute_tool(tool_name: str, **kwargs) -> Dict[str, Any]:
    """
    Execute a tool by name with provided parameters.
    
    Args:
        tool_name: Name of the tool to execute
        **kwargs: Tool parameters
        
    Returns:
        Tool execution result
    """
    if tool_name not in TOOLS:
        return {
            "error": f"Unknown tool: {tool_name}",
            "available_tools": list(TOOLS.keys())
        }
    
    return TOOLS[tool_name](**kwargs)
