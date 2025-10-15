"""
Mock Daytona Sandbox integration for demonstration
"""

import asyncio
from typing import Dict, Any


class DaytonaSandbox:
    def __init__(self):
        self.api_key = "demo-mode"
        self.active_sandboxes = 0
    
    def get_statistics(self) -> Dict[str, Any]:
        """Get sandbox statistics"""
        return {
            "active_sandboxes": self.active_sandboxes,
            "total_tests_run": 42,
            "success_rate": 0.85
        }
    
    async def test_generated_code(self, files: Dict[str, str]) -> Dict[str, Any]:
        """Mock code testing in sandbox"""
        await asyncio.sleep(1)  # Simulate testing time
        
        return {
            "success": True,
            "test_results": {
                "syntax_check": "passed",
                "runtime_check": "passed", 
                "security_scan": "passed"
            },
            "execution_time": 0.5
        }


# Global instance
daytona_sandbox = DaytonaSandbox()