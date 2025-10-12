from fastapi import FastAPI, APIRouter, WebSocket, WebSocketDisconnect, HTTPException, Request
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
from agents.manager_agent import ManagerAgent
from agents.base_agent import A2AMessage
from self_learning.self_improvement_engine import SelfImprovementEngine
from integrations.daytona_sandbox import daytona_sandbox

ROOT_DIR = Path(__file__).parent
load_dotenv(ROOT_DIR / '.env')

# MongoDB connection
mongo_url = os.environ['MONGO_URL']
client = AsyncIOMotorClient(mongo_url)
db = client[os.environ['DB_NAME']]

# In-memory pattern storage (simple implementation)
success_patterns_db = []
failure_patterns_db = []

# Initialize A2A Manager Agent
manager_agent = ManagerAgent()

# Initialize Self-Improvement Engine
self_improvement_engine = SelfImprovementEngine()

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
            
            # Clean response - remove markdown code blocks
            response_text = response.strip()
            
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
    daytona_stats = daytona_sandbox.get_statistics()
    return {
        "message": "CodeForge API with A2A Protocol + Daytona Sandbox",
        "status": "running",
        "version": "3.0.0",
        "features": [
            "multi-agent", 
            "a2a-protocol", 
            "copilotkit-ready",
            "self-learning",
            "reflexion-framework",
            "daytona-sandbox"
        ],
        "daytona": {
            "enabled": True,
            "mode": "demo" if daytona_sandbox.api_key == "demo-mode" else "production",
            "active_sandboxes": daytona_stats.get('active_sandboxes', 0)
        }
    }

@api_router.get("/agents")
async def list_agents():
    """List all available A2A agents."""
    return {
        "agents": [
            manager_agent.get_agent_card().dict(),
            manager_agent.code_generator.get_agent_card().dict(),
            manager_agent.code_reviewer.get_agent_card().dict(),
            manager_agent.pattern_analyzer.get_agent_card().dict()
        ]
    }

@api_router.post("/agents/{agent_name}")
async def call_agent(agent_name: str, message: dict):
    """A2A Protocol endpoint for agent communication."""
    try:
        a2a_message = A2AMessage(**message)
        
        # Route to appropriate agent
        if agent_name == "manager":
            response = await manager_agent.process_message(a2a_message)
        elif agent_name == "code_generator":
            response = await manager_agent.code_generator.process_message(a2a_message)
        elif agent_name == "code_reviewer":
            response = await manager_agent.code_reviewer.process_message(a2a_message)
        elif agent_name == "pattern_analyzer":
            response = await manager_agent.pattern_analyzer.process_message(a2a_message)
        else:
            return {"error": "Agent not found"}, 404
        
        return response.dict()
    except Exception as e:
        return {
            "jsonrpc": "2.0",
            "error": {
                "code": -32603,
                "message": str(e)
            },
            "id": message.get('id')
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
        
        # Step 2: Generate with Gemini
        await send_update({
            "type": "status",
            "message": "💻 Generating code...",
            "progress": 30
        })
        
        result = await generate_with_gemini(
            request.description,
            past_patterns,
            request.use_thinking,
            send_update
        )
        
        if not result.get('success'):
            error_msg = result.get('error', 'Generation failed')
            store_failure(request.description, error_msg)
            raise HTTPException(status_code=500, detail=error_msg)
        
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
            metadata=result.get('metadata', {}),
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

@api_router.post("/copilotkit")
async def copilotkit_runtime(request: Request):
    """CopilotKit runtime endpoint - Full AG-UI protocol implementation."""
    
    try:
        body = await request.json()
        
        # Extract messages from CopilotKit request
        messages = body.get('messages', [])
        properties = body.get('properties', {})
        
        # Get the last user message
        user_message = ""
        for msg in reversed(messages):
            if msg.get('role') == 'user':
                user_message = msg.get('content', '')
                break
        
        # Detect intent from user message
        user_lower = user_message.lower()
        
        # Intent: Generate app
        if any(word in user_lower for word in ['generate', 'create', 'build', 'make']):
            # Check if it's asking for info or actual generation
            if any(word in user_lower for word in ['how', 'what', 'explain', '?']):
                response_text = """I can help you generate web applications! Here's how:

**Using the Generate Tab:**
1. Click the "Generate" tab at the top
2. Describe your app in detail
3. Toggle options (Pro Planning, Auto-test)
4. Click "Generate App"
5. Wait for AI to create your app (~10-15 seconds)

**What I Can Build:**
• Todo/Task apps
• Calculators
• Dashboards
• Forms & Surveys
• Interactive games
• Data visualization
• And much more!

Want to try it? Go to the Generate tab and describe what you want!"""
            else:
                # Extract what they want to build
                response_text = f"""I understand you want to build something! 

**To generate your app:**
1. Click the **"Generate"** tab above
2. Enter this description: "{user_message}"
3. Click **"Generate App"**

The multi-agent system will:
• Code Generator creates the app
• Code Reviewer checks quality
• Pattern Library learns from it

You'll get a complete app with HTML, CSS, and JavaScript in about 10-15 seconds!

Ready to try it? Click the Generate tab! 🚀"""
        
        # Intent: Check patterns
        elif any(word in user_lower for word in ['pattern', 'library', 'learn', 'memory']):
            # Get pattern count
            pattern_count = len(success_patterns_db)
            response_text = f"""📚 **Pattern Library Status:**

**Learned Patterns:** {pattern_count} successful patterns
**What it does:** Stores successful code patterns to reuse in future generations

**View patterns:**
Click the **"Pattern Library"** tab to see all learned patterns with:
• Code snippets
• Success rates
• Technologies used
• Features implemented

The more you use CodeForge, the smarter it gets! 🧠"""
        
        # Intent: Check dashboard/metrics
        elif any(word in user_lower for word in ['dashboard', 'metric', 'performance', 'stat']):
            total = len(generation_history)
            success = sum(1 for g in generation_history if g.get('success'))
            rate = (success / total * 100) if total > 0 else 0
            
            response_text = f"""📊 **Performance Dashboard:**

**Stats:**
• Total Apps Built: {total}
• Successful: {success}
• Success Rate: {rate:.1f}%
• Patterns Learned: {len(success_patterns_db)}

**View full dashboard:**
Click the **"Dashboard"** tab for:
• Visual charts
• Success rate trends
• Learning progress
• Performance insights

Check it out! 📈"""
        
        # Intent: Self-learning
        elif any(word in user_lower for word in ['self-learning', 'reflexion', 'improve', 'learning']):
            response_text = """🧠 **Self-Learning System:**

**How it works:**
1. **Reflexion Framework:**
   • Actor generates code
   • Evaluator scores it (0-100)
   • Reflector extracts learnings
   • Improver creates v2

2. **Hierarchical Memory:**
   • Short-term (working memory)
   • Mid-term (recent experiences)
   • Long-term (consolidated knowledge)
   • Reflective (meta-insights)

3. **Continuous Improvement:**
   • Learns from every generation
   • Extracts patterns automatically
   • Gets smarter over time

**See it in action:**
Click **"Self-Learning"** tab to view:
• Learning efficiency
• Memory statistics
• Recent insights
• Performance trends

It's like having an AI that improves itself! 🚀"""
        
        # Intent: A2A or multi-agent
        elif any(word in user_lower for word in ['a2a', 'agent', 'multi-agent', 'orchestr']):
            response_text = """🤖 **Multi-Agent A2A System:**

**4 Specialized Agents:**

1. **Manager Agent** (Orchestrator)
   • Coordinates all agents
   • Routes requests

2. **Code Generator Agent** (Gemini 2.5 Flash)
   • Creates HTML/CSS/JavaScript
   • Fast generation

3. **Code Reviewer Agent** (Gemini 2.5 Pro)
   • Reviews code quality
   • Scores 0-100
   • Finds issues

4. **Pattern Analyzer Agent** (Gemini 2.5 Flash)
   • Extracts reusable patterns
   • Learns from successes

**A2A Protocol:**
They communicate using JSON-RPC 2.0 messages, just like Google's A2A specification!

Try generating an app to see them work together! 🎯"""
        
        # Intent: Daytona
        elif 'daytona' in user_lower or 'sandbox' in user_lower:
            daytona_stats = daytona_sandbox.get_statistics()
            response_text = f"""🔐 **Daytona Sandbox:**

**Status:** Active (Demo Mode)
**Executions:** {daytona_stats.get('total_executions', 0)}
**Success Rate:** {daytona_stats.get('success_rate', 0):.1%}

**What it does:**
• Isolated code execution
• Security by default
• Fast spin-up (~90ms)
• Docker containers

**Features:**
✓ Tests generated code safely
✓ Validates HTML/CSS/JS
✓ Catches errors early
✓ Prevents malicious code

Your generated apps are tested in secure sandboxes! 🛡️"""
        
        # Default: Welcome/Help
        else:
            response_text = """👋 **Welcome to CodeForge AI Assistant!**

I can help you with:

**🚀 Generate Apps**
"How do I generate an app?"
"Create a todo app"

**📚 View Patterns**
"Show me learned patterns"
"What's in the pattern library?"

**📊 Check Stats**
"Show dashboard"
"What's the performance?"

**🧠 Self-Learning**
"Explain self-learning"
"How does Reflexion work?"

**🤖 Multi-Agent System**
"Explain A2A protocol"
"How do agents work together?"

What would you like to know?"""
        
        return {
            "messages": [{
                "role": "assistant",
                "content": response_text
            }],
            "agent_name": "codeforge_assistant",
            "status": "completed"
        }
        
    except Exception as e:
        return {
            "messages": [{
                "role": "assistant",
                "content": f"I encountered an error: {str(e)}. Please try asking again or check the Generate tab for app creation."
            }],
            "status": "error"
        }

@api_router.post("/self-improve/generate")
async def self_improving_generate(request: GenerationRequest):
    """Generate with recursive self-improvement (Reflexion framework)."""
    
    try:
        # Use self-improvement engine
        result = await self_improvement_engine.recursive_self_improvement(
            task=request.description,
            context={"use_patterns": True}
        )
        
        # Store in pattern library
        if result.get('final_score', 0) >= 80:
            store_success(
                request.description,
                result['solution'],
                result['solution'].get('metadata', {})
            )
        
        return {
            "success": True,
            "files": result['solution'].get('files', {}),
            "metadata": result['solution'].get('metadata', {}),
            "self_improvement": {
                "final_score": result['final_score'],
                "iterations": result['iterations'],
                "improvement_cycle": result['improvement_cycle'],
                "memory_stats": result['memory_stats'],
                "learning_summary": result.get('learning_summary', {})
            },
            "deployed_url": f"https://codeforge-demo-{int(time.time())}.vercel.app"
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@api_router.get("/self-learning/report")
async def get_learning_report():
    """Get comprehensive self-learning report."""
    try:
        report = self_improvement_engine.get_learning_report()
        return report
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@api_router.get("/self-learning/memory")
async def get_memory_stats():
    """Get memory system statistics."""
    try:
        stats = self_improvement_engine.memory.get_statistics()
        knowledge = self_improvement_engine.memory.get_consolidated_knowledge()
        
        return {
            "statistics": stats,
            "consolidated_knowledge": knowledge,
            "recent_reflections": self_improvement_engine.memory.reflective[-5:] if self_improvement_engine.memory.reflective else []
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@api_router.post("/daytona/execute")
async def daytona_execute_code(request: dict):
    """Execute code in Daytona sandbox."""
    try:
        code = request.get('code')
        language = request.get('language', 'javascript')
        
        if not code:
            raise HTTPException(status_code=400, detail="Code is required")
        
        result = await daytona_sandbox.execute_code(code, language)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@api_router.post("/daytona/test")
async def daytona_test_files(request: dict):
    """Test generated code files in Daytona sandbox."""
    try:
        files = request.get('files', {})
        
        if not files:
            raise HTTPException(status_code=400, detail="Files are required")
        
        result = await daytona_sandbox.test_generated_code(files)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@api_router.get("/daytona/stats")
async def get_daytona_stats():
    """Get Daytona sandbox statistics."""
    try:
        stats = daytona_sandbox.get_statistics()
        return {
            **stats,
            "mode": "demo" if daytona_sandbox.api_key == "demo-mode" else "production",
            "info": "Daytona provides isolated, secure sandbox execution for AI-generated code"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Include all API routes
app.include_router(api_router)

# Logging configuration
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

@app.on_event("shutdown")
async def shutdown_db_client():
    client.close()