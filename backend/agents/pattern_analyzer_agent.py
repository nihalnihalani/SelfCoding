from typing import Dict, Any, List
from .base_agent import BaseAgent, A2AMessage, A2AResponse
from emergentintegrations.llm.chat import LlmChat, UserMessage
import os
import json
import uuid


class PatternAnalyzerAgent(BaseAgent):
    """Specialized agent for analyzing patterns in successful code."""
    
    def __init__(self):
        super().__init__(
            name="pattern_analyzer",
            description="Analyzes patterns in successful code generations",
            capabilities=["pattern_recognition", "code_analysis", "learning"]
        )
        self.model = "gemini-2.5-flash"
    
    def get_skills(self) -> List[Dict[str, Any]]:
        return [{
            "name": "analyze_patterns",
            "description": "Extract reusable patterns from successful code",
            "input": {
                "files": "object",
                "description": "string",
                "success_rate": "number"
            },
            "output": {
                "patterns": "array",
                "tech_stack": "array",
                "features": "array",
                "key_insights": "string"
            }
        }]
    
    async def process_message(self, message: A2AMessage) -> A2AResponse:
        """Process pattern analysis request."""
        try:
            if message.method == "analyze_patterns":
                result = await self._analyze_patterns(
                    message.params.get('files', {}),
                    message.params.get('description', ''),
                    message.params.get('success_rate', 1.0)
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
    
    async def _analyze_patterns(self, files: Dict, description: str, success_rate: float) -> Dict:
        """Analyze patterns using Gemini."""
        
        analyzer_chat = LlmChat(
            api_key=os.getenv('EMERGENT_LLM_KEY'),
            session_id=f"analyzer_{uuid.uuid4()}",
            system_message="You are a pattern recognition expert. Extract reusable patterns from code."
        ).with_model("gemini", "gemini-2.5-flash")
        
        code_summary = "\n".join([f"// {name}\n{content[:400]}..." for name, content in files.items()])
        
        prompt = f"""Analyze this successful code generation.

DESCRIPTION: {description}
SUCCESS RATE: {success_rate}

CODE:
{code_summary}

Extract:
1. Reusable code patterns
2. Design patterns used
3. Tech stack and libraries
4. Key features implemented
5. Architecture insights

Return JSON:
{{
  "patterns": ["pattern 1", "pattern 2"],
  "tech_stack": ["HTML", "CSS", "JavaScript"],
  "features": ["feature 1", "feature 2"],
  "key_insights": "What makes this successful",
  "reusability_score": 0-100
}}"""
        
        response = await analyzer_chat.send_message(UserMessage(text=prompt))
        
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
