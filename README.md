# 🤖 Multi-Agent Software Testing Team [MASTT]

A comprehensive, AI-powered test automation system using Google ADK (Agent Development Kit) with 11 specialized AI agents that automatically analyze code, create test plans, write test cases, generate automation code, and produce complete documentation. Your Code, Anchored in Quality!!!

## 📋 Table of Contents

- [Overview](#overview)
- [Problem Statement](#problem-statement)
- [Solution](#solution)
- [Architecture](#architecture)
- [Features](#features)
- [Technology Stack](#technology-stack)
- [Installation](#installation)
- [Usage](#usage)
- [Agent Overview](#agent-overview)
- [Output Structure](#output-structure)
- [Configuration](#configuration)
- [Troubleshooting](#troubleshooting)

## 🎯 Overview

This project implements a multi-agent system that automates the entire software testing lifecycle. From analyzing your codebase to generating production-ready test automation code, this system handles everything with minimal human intervention.

### What It Does

1. **Analyzes** your code repository (local or GitHub)
2. **Processes** documentation (PDFs, Confluence, Wiki, etc.)
3. **Creates** comprehensive test plans and strategies
4. **Writes** detailed test cases for all components
5. **Generates** complete automation framework
6. **Implements** automated tests (API, Database, CLI, GUI)
7. **Produces** all necessary documentation

## 🔍 Problem Statement

Software testing is time-consuming and requires:
- Deep understanding of the codebase
- Comprehensive test planning
- Writing hundreds of test cases
- Building automation frameworks from scratch
- Implementing tests across multiple layers (API, DB, CLI, GUI)
- Creating extensive documentation

**Manual process:** Weeks to months  
**This system:** Hours

## ✨ Solution

An intelligent multi-agent system powered by Google's Gemini AI that:

### Key Innovations

1. **Multi-Agent Collaboration**: 11 specialized AI agents work together, each expert in their domain
2. **Autonomous Decision Making**: Agents make intelligent decisions based on code analysis
3. **Quality Assurance**: Critic agents review work and provide feedback
4. **RAG Integration**: Uses Retrieval-Augmented Generation for context-aware responses
5. **Complete Automation**: From analysis to deliverable code

### Deliverables

✅ Test Plan & Strategy Documents  
✅ 100+ Comprehensive Test Cases  
✅ Complete Automation Framework (Python + TypeScript)  
✅ API Test Automation (Python/pytest)  
✅ Database Test Automation (Python/pytest)  
✅ CLI Test Automation (Python/pytest)  
✅ GUI Test Automation (Selenium/TypeScript/Jest)  
✅ Integration & E2E Tests  
✅ Complete Documentation (README, Installation, Architecture, Usage, Debugging)  

## 🏗️ Architecture

### System Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                     User Interface (React)                   │
└────────────────────────────┬────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────┐
│                   FastAPI Backend Server                     │
└────────────────────────────┬────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────┐
│                  Workflow Orchestrator                       │
│  ┌──────────────────────────────────────────────────────┐   │
│  │  • Code Analyzer    • Document Processor             │   │
│  │  • RAG Engine       • Agent Coordinator              │   │
│  └──────────────────────────────────────────────────────┘   │
└────────────────────────────┬────────────────────────────────┘
                             │
        ┌────────────────────┼────────────────────┐
        │                    │                    │
        ▼                    ▼                    ▼
┌──────────────┐    ┌──────────────┐    ┌──────────────┐
│   Planning   │    │   Testing    │    │  Automation  │
│    Agents    │    │    Agents    │    │    Agents    │
├──────────────┤    ├──────────────┤    ├──────────────┤
│ • PM         │    │ • Test Case  │    │ • Auto Arch  │
│ • Architect  │    │   Writer     │    │ • API Auto   │
│ • Arch Crit  │    │ • Test Crit  │    │ • DB Auto    │
│              │    │              │    │ • CLI Auto   │
│              │    │              │    │ • GUI Auto   │
│              │    │              │    │ • Docs       │
└──────────────┘    └──────────────┘    └──────────────┘
        │                    │                    │
        └────────────────────┼────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────┐
│                    Output Generation                         │
│  Test Plans │ Test Cases │ Automation Code │ Documentation  │
└─────────────────────────────────────────────────────────────┘
```

### Agent Workflow

```
1. Project Manager Agent
   ├─> Coordinates all agents
   ├─> Assigns tasks
   └─> Monitors progress

2. Analysis Phase
   ├─> Code Analyzer: Analyzes repository structure
   ├─> Document Processor: Processes documentation
   └─> RAG Engine: Indexes knowledge

3. Planning Phase
   ├─> Architect Agent: Creates test plan
   └─> Architect Critic Agent: Reviews & provides feedback

4. Test Case Phase
   ├─> Test Case Writer Agent: Writes test cases
   └─> Test Critic Agent: Reviews test cases

5. Automation Phase
   ├─> Automation Architect Agent: Designs framework
   ├─> API Automation Agent: Generates API tests
   ├─> DB Automation Agent: Generates DB tests
   ├─> CLI Automation Agent: Generates CLI tests
   └─> GUI Automation Agent: Generates GUI tests

6. Documentation Phase
   └─> Documentation Agent: Creates all docs

7. Completion
   └─> Project Manager: Final report
```

## 🌟 Features

### Core Features

- **🤖 11 Specialized AI Agents**: Each agent is an expert in its domain
- **📊 Intelligent Code Analysis**: Deep analysis of code structure and complexity
- **📄 Document Processing**: Supports PDFs, Word, Markdown, Confluence
- **🧠 RAG Integration**: Context-aware responses using vector embeddings
- **✅ Quality Assurance**: Critic agents ensure high-quality output
- **🔄 Iterative Refinement**: Agents incorporate feedback automatically
- **🎯 Multi-Language Support**: Python, JavaScript, TypeScript, Java
- **🌐 Web Interface**: Beautiful React UI for easy interaction
- **📦 Complete Deliverables**: Production-ready code and documentation

### Testing Coverage

- **Backend Testing**
  - REST API testing (all HTTP methods)
  - Database testing (CRUD, integrity, transactions)
  - CLI testing (commands, arguments, outputs)
  
- **Frontend Testing**
  - GUI testing with Selenium
  - Component testing
  - Cross-browser support
  
- **Integration Testing**
  - API-Database integration
  - Frontend-Backend integration
  - Third-party integrations
  
- **End-to-End Testing**
  - Complete user journeys
  - Business workflows
  - Critical paths

## 💻 Technology Stack

### Backend
- **Python 3.11+**
- **Google ADK (Agent Development Kit)**
- **Google Gemini AI** (gemini-1.5-pro)
- **FastAPI** (API server)
- **LangChain** (RAG implementation)
- **ChromaDB** (Vector database)
- **pytest** (Testing framework)

### Frontend
- **React 18**
- **Axios** (HTTP client)
- **Modern CSS** (Responsive design)

### Test Automation
- **Python**: requests, psycopg2, SQLAlchemy
- **TypeScript**: Selenium WebDriver, Jest
- **pytest**: Testing framework for Python
- **Jest**: Testing framework for TypeScript

### DevOps
- **Git** (Version control)
- **Docker** (Containerization ready)
- **CI/CD** (GitHub Actions, Jenkins compatible)

## 🚀 Installation

### Prerequisites

- **macOS** (tested), Linux, or Windows
- **Python 3.11+**
- **Node.js 18+**
- **Git**
- **Google API Key** (for Gemini AI)

### Step 1: Clone Repository

```bash
git clone <your-repository-url>
cd mastt
```

### Step 2: Run Setup Script (macOS/Linux)

```bash
chmod +x setup.sh
./setup.sh
```

This script will:
- Install Python and Node.js (if not present)
- Create Python virtual environment
- Install all dependencies
- Setup project structure

### Step 3: Configure Environment

```bash
# Copy environment template
cp .env.example .env

# Edit .env and add your Google API key
# Get your key from: https://makersuite.google.com/app/apikey
nano .env
```

Add your configuration:
```env
GOOGLE_API_KEY=your_google_api_key_here
GEMINI_MODEL=gemini-1.5-pro
PROJECT_NAME=my_test_project
OUTPUT_DIR=./output
```

### Step 4: Verify Installation

```bash
# Activate virtual environment
source venv/bin/activate

# Test Python installation
python --version
pytest --version

# Test Node.js installation
cd frontend
npm --version
cd ..
```

## 📖 Usage

### Option 1: Using the Web Interface (Recommended)

1. **Start the Backend API Server**:
   ```bash
   source venv/bin/activate
   python api_server.py
   ```
   Server starts at `http://localhost:8000`

2. **Start the Frontend** (in a new terminal):
   ```bash
   cd frontend
   npm start
   ```
   UI opens at `http://localhost:3000`

3. **Configure Your Project**:
   - Enter project name
   - Provide repository path (local or GitHub URL)
   - Add documentation paths
   - Click "Start Project"

4. **Monitor Progress**:
   - Watch real-time progress
   - See which agents are working
   - View completion status

5. **Download Results**:
   - Download generated files
   - Copy automation code
   - Review documentation

### Option 2: Using Command Line

```bash
# Activate environment
source venv/bin/activate

# Edit main.py with your configuration
# Then run:
python main.py
```

### Option 3: Python API

```python
from main import MASTT

# Configure project
config = {
    'project_name': 'my_project',
    'repository_path': './my_code',
    'document_paths': ['./docs'],
    'output_dir': './output'
}

# Initialize and run
app = MASTT(config)
app.initialize()
result = app.run_complete_workflow()

print(f"Output: {result['output_directory']}")
```

## 🤖 Agent Overview

### 1. Project Manager Agent
**Role**: Orchestrates all activities, assigns tasks, monitors progress

**Responsibilities**:
- Create project plan
- Assign tasks to agents
- Monitor progress
- Handle user feedback
- Generate final report

### 2. Architect Agent
**Role**: Creates comprehensive test plans and strategies

**Outputs**:
- Test plan document
- Testing strategies
- Coverage analysis
- Risk assessment

### 3. Architect Critic Agent
**Role**: Reviews test plans and provides feedback

**Provides**:
- Completeness assessment
- Technical accuracy review
- Gap identification
- Improvement recommendations

### 4. Test Case Writer Agent
**Role**: Writes detailed test cases

**Generates**:
- API test cases
- Database test cases
- CLI test cases
- GUI test cases
- Integration test cases
- E2E test cases

### 5. Test Critic Agent
**Role**: Reviews test cases for quality

**Reviews**:
- Completeness
- Clarity
- Executability
- Coverage
- Test data quality

### 6. Automation Architect Agent
**Role**: Designs automation framework

**Creates**:
- Framework structure
- Base classes
- Configuration management
- Utilities
- Reporting setup

### 7. API Automation Agent
**Role**: Generates Python-based API tests

**Produces**:
- BaseAPIClient class
- Endpoint implementations
- Test files with pytest
- Fixtures and utilities

### 8. DB Automation Agent
**Role**: Generates Python-based database tests

**Produces**:
- Database connection handler
- Model classes
- CRUD test implementations
- Data validators

### 9. CLI Automation Agent
**Role**: Generates Python-based CLI tests

**Produces**:
- CLI wrapper class
- Command execution utilities
- Output parsers
- Validation helpers

### 10. GUI Automation Agent
**Role**: Generates Selenium TypeScript tests

**Produces**:
- Page Object classes
- Selenium test files
- Wait utilities
- Screenshot helpers

### 11. Documentation Agent
**Role**: Creates all documentation

**Generates**:
- README.md
- INSTALLATION.md
- ARCHITECTURE.md
- USAGE.md
- DEBUGGING.md
- API_REFERENCE.md

## 📁 Output Structure

```
output/
└── my_project/
    ├── test_plans/
    │   ├── test_plan.md
    │   ├── test_plan_review.json
    │   └── test_plan_revised.md
    ├── test_cases/
    │   ├── test_cases.json
    │   └── test_cases_review.json
    ├── automation_code/
    │   ├── framework/
    │   │   ├── config/
    │   │   ├── utilities/
    │   │   └── requirements.txt
    │   ├── api_tests/
    │   │   ├── base_api.py
    │   │   ├── tests/
    │   │   └── fixtures.py
    │   ├── db_tests/
    │   │   ├── db_connection.py
    │   │   ├── models/
    │   │   └── tests/
    │   ├── cli_tests/
    │   │   ├── cli_wrapper.py
    │   │   └── tests/
    │   └── gui_tests/
    │       ├── pages/
    │       ├── tests/
    │       └── package.json
    ├── documentation/
    │   ├── README.md
    │   ├── INSTALLATION.md
    │   ├── ARCHITECTURE.md
    │   ├── USAGE.md
    │   └── DEBUGGING.md
    ├── reports/
    │   └── final_report.md
    └── logs/
        └── execution.log
```

## ⚙️ Configuration

### Environment Variables

```env
# Required
GOOGLE_API_KEY=your_api_key

# Optional
GEMINI_MODEL=gemini-1.5-pro
GEMINI_TEMPERATURE=0.7
PROJECT_NAME=my_project
OUTPUT_DIR=./output

# Confluence (Optional)
CONFLUENCE_URL=https://your-instance.atlassian.net
CONFLUENCE_USERNAME=your-email
CONFLUENCE_API_TOKEN=your-token
CONFLUENCE_SPACE_KEY=SPACE

# Database (for testing)
DB_HOST=localhost
DB_PORT=5432
```

### Project Configuration

```python
project_config = {
    'project_name': 'my_project',
    'repository_path': './code',  # or GitHub URL
    'document_paths': ['./docs', './requirements'],
    'output_dir': './output',
    'confluence': {
        'url': 'https://...',
        'username': 'email',
        'token': 'token',
        'space_key': 'KEY'
    }
}
```

## 🐛 Troubleshooting

### Common Issues

**Issue**: `GOOGLE_API_KEY not found`
**Solution**: Ensure `.env` file exists with valid API key

**Issue**: `Module not found`
**Solution**: Activate virtual environment: `source venv/bin/activate`

**Issue**: `Port 8000 already in use`
**Solution**: Change port in `.env`: `API_PORT=8001`

**Issue**: Frontend not connecting to backend
**Solution**: Check `proxy` in `frontend/package.json` matches backend URL

### Getting Help

1. Check logs in `./logs/`
2. Review error messages carefully
3. Ensure all prerequisites are installed
4. Verify environment variables are set

## 🎓 Technical Implementation Details

### RAG Implementation

The system uses Retrieval-Augmented Generation (RAG) to provide context-aware responses:

1. **Document Processing**: All documentation is processed and chunked
2. **Embedding Generation**: Google's embedding model creates vector representations
3. **Vector Storage**: ChromaDB stores embeddings for fast retrieval
4. **Context Retrieval**: Agents query relevant context before generating responses

### Agent Communication

Agents communicate through the Workflow Orchestrator:

1. **Task Assignment**: PM Agent assigns tasks
2. **Context Provision**: Orchestrator provides necessary context
3. **Result Storage**: Agent outputs are stored centrally
4. **Feedback Loop**: Critic agents provide feedback for refinement

### Code Generation Strategy

Code generation follows these principles:

1. **Template-Based**: Uses proven patterns and templates
2. **Context-Aware**: Incorporates project-specific information
3. **Best Practices**: Follows industry standards
4. **Production-Ready**: Generates executable, maintainable code

## 🚀 Future Enhancements

- [ ] Support for more programming languages
- [ ] Integration with JIRA for ticket analysis
- [ ] Visual test reporting dashboard
- [ ] CI/CD pipeline auto-generation
- [ ] Performance testing capabilities
- [ ] Security testing integration
- [ ] Test execution engine
- [ ] Real-time collaboration features

## 📄 License

MIT License - Feel free to use and modify for your projects

## 👥 Contributing

Contributions are welcome! Please:

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## 🙏 Acknowledgments

- Google ADK Team for the agent framework
- Google Gemini AI for powerful language models
- Open source community for amazing tools

## 📧 Support

For issues, questions, or feedback:
- Create an issue on GitHub
- Check documentation
- Review troubleshooting guide

## 👤 Author

### Rajarajan Ezhumalai
#### Engineering Leader | AI | Automation Enthusiast
https://www.linkedin.com/in/rajarajanezhumalai/

---

**Built with ❤️ using Google ADK and Gemini AI**