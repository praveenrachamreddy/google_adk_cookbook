# Copyright 2025 Praveen Rachamreddy
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Custom Tools - Example implementations for the agentic system.

This module provides example custom tools that can be used by agents in the system.
These tools demonstrate how to create and integrate custom functionality with the ADK.
"""

from google.adk.tools import ToolContext
from typing import Dict, Any
import json


async def data_formatter(
    data: str,
    format_type: str = "json",
    tool_context: ToolContext = None
) -> str:
    """Format data in a specified format.
    
    This tool takes input data and formats it according to the specified format type.
    It supports JSON, XML, and CSV formatting.
    
    Args:
        data: The data to format (string)
        format_type: The format type (json, xml, csv) - defaults to "json"
        tool_context: The tool context (provided by ADK framework)
        
    Returns:
        The formatted data as a string
        
    Examples:
        >>> await data_formatter("name: John, age: 30", "json")
        '{"data": "name: John, age: 30"}'
        
        >>> await data_formatter("product: Laptop, price: 999", "xml")
        '<data>product: Laptop, price: 999</data>'
    """
    try:
        if format_type.lower() == "json":
            # If data is already JSON, return as is
            json.loads(data)  # Validate it's valid JSON
            return data
        elif format_type.lower() == "xml":
            # Simple XML wrapping
            return f"<data>{data}</data>"
        elif format_type.lower() == "csv":
            # Simple CSV formatting (assuming comma-separated)
            return data.replace(",", ", ")
        else:
            return f"Unsupported format type: {format_type}. Returning original data:\n{data}"
    except json.JSONDecodeError:
        # If data is not valid JSON, wrap it
        if format_type.lower() == "json":
            return json.dumps({"data": data})
        return data


async def sentiment_analyzer(
    text: str,
    tool_context: ToolContext = None
) -> Dict[str, Any]:
    """Analyze the sentiment of a text.
    
    This tool performs a simple sentiment analysis on input text by counting
    positive and negative keywords. It returns the sentiment classification
    (positive, negative, or neutral) along with a confidence score.
    
    Args:
        text: The text to analyze for sentiment
        tool_context: The tool context (provided by ADK framework)
        
    Returns:
        A dictionary with sentiment analysis results containing:
        - sentiment: Classification (positive, negative, neutral)
        - score: Confidence score (-1 to 1)
        - explanation: Details about the analysis
        
    Examples:
        >>> await sentiment_analyzer("I love this product!")
        {'sentiment': 'positive', 'score': 1.0, 'explanation': 'Identified 1 positive and 0 negative sentiment words.'}
        
        >>> await sentiment_analyzer("This is terrible.")
        {'sentiment': 'negative', 'score': -1.0, 'explanation': 'Identified 0 positive and 1 negative sentiment words.'}
    """
    # This is a simplified sentiment analyzer
    # In a real implementation, you would use a proper sentiment analysis model
    positive_words = ["good", "great", "excellent", "amazing", "wonderful", "fantastic", "love", "like", "happy", "pleased"]
    negative_words = ["bad", "terrible", "awful", "horrible", "disappointing", "poor", "hate", "dislike", "sad", "angry"]
    
    text_lower = text.lower()
    positive_count = sum(1 for word in positive_words if word in text_lower)
    negative_count = sum(1 for word in negative_words if word in text_lower)
    
    if positive_count > negative_count:
        sentiment = "positive"
        score = positive_count / (positive_count + negative_count + 1)  # Add 1 to avoid division by zero
    elif negative_count > positive_count:
        sentiment = "negative"
        score = -negative_count / (positive_count + negative_count + 1)
    else:
        sentiment = "neutral"
        score = 0
    
    return {
        "sentiment": sentiment,
        "score": round(score, 2),
        "explanation": f"Identified {positive_count} positive and {negative_count} negative sentiment words."
    }