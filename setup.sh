#!/bin/bash

echo "==================================================================="
echo "MASTT - Multi Agent Software Testing Team - Setup Script - MacOS"
echo "Your Code, Anchored in Quality."
echo "==================================================================="

# Check if Homebrew is installed
if ! command -v brew &> /dev/null; then
    echo "Installing Homebrew..."
    /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
else
    echo "✓ Homebrew already installed"
fi

# Install Python 3.11
echo "Installing Python 3.11..."
if ! command -v python3.11 &> /dev/null; then
    brew install python@3.11
else
    echo "✓ Python 3.11 already installed"
fi

# Install Node.js and npm
echo "Installing Node.js..."
if ! command -v node &> /dev/null; then
    brew install node
else
    echo "✓ Node.js already installed"
fi

# Install TypeScript globally
echo "Installing TypeScript..."
npm install -g typescript

# Create virtual environment
echo "Creating Python virtual environment..."
python3.11 -m venv venv

# Activate virtual environment
source venv/bin/activate

# Upgrade pip
echo "Upgrading pip..."
pip install --upgrade pip

# Install Python dependencies
echo "Installing Python dependencies..."
pip install -r requirements.txt

# Install Node.js dependencies for frontend
echo "Installing Node.js dependencies..."
cd frontend
npm install
cd ..

# Create .env file from example
if [ ! -f .env ]; then
    echo "Creating .env file..."
    cp .env.example .env
    echo "⚠️  Please edit .env file and add your Google API key"
else
    echo "✓ .env file already exists"
fi

# Create output directory
mkdir -p output/{test_plans,test_cases,automation_code,reports,documentation}

echo ""
echo "================================================"
echo "Setup Complete!"
echo "================================================"
echo ""
echo "Next Steps:"
echo "1. Edit .env file and add your GOOGLE_API_KEY"
echo "2. Activate the virtual environment: source venv/bin/activate"
echo "3. Run the application: python api_server.py.py"
echo "4. Start frontend (in another terminal): cd frontend && npm start"
echo ""
echo "To get your Google API Key:"
echo "Visit: https://makersuite.google.com/app/apikey"
echo ""
