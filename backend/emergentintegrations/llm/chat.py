"""
Mock emergentintegrations LLM chat module for demonstration
"""

import json
import asyncio
from typing import Dict, Any, Optional


class UserMessage:
    def __init__(self, text: str):
        self.text = text


class LlmChat:
    def __init__(self, api_key: str, session_id: str, system_message: str):
        self.api_key = api_key
        self.session_id = session_id
        self.system_message = system_message
        self.model_name = "gemini-2.5-flash"
    
    def with_model(self, provider: str, model: str):
        self.model_name = model
        return self
    
    async def send_message(self, message: UserMessage) -> str:
        """Mock LLM response generation"""
        
        # Simulate API delay
        await asyncio.sleep(0.5)
        
        # Generate mock responses based on message content
        text = message.text.lower()
        
        if "technical plan" in text or "analyze" in text:
            return """
            Technical Plan:
            1. Core Features: Interactive UI components with modern styling
            2. Tech Stack: HTML5, CSS3 (Flexbox/Grid), Vanilla JavaScript
            3. Architecture: Component-based structure with event handling
            4. Edge Cases: Input validation, responsive design, accessibility
            5. Code Structure: Modular functions, clean separation of concerns
            """
        
        elif "generate" in text and "json" in text:
            # Mock code generation response
            if "todo" in text or "task" in text:
                return '''```json
{
  "files": {
    "index.html": "<!DOCTYPE html>\\n<html lang=\\"en\\">\\n<head>\\n    <meta charset=\\"UTF-8\\">\\n    <meta name=\\"viewport\\" content=\\"width=device-width, initial-scale=1.0\\">\\n    <title>Todo App</title>\\n    <link rel=\\"stylesheet\\" href=\\"styles.css\\">\\n</head>\\n<body>\\n    <div class=\\"container\\">\\n        <h1>My Todo App</h1>\\n        <div class=\\"input-section\\">\\n            <input type=\\"text\\" id=\\"todoInput\\" placeholder=\\"Add a new task...\\">\\n            <button id=\\"addBtn\\">Add Task</button>\\n        </div>\\n        <ul id=\\"todoList\\"></ul>\\n    </div>\\n    <script src=\\"script.js\\"></script>\\n</body>\\n</html>",
    "styles.css": "* {\\n    margin: 0;\\n    padding: 0;\\n    box-sizing: border-box;\\n}\\n\\nbody {\\n    font-family: 'Arial', sans-serif;\\n    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);\\n    min-height: 100vh;\\n    display: flex;\\n    align-items: center;\\n    justify-content: center;\\n}\\n\\n.container {\\n    background: white;\\n    padding: 2rem;\\n    border-radius: 15px;\\n    box-shadow: 0 10px 30px rgba(0,0,0,0.2);\\n    width: 100%;\\n    max-width: 500px;\\n}\\n\\nh1 {\\n    text-align: center;\\n    color: #333;\\n    margin-bottom: 2rem;\\n}\\n\\n.input-section {\\n    display: flex;\\n    gap: 10px;\\n    margin-bottom: 2rem;\\n}\\n\\n#todoInput {\\n    flex: 1;\\n    padding: 12px;\\n    border: 2px solid #ddd;\\n    border-radius: 8px;\\n    font-size: 16px;\\n}\\n\\n#addBtn {\\n    padding: 12px 20px;\\n    background: #667eea;\\n    color: white;\\n    border: none;\\n    border-radius: 8px;\\n    cursor: pointer;\\n    font-size: 16px;\\n}\\n\\n#addBtn:hover {\\n    background: #5a6fd8;\\n}\\n\\n#todoList {\\n    list-style: none;\\n}\\n\\n.todo-item {\\n    display: flex;\\n    align-items: center;\\n    padding: 15px;\\n    margin-bottom: 10px;\\n    background: #f8f9fa;\\n    border-radius: 8px;\\n    border-left: 4px solid #667eea;\\n}\\n\\n.todo-text {\\n    flex: 1;\\n    margin-left: 10px;\\n}\\n\\n.delete-btn {\\n    background: #e74c3c;\\n    color: white;\\n    border: none;\\n    padding: 8px 12px;\\n    border-radius: 5px;\\n    cursor: pointer;\\n}\\n\\n.delete-btn:hover {\\n    background: #c0392b;\\n}\\n\\n.completed {\\n    text-decoration: line-through;\\n    opacity: 0.6;\\n}",
    "script.js": "class TodoApp {\\n    constructor() {\\n        this.todos = JSON.parse(localStorage.getItem('todos')) || [];\\n        this.todoInput = document.getElementById('todoInput');\\n        this.addBtn = document.getElementById('addBtn');\\n        this.todoList = document.getElementById('todoList');\\n        \\n        this.init();\\n    }\\n    \\n    init() {\\n        this.addBtn.addEventListener('click', () => this.addTodo());\\n        this.todoInput.addEventListener('keypress', (e) => {\\n            if (e.key === 'Enter') this.addTodo();\\n        });\\n        \\n        this.renderTodos();\\n    }\\n    \\n    addTodo() {\\n        const text = this.todoInput.value.trim();\\n        if (!text) return;\\n        \\n        const todo = {\\n            id: Date.now(),\\n            text: text,\\n            completed: false\\n        };\\n        \\n        this.todos.push(todo);\\n        this.saveTodos();\\n        this.renderTodos();\\n        this.todoInput.value = '';\\n    }\\n    \\n    deleteTodo(id) {\\n        this.todos = this.todos.filter(todo => todo.id !== id);\\n        this.saveTodos();\\n        this.renderTodos();\\n    }\\n    \\n    toggleTodo(id) {\\n        const todo = this.todos.find(t => t.id === id);\\n        if (todo) {\\n            todo.completed = !todo.completed;\\n            this.saveTodos();\\n            this.renderTodos();\\n        }\\n    }\\n    \\n    renderTodos() {\\n        this.todoList.innerHTML = '';\\n        \\n        this.todos.forEach(todo => {\\n            const li = document.createElement('li');\\n            li.className = 'todo-item';\\n            \\n            li.innerHTML = \\`\\n                <input type=\\"checkbox\\" ${todo.completed ? 'checked' : ''} \\n                       onchange=\\"app.toggleTodo(${todo.id})\\">\\n                <span class=\\"todo-text ${todo.completed ? 'completed' : ''}\\">${todo.text}</span>\\n                <button class=\\"delete-btn\\" onclick=\\"app.deleteTodo(${todo.id})\\">Delete</button>\\n            \\`;\\n            \\n            this.todoList.appendChild(li);\\n        });\\n    }\\n    \\n    saveTodos() {\\n        localStorage.setItem('todos', JSON.stringify(this.todos));\\n    }\\n}\\n\\n// Initialize the app\\nconst app = new TodoApp();",
    "README.md": "# Todo App\\n\\nA modern, responsive todo application built with vanilla HTML, CSS, and JavaScript.\\n\\n## Features\\n\\n- Add new tasks\\n- Mark tasks as completed\\n- Delete tasks\\n- Local storage persistence\\n- Responsive design\\n- Modern UI with animations\\n\\n## Usage\\n\\n1. Open index.html in your browser\\n2. Type a task in the input field\\n3. Click \\"Add Task\\" or press Enter\\n4. Click the checkbox to mark tasks as completed\\n5. Click \\"Delete\\" to remove tasks\\n\\n## Technologies Used\\n\\n- HTML5\\n- CSS3 (Flexbox, Grid, Animations)\\n- Vanilla JavaScript (ES6+)\\n- Local Storage API"
  },
  "metadata": {
    "tech_stack": ["HTML", "CSS", "JavaScript"],
    "features": ["Add tasks", "Mark complete", "Delete tasks", "Local storage", "Responsive design"],
    "patterns_used": ["Component pattern", "Event handling", "Local storage persistence"]
  }
}
```'''
            else:
                return '''```json
{
  "files": {
    "index.html": "<!DOCTYPE html>\\n<html lang=\\"en\\">\\n<head>\\n    <meta charset=\\"UTF-8\\">\\n    <meta name=\\"viewport\\" content=\\"width=device-width, initial-scale=1.0\\">\\n    <title>Interactive App</title>\\n    <link rel=\\"stylesheet\\" href=\\"styles.css\\">\\n</head>\\n<body>\\n    <div class=\\"container\\">\\n        <h1>Interactive Web App</h1>\\n        <div class=\\"content\\">\\n            <p>Welcome to your new web application!</p>\\n            <button id=\\"actionBtn\\">Click Me!</button>\\n        </div>\\n    </div>\\n    <script src=\\"script.js\\"></script>\\n</body>\\n</html>",
    "styles.css": "body { font-family: Arial, sans-serif; margin: 0; padding: 20px; background: #f0f0f0; } .container { max-width: 800px; margin: 0 auto; background: white; padding: 2rem; border-radius: 10px; box-shadow: 0 4px 6px rgba(0,0,0,0.1); } h1 { color: #333; text-align: center; } button { background: #007bff; color: white; border: none; padding: 10px 20px; border-radius: 5px; cursor: pointer; } button:hover { background: #0056b3; }",
    "script.js": "document.getElementById('actionBtn').addEventListener('click', function() { alert('Hello from your new app!'); });",
    "README.md": "# Interactive Web App\\n\\nA simple interactive web application.\\n\\n## Usage\\n\\nOpen index.html in your browser and click the button!"
  },
  "metadata": {
    "tech_stack": ["HTML", "CSS", "JavaScript"],
    "features": ["Interactive button", "Modern styling"],
    "patterns_used": ["Event handling", "DOM manipulation"]
  }
}
```'''
        
        elif "causal" in text:
            return '''```json
{
  "primary_causes": ["Insufficient validation", "Complex user requirements"],
  "causal_chains": [["User input", "Processing logic", "Output generation"], ["Pattern matching", "Code structure", "Final result"]],
  "confidence": 0.8,
  "evidence": ["Error patterns in logs", "User feedback analysis"]
}
```'''
        
        elif "counterfactual" in text:
            return '''```json
{
  "counterfactuals": [
    {
      "alternative_approach": "Step-by-step validation",
      "likely_outcome": "success",
      "confidence": 0.75,
      "reasoning": "More thorough validation would catch edge cases"
    },
    {
      "alternative_approach": "Template-based generation",
      "likely_outcome": "success", 
      "confidence": 0.8,
      "reasoning": "Templates provide more structure and consistency"
    }
  ],
  "most_promising": "Template-based generation"
}
```'''
        
        elif "similarity" in text:
            return '''```json
{
  "similarities": {
    "ui_components": {"data_visualization": 0.6, "interactive_apps": 0.7},
    "data_visualization": {"ui_components": 0.6, "interactive_apps": 0.5},
    "interactive_apps": {"ui_components": 0.7, "data_visualization": 0.5}
  }
}
```'''
        
        else:
            return "I understand your request. Let me help you with that."