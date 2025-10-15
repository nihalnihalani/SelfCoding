# CodeForge Product Overview

CodeForge is a self-improving AI code generation system that implements Google's Agent-to-Agent (A2A) Protocol with CopilotKit integration. It's a multi-agent system designed for the AI Agents Hackathon 2025.

## Core Functionality

- **Multi-Agent Code Generation**: Uses 4 specialized agents (Manager, Code Generator, Code Reviewer, Pattern Analyzer) that communicate via JSON-RPC 2.0
- **Self-Learning System**: Implements Reflexion Framework with hierarchical memory to improve over time
- **Pattern Library**: Automatically extracts and reuses successful code patterns
- **Web Application Generation**: Creates complete HTML/CSS/JavaScript applications from natural language descriptions

## Key Features

- **A2A Protocol Compliance**: Full JSON-RPC 2.0 implementation for agent communication
- **CopilotKit Integration**: Chat interface using AG UI protocol
- **Gemini 2.5 Models**: Uses both Pro (for planning/review) and Flash (for generation) models
- **Real-time Progress**: WebSocket updates during generation
- **Performance Tracking**: Dashboard with metrics and learning analytics
- **Daytona Sandbox**: Integration for secure code execution (demo mode)

## Target Users

AI developers and researchers interested in multi-agent systems, self-improving AI, and automated code generation.