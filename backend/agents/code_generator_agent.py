from typing import Dict, Any, List
from .base_agent import BaseAgent, A2AMessage, A2AResponse
from emergentintegrations.llm.chat import LlmChat, UserMessage
import os
import json
import uuid


class CodeGeneratorAgent(BaseAgent):
    """Specialized agent for generating code using Gemini 2.5."""
    
    def __init__(self):
        super().__init__(
            name="code_generator",
            description="Generates web applications using Gemini 2.5 Flash",
            capabilities=["code_generation", "web_development", "html_css_js"]
        )
        self.model = "gemini-2.5-flash"
    
    def get_skills(self) -> List[Dict[str, Any]]:
        return [{
            "name": "generate_code",
            "description": "Generate complete web application code",
            "input": {
                "description": "string",
                "patterns": "array",
                "requirements": "object"
            },
            "output": {
                "files": "object",
                "metadata": "object"
            }
        }]
    
    async def process_message(self, message: A2AMessage) -> A2AResponse:
        """Process code generation request."""
        try:
            if message.method == "generate_code":
                result = await self._generate_code(
                    message.params.get('description', ''),
                    message.params.get('patterns', []),
                    message.params.get('requirements', {})
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
    
    async def _generate_code(self, description: str, patterns: List, requirements: Dict) -> Dict:
        """Generate code using Gemini."""
        
        # Build context from patterns
        pattern_context = ""
        if patterns:
            pattern_context = "\n\nLEARNED PATTERNS:\n"
            for i, pattern in enumerate(patterns[:2], 1):
                pattern_context += f"\nPattern {i}:\n"
                pattern_context += f"Description: {pattern.get('description', 'N/A')}\n"
                pattern_context += f"Code: {pattern.get('code_snippet', 'N/A')[:300]}\n"
        
        code_chat = LlmChat(
            api_key=os.getenv('EMERGENT_LLM_KEY'),
            session_id=f"codegen_{uuid.uuid4()}",
            system_message="You are an expert web developer. Generate complete, production-ready code."
        ).with_model("gemini", "gemini-2.5-flash")
        
        prompt = f"""Generate a complete web application.

DESCRIPTION: {description}

{pattern_context}

REQUIREMENTS:
{json.dumps(requirements, indent=2)}

Return ONLY valid JSON in this format:
{{
  "files": {{
    "index.html": "<complete HTML>",
    "styles.css": "<complete CSS>",
    "script.js": "<complete JavaScript>",
    "README.md": "<instructions>"
  }},
  "metadata": {{
    "tech_stack": ["HTML", "CSS", "JavaScript"],
    "features": ["list of features"],
    "patterns_used": ["patterns applied"]
  }}
}}

IMPORTANT: Return ONLY the JSON, no additional text."""
        
        response = await code_chat.send_message(UserMessage(text=prompt))
        
        # Parse JSON
        response_text = response.strip()
        if '```json' in response_text:
            response_text = response_text.split('```json')[1].split('```')[0]
        elif '```' in response_text:
            response_text = response_text.split('```')[1].split('```')[0]
        
        result = json.loads(response_text.strip())
        
        return {
            "success": True,
            "files": result.get('files', {}),
            "metadata": result.get('metadata', {}),
            "agent": self.name,
            "model": self.model
        }
