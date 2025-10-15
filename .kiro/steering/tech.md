# Technology Stack & Build System

## Backend Stack

- **Framework**: FastAPI (async Python web framework)
- **AI Models**: Google Gemini 2.5 Pro + Flash via emergentintegrations
- **Database**: MongoDB with Motor (async driver) + in-memory pattern storage
- **Protocol**: A2A (Agent-to-Agent) with JSON-RPC 2.0 messaging
- **WebSockets**: Real-time progress updates during generation
- **Environment**: Python with dotenv for configuration

### Key Backend Dependencies
```
fastapi==0.115.14
uvicorn==0.25.0
motor==3.3.1
pymongo==4.5.0
copilotkit==0.1.67
emergentintegrations (for Gemini LLM)
```

## Frontend Stack

- **Framework**: React 19 with Create React App
- **Build Tool**: CRACO (Create React App Configuration Override)
- **UI Library**: Shadcn UI + Radix UI components
- **Styling**: Tailwind CSS with custom design system
- **AI Chat**: CopilotKit React components
- **HTTP Client**: Axios for API communication
- **Routing**: React Router DOM

### Key Frontend Dependencies
```
@copilotkit/react-core: ^1.10.6
@copilotkit/react-ui: ^1.10.6
@radix-ui/* (comprehensive UI component library)
tailwindcss: ^3.4.17
react: ^19.0.0
```

## Development Commands

### Backend
```bash
# Install dependencies
pip install -r backend/requirements.txt

# Run development server
cd backend && uvicorn server:app --reload --host 0.0.0.0 --port 8000

# Environment setup
# Create backend/.env with:
# MONGO_URL=mongodb://localhost:27017
# DB_NAME=codeforge
# EMERGENT_LLM_KEY=your_gemini_key
# CORS_ORIGINS=http://localhost:3000
```

### Frontend
```bash
# Install dependencies
cd frontend && yarn install

# Run development server
yarn start  # Uses CRACO, starts on port 3000

# Build for production
yarn build

# Environment setup
# Create frontend/.env with:
# REACT_APP_BACKEND_URL=http://localhost:8000
```

## Architecture Patterns

- **Multi-Agent A2A**: JSON-RPC 2.0 communication between specialized agents
- **Async/Await**: Extensive use throughout backend for non-blocking operations
- **Component-Based UI**: React functional components with hooks
- **Real-time Updates**: WebSocket connections for live progress tracking
- **Memory Hierarchies**: Short-term, mid-term, long-term, and reflective memory systems

## Build Configuration

- **CRACO Config**: Custom webpack aliases (`@` -> `src/`) and hot reload controls
- **Tailwind**: Extended theme with custom colors, animations, and design tokens
- **Path Aliases**: `@/` prefix for clean imports in frontend
- **Environment Variables**: Separate `.env` files for backend and frontend