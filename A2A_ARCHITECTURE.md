# CodeForge A2A Multi-Agent Architecture

## Overview
CodeForge implements Google's **Agent-to-Agent (A2A) Protocol** with **CopilotKit** integration for a sophisticated multi-agent code generation system.

## Architecture Diagram

```
┌─────────────────────────────────────────────────────────────┐
│                    Frontend Layer                            │
│  ┌─────────────────┐         ┌──────────────────────────┐  │
│  │  React UI       │         │  CopilotKit Assistant    │  │
│  │  - Generator    │◄────────┤  - AG UI Protocol        │  │
│  │  - Dashboard    │         │  - Chat Interface        │  │
│  │  - Patterns     │         │  - Action Handlers       │  │
│  └────────┬────────┘         └────────────┬─────────────┘  │
└───────────┼────────────────────────────────┼────────────────┘
            │                                │
            │ REST API                       │ AG UI
            │                                │
┌───────────▼────────────────────────────────▼────────────────┐
│                 FastAPI Backend + A2A Layer                  │
│                                                              │
│  ┌──────────────────────────────────────────────────────┐  │
│  │           Manager Agent (Orchestrator)               │  │
│  │  - Coordinates multi-agent workflows                 │  │
│  │  - Implements JSON-RPC 2.0                          │  │
│  │  - Manages agent communication                       │  │
│  └───────┬────────────────┬───────────────┬─────────────┘  │
│          │                │               │                 │
│  ┌───────▼──────┐  ┌──────▼──────┐  ┌────▼─────────────┐  │
│  │   Code       │  │    Code     │  │    Pattern       │  │
│  │  Generator   │  │   Reviewer  │  │    Analyzer      │  │
│  │   Agent      │  │    Agent    │  │     Agent        │  │
│  ├──────────────┤  ├─────────────┤  ├──────────────────┤  │
│  │ Gemini 2.5   │  │ Gemini 2.5  │  │  Gemini 2.5      │  │
│  │   Flash      │  │    Pro      │  │    Flash         │  │
│  │              │  │             │  │                  │  │
│  │ Generates    │  │ Reviews &   │  │ Extracts         │  │
│  │ complete     │  │ validates   │  │ reusable         │  │
│  │ web apps     │  │ code        │  │ patterns         │  │
│  └──────────────┘  └─────────────┘  └──────────────────┘  │
│                                                              │
│  ┌──────────────────────────────────────────────────────┐  │
│  │           Pattern Library (In-Memory)                │  │
│  │  - Successful patterns                               │  │
│  │  - Failed patterns                                   │  │
│  │  - Learning metrics                                  │  │
│  └──────────────────────────────────────────────────────┘  │
└──────────────────────────────────────────────────────────────┘
```

## A2A Protocol Implementation

### 1. Agent Cards (Discovery)
Each agent exposes an Agent Card conforming to A2A specification:

```json
{
  "name": "code_generator",
  "description": "Generates web applications using Gemini 2.5 Flash",
  "version": "1.0.0",
  "url": "/api/agents/code_generator",
  "capabilities": ["code_generation", "web_development", "html_css_js"],
  "skills": [{
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
  }],
  "authentication": "api_key"
}
```

### 2. JSON-RPC 2.0 Communication
Agents communicate via JSON-RPC 2.0 messages:

**Request:**
```json
{
  "jsonrpc": "2.0",
  "method": "generate_and_review",
  "params": {
    "description": "Create a todo app",
    "patterns": [],
    "auto_review": true
  },
  "id": "unique-id"
}
```

**Response:**
```json
{
  "jsonrpc": "2.0",
  "result": {
    "success": true,
    "files": {...},
    "review": {
      "quality_score": 95,
      "approved": true
    },
    "workflow_log": [...]
  },
  "id": "unique-id"
}
```

## Multi-Agent Workflow

### Standard Generation Flow:

1. **User Request** → Frontend/CopilotKit
2. **Manager Agent** receives request
3. **Code Generator Agent** creates application
4. **Code Reviewer Agent** validates quality
5. **Pattern Analyzer Agent** extracts patterns (async)
6. **Response** back to user with metadata

### Workflow Example:
```python
# Manager orchestrates the workflow
workflow = [
    {"step": "code_generation", "status": "starting"},
    {"step": "code_generation", "status": "completed"},
    {"step": "code_review", "status": "starting"},
    {"step": "code_review", "status": "completed", "quality_score": 95}
]
```

## Agent Details

### 1. Manager Agent
- **Role**: Orchestrator
- **Capabilities**: workflow_management, agent_coordination
- **Functions**:
  - Coordinates multi-agent workflows
  - Routes messages to appropriate agents
  - Aggregates results
  - Handles error recovery

### 2. Code Generator Agent
- **Role**: Code Creation
- **Model**: Gemini 2.5 Flash
- **Capabilities**: code_generation, web_development
- **Functions**:
  - Generates HTML/CSS/JavaScript
  - Uses learned patterns
  - Creates complete applications

### 3. Code Reviewer Agent
- **Role**: Quality Assurance
- **Model**: Gemini 2.5 Pro
- **Capabilities**: code_review, quality_analysis, security_check
- **Functions**:
  - Reviews code quality (0-100 score)
  - Identifies issues and bugs
  - Provides improvement suggestions
  - Approves/rejects code

### 4. Pattern Analyzer Agent
- **Role**: Learning System
- **Model**: Gemini 2.5 Flash
- **Capabilities**: pattern_recognition, code_analysis
- **Functions**:
  - Extracts reusable patterns
  - Analyzes successful code
  - Builds pattern library
  - Improves future generations

## CopilotKit Integration

### AG UI Protocol
CopilotKit uses the AG UI protocol to communicate with A2A agents:

```typescript
// Frontend action definition
useCopilotAction({
  name: "generate_app",
  description: "Generate a web application",
  parameters: [{
    name: "description",
    type: "string",
    required: true
  }],
  handler: async ({ description }) => {
    // Calls A2A Manager Agent
    return await generateViaA2A(description);
  }
});
```

### Runtime Endpoint
- **Endpoint**: `/api/copilotkit`
- **Protocol**: AG UI over HTTP
- **Integration**: Direct A2A agent invocation

## API Endpoints

### A2A Protocol Endpoints

```
GET  /api/agents
     → List all available agents with capabilities

POST /api/agents/{agent_name}
     → Send JSON-RPC 2.0 message to specific agent
     Body: {
       "jsonrpc": "2.0",
       "method": "method_name",
       "params": {...},
       "id": "msg-id"
     }

POST /api/generate
     → Enhanced generation using A2A orchestration
     Includes: workflow_log, code_review, patterns_used

GET  /api/patterns
     → Retrieve learned patterns

GET  /api/metrics
     → Get learning metrics and success rates
```

### CopilotKit Endpoints

```
POST /api/copilotkit
     → AG UI protocol endpoint
     → Handles chat and action requests
     → Routes to A2A agents
```

## Benefits of A2A Architecture

### 1. **Specialization**
Each agent focuses on one task:
- Generator creates code
- Reviewer ensures quality
- Analyzer learns patterns

### 2. **Scalability**
Easy to add new agents:
- Testing Agent
- Documentation Agent
- Deployment Agent
- Security Agent

### 3. **Quality Improvement**
Multi-agent review process:
- Code generation by Flash (fast)
- Code review by Pro (thorough)
- Pattern learning (continuous improvement)

### 4. **Interoperability**
Standard A2A protocol:
- JSON-RPC 2.0 messaging
- Agent Cards for discovery
- OAuth 2.0 / API key auth
- Works with any A2A-compatible system

### 5. **Self-Improvement**
Learning loop:
- Pattern extraction from successes
- Failure analysis
- Rolling success rate tracking
- Adaptive pattern matching

## Technology Stack

### Backend
- **Framework**: FastAPI (async)
- **Protocol**: A2A (JSON-RPC 2.0)
- **LLM**: Google Gemini 2.5 Pro + Flash
- **Integration**: Google Gemini SDK
- **Storage**: In-memory patterns + MongoDB

### Frontend
- **Framework**: React
- **AI Chat**: CopilotKit
- **Protocol**: AG UI
- **UI**: Shadcn UI + Tailwind CSS
- **Communication**: REST + WebSocket

## Security Considerations

### Current Implementation
- API key authentication (GEMINI_API_KEY)
- CORS configuration
- Input validation with Pydantic

### Production Recommendations
- OAuth 2.0 for agent authentication
- JWT tokens for agent-to-agent calls
- TLS 1.2+ for all communications
- Rate limiting per agent
- VPC isolation
- Agent capability permissions

## Monitoring & Observability

Each agent logs:
- Message history
- Response times
- Success/failure rates
- Error traces

Manager tracks:
- Workflow execution paths
- Agent call patterns
- Quality metrics
- Pattern usage statistics

## Future Enhancements

### Planned Agents
1. **Testing Agent** - Automated testing with Browserbase
2. **Documentation Agent** - Auto-generate docs
3. **Deployment Agent** - CI/CD integration
4. **Security Agent** - Vulnerability scanning
5. **Performance Agent** - Optimization suggestions

### Planned Features
- Real-time A2A message streaming
- Agent marketplace integration
- Multi-user agent sharing
- Distributed agent execution
- Advanced pattern clustering

## Getting Started

### Test A2A Agents

```bash
# List available agents
curl http://localhost:8000/api/agents

# Call Manager Agent
curl -X POST http://localhost:8000/api/agents/manager \
  -H "Content-Type: application/json" \
  -d '{
    "jsonrpc": "2.0",
    "method": "generate_and_review",
    "params": {
      "description": "Create a calculator app",
      "patterns": [],
      "auto_review": true
    },
    "id": "test-1"
  }'
```

### Use CopilotKit Interface
1. Open http://localhost:3000
2. Click the floating AI Assistant button
3. Chat with the multi-agent system
4. Request app generation via natural language

## References

- [Google A2A Protocol](https://cloud.google.com/vertex-ai/generative-ai/docs/agent-engine/develop/a2a)
- [CopilotKit AG UI](https://docs.copilotkit.ai/)
- [JSON-RPC 2.0 Spec](https://www.jsonrpc.org/specification)
- [Gemini 2.5 Models](https://ai.google.dev/gemini-api/docs/models)

---

**Built for AI Agents Hackathon 2025**
Multi-Agent • A2A Protocol • Google Gemini 2.5 • CopilotKit
