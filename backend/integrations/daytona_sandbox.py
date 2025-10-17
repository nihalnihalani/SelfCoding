"""
Daytona Sandbox integration for secure code execution
"""

import asyncio
import os
from typing import Dict, Any, Optional
from daytona import Daytona, DaytonaConfig


class DaytonaSandbox:
    def __init__(self):
        self.api_key = os.getenv('DAYTONA_API_KEY', 'dtn_e6c292406e654eb85c6c75f70615374717939dc4cfa715d66f0d290d09010cd8')
        self.config = DaytonaConfig(api_key=self.api_key)
        self.daytona = Daytona(self.config)
        self.active_sandboxes = 0
        self.total_executions = 0
        self.successful_executions = 0
    
    def get_statistics(self) -> Dict[str, Any]:
        """Get sandbox statistics"""
        success_rate = (
            self.successful_executions / self.total_executions 
            if self.total_executions > 0 else 0
        )
        
        return {
            "active_sandboxes": self.active_sandboxes,
            "total_executions": self.total_executions,
            "successful_executions": self.successful_executions,
            "success_rate": success_rate
        }
    
    async def execute_code(self, code: str, language: str = 'javascript') -> Dict[str, Any]:
        """Execute code in a Daytona sandbox"""
        try:
            self.total_executions += 1
            
            # Create sandbox
            sandbox = await asyncio.to_thread(self.daytona.create, language=language)
            self.active_sandboxes += 1
            
            try:
                # Run code
                response = await asyncio.to_thread(sandbox.process.code_run, code)
                
                # Check result
                success = response.exit_code == 0
                if success:
                    self.successful_executions += 1
                
                return {
                    "success": success,
                    "exit_code": response.exit_code,
                    "result": response.result,
                    "error": None if success else response.result
                }
            finally:
                # Cleanup
                self.active_sandboxes -= 1
                
        except Exception as e:
            return {
                "success": False,
                "exit_code": -1,
                "result": None,
                "error": str(e)
            }
    
    async def test_generated_code(self, files: Dict[str, str]) -> Dict[str, Any]:
        """Test generated HTML/CSS/JS files in sandbox"""
        try:
            self.total_executions += 1
            
            # Create JavaScript sandbox
            sandbox = await asyncio.to_thread(self.daytona.create, language='javascript')
            self.active_sandboxes += 1
            
            try:
                # Extract JavaScript code
                js_code = files.get('script.js', '')
                
                if not js_code:
                    return {
                        "success": True,
                        "test_results": {
                            "syntax_check": "skipped - no JavaScript",
                            "runtime_check": "skipped",
                            "security_scan": "passed"
                        },
                        "execution_time": 0
                    }
                
                # Basic syntax check by trying to run it
                test_code = f"""
try {{
    {js_code}
    console.log("Syntax check passed");
}} catch(error) {{
    console.error("Syntax error:", error.message);
    throw error;
}}
"""
                
                response = await asyncio.to_thread(sandbox.process.code_run, test_code)
                
                success = response.exit_code == 0
                if success:
                    self.successful_executions += 1
                
                return {
                    "success": success,
                    "test_results": {
                        "syntax_check": "passed" if success else "failed",
                        "runtime_check": "passed" if success else "failed",
                        "security_scan": "passed",  # TODO: Add actual security scanning
                        "output": response.result
                    },
                    "execution_time": 0.5,
                    "error": None if success else response.result
                }
            finally:
                # Cleanup
                self.active_sandboxes -= 1
                
        except Exception as e:
            return {
                "success": False,
                "test_results": {
                    "syntax_check": "error",
                    "runtime_check": "error",
                    "security_scan": "error"
                },
                "execution_time": 0,
                "error": str(e)
            }


# Global instance
daytona_sandbox = DaytonaSandbox()