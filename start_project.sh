#!/bin/bash

echo "🚀 Starting CodeForge with Advanced Self-Learning System"
echo "=========================================================="

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Function to check if a command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Check prerequisites
echo -e "${BLUE}Checking prerequisites...${NC}"

if ! command_exists python3; then
    echo -e "${RED}Error: Python 3 is not installed${NC}"
    exit 1
fi

if ! command_exists node; then
    echo -e "${RED}Error: Node.js is not installed${NC}"
    exit 1
fi

if ! command_exists yarn; then
    echo -e "${RED}Error: Yarn is not installed. Installing...${NC}"
    npm install -g yarn
fi

# Setup Backend
echo -e "\n${BLUE}Setting up Backend...${NC}"
cd backend

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment and install dependencies
echo "Installing backend dependencies..."
source venv/bin/activate
pip install -q -r requirements.txt

# Check if .env exists
if [ ! -f ".env" ]; then
    echo "Creating .env file..."
    cat > .env << EOF
MONGO_URL=mongodb://localhost:27017
DB_NAME=codeforge
EMERGENT_LLM_KEY=demo-key
CORS_ORIGINS=http://localhost:3000
EOF
fi

echo -e "${GREEN}✓ Backend setup complete${NC}"

# Setup Frontend
echo -e "\n${BLUE}Setting up Frontend...${NC}"
cd ../frontend

# Install frontend dependencies if needed
if [ ! -d "node_modules" ]; then
    echo "Installing frontend dependencies..."
    yarn install
fi

# Check if .env exists
if [ ! -f ".env" ]; then
    echo "Creating frontend .env file..."
    cat > .env << EOF
REACT_APP_BACKEND_URL=http://localhost:8000
EOF
fi

echo -e "${GREEN}✓ Frontend setup complete${NC}"

# Start MongoDB (if not running)
echo -e "\n${BLUE}Checking MongoDB...${NC}"
if ! pgrep -x "mongod" > /dev/null; then
    echo "MongoDB is not running. Attempting to start..."
    if command_exists mongod; then
        mongod --fork --logpath /tmp/mongodb.log --dbpath /tmp/mongodb-data 2>/dev/null || echo "Note: MongoDB not started (optional for demo)"
    else
        echo "Note: MongoDB not installed. Using in-memory storage for demo."
    fi
else
    echo -e "${GREEN}✓ MongoDB is running${NC}"
fi

# Start Backend Server
echo -e "\n${BLUE}Starting Backend Server on http://localhost:8000${NC}"
cd ../backend
source venv/bin/activate
uvicorn server:app --reload --host 0.0.0.0 --port 8000 > /tmp/codeforge-backend.log 2>&1 &
BACKEND_PID=$!
echo "Backend PID: $BACKEND_PID"

# Wait for backend to start
echo "Waiting for backend to start..."
sleep 3

# Check if backend is running
if curl -s http://localhost:8000/api/ > /dev/null; then
    echo -e "${GREEN}✓ Backend is running${NC}"
else
    echo -e "${RED}Warning: Backend may not have started properly${NC}"
    echo "Check logs: tail -f /tmp/codeforge-backend.log"
fi

# Start Frontend Server
echo -e "\n${BLUE}Starting Frontend Server on http://localhost:3000${NC}"
cd ../frontend
BROWSER=none yarn start > /tmp/codeforge-frontend.log 2>&1 &
FRONTEND_PID=$!
echo "Frontend PID: $FRONTEND_PID"

# Wait for frontend to start
echo "Waiting for frontend to start..."
sleep 5

echo -e "\n${GREEN}=========================================================="
echo "✓ CodeForge is now running!"
echo "==========================================================${NC}"
echo ""
echo "📊 Access the application:"
echo "   Frontend: http://localhost:3000"
echo "   Backend API: http://localhost:8000/api/"
echo "   API Docs: http://localhost:8000/docs"
echo ""
echo "🧠 Advanced Self-Learning Features:"
echo "   • Multi-level Reflexion Framework"
echo "   • Curriculum Learning System"
echo "   • Meta-Learning Engine"
echo "   • Adaptive Task Recommendations"
echo ""
echo "📝 Logs:"
echo "   Backend: tail -f /tmp/codeforge-backend.log"
echo "   Frontend: tail -f /tmp/codeforge-frontend.log"
echo ""
echo "🛑 To stop the servers:"
echo "   kill $BACKEND_PID $FRONTEND_PID"
echo ""
echo "Press Ctrl+C to stop monitoring..."

# Monitor logs
tail -f /tmp/codeforge-backend.log /tmp/codeforge-frontend.log
