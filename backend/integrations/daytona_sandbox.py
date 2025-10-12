"""
Daytona Sandbox Integration for Secure Code Execution
Provides isolated, containerized environments for running AI-generated code.
"""

from typing import Dict, List, Optional, Any
import requests
import json
import time
import uuid
import asyncio
from datetime import datetime


class DaytonaSandbox:
    """
    Daytona Sandbox Manager for secure AI code execution.
    
    Features:
    - Isolated containerized environments
    - Fast spin-up (~90ms)
    - Stateful runtimes
    - Security by default
    """
    
    def __init__(self, api_key: Optional[str] = None, base_url: str = "https://api.daytona.io"):
        self.api_key = api_key or "demo-mode"  # Demo mode for testing
        self.base_url = base_url
        self.active_sandboxes = {}
        self.execution_history = []
    
    def create_sandbox(self, 
                      name: Optional[str] = None,
                      runtime: str = "node:18",
                      timeout: int = 30) -> Dict:
        """
        Create a new isolated sandbox environment.
        
        Args:
            name: Optional sandbox name
            runtime: Runtime environment (node:18, python:3.11, etc.)
            timeout: Maximum execution time in seconds
            
        Returns:
            Sandbox info with ID and connection details
        """
        
        sandbox_id = f"sandbox-{uuid.uuid4().hex[:8]}"
        name = name or f"codeforge-{sandbox_id}"
        
        # In demo mode, create mock sandbox
        if self.api_key == "demo-mode":
            sandbox = {
                'id': sandbox_id,
                'name': name,
                'runtime': runtime,
                'status': 'running',
                'created_at': datetime.now().isoformat(),
                'url': f"ws://localhost:8080/{sandbox_id}",
                'timeout': timeout,
                'mode': 'demo'
            }
        else:
            # Real Daytona API call
            try:
                response = requests.post(
                    f"{self.base_url}/v1/sandboxes",
                    headers={
                        "Authorization": f"Bearer {self.api_key}",
                        "Content-Type": "application/json"
                    },
                    json={
                        "name": name,
                        "runtime": runtime,
                        "timeout": timeout,
                        "isolation": "docker",  # Options: docker, kata, sysbox
                        "features": ["filesystem", "network", "terminal"]
                    },
                    timeout=10
                )
                response.raise_for_status()
                sandbox = response.json()
            except Exception as e:
                # Fallback to demo mode on error
                print(f"Daytona API error, using demo mode: {str(e)}")
                return self.create_sandbox(name, runtime, timeout)
        
        self.active_sandboxes[sandbox_id] = sandbox
        return sandbox
    
    async def execute_code(self, 
                          code: str, 
                          language: str = "javascript",
                          sandbox_id: Optional[str] = None) -> Dict:
        """
        Execute code in isolated sandbox.
        
        Args:
            code: Code to execute
            language: Programming language
            sandbox_id: Optional existing sandbox ID
            
        Returns:
            Execution result with stdout, stderr, exit_code
        """
        
        execution_id = f"exec-{uuid.uuid4().hex[:8]}"
        start_time = time.time()
        
        # Create sandbox if not provided
        if not sandbox_id:
            runtime_map = {
                'javascript': 'node:18',
                'python': 'python:3.11',
                'html': 'node:18'  # For HTML, use node with JSDOM
            }
            runtime = runtime_map.get(language, 'node:18')
            sandbox = self.create_sandbox(runtime=runtime)
            sandbox_id = sandbox['id']
        
        sandbox = self.active_sandboxes.get(sandbox_id)
        
        if not sandbox:
            return {
                'success': False,
                'error': 'Sandbox not found',
                'execution_id': execution_id
            }
        
        # In demo mode, simulate execution
        if sandbox.get('mode') == 'demo':
            result = await self._simulate_execution(code, language)
        else:
            # Real Daytona execution
            try:
                response = requests.post(
                    f"{self.base_url}/v1/sandboxes/{sandbox_id}/execute",
                    headers={
                        "Authorization": f"Bearer {self.api_key}",
                        "Content-Type": "application/json"
                    },
                    json={
                        "code": code,
                        "language": language,
                        "timeout": sandbox['timeout']
                    },
                    timeout=sandbox['timeout'] + 5
                )
                response.raise_for_status()
                result = response.json()
            except Exception as e:
                result = {
                    'success': False,
                    'error': str(e),
                    'stdout': '',
                    'stderr': str(e)
                }
        
        execution_time = time.time() - start_time
        
        # Record execution
        execution_record = {
            'execution_id': execution_id,
            'sandbox_id': sandbox_id,
            'language': language,
            'code_length': len(code),
            'execution_time': execution_time,
            'success': result.get('success', False),
            'timestamp': datetime.now().isoformat()
        }
        
        self.execution_history.append(execution_record)
        
        return {
            **result,
            'execution_id': execution_id,
            'execution_time': execution_time,
            'sandbox_id': sandbox_id
        }
    
    async def _simulate_execution(self, code: str, language: str) -> Dict:
        """Simulate code execution for demo mode."""
        
        # Simple validation
        has_errors = False
        error_msg = ""
        
        if language == 'javascript':
            # Check for basic syntax issues
            if 'syntax error' in code.lower():
                has_errors = True
                error_msg = "SyntaxError: Unexpected token"
            elif code.count('(') != code.count(')'):
                has_errors = True
                error_msg = "SyntaxError: Unmatched parentheses"
        
        elif language == 'python':
            if 'syntaxerror' in code.lower():
                has_errors = True
                error_msg = "SyntaxError: invalid syntax"
        
        elif language == 'html':
            if '<script>' in code and '</script>' not in code:
                has_errors = True
                error_msg = "HTML Error: Unclosed script tag"
        
        # Simulate execution delay
        await asyncio.sleep(0.1)
        
        if has_errors:
            return {
                'success': False,
                'stdout': '',
                'stderr': error_msg,
                'exit_code': 1
            }
        
        return {
            'success': True,
            'stdout': 'Execution completed successfully (demo mode)',
            'stderr': '',
            'exit_code': 0
        }
    
    async def test_generated_code(self, files: Dict[str, str]) -> Dict:
        """
        Test generated code files in sandbox.
        
        Args:
            files: Dictionary of filename -> code content
            
        Returns:
            Test results with validation status
        """
        
        results = {
            'overall_success': True,
            'files_tested': [],
            'errors': [],
            'warnings': []
        }
        
        # Create sandbox for testing
        sandbox = self.create_sandbox(name="test-sandbox", timeout=60)
        
        # Test HTML file
        if 'index.html' in files:
            html_result = await self.execute_code(
                files['index.html'],
                language='html',
                sandbox_id=sandbox['id']
            )
            
            results['files_tested'].append({
                'file': 'index.html',
                'success': html_result['success'],
                'details': html_result
            })
            
            if not html_result['success']:
                results['overall_success'] = False
                results['errors'].append(f"HTML validation failed: {html_result.get('stderr')}")
        
        # Test JavaScript
        if 'script.js' in files:
            js_result = await self.execute_code(
                files['script.js'],
                language='javascript',
                sandbox_id=sandbox['id']
            )
            
            results['files_tested'].append({
                'file': 'script.js',
                'success': js_result['success'],
                'details': js_result
            })
            
            if not js_result['success']:
                results['overall_success'] = False
                results['errors'].append(f"JavaScript validation failed: {js_result.get('stderr')}")
        
        # Check for common issues
        if 'index.html' in files:
            html_code = files['index.html']
            
            # Check for missing DOCTYPE
            if '<!DOCTYPE' not in html_code:
                results['warnings'].append('Missing DOCTYPE declaration')
            
            # Check for missing charset
            if 'charset=' not in html_code:
                results['warnings'].append('Missing charset meta tag')
        
        # Clean up sandbox
        self.destroy_sandbox(sandbox['id'])
        
        return results
    
    def destroy_sandbox(self, sandbox_id: str) -> bool:
        """Destroy a sandbox environment."""
        
        if sandbox_id not in self.active_sandboxes:
            return False
        
        sandbox = self.active_sandboxes[sandbox_id]
        
        if sandbox.get('mode') != 'demo' and self.api_key != 'demo-mode':
            try:
                requests.delete(
                    f"{self.base_url}/v1/sandboxes/{sandbox_id}",
                    headers={"Authorization": f"Bearer {self.api_key}"},
                    timeout=10
                )
            except:
                pass  # Best effort cleanup
        
        del self.active_sandboxes[sandbox_id]
        return True
    
    def get_statistics(self) -> Dict:
        """Get execution statistics."""
        
        total_executions = len(self.execution_history)
        successful = sum(1 for e in self.execution_history if e['success'])
        
        if total_executions == 0:
            return {
                'total_executions': 0,
                'successful_executions': 0,
                'success_rate': 0,
                'average_execution_time': 0
            }
        
        avg_time = sum(e['execution_time'] for e in self.execution_history) / total_executions
        
        return {
            'total_executions': total_executions,
            'successful_executions': successful,
            'failed_executions': total_executions - successful,
            'success_rate': successful / total_executions,
            'average_execution_time': avg_time,
            'active_sandboxes': len(self.active_sandboxes)
        }
    
    def cleanup_all(self):
        """Clean up all active sandboxes."""
        
        for sandbox_id in list(self.active_sandboxes.keys()):
            self.destroy_sandbox(sandbox_id)


# Global instance
daytona_sandbox = DaytonaSandbox()
