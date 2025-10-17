# CodeForge Technology Stack

## 🤖 AI & Machine Learning

### **Primary AI Models**
- **Google Gemini Flash Latest** - Main code generation and analysis model
  - Used for: Code generation, planning, causal analysis, counterfactual reasoning
  - SDK: `google-generativeai` (Python)
  - Features: JSON mode, structured output, async generation

### **AI Frameworks & Protocols**
- **Google A2A Protocol** (Agent-to-Agent)
  - JSON-RPC 2.0 messaging
  - Agent Cards for discovery
  - Multi-agent coordination
- **CopilotKit** (v1.10.6)
  - AG UI Protocol implementation
  - Conversational AI assistant
  - Action handlers and chat interface

---

## 💻 Backend Technologies

### **Core Framework**
- **Python 3.13** - Programming language
- **FastAPI** (v0.115.14) - Modern async web framework
  - ASGI server architecture
  - Automatic API documentation (OpenAPI/Swagger)
  - WebSocket support
  - CORS middleware
- **Uvicorn** (v0.25.0) - Lightning-fast ASGI server
  - Auto-reload for development
  - Production-ready performance

### **Database**
- **MongoDB** - NoSQL database
  - **Motor** (v3.3.1) - Async MongoDB driver
  - **PyMongo** (v4.5.0) - Synchronous driver fallback
  - Stores: patterns, learning history, metrics

### **Data Validation & Modeling**
- **Pydantic** (v2.6.4+)
  - Type validation
  - Data models
  - Request/response schemas

### **AI & ML Libraries**
- **NumPy** - Numerical computing
  - Statistical analysis
  - Trend calculations
  - Learning efficiency metrics
- **Google Generative AI** (v0.8.0+)
  - Official Gemini SDK
  - Async support
  - Structured output generation

### **Security & Sandboxing**
- **Daytona Sandbox** (v0.110.2)
  - Secure code execution
  - Isolated container environments
  - Python SDK integration
  - Real-time execution monitoring

### **Utilities**
- **python-dotenv** (v1.0.1+) - Environment variable management
- **python-multipart** (v0.0.9+) - File upload support
- **websockets** (v15.0.0+) - Real-time communication
- **boto3** (v1.34.129+) - AWS SDK (for future S3 integration)
- **requests** (v2.31.0+) - HTTP client

---

## 🎨 Frontend Technologies

### **Core Framework**
- **React** (v19.0.0) - UI library
  - Latest stable version
  - Modern hooks API
  - Concurrent features
- **React DOM** (v19.0.0) - DOM rendering

### **Build Tools**
- **Create React App** (v5.0.1) - Project scaffolding
- **Craco** (v7.1.0) - Configuration override
  - Custom webpack config
  - Alias support (@/ imports)
  - Warning suppression
- **Webpack 5** - Module bundler (via CRA)

### **UI Component Libraries**
- **Shadcn UI** - Beautiful component system
  - Based on Radix UI primitives
  - Accessible, composable components
- **Radix UI** - Headless UI components
  - 30+ components used including:
    - Accordion, Alert Dialog, Avatar
    - Card, Checkbox, Dialog
    - Dropdown, Popover, Progress
    - Select, Switch, Tabs, Tooltip
    - Toast, Toggle, etc.

### **Styling**
- **Tailwind CSS** (v3.4.17) - Utility-first CSS framework
  - Custom configuration
  - Dark mode support
  - JIT compiler
- **PostCSS** (v8.4.49) - CSS processor
- **Autoprefixer** (v10.4.20) - Vendor prefixing
- **tailwindcss-animate** (v1.0.7) - Animation utilities
- **class-variance-authority** (v0.7.1) - Component variants
- **tailwind-merge** (v3.2.0) - Class merging utility
- **clsx** (v2.1.1) - Conditional classes

### **Animation**
- **Framer Motion** (v12.23.24)
  - Smooth animations
  - Page transitions
  - Gesture support
  - Spring physics

### **Data Visualization**
- **Recharts** (v3.2.1)
  - Line charts
  - Area charts
  - Bar charts
  - Responsive containers

### **Icons**
- **Lucide React** (v0.507.0)
  - Modern icon library
  - Tree-shakeable
  - 1000+ icons

### **Forms & Validation**
- **React Hook Form** (v7.56.2) - Form management
- **Zod** (v3.24.4) - Schema validation
- **@hookform/resolvers** (v5.0.1) - Validation integration

### **State Management & Routing**
- **React Router DOM** (v7.5.1) - Client-side routing
- **React Context API** - Theme management

### **Theming**
- **next-themes** (v0.4.6)
  - Dark/light mode
  - System preference detection
  - Persistent theme storage

### **Notifications**
- **Sonner** (v2.0.3) - Toast notifications
  - Beautiful, accessible toasts
  - Promise-based API

### **HTTP Client**
- **Axios** (v1.8.4)
  - Promise-based requests
  - Interceptors
  - Timeout handling

### **Code Display**
- **react-syntax-highlighter** (v15.6.6)
  - Syntax highlighting for generated code
  - Multiple language support

### **Utilities**
- **date-fns** (v4.1.0) - Date manipulation
- **cmdk** (v1.1.1) - Command menu component
- **input-otp** (v1.4.2) - OTP input component
- **embla-carousel-react** (v8.6.0) - Carousel component
- **vaul** (v1.1.2) - Drawer component
- **react-resizable-panels** (v3.0.1) - Resizable layouts

### **Development Tools**
- **ESLint** (v9.37.0) - Linting
  - React plugin
  - JSX accessibility plugin
  - Import plugin
- **@babel/plugin-proposal-private-property-in-object** - Babel support

---

## 🔌 APIs & External Services

### **AI Services**
- **Google AI Studio API**
  - Gemini Flash Latest model
  - Free tier available
  - API Key: `GEMINI_API_KEY`

### **Sandbox Services**
- **Daytona Sandbox API**
  - Secure code execution
  - Container-based sandboxes
  - API Key: `DAYTONA_API_KEY`

### **Future Integrations (Planned)**
- Vercel API - Deployment
- GitHub API - Repository management
- Browserbase - Browser testing

---

## 🗄️ Data Storage

### **Primary Database**
- **MongoDB**
  - NoSQL document database
  - Async operations via Motor
  - Collections: patterns, history, metrics

### **In-Memory Storage**
- **Python Lists/Dicts**
  - Success patterns cache
  - Failure patterns cache
  - Generation history
  - Active WebSocket connections

---

## 🏗️ Architecture & Protocols

### **Communication Protocols**
- **REST API** - HTTP endpoints
- **WebSocket** - Real-time updates
- **JSON-RPC 2.0** - Agent-to-agent communication
- **AG UI Protocol** - CopilotKit integration

### **Design Patterns**
- **Multi-Agent System** - Specialized agents
- **Observer Pattern** - WebSocket updates
- **Factory Pattern** - Agent creation
- **Strategy Pattern** - Learning strategies
- **Repository Pattern** - Data access

---

## 📦 Package Managers

- **pip** - Python package manager
- **npm** - Node.js package manager
- **venv** - Python virtual environments

---

## 🔧 Development Tools

### **Version Control**
- **Git** - Source control
- **GitHub** - Repository hosting

### **Environment Management**
- **dotenv** - Environment variables
- **.env files** - Configuration
- **Environment separation** - Dev/prod configs

### **Process Management**
- **Shell scripts** - Project startup
- **Background processes** - Server management

---

## 🧪 Testing & Quality

### **Code Quality**
- **Type hints** - Python type annotations
- **Pydantic models** - Runtime type checking
- **ESLint** - JavaScript linting
- **PropTypes** - React prop validation (implicit)

### **Security**
- **Daytona Sandboxes** - Isolated code execution
- **CORS** - Cross-origin configuration
- **API key management** - Environment-based secrets
- **Input validation** - Pydantic schemas

---

## 🌐 Deployment & Hosting

### **Current Setup**
- **Local Development**
  - Backend: localhost:8000
  - Frontend: localhost:3000
  - MongoDB: localhost:27017

### **Production-Ready For**
- **Backend**: Vercel, Google Cloud Run, AWS Lambda, Heroku
- **Frontend**: Vercel, Netlify, AWS Amplify
- **Database**: MongoDB Atlas, AWS DocumentDB

---

## 📚 Research & Academic

### **Implemented Research Papers**
1. **Reflexion Framework** - Verbal reinforcement learning
2. **Curriculum Learning** - Progressive difficulty
3. **Model-Agnostic Meta-Learning (MAML)** - Strategy optimization
4. **Causal Reasoning** - Performance attribution
5. **Hierarchical Memory Networks** - Multi-tier memory

### **AI Techniques**
- Multi-level reflection
- Counterfactual reasoning
- Confidence-weighted consolidation
- Cross-domain transfer learning
- Adaptive parameter tuning

---

## 🔗 Key Dependencies Summary

### **Backend (Python)**
```txt
fastapi==0.115.14
uvicorn==0.25.0
motor==3.3.1
pymongo==4.5.0
pydantic>=2.6.4
python-dotenv>=1.0.1
google-generativeai>=0.8.0
daytona>=0.110.0
numpy
websockets>=15.0.0
```

### **Frontend (Node.js)**
```json
{
  "react": "^19.0.0",
  "@copilotkit/react-core": "^1.10.6",
  "@copilotkit/react-ui": "^1.10.6",
  "recharts": "^3.2.1",
  "framer-motion": "^12.23.24",
  "tailwindcss": "^3.4.17",
  "axios": "^1.8.4",
  "lucide-react": "^0.507.0"
}
```

---

## 🌟 Technology Highlights

### **Modern Stack**
✅ Latest React 19  
✅ Python 3.13  
✅ FastAPI (one of fastest Python frameworks)  
✅ Google's newest Gemini models  

### **Production-Ready**
✅ Type safety (Pydantic, PropTypes)  
✅ Error handling throughout  
✅ Environment-based configuration  
✅ Scalable architecture  

### **Developer Experience**
✅ Hot reload (both frontend & backend)  
✅ Beautiful UI components (Shadcn)  
✅ Auto-generated API docs  
✅ Comprehensive logging  

### **Advanced Features**
✅ Multi-agent AI system  
✅ Real-time WebSocket updates  
✅ Secure sandbox execution  
✅ Self-improving algorithms  
✅ Research-backed techniques  

---

## 🎯 Hackathon-Specific Technologies

### **Required/Recommended**
- ✅ **Google Gemini** - Latest Flash model
- ✅ **Multi-Agent System** - A2A protocol
- ✅ **Daytona Sandbox** - Secure execution
- ✅ **CopilotKit** - AI assistant integration

### **Innovative Additions**
- ✅ **Self-Learning Framework** - Research implementation
- ✅ **Curriculum Learning** - Progressive AI development
- ✅ **Meta-Learning Engine** - Strategy optimization
- ✅ **Advanced Reflexion** - Multi-level AI analysis

---

## 📊 Technology Breakdown by Layer

### **Presentation Layer (Frontend)**
- React 19
- Shadcn UI + Radix UI
- Tailwind CSS
- Framer Motion
- Recharts
- CopilotKit

### **Application Layer (Backend)**
- FastAPI
- Pydantic
- Multi-Agent System
- Self-Learning Engine
- Pattern Analyzer

### **AI/ML Layer**
- Google Gemini Flash Latest
- Reflexion Framework
- Curriculum Learning
- Meta-Learning Engine
- Hierarchical Memory

### **Data Layer**
- MongoDB (persistent)
- In-memory cache (fast access)
- WebSocket state

### **Security Layer**
- Daytona Sandbox
- Environment variables
- CORS configuration
- Input validation

---

## 🏆 Why This Stack?

### **Performance**
- FastAPI = Fastest Python framework
- React 19 = Latest concurrent features
- Gemini Flash = Optimized for speed
- Async everywhere = Non-blocking operations

### **Scalability**
- Multi-agent architecture
- Stateless API design
- MongoDB horizontal scaling
- WebSocket for real-time

### **Developer Experience**
- Hot reload everywhere
- Type safety
- Beautiful UI components
- Auto-generated docs

### **Innovation**
- Latest AI models
- Research-backed techniques
- Novel multi-agent patterns
- Self-improving systems

---

## 📝 Complete Technology List

**Languages:** Python, JavaScript, HTML, CSS, Shell  
**Frameworks:** FastAPI, React, Tailwind CSS  
**Platforms:** Node.js, Web Browsers  
**Cloud Services:** Google AI Studio, Daytona Cloud  
**Databases:** MongoDB  
**APIs:** Google Gemini API, Daytona Sandbox API  
**Protocols:** REST, WebSocket, JSON-RPC 2.0, A2A, AG UI  
**UI Libraries:** Shadcn UI, Radix UI, Lucide Icons  
**Animation:** Framer Motion  
**Visualization:** Recharts  
**AI/ML:** Google Gemini, Custom learning frameworks  
**Security:** Daytona Sandboxes, Environment-based secrets  
**Package Managers:** pip, npm, venv  
**Development:** Git, GitHub, ESLint, Hot Reload  

---

**Total Technologies Used:** 50+ libraries, frameworks, and services integrated into a cohesive, production-ready application.

