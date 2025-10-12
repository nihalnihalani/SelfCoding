from typing import Dict, Any, List
from .base_agent import BaseAgent, A2AMessage, A2AResponse
from .code_generator_agent import CodeGeneratorAgent
from .code_reviewer_agent import CodeReviewerAgent
from .pattern_analyzer_agent import PatternAnalyzerAgent
import asyncio


class ManagerAgent(BaseAgent):
    """Orchestrates multiple agents using A2A protocol."""
    
    def __init__(self):
        super().__init__(
            name="manager",
            description="Orchestrates multi-agent code generation workflow",
            capabilities=["orchestration", "workflow_management", "agent_coordination"]
        )
        
        # Initialize sub-agents
        self.code_generator = CodeGeneratorAgent()
        self.code_reviewer = CodeReviewerAgent()
        self.pattern_analyzer = PatternAnalyzerAgent()
    
    def get_skills(self) -> List[Dict[str, Any]]:
        return [{
            "name": "generate_and_review",
            "description": "Orchestrate code generation with automatic review",
            "input": {
                "description": "string",
                "patterns": "array",
                "auto_review": "boolean"
            },
            "output": {
                "files": "object",
                "review": "object",
                "metadata": "object"
            }
        }]
    
    async def process_message(self, message: A2AMessage) -> A2AResponse:
        """Process orchestration request."""
        try:
            if message.method == "generate_and_review":
                result = await self._orchestrate_generation(
                    message.params.get('description', ''),
                    message.params.get('patterns', []),
                    message.params.get('auto_review', True)
                )
                
                response = A2AResponse(
                    id=message.id,
                    result=result
                )
            else:
                response = A2AResponse(
                    id=message.id,
                    error={
                        "code": -32601,
                        "message": f"Method not found: {message.method}"
                    }
                )
            
            self.log_message(message, response)
            return response
            
        except Exception as e:
            error_response = A2AResponse(
                id=message.id,
                error={
                    "code": -32603,
                    "message": f"Internal error: {str(e)}"
                }
            )
            self.log_message(message, error_response)
            return error_response
    
    async def _orchestrate_generation(self, description: str, patterns: List, auto_review: bool) -> Dict:
        """Orchestrate multi-agent workflow."""
        
        workflow_log = []
        
        # Step 1: Generate code
        workflow_log.append({"step": "code_generation", "status": "starting"})
        gen_message = A2AMessage(
            method="generate_code",
            params={
                "description": description,
                "patterns": patterns,
                "requirements": {}
            }
        )
        
        gen_response = await self.code_generator.process_message(gen_message)
        
        if gen_response.error:
            return {
                "success": False,
                "error": gen_response.error,
                "workflow_log": workflow_log
            }
        
        workflow_log.append({"step": "code_generation", "status": "completed"})
        generated_code = gen_response.result
        
        # Step 2: Review code (if enabled)
        review_result = None
        if auto_review:
            workflow_log.append({"step": "code_review", "status": "starting"})
            review_message = A2AMessage(
                method="review_code",
                params={
                    "files": generated_code.get('files', {}),
                    "description": description
                }
            )
            
            review_response = await self.code_reviewer.process_message(review_message)
            
            if not review_response.error:
                review_result = review_response.result
                workflow_log.append({
                    "step": "code_review",
                    "status": "completed",
                    "quality_score": review_result.get('quality_score', 0)
                })
        
        # Step 3: Analyze patterns (async, don't block)
        if generated_code.get('success'):
            asyncio.create_task(self._analyze_in_background(
                generated_code.get('files', {}),
                description
            ))
        
        # Return orchestrated result
        return {
            "success": True,
            "files": generated_code.get('files', {}),
            "metadata": generated_code.get('metadata', {}),
            "review": review_result,
            "workflow_log": workflow_log,
            "orchestrated_by": self.name
        }
    
    async def _analyze_in_background(self, files: Dict, description: str):
        """Analyze patterns in background (non-blocking)."""
        try:
            analyze_message = A2AMessage(
                method="analyze_patterns",
                params={
                    "files": files,
                    "description": description,
                    "success_rate": 1.0
                }
            )
            
            await self.pattern_analyzer.process_message(analyze_message)
        except Exception as e:
            print(f"Background pattern analysis failed: {str(e)}")
