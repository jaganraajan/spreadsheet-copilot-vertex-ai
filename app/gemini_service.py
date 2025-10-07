"""Gemini AI service for spreadsheet analysis."""

import os
import json
from typing import Optional
import google.generativeai as genai
import pandas as pd
from dotenv import load_dotenv

from app.schemas import ActionPlan, ToolCall

# Load environment variables
load_dotenv()


class GeminiService:
    """Service for interacting with Gemini AI model."""
    
    def __init__(self):
        """Initialize Gemini service with API key."""
        api_key = os.getenv("GOOGLE_API_KEY")
        if not api_key:
            raise ValueError("GOOGLE_API_KEY environment variable is not set")
        
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel('gemini-pro')
    
    def analyze_spreadsheet(
        self,
        csv_path: str,
        user_prompt: Optional[str] = None
    ) -> ActionPlan:
        """
        Analyze a CSV file and generate an action plan.
        
        Args:
            csv_path: Path to the CSV file
            user_prompt: Optional user prompt for specific analysis
            
        Returns:
            ActionPlan object with recommended actions
        """
        # Read and analyze CSV
        df = pd.read_csv(csv_path)
        
        # Create data summary
        data_summary = self._create_data_summary(df)
        
        # Build prompt for Gemini
        prompt = self._build_prompt(data_summary, user_prompt)
        
        # Generate response with structured output
        response = self.model.generate_content(prompt)
        
        # Parse response into ActionPlan
        action_plan = self._parse_response(response.text, df)
        
        return action_plan
    
    def _create_data_summary(self, df: pd.DataFrame) -> str:
        """Create a summary of the dataframe."""
        summary = f"""
Spreadsheet Summary:
- Shape: {df.shape[0]} rows × {df.shape[1]} columns
- Columns: {', '.join(df.columns.tolist())}
- Data Types:
{df.dtypes.to_string()}

First 5 rows:
{df.head().to_string()}

Statistical Summary (numeric columns):
{df.describe().to_string()}

Missing Values:
{df.isnull().sum().to_string()}
"""
        return summary
    
    def _build_prompt(
        self,
        data_summary: str,
        user_prompt: Optional[str] = None
    ) -> str:
        """Build the prompt for Gemini."""
        base_prompt = f"""
You are an expert spreadsheet analyst. Analyze the following spreadsheet data and provide recommendations.

{data_summary}

Available tools:
1. apply_formula: Apply formulas to columns (e.g., calculate totals, percentages, transformations)
2. create_pivot: Create pivot tables to summarize data
3. conditional_format: Apply conditional formatting based on rules

Please analyze this data and respond with a JSON object following this exact structure:
{{
    "analysis": "Your detailed analysis of the data",
    "recommended_actions": [
        {{
            "tool_name": "tool name (apply_formula, create_pivot, or conditional_format)",
            "parameters": {{"param1": "value1", "param2": "value2"}},
            "reasoning": "Why this action is recommended"
        }}
    ],
    "summary": "Brief summary of recommended actions",
    "priority": "high/medium/low"
}}
"""
        
        if user_prompt:
            base_prompt += f"\n\nUser Request: {user_prompt}\n"
        
        base_prompt += "\nProvide your response as a valid JSON object only, with no additional text."
        
        return base_prompt
    
    def _parse_response(self, response_text: str, df: pd.DataFrame) -> ActionPlan:
        """Parse Gemini response into ActionPlan schema."""
        try:
            # Extract JSON from response
            response_text = response_text.strip()
            if response_text.startswith("```json"):
                response_text = response_text[7:]
            if response_text.startswith("```"):
                response_text = response_text[3:]
            if response_text.endswith("```"):
                response_text = response_text[:-3]
            response_text = response_text.strip()
            
            # Parse JSON
            data = json.loads(response_text)
            
            # Convert to ActionPlan
            tool_calls = [
                ToolCall(
                    tool_name=action["tool_name"],
                    parameters=action["parameters"],
                    reasoning=action.get("reasoning", "")
                )
                for action in data.get("recommended_actions", [])
            ]
            
            action_plan = ActionPlan(
                analysis=data.get("analysis", "No analysis provided"),
                recommended_actions=tool_calls,
                summary=data.get("summary", "No summary provided"),
                priority=data.get("priority", "medium")
            )
            
            return action_plan
            
        except json.JSONDecodeError as e:
            # Fallback: create a basic action plan
            return ActionPlan(
                analysis=f"Analysis of {len(df)} rows and {len(df.columns)} columns",
                recommended_actions=[],
                summary="Failed to parse AI response",
                priority="low"
            )
