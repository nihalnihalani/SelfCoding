"""
CopilotKit SDK Integration for CodeForge
Provides proper streaming AG-UI protocol support
"""

from copilotkit import CopilotKitRemoteEndpoint, Action, CopilotKitSDK
from copilotkit.integrations.fastapi import add_fastapi_endpoint
from typing import Dict, List
import os

# Store reference to pattern DBs (will be set from server.py)
_success_patterns_db = []
_failure_patterns_db = []
_generation_history = []

def set_data_refs(success_patterns, failure_patterns, generation_history):
    """Set references to the main application's data stores."""
    global _success_patterns_db, _failure_patterns_db, _generation_history
    _success_patterns_db = success_patterns
    _failure_patterns_db = failure_patterns
    _generation_history = generation_history

# Define backend actions that CopilotKit can call
async def get_system_metrics() -> Dict:
    """Get system metrics and statistics."""
    total = len(_generation_history)
    success = sum(1 for g in _generation_history if g.get('success'))
    rate = (success / total * 100) if total > 0 else 0
    
    return {
        "total_apps": total,
        "successful_apps": success,
        "success_rate": rate,
        "pattern_count": len(_success_patterns_db),
        "failed_attempts": total - success
    }

async def get_pattern_library() -> List[Dict]:
    """Get all learned patterns."""
    return [
        {
            "description": p.get("description", ""),
            "tech_stack": p.get("tech_stack", []),
            "usage_count": p.get("usage_count", 0),
            "success_rate": p.get("success_rate", 0.0)
        }
        for p in _success_patterns_db[:10]  # Return top 10
    ]

async def get_app_suggestions(query: str) -> List[str]:
    """Get app suggestions based on query."""
    suggestions = [
        "Todo app with dark mode and local storage",
        "Calculator with scientific functions",
        "Dashboard with charts and analytics",
        "Form builder with validation",
        "Interactive game (e.g., tic-tac-toe, memory game)",
        "Data visualization with real-time updates"
    ]
    
    # Simple filtering
    if query:
        query_lower = query.lower()
        suggestions = [s for s in suggestions if any(word in s.lower() for word in query_lower.split())]
    
    return suggestions[:3]

# Create CopilotKit actions
metrics_action = CopilotAction(
    get_system_metrics,
    name="get_metrics",
    description="Get CodeForge system metrics including success rate, total apps, and patterns learned"
)

patterns_action = CopilotAction(
    get_pattern_library,
    name="get_patterns",
    description="Get the pattern library with learned code patterns and their success rates"
)

suggestions_action = CopilotAction(
    get_app_suggestions,
    name="get_suggestions",
    description="Get app building suggestions based on a query or user needs"
)

# Initialize CopilotKit Remote Endpoint
copilotkit_sdk = CopilotKitRemoteEndpoint(
    actions=[metrics_action, patterns_action, suggestions_action]
)

def setup_copilotkit(app):
    """Add CopilotKit endpoint to FastAPI app."""
    add_fastapi_endpoint(app, copilotkit_sdk, path="/api/copilotkit")
    return copilotkit_sdk
