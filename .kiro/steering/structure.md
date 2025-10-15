# Project Structure & Organization

## Root Directory Layout

```
├── backend/                 # FastAPI Python backend
├── frontend/               # React frontend application
├── tests/                  # Test files
├── .emergent/             # Emergent platform configuration
├── .kiro/                 # Kiro IDE steering rules
├── A2A_ARCHITECTURE.md    # Detailed architecture documentation
└── README.md              # Project overview
```

## Backend Structure (`backend/`)

```
backend/
├── agents/                # A2A Protocol agents
│   ├── base_agent.py     # Base agent class with A2A message handling
│   ├── manager_agent.py  # Orchestrator agent
│   ├── code_generator_agent.py
│   ├── code_reviewer_agent.py
│   └── pattern_analyzer_agent.py
├── integrations/         # External service integrations
│   └── daytona_sandbox.py
├── self_learning/        # Self-improvement system
│   ├── memory_system.py  # Hierarchical memory implementation
│   ├── reflexion.py      # Reflexion framework
│   └── self_improvement_engine.py
├── server.py            # Main FastAPI application
├── copilotkit_setup.py  # CopilotKit configuration
└── requirements.txt     # Python dependencies
```

## Frontend Structure (`frontend/`)

```
frontend/
├── src/
│   ├── components/       # React components
│   │   ├── ui/          # Shadcn UI components (40+ components)
│   │   ├── Dashboard.jsx     # Metrics and analytics
│   │   ├── Generator.jsx     # Code generation interface
│   │   ├── PatternLibrary.jsx # Pattern management
│   │   ├── SelfLearning.jsx  # Learning system UI
│   │   ├── CopilotAssistant.jsx # AI chat interface
│   │   └── CopilotKitProvider.jsx # CopilotKit setup
│   ├── hooks/           # Custom React hooks
│   ├── lib/             # Utility functions
│   ├── App.js           # Main application component
│   └── index.js         # Application entry point
├── public/              # Static assets
├── package.json         # Node.js dependencies
├── craco.config.js      # Build configuration
└── tailwind.config.js   # Tailwind CSS configuration
```

## Key Architectural Patterns

### Agent Organization
- **Base Agent**: All agents inherit from `BaseAgent` class
- **A2A Messages**: Standardized `A2AMessage` and `A2AResponse` models
- **Agent Cards**: Each agent exposes capabilities via agent cards
- **JSON-RPC 2.0**: All inter-agent communication follows this protocol

### Component Hierarchy
- **App.js**: Root component with tab navigation
- **Tab Components**: Dashboard, Generator, PatternLibrary, SelfLearning
- **UI Components**: Reusable Shadcn/Radix components in `ui/` folder
- **CopilotKit**: Separate provider and assistant components

### Data Flow
- **Frontend → Backend**: REST API calls via Axios
- **Real-time Updates**: WebSocket connections for progress tracking
- **Agent Communication**: Internal A2A protocol messaging
- **Memory Storage**: In-memory patterns + MongoDB for persistence

## File Naming Conventions

### Backend (Python)
- **snake_case** for all Python files and functions
- **PascalCase** for class names
- **Descriptive names**: `code_generator_agent.py`, `memory_system.py`

### Frontend (React)
- **PascalCase** for React components: `Dashboard.jsx`, `Generator.jsx`
- **camelCase** for JavaScript functions and variables
- **kebab-case** for CSS classes (via Tailwind)

## Import Patterns

### Backend
```python
# Relative imports within backend
from .base_agent import BaseAgent, A2AMessage
from agents.manager_agent import ManagerAgent

# External dependencies
from fastapi import FastAPI
from emergentintegrations.llm.chat import LlmChat
```

### Frontend
```javascript
// Path alias imports
import { Card } from '@/components/ui/card';
import Dashboard from '@/components/Dashboard';

// External dependencies
import { useState, useEffect } from 'react';
import axios from 'axios';
```

## Configuration Files

- **Backend**: `.env` file for environment variables (API keys, database URLs)
- **Frontend**: `.env` file for React app configuration (backend URL)
- **Build**: `craco.config.js` for webpack customization
- **Styling**: `tailwind.config.js` for design system configuration
- **Dependencies**: `requirements.txt` (Python) and `package.json` (Node.js)