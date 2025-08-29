#!/usr/bin/env python3
# Copyright 2025 Your Name
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

# Script to test the custom tools directly.

import sys
import os

# Add the project root to the path
project_root = os.path.abspath(os.path.dirname(__file__))
sys.path.insert(0, project_root)

import dotenv
dotenv.load_dotenv()

async def test_custom_tools():
    # Import the custom tools
    from my_agent_system.tools.custom_tools import data_formatter, sentiment_analyzer
    
    print("=== Custom Tools Test ===\n")
    
    # Test data_formatter
    print("1. Testing data_formatter tool:")
    test_data = "name: John, age: 30, city: New York"
    
    # Test JSON formatting
    result = await data_formatter(test_data, "json")
    print(f"   JSON format: {result}")
    
    # Test XML formatting
    result = await data_formatter(test_data, "xml")
    print(f"   XML format: {result}")
    
    # Test CSV formatting
    result = await data_formatter(test_data, "csv")
    print(f"   CSV format: {result}")
    
    print("\n" + "-" * 50 + "\n")
    
    # Test sentiment_analyzer
    print("2. Testing sentiment_analyzer tool:")
    positive_text = "I love this new technology! It's amazing and wonderful."
    negative_text = "This product is terrible and disappointing. I hate it."
    neutral_text = "The weather is sunny today. It is 75 degrees."
    
    result = await sentiment_analyzer(positive_text)
    print(f"   Positive text: {result}")
    
    result = await sentiment_analyzer(negative_text)
    print(f"   Negative text: {result}")
    
    result = await sentiment_analyzer(neutral_text)
    print(f"   Neutral text: {result}")

if __name__ == "__main__":
    import asyncio
    asyncio.run(test_custom_tools())