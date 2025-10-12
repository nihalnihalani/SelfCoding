from typing import Dict, Any, List
from .base_agent import BaseAgent, A2AMessage, A2AResponse
from emergentintegrations.llm.chat import LlmChat, UserMessage
import os
import json
import uuid


class CodeReviewerAgent(BaseAgent):
    """Specialized agent for reviewing generated code."""
    
    def __init__(self):
        super().__init__(
            name="code_reviewer",
            description="Reviews and suggests improvements for generated code",
            capabilities=["code_review", "quality_analysis", "security_check"]
        )
        self.model = "gemini-2.5-pro"
    
    def get_skills(self) -> List[Dict[str, Any]]:
        return [{
            "name": "review_code",
            "description": "Review code for quality, security, and best practices",
            "input": {
                "files": "object",
                "description": "string"
            },
            "output": {
                "quality_score": "number",
                "issues": "array",
                "suggestions": "array",
                "approved": "boolean"
            }
        }]
    
    async def process_message(self, message: A2AMessage) -> A2AResponse:
        """Process code review request."""
        try:
            if message.method == "review_code":
                result = await self._review_code(
                    message.params.get('files', {}),
                    message.params.get('description', '')
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
    
    async def _review_code(self, files: Dict, description: str) -> Dict:
        """Review code using Gemini Pro."""
        
        review_chat = LlmChat(
            api_key=os.getenv('EMERGENT_LLM_KEY'),
            session_id=f"review_{uuid.uuid4()}",
            system_message="You are an expert code reviewer. Analyze code for quality, security, and best practices."
        ).with_model("gemini", "gemini-2.5-pro")
        
        code_summary = "\n".join([f"File: {name}\n{content[:500]}..." for name, content in files.items()])
        
        prompt = f"""Review this generated code.

DESCRIPTION: {description}

CODE:
{code_summary}

Analyze:
1. Code quality (structure, readability)
2. Security issues
3. Best practices adherence
4. Potential bugs
5. Performance concerns

Return JSON:
{{
  "quality_score": 0-100,
  "issues": [{{"type": "error/warning", "message": "...", "file": "..."}}],
  "suggestions": ["improvement 1", "improvement 2"],
  "approved": true/false,
  "summary": "Overall assessment"
}}"""
        
        response = await review_chat.send_message(UserMessage(text=prompt))
        
        # Parse JSON
        response_text = response.strip()
        if '```json' in response_text:
            response_text = response_text.split('```json')[1].split('```')[0]
        elif '```' in response_text:
            response_text = response_text.split('```')[1].split('```')[0]
        
        result = json.loads(response_text.strip())
        result['agent'] = self.name
        result['model'] = self.model
        
        return result
