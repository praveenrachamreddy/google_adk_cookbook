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

"""Evaluation script for the agent system."""

import asyncio
import dotenv
dotenv.load_dotenv()

from google.adk.evaluators import AgentEvaluator
from google.adk.evaluators.scores import response_match_score
from google.genai.types import Part, UserContent
from ..my_agent_system.agent import root_agent


async def evaluate_agent():
    """Run evaluation on the agent."""
    # Create an evaluator
    evaluator = AgentEvaluator(
        agent=root_agent,
        scores=[response_match_score],
    )
    
    # Define test cases
    test_cases = [
        {
            "input": UserContent(parts=[Part(text="Research the benefits of renewable energy")]),
            "expected": "Renewable energy has environmental and economic benefits"
        },
        {
            "input": UserContent(parts=[Part(text="Analyze the impact of AI on job markets")]),
            "expected": "AI has both positive and negative impacts on employment"
        }
    ]
    
    # Run evaluation
    results = await evaluator.evaluate(test_cases=test_cases)
    
    # Print results
    print("Evaluation Results:")
    for i, result in enumerate(results):
        print(f"Test Case {i+1}:")
        print(f"  Score: {result.score}")
        print(f"  Input: {test_cases[i]['input'].parts[0].text}")
        print(f"  Output: {result.output.content.parts[0].text[:100]}...")
        print()


if __name__ == "__main__":
    asyncio.run(evaluate_agent())