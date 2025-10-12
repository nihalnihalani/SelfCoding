from fastapi import FastAPI, APIRouter, WebSocket, WebSocketDisconnect, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from motor.motor_asyncio import AsyncIOMotorClient
from dotenv import load_dotenv
from pathlib import Path
from pydantic import BaseModel, Field, ConfigDict
from typing import List, Dict, Optional
import os
import uuid
import json
import time
import asyncio
import logging
from datetime import datetime, timezone
from emergentintegrations.llm.chat import LlmChat, UserMessage
ROOT_DIR = Path(__file__).parent
load_dotenv(ROOT_DIR / '.env')

# MongoDB connection
mongo_url = os.environ['MONGO_URL']
client = AsyncIOMotorClient(mongo_url)
db = client[os.environ['DB_NAME']]

# In-memory pattern storage (simple implementation)
success_patterns_db = []
failure_patterns_db = []

# Models
class GenerationRequest(BaseModel):
    description: str
    use_thinking: bool = True
    auto_test: bool = False
    max_iterations: int = 2

class GenerationResponse(BaseModel):
    success: bool
    files: Optional[Dict[str, str]] = None
    metadata: Optional[Dict] = None
    deployed_url: Optional[str] = None
    technical_plan: Optional[str] = None
    patterns_used: int = 0
    time_taken: float = 0
    error: Optional[str] = None

class FeedbackRequest(BaseModel):
    description: str
    code: Dict[str, str]
    rating: str
    feedback_text: Optional[str] = None
    metadata: Optional[Dict] = None

class Pattern(BaseModel):
    id: str
    description: str
    code_snippet: str
    tech_stack: List[str]
    features: List[str]
    success_rate: float
    usage_count: int
    timestamp: str

class Metrics(BaseModel):
    total_apps: int
    successful_apps: int
    success_rate: float
    pattern_count: int
    failed_attempts: int
    success_history: List[float]

# WebSocket Manager
class ConnectionManager:
    def __init__(self):
        self.active_connections: Dict[str, WebSocket] = {}

    async def connect(self, websocket: WebSocket, client_id: str):
        await websocket.accept()
        self.active_connections[client_id] = websocket

    def disconnect(self, client_id: str):
        if client_id in self.active_connections:
            del self.active_connections[client_id]

    async def send_message(self, client_id: str, message: dict):
        if client_id in self.active_connections:
            try:
                await self.active_connections[client_id].send_text(json.dumps(message))
            except:
                self.disconnect(client_id)

manager = ConnectionManager()
generation_history = []

# Helper functions
def retrieve_similar_patterns(description: str, n: int = 3) -> List[Dict]:
    """Retrieve similar patterns from in-memory storage."""
    if not success_patterns_db:
        return []
    
    # Simple keyword matching for patterns
    description_lower = description.lower()
    scored_patterns = []
    
    for pattern in success_patterns_db:
        pattern_desc_lower = pattern['description'].lower()
        # Count matching words
        desc_words = set(description_lower.split())
        pattern_words = set(pattern_desc_lower.split())
        match_score = len(desc_words & pattern_words)
        
        if match_score > 0:
            scored_patterns.append((match_score, pattern))
    
    # Sort by score and return top n
    scored_patterns.sort(key=lambda x: x[0], reverse=True)
    top_patterns = [p[1] for p in scored_patterns[:n]]
    
    # Increment usage count
    for pattern in top_patterns:
        pattern['usage_count'] = pattern.get('usage_count', 0) + 1
    
    return top_patterns

def store_success(description: str, code: Dict, metadata: Dict):
    """Store successful generation."""
    code_snippet = code.get('files', {}).get('index.html', '')[:500] if 'files' in code else str(code)[:500]
    pattern_id = f"success_{datetime.now().timestamp()}"
    
    pattern = {
        'id': pattern_id,
        'description': description,
        'code_snippet': code_snippet,
        'tech_stack': metadata.get('tech_stack', []),
        'features': metadata.get('features', []),
        'timestamp': datetime.now().isoformat(),
        'success_rate': 1.0,
        'usage_count': 0
    }
    
    success_patterns_db.append(pattern)
    
    generation_history.append({
        'timestamp': datetime.now(),
        'success': True,
        'description': description
    })

def store_failure(description: str, error: str, code: Optional[Dict] = None):
    """Store failed generation."""
    failure_id = f"failure_{datetime.now().timestamp()}"
    
    failure = {
        'id': failure_id,
        'description': description,
        'error': error,
        'timestamp': datetime.now().isoformat(),
        'code_snippet': str(code)[:500] if code else ''
    }
    
    failure_patterns_db.append(failure)
    
    generation_history.append({
        'timestamp': datetime.now(),
        'success': False,
        'description': description,
        'error': error
    })

async def generate_with_gemini(description: str, past_patterns: List[Dict], use_thinking: bool, send_update) -> Dict:
    """Generate app using Gemini via emergentintegrations."""
    
    try:
        # Build context
        pattern_context = ""
        if past_patterns:
            pattern_context = "\n\nLEARNED FROM PAST SUCCESSES:\n"
            for i, pattern in enumerate(past_patterns[:3], 1):
                pattern_context += f"\nExample {i}:\n"
                pattern_context += f"Description: {pattern['description']}\n"
                pattern_context += f"Success Rate: {pattern.get('success_rate', 1.0):.1%}\n"
                pattern_context += f"Code Pattern:\n{pattern['code_snippet']}\n"
        
        if use_thinking:
            # Step 1: Planning with Gemini 2.5 Pro
            await send_update({
                "type": "status",
                "message": "🧠 Planning with Gemini 2.5 Pro...",
                "progress": 20
            })
            
            planning_chat = LlmChat(
                api_key=os.getenv('EMERGENT_LLM_KEY'),
                session_id=f"planning_{uuid.uuid4()}",
                system_message="You are an expert technical architect. Analyze app requirements and create detailed technical plans."
            ).with_model("gemini", "gemini-2.5-pro")
            
            planning_prompt = f"""Analyze this app request and create a technical plan.

REQUEST: {description}

PAST PATTERNS:
{json.dumps(past_patterns, indent=2) if past_patterns else "None yet"}

Analyze:
1. Core features needed
2. Best tech stack (HTML/CSS/JS)
3. Edge cases to handle
4. Code structure
5. Reusable patterns

Provide detailed technical plan."""
            
            planning_response = await planning_chat.send_message(UserMessage(text=planning_prompt))
            technical_plan = planning_response
            
            await send_update({
                "type": "status",
                "message": "💻 Generating code with Gemini 2.5 Flash...",
                "progress": 50
            })
            
            # Step 2: Code generation with Flash
            code_chat = LlmChat(
                api_key=os.getenv('EMERGENT_LLM_KEY'),
                session_id=f"coding_{uuid.uuid4()}",
                system_message="You are an expert full-stack developer. Generate complete, production-ready web applications."
            ).with_model("gemini", "gemini-2.5-flash")
            
            code_prompt = f"""Based on this plan, generate complete code:

PLAN:
{technical_plan}

REQUEST:
{description}

{pattern_context}

Generate a COMPLETE, production-ready web application with:
1. index.html - Full HTML structure
2. styles.css - Beautiful, modern CSS styling
3. script.js - Complete JavaScript functionality
4. README.md - Usage instructions

IMPORTANT:
- NO placeholders or TODO comments
- Complete, runnable code
- Modern, beautiful design
- All functionality working

Return ONLY valid JSON in this exact format:
{{
  "files": {{
    "index.html": "<complete HTML code>",
    "styles.css": "<complete CSS code>",
    "script.js": "<complete JavaScript code>",
    "README.md": "<instructions>"
  }},
  "metadata": {{
    "tech_stack": ["HTML", "CSS", "JavaScript"],
    "features": ["list of features"],
    "patterns_used": ["patterns applied"]
  }}
}}"""
            
            code_response = await code_chat.send_message(UserMessage(text=code_prompt))
            
            # Parse JSON response
            try:
                # Clean response - remove markdown code blocks
                response_text = code_response.strip()
                
                # Remove markdown code block markers
                if '```json' in response_text:
                    response_text = response_text.split('```json')[1]
                    if '```' in response_text:
                        response_text = response_text.split('```')[0]
                elif '```' in response_text:
                    response_text = response_text.split('```')[1]
                    if '```' in response_text:
                        response_text = response_text.split('```')[0]
                
                response_text = response_text.strip()
                
                # Try to parse JSON
                result = json.loads(response_text)
                
                # Validate structure
                if 'files' not in result or not isinstance(result['files'], dict):
                    return {
                        'success': False,
                        'error': "Invalid response structure: missing 'files' dictionary"
                    }
                
                return {
                    'success': True,
                    'files': result.get('files', {}),
                    'metadata': result.get('metadata', {}),
                    'technical_plan': technical_plan,
                    'model': 'gemini-2.5-pro + flash'
                }
            except json.JSONDecodeError as e:
                # If JSON parsing fails, create a simple error response
                return {
                    'success': False,
                    'error': f"Failed to parse AI response as JSON. The model may have returned plain text instead of JSON format. Error: {str(e)[:200]}"
                }
        
        else:
            # Direct generation with Flash
            await send_update({
                "type": "status",
                "message": "💻 Generating with Gemini 2.5 Flash...",
                "progress": 30
            })
            
            code_chat = LlmChat(
                api_key=os.getenv('EMERGENT_LLM_KEY'),
                session_id=f"direct_{uuid.uuid4()}",
                system_message="You are an expert full-stack developer."
            ).with_model("gemini", "gemini-2.5-flash")
            
            prompt = f"""Generate a COMPLETE web application.

REQUEST: {description}

{pattern_context}

Return ONLY valid JSON:
{{
  "files": {{
    "index.html": "<complete HTML>",
    "styles.css": "<complete CSS>",
    "script.js": "<complete JS>",
    "README.md": "<instructions>"
  }},
  "metadata": {{
    "tech_stack": [],
    "features": [],
    "patterns_used": []
  }}
}}"""
            
            response = await code_chat.send_message(UserMessage(text=prompt))
            
            # Clean and parse
            response_text = response.strip()
            if response_text.startswith('```json'):
                response_text = response_text[7:]
            if response_text.startswith('```'):
                response_text = response_text[3:]
            if response_text.endswith('```'):
                response_text = response_text[:-3]
            
            result = json.loads(response_text.strip())
            
            return {
                'success': True,
                'files': result.get('files', {}),
                'metadata': result.get('metadata', {}),
                'model': 'gemini-2.5-flash'
            }
    
    except Exception as e:
        return {
            'success': False,
            'error': str(e)
        }

# Create FastAPI app
app = FastAPI(title="CodeForge API")
api_router = APIRouter(prefix="/api")

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_credentials=True,
    allow_origins=os.environ.get('CORS_ORIGINS', '*').split(','),
    allow_methods=["*"],
    allow_headers=["*"],
)

# WebSocket endpoint
@app.websocket("/ws/{client_id}")
async def websocket_endpoint(websocket: WebSocket, client_id: str):
    await manager.connect(websocket, client_id)
    try:
        while True:
            data = await websocket.receive_text()
            # Keep connection alive
    except WebSocketDisconnect:
        manager.disconnect(client_id)

# Routes
@api_router.get("/")
async def root():
    return {
        "message": "CodeForge API",
        "status": "running",
        "version": "1.0.0"
    }

@api_router.post("/generate", response_model=GenerationResponse)
async def generate_app_endpoint(request: GenerationRequest):
    """Generate a web application."""
    
    client_id = str(uuid.uuid4())
    start_time = time.time()
    
    async def send_update(message: dict):
        await manager.send_message(client_id, message)
    
    try:
        # Step 1: Retrieve patterns
        await send_update({
            "type": "status",
            "message": "📚 Retrieving similar patterns...",
            "progress": 10
        })
        
        past_patterns = retrieve_similar_patterns(request.description, n=3)
        
        # Step 2: Generate
        result = await generate_with_gemini(
            request.description,
            past_patterns,
            request.use_thinking,
            send_update
        )
        
        if not result['success']:
            store_failure(request.description, result.get('error', 'Unknown error'))
            raise HTTPException(status_code=500, detail=result.get('error'))
        
        # Step 3: Mock deployment
        await send_update({
            "type": "status",
            "message": "🚀 Deploying application...",
            "progress": 80
        })
        
        deployed_url = f"https://codeforge-demo-{int(time.time())}.vercel.app"
        
        # Store success
        store_success(
            request.description,
            result,
            result.get('metadata', {})
        )
        
        # Complete
        await send_update({
            "type": "complete",
            "message": "✅ Generation complete!",
            "progress": 100
        })
        
        time_taken = time.time() - start_time
        
        return GenerationResponse(
            success=True,
            files=result.get('files'),
            metadata=result.get('metadata'),
            deployed_url=deployed_url,
            technical_plan=result.get('technical_plan'),
            patterns_used=len(past_patterns),
            time_taken=time_taken
        )
        
    except Exception as e:
        await send_update({
            "type": "error",
            "message": f"❌ Error: {str(e)}",
            "progress": 0
        })
        
        store_failure(request.description, str(e))
        raise HTTPException(status_code=500, detail=str(e))

@api_router.post("/feedback")
async def submit_feedback(feedback: FeedbackRequest):
    """Submit feedback on a generation."""
    
    try:
        if feedback.rating == "success":
            store_success(
                feedback.description,
                feedback.code,
                feedback.metadata or {}
            )
        else:
            store_failure(
                feedback.description,
                feedback.feedback_text or "User marked as failure",
                feedback.code
            )
        
        return {"status": "success", "message": "Feedback recorded"}
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@api_router.get("/patterns", response_model=List[Pattern])
async def get_patterns():
    """Get all learned patterns."""
    
    try:
        patterns = []
        for pattern in success_patterns_db:
            patterns.append(Pattern(
                id=pattern['id'],
                description=pattern['description'],
                code_snippet=pattern['code_snippet'],
                tech_stack=pattern['tech_stack'],
                features=pattern['features'],
                usage_count=pattern.get('usage_count', 0),
                success_rate=pattern.get('success_rate', 1.0),
                timestamp=pattern['timestamp']
            ))
        
        return patterns
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@api_router.get("/metrics", response_model=Metrics)
async def get_metrics():
    """Get learning metrics."""
    
    try:
        total_apps = len(generation_history)
        successful_apps = sum(1 for g in generation_history if g['success'])
        
        # Calculate rolling success rate
        success_history = []
        window_size = 5
        
        for i in range(len(generation_history)):
            start = max(0, i - window_size + 1)
            window = generation_history[start:i+1]
            successes = sum(1 for g in window if g['success'])
            rate = successes / len(window)
            success_history.append(rate)
        
        return Metrics(
            total_apps=total_apps,
            successful_apps=successful_apps,
            success_rate=successful_apps / total_apps if total_apps > 0 else 0,
            pattern_count=len(success_patterns_db),
            failed_attempts=total_apps - successful_apps,
            success_history=success_history
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

app.include_router(api_router)

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

@app.on_event("shutdown")
async def shutdown_db_client():
    client.close()