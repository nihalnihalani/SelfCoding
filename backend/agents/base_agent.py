from typing import Dict, List, Optional, Any
from pydantic import BaseModel
import uuid
import json
from datetime import datetime


class AgentCard(BaseModel):
    """A2A Protocol Agent Card Definition."""
    name: str
    description: str
    version: str
    url: str
    capabilities: List[str]
    skills: List[Dict[str, Any]]
    authentication: str = "api_key"


class A2AMessage(BaseModel):
    """JSON-RPC 2.0 compliant A2A message."""
    jsonrpc: str = "2.0"
    method: str
    params: Dict[str, Any]
    id: str = None
    
    def __init__(self, **data):
        if 'id' not in data:
            data['id'] = str(uuid.uuid4())
        super().__init__(**data)


class A2AResponse(BaseModel):
    """JSON-RPC 2.0 compliant A2A response."""
    jsonrpc: str = "2.0"
    result: Optional[Dict[str, Any]] = None
    error: Optional[Dict[str, Any]] = None
    id: str


class BaseAgent:
    """Base class for all A2A agents."""
    
    def __init__(self, name: str, description: str, capabilities: List[str]):
        self.name = name
        self.description = description
        self.capabilities = capabilities
        self.agent_id = str(uuid.uuid4())
        self.message_history = []
    
    def get_agent_card(self) -> AgentCard:
        """Return agent card for A2A protocol discovery."""
        return AgentCard(
            name=self.name,
            description=self.description,
            version="1.0.0",
            url=f"/api/agents/{self.name}",
            capabilities=self.capabilities,
            skills=self.get_skills(),
            authentication="api_key"
        )
    
    def get_skills(self) -> List[Dict[str, Any]]:
        """Return list of agent skills."""
        return []
    
    async def process_message(self, message: A2AMessage) -> A2AResponse:
        """Process incoming A2A message."""
        raise NotImplementedError("Subclass must implement process_message")
    
    def log_message(self, message: A2AMessage, response: A2AResponse):
        """Log message for debugging and tracing."""
        self.message_history.append({
            'timestamp': datetime.now().isoformat(),
            'message': message.dict(),
            'response': response.dict()
        })
