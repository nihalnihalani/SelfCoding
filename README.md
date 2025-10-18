# 🚀 CodeForge - Self-Improving AI Code Generation Platform

<div align="center">

[![Python](https://img.shields.io/badge/Python-3.13-blue.svg)](https://www.python.org/)
[![React](https://img.shields.io/badge/React-19.0-61DAFB.svg)](https://reactjs.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.115-009688.svg)](https://fastapi.tiangolo.com/)
[![Google Gemini](https://img.shields.io/badge/Gemini-Flash_Latest-4285F4.svg)](https://ai.google.dev/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

**A research-backed, self-improving AI code generation platform that learns from every interaction**

[Features](#-features) • [Quick Start](#-quick-start) • [Architecture](#-architecture) • [Tech Stack](#-technology-stack) • [Documentation](#-documentation)

</div>

---

## 📖 Overview

CodeForge is an advanced AI-powered code generation platform that doesn't just generate code—it **learns and improves from every interaction**. Built on cutting-edge research in meta-learning, curriculum learning, and multi-agent systems, CodeForge represents the next generation of AI development tools.

### 🎯 What Makes CodeForge Unique?

- **🧠 Self-Learning System**: Implements advanced reflexion, curriculum learning, and meta-learning to continuously improve
- **🤖 Multi-Agent Architecture**: Specialized AI agents (Manager, Generator, Reviewer, Analyzer) work together using Google's A2A protocol
- **🔒 Secure Execution**: Integrated Daytona Sandbox for safe code testing
- **📊 Real-Time Analytics**: Comprehensive dashboard tracking learning progress, patterns, and performance
- **💡 Pattern Recognition**: Automatically extracts and reuses successful code patterns
- **🎨 Beautiful UI**: Modern, responsive interface built with React 19 and Tailwind CSS

---

## ✨ Features

### Core Capabilities

- **🎨 AI Code Generation**: Generate complete web applications from natural language descriptions
- **🔄 Self-Improvement**: System learns from successes and failures, improving over time
- **🧪 Automated Testing**: Daytona Sandbox integration for secure code execution
- **📈 Learning Analytics**: Advanced metrics on curriculum progress, meta-learning, and efficiency
- **💬 AI Assistant**: Integrated CopilotKit for conversational help
- **🌓 Dark Mode**: Seamless theme switching for comfortable coding

### Advanced Self-Learning

#### 1. **Multi-Level Reflexion** 
- Surface-level analysis of successes/failures
- Causal reasoning about what led to outcomes
- Counterfactual thinking ("what if" scenarios)
- Pattern discovery across generations

#### 2. **Curriculum Learning**
- Progressive difficulty levels (Beginner → Research)
- Adaptive task suggestions based on mastery
- Focus area identification
- Performance tracking by category

#### 3. **Meta-Learning Engine**
- Strategy performance tracking (Imitation, Exploration, Refinement, Transfer, Composition)
- Domain mastery assessment
- Learning efficiency optimization
- Cross-domain transfer learning

#### 4. **Hierarchical Memory**
- Short-term (recent experiences)
- Mid-term (consolidating patterns)
- Long-term (proven strategies)
- Reflective insights layer

---

## 🏗️ Architecture

### Multi-Agent System (A2A Protocol)

```
┌─────────────────────────────────────────────────────────────┐
│                     Manager Agent                            │
│  • Orchestrates workflow                                     │
│  • Coordinates other agents                                  │
│  • Makes high-level decisions                                │
└─────────────────┬───────────────────────────────────────────┘
                  │
        ┌─────────┼─────────┬─────────────┐
        ▼         ▼         ▼             ▼
    ┌─────┐  ┌─────┐  ┌─────────┐  ┌──────────┐
    │Code │  │Code │  │ Pattern  │  │Self-Learn│
    │Gen  │  │Review│  │Analyzer │  │ Engine   │
    └─────┘  └─────┘  └─────────┘  └──────────┘
```

### System Flow

```
User Input → Manager Agent → Code Generator Agent
                ↓
          Technical Plan
                ↓
          Code Generation (Gemini Flash)
                ↓
          Code Reviewer Agent
                ↓
          Pattern Analyzer Agent
                ↓
          Self-Learning System
                ↓
          [Memory, Curriculum, Meta-Learning, Reflexion]
                ↓
          Improved Future Generations
```

---

## 🛠️ Technology Stack

### Backend
- **Python 3.13** - Core language
- **FastAPI** - High-performance async web framework
- **Google Gemini Flash Latest** - AI code generation
- **MongoDB** - NoSQL database (Motor async driver)
- **Daytona Sandbox** - Secure code execution
- **WebSocket** - Real-time updates
- **Pydantic** - Data validation

### Frontend
- **React 19** - Latest React with concurrent features
- **Tailwind CSS** - Utility-first styling
- **Shadcn UI** - Beautiful component system
- **Radix UI** - Accessible primitives
- **Framer Motion** - Smooth animations
- **Recharts** - Data visualization
- **CopilotKit** - AI assistant integration
- **Axios** - HTTP client

### AI & ML
- **Google Gemini API** - Code generation
- **Custom Learning Frameworks**:
  - Advanced Reflexion
  - Curriculum Learning
  - Meta-Learning Engine
  - Hierarchical Memory
- **NumPy** - Statistical analysis

### Infrastructure
- **Daytona Cloud** - Sandbox execution
- **MongoDB Atlas** - Database hosting (production)
- **Vercel/AWS** - Deployment ready

---

## 🚀 Quick Start

### Prerequisites

- Python 3.13+
- Node.js 18+
- MongoDB (local or Atlas)
- Google AI Studio API Key
- Daytona API Key (optional)

### Installation

1. **Clone the repository**
```bash
git clone https://github.com/nihalnihalani/SelfCoding.git
cd SelfCoding
```

2. **Set up environment variables**

Create `backend/.env`:
```env
GEMINI_API_KEY=your_google_ai_studio_api_key
DAYTONA_API_KEY=your_daytona_api_key
MONGO_URL=mongodb://localhost:27017
DB_NAME=codeforge
CORS_ORIGINS=http://localhost:3000
```

Create `frontend/.env`:
```env
REACT_APP_BACKEND_URL=http://localhost:8000
REACT_APP_DAYTONA_API_KEY=your_daytona_api_key
```

3. **Install dependencies**

```bash
# Backend
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt

# Frontend
cd ../frontend
npm install
```

4. **Start the application**

```bash
# Terminal 1 - Backend
cd backend
source venv/bin/activate
python -m uvicorn server:app --reload --host 0.0.0.0 --port 8000

# Terminal 2 - Frontend
cd frontend
npm start
```

5. **Open your browser**
```
http://localhost:3000
```

### 🎯 Quick Test

1. Go to the **Generate** tab
2. Enter: "Create a counter button with red background"
3. Click **Generate App**
4. Watch the AI generate, review, and improve the code!

---

## 📚 API Documentation

### REST Endpoints

#### Code Generation
```http
POST /api/generate
Content-Type: application/json

{
  "description": "Create a todo list app",
  "use_thinking": true,
  "auto_test": true,
  "max_iterations": 3
}
```

#### Self-Learning Report
```http
GET /api/self-learning/comprehensive-report

Response: {
  "overall_learning_score": 73.5,
  "score_breakdown": [...],
  "curriculum_progress": {...},
  "meta_learning_insights": {...},
  "recommendations": [...]
}
```

#### Pattern Library
```http
GET /api/patterns

Response: {
  "total_patterns": 25,
  "patterns": [{
    "category": "ui_components",
    "usage_count": 12,
    "success_rate": 0.92
  }]
}
```

### WebSocket Connection
```javascript
const ws = new WebSocket('ws://localhost:8000/ws');
ws.onmessage = (event) => {
  const data = JSON.parse(event.data);
  console.log('Update:', data);
};
```

For complete API documentation, visit: `http://localhost:8000/docs` (Swagger UI)

---

## 📊 Dashboard & Analytics

### Learning Score Breakdown

The system calculates an overall learning score (0-100) based on:

- **Curriculum Mastery (30%)**: Task completion and mastery rates
- **Memory Performance (25%)**: Pattern recognition and reuse
- **Reflection Quality (20%)**: Depth of self-analysis
- **Learning Velocity (25%)**: Improvement rate over time

### Key Metrics

- **Tasks Attempted/Mastered**: Track learning progress
- **Success Rate**: Overall generation success
- **Strategy Performance**: Which learning strategies work best
- **Domain Mastery**: Skill levels in different areas (UI, Data Viz, APIs, etc.)
- **Learning Velocity**: Quality improvement per hour

---

## 🧪 Testing

### Backend Tests
```bash
cd backend
pytest
```

### Frontend Tests
```bash
cd frontend
npm test
```

### Integration Tests
```bash
# Test code generation
curl -X POST http://localhost:8000/api/generate \
  -H "Content-Type: application/json" \
  -d '{"description":"Create a button","use_thinking":false}'

# Test self-learning data
curl http://localhost:8000/api/self-learning/comprehensive-report
```

---

## 📖 Documentation

Comprehensive documentation is available in the `/docs` folder:

- **[PROJECT_OVERVIEW.md](PROJECT_OVERVIEW.md)** - Complete project guide (952 lines)
- **[A2A_ARCHITECTURE.md](A2A_ARCHITECTURE.md)** - Multi-agent system details
- **[ADVANCED_SELF_LEARNING.md](ADVANCED_SELF_LEARNING.md)** - Learning framework details
- **[TECHNOLOGY_STACK.md](TECHNOLOGY_STACK.md)** - Full tech stack breakdown
- **[SETUP_API_KEY.md](SETUP_API_KEY.md)** - API key configuration guide

---

## 🎨 Screenshots

### Main Dashboard
![Dashboard](screenshots/dashboard.png)
*Real-time learning analytics and metrics*

### Code Generation
![Generation](screenshots/generation.png)
*AI-powered code generation with live updates*

### Advanced Self-Learning
![Self-Learning](screenshots/self-learning.png)
*Comprehensive learning progress tracking*

### Pattern Library
![Patterns](screenshots/patterns.png)
*Automatically extracted code patterns*

---

## 🔬 Research Implementation

CodeForge implements several cutting-edge research papers:

1. **Reflexion: Language Agents with Verbal Reinforcement Learning**
   - Multi-level self-reflection
   - Causal and counterfactual reasoning
   
2. **Curriculum Learning**
   - Progressive difficulty scaling
   - Adaptive task selection

3. **Model-Agnostic Meta-Learning (MAML)**
   - Fast adaptation to new tasks
   - Strategy optimization

4. **Hierarchical Memory Networks**
   - Multi-tier memory consolidation
   - Confidence-weighted pattern storage

---

## 🤝 Contributing

We welcome contributions! Please see our [Contributing Guide](CONTRIBUTING.md) for details.

### Development Setup

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Make your changes
4. Run tests (`pytest` and `npm test`)
5. Commit (`git commit -m 'Add amazing feature'`)
6. Push (`git push origin feature/amazing-feature`)
7. Open a Pull Request

---

## 🐛 Troubleshooting

### Common Issues

**Issue**: `GEMINI_API_KEY not configured`
- **Solution**: Get an API key from [Google AI Studio](https://aistudio.google.com/apikey) and add it to `backend/.env`

**Issue**: MongoDB connection failed
- **Solution**: Ensure MongoDB is running (`mongod`) or update `MONGO_URL` in `.env`

**Issue**: Frontend can't connect to backend
- **Solution**: Check that backend is running on port 8000 and `REACT_APP_BACKEND_URL` is correct

**Issue**: Import errors in Python
- **Solution**: Activate virtual environment: `source venv/bin/activate`

For more help, see our [FAQ](docs/FAQ.md) or [open an issue](https://github.com/nihalnihalani/SelfCoding/issues).

---

## 📜 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 🏆 Hackathon

This project was built for **[Hackathon Name]** showcasing:
- ✅ Google Gemini Flash Latest integration
- ✅ Multi-agent architecture with A2A protocol
- ✅ Daytona Sandbox for secure execution
- ✅ Research-backed self-learning algorithms
- ✅ Production-ready, scalable architecture

---

## 👥 Team

**CodeForge** was created by passionate developers who believe AI should continuously learn and improve.

- **Lead Developer**: [Your Name]
- **GitHub**: [@nihalnihalani](https://github.com/nihalnihalani)

---

## 🙏 Acknowledgments

- **Google** for the Gemini API
- **Daytona** for secure sandbox execution
- **Research Papers** that inspired our learning frameworks
- **Open Source Community** for amazing tools and libraries

---

## 📞 Contact & Support

- **GitHub Issues**: [Report a bug](https://github.com/nihalnihalani/SelfCoding/issues)
- **Email**: your.email@example.com
- **Discord**: [Join our community](#)

---

<div align="center">

**⭐ Star this repo if you find it helpful! ⭐**

Made with ❤️ using Google Gemini, React, and FastAPI

[⬆ Back to Top](#-codeforge---self-improving-ai-code-generation-platform)

</div>
