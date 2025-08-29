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

"""Shared Utilities - Common functions used across the agentic system.

This module provides utility functions that can be used by various components
of the agentic system. These utilities help with common tasks like response
formatting and information extraction.
"""

def format_response(title: str, content: str) -> str:
    """Format a response with a title and content using Markdown headers.
    
    This utility function creates a properly formatted response section
    with a title and content, using Markdown heading syntax.
    
    Args:
        title: The title for the response section
        content: The content to format
        
    Returns:
        A formatted string with the title (as H2 header) and content
        
    Examples:
        >>> format_response("Summary", "This is the summary content.")
        '## Summary\n\nThis is the summary content.\n'
    """
    return f"## {title}\n\n{content}\n"

def extract_key_points(text: str, max_points: int = 5) -> list:
    """Extract key points from a text by splitting on sentence boundaries.
    
    This utility function extracts key points from input text by splitting
    on periods and returning the first few sentences as key points.
    
    Note: This is a simple implementation. In a production system, you might
    use an LLM to intelligently extract key points based on content.
    
    Args:
        text: The text to extract key points from
        max_points: Maximum number of key points to extract (default: 5)
        
    Returns:
        A list of key points (sentences) extracted from the text
        
    Examples:
        >>> extract_key_points("First point. Second point. Third point.", 2)
        ['First point.', 'Second point.']
    """
    # This is a placeholder implementation
    # In a real implementation, you might use an LLM to extract key points
    sentences = text.split('.')
    return [sentence.strip() + '.' for sentence in sentences if sentence.strip()][:max_points]