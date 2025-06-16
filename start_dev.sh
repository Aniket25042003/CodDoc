#!/bin/bash

echo "🚀 Starting RepoWhisperer Development Environment"
echo "=============================================="

# Check if .env file exists
if [ ! -f .env ]; then
    echo "❌ .env file not found! Please create one with your GEMINI_API_KEY"
    echo "Example:"
    echo "GEMINI_API_KEY=your_api_key_here"
    exit 1
fi

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "📦 Creating Python virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
echo "🔧 Activating virtual environment..."
source venv/bin/activate

# Install Python dependencies
echo "📚 Installing Python dependencies..."
pip install -r requirements.txt

# Check if frontend dependencies are installed
if [ ! -d "repowhisperer/node_modules" ]; then
    echo "📦 Installing frontend dependencies..."
    cd repowhisperer
    npm install
    cd ..
fi

# Create .env.local for frontend if it doesn't exist
if [ ! -f "repowhisperer/.env.local" ]; then
    echo "🔧 Creating frontend environment file..."
    echo "BACKEND_URL=http://localhost:8000" > repowhisperer/.env.local
fi

echo "🎯 Starting services..."

# Function to cleanup processes on exit
cleanup() {
    echo ""
    echo "🛑 Shutting down services..."
    kill $BACKEND_PID $FRONTEND_PID 2>/dev/null
    wait $BACKEND_PID $FRONTEND_PID 2>/dev/null
    echo "✅ Services stopped"
    exit 0
}

# Set trap to cleanup on script exit
trap cleanup EXIT INT TERM

# Start FastAPI backend
echo "🔥 Starting FastAPI backend on http://localhost:8000"
python main.py &
BACKEND_PID=$!

# Wait a moment for backend to start
sleep 3

# Start Next.js frontend
echo "⚛️  Starting Next.js frontend on http://localhost:3000"
cd repowhisperer
npm run dev &
FRONTEND_PID=$!
cd ..

echo ""
echo "✅ Both services are starting up!"
echo "   Backend:  http://localhost:8000"
echo "   Frontend: http://localhost:3000"
echo "   API Docs: http://localhost:8000/docs"
echo ""
echo "Press Ctrl+C to stop both services"

# Wait for both processes
wait $BACKEND_PID $FRONTEND_PID 