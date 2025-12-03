# 🚀 Quick Start Guide

Get up and running with the MASTT in under 10 minutes!

## Prerequisites Checklist

Before you begin, make sure you have:

- [ ] **macOS** (or Linux/Windows with appropriate modifications)
- [ ] **Internet connection** (for downloading dependencies)
- [ ] **Google API Key** ([Get one here](https://makersuite.google.com/app/apikey))
- [ ] **Code repository** to test (local folder or GitHub URL)

## 5-Minute Setup

### Step 1: Get the Code

```bash
# Clone or download the project
cd mastt
```

### Step 2: Run Setup

```bash
# Make setup script executable
chmod +x setup.sh

# Run setup (installs everything automatically)
./setup.sh
```

**What this does:**
- ✅ Installs Python 3.11 and Node.js
- ✅ Creates Python virtual environment
- ✅ Installs all Python dependencies
- ✅ Installs all Node.js dependencies
- ✅ Creates output directories
- ✅ Sets up environment file

### Step 3: Configure API Key

```bash
# Edit .env file
nano .env

# Add your Google API key
GOOGLE_API_KEY=your_key_here

# Save and exit (Ctrl+X, then Y, then Enter)
```

### Step 4: Start the Application

**Terminal 1** - Start Backend:
```bash
source venv/bin/activate
python api_server.py
```

**Terminal 2** - Start Frontend:
```bash
cd frontend
npm start
```

### Step 5: Use the Web Interface

1. Browser opens automatically at `http://localhost:3000`
2. Fill in the form:
   - **Project Name**: `my_first_project`
   - **Repository Path**: Path to your code or GitHub URL
   - **Document Paths**: (Optional) Paths to docs
3. Click **"Start Project"**
4. Watch the magic happen! ✨

## What to Expect

### Timeline
- **Analysis**: 2-3 minutes
- **Planning**: 3-5 minutes
- **Test Cases**: 5-7 minutes
- **Automation**: 10-15 minutes
- **Documentation**: 2-3 minutes

**Total: ~20-30 minutes** for complete project

### Progress Phases

You'll see these phases in order:

1. 📊 **Code Analysis** - Understanding your codebase
2. 📄 **Document Processing** - Reading your docs
3. 📝 **Test Planning** - Creating strategy
4. ✍️ **Test Case Writing** - Writing test cases
5. 🤖 **Automation Generation** - Creating automation code
6. 📚 **Documentation** - Writing guides
7. ✅ **Complete** - All done!

### Output Location

Find your generated files in:
```
output/
└── my_first_project/
    ├── test_plans/          # Test plan documents
    ├── test_cases/          # All test cases
    ├── automation_code/     # Complete automation code
    ├── documentation/       # All documentation
    └── reports/            # Final reports
```

## Quick Examples

### Example 1: Test a GitHub Project

```javascript
// In the web interface, enter:
Project Name: github_project
Repository Type: GitHub URL
Repository Path: https://github.com/user/repo
```

### Example 2: Test Local Code

```javascript
Project Name: local_project
Repository Type: Local Path
Repository Path: /Users/yourname/projects/myapp
Document Paths: /Users/yourname/projects/myapp/docs
```

### Example 3: With Confluence

```javascript
// First, add to .env:
CONFLUENCE_URL=https://yourcompany.atlassian.net
CONFLUENCE_USERNAME=your-email@company.com
CONFLUENCE_API_TOKEN=your_token
CONFLUENCE_SPACE_KEY=PROJ

// Then in web interface:
Project Name: confluence_project
Repository Path: /path/to/code
// Confluence pages will be automatically fetched
```

## Using the Generated Code

### Run API Tests

```bash
cd output/my_first_project/automation_code/api_tests
source ../../../venv/bin/activate
pytest tests/ -v
```

### Run Database Tests

```bash
cd output/my_first_project/automation_code/db_tests
pytest tests/ -v
```

### Run CLI Tests

```bash
cd output/my_first_project/automation_code/cli_tests
pytest tests/ -v
```

### Run GUI Tests

```bash
cd output/my_first_project/automation_code/gui_tests
npm install
npm test
```

## Common Issues & Quick Fixes

### Issue: "GOOGLE_API_KEY not found"
```bash
# Make sure .env file exists and has the key
cat .env | grep GOOGLE_API_KEY

# If not, add it:
echo "GOOGLE_API_KEY=your_key_here" >> .env
```

### Issue: "Port 8000 already in use"
```bash
# Option 1: Kill the process
lsof -ti:8000 | xargs kill -9

# Option 2: Use different port
# Edit .env:
API_PORT=8001
```

### Issue: Frontend not connecting
```bash
# Check backend is running
curl http://localhost:8000/api/health

# Check proxy in frontend/package.json
# Should be: "proxy": "http://localhost:8000"
```

### Issue: Module not found
```bash
# Make sure virtual environment is activated
source venv/bin/activate

# Reinstall requirements
pip install -r requirements.txt
```

## Next Steps

Once your first project is complete:

1. **Review the Output**
   - Check test plans for completeness
   - Review test cases for your scenarios
   - Examine automation code quality

2. **Customize**
   - Modify generated test cases
   - Add more test scenarios
   - Extend automation code

3. **Integrate**
   - Add to your CI/CD pipeline
   - Share with your team
   - Run automated tests

4. **Learn More**
   - Read ARCHITECTURE.md for technical details
   - Check USAGE.md for advanced features
   - See API_REFERENCE.md for APIs

## Getting Help

### Check Logs
```bash
# Application logs
tail -f logs/app_*.log

# API server logs (if running)
# Check the terminal where api_server.py is running
```

### Verify Installation
```bash
# Check Python
python --version  # Should be 3.11+

# Check Node
node --version    # Should be 18+

# Check virtual environment
which python      # Should point to venv
```

### Test Configuration
```bash
# Use the API endpoint
curl http://localhost:8000/api/config/check

# Should return:
# {
#   "google_api_key": true,
#   "python_version": "3.11",
#   "all_valid": true
# }
```

## Pro Tips

💡 **Use meaningful project names** - They become folder names  
💡 **Start small** - Test with a small repository first  
💡 **Keep documents organized** - Better docs = better results  
💡 **Review generated code** - Customize as needed  
💡 **Provide feedback** - System learns from corrections  

## Success Checklist

- [ ] Setup completed without errors
- [ ] API key configured
- [ ] Backend server running
- [ ] Frontend accessible
- [ ] First project started successfully
- [ ] Output files generated
- [ ] Generated code reviewed

## What's Next?

🎯 **Try a Real Project**: Use your actual codebase  
📚 **Read Full Docs**: Check README.md for details  
🔧 **Customize**: Modify agents for your needs  
👥 **Share**: Show your team the results  
🚀 **Integrate**: Add to your workflow  

---

**Need Help?** Check:
- README.md - Complete documentation
- TROUBLESHOOTING.md - Common issues
- PROJECT_DOCUMENTATION.md - Technical details

**Ready to automate testing at scale!** 🎉