#!/bin/bash
# Quick setup script for Gemma Validation

set -e

echo "🚀 Gemma Validation - Quick Setup"
echo "=================================="

# Check Python
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 not found. Please install Python 3.8+"
    exit 1
fi

echo "✅ Python3 found: $(python3 --version)"

# Create venv if needed
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
fi

# Activate venv
source venv/bin/activate

# Install dependencies
echo "📚 Installing dependencies..."
pip install -q -r requirements.txt

# Navigate to validation directory
cd gemma_validation

# Run migrations
echo "🔄 Initializing database..."
python manage.py migrate --no-input

# Load sample data
echo "📝 Loading sample exercises..."
python manage.py load_sample_exercises

echo ""
echo "✅ Setup complete!"
echo ""
echo "📖 Next steps:"
echo "  1. Make sure Ollama/LM Studio is running:"
echo "     ollama serve"
echo ""
echo "  2. In another terminal, start the API server:"
echo "     python run_server.py"
echo ""
echo "  3. In another terminal, run tests:"
echo "     python test_validation.py"
echo ""
echo "  4. Access the API:"
echo "     http://localhost:8000/api/exercises/"
echo ""
echo "For more details, see GETTING_STARTED.md"
