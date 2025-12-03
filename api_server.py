"""
FastAPI server for the frontend interface.
"""

import os
import sys
from pathlib import Path
from typing import Dict, Optional
from fastapi import FastAPI, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from dotenv import load_dotenv
from loguru import logger
import json
from datetime import datetime

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent))

# Load environment variables
load_dotenv()

from main import MASTT

# Initialize FastAPI
app = FastAPI(
    title="MASTT Automation API",
    description="API for Multi-Agent Test Automation System",
    version="1.0.0"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify exact origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global state
current_workflow = None
workflow_status = {
    'status': 'idle',
    'progress': 0,
    'current_phase': None,
    'message': 'Ready to start'
}


class ProjectConfig(BaseModel):
    """Project configuration model."""
    project_name: str
    repository_path: str
    repository_type: str = 'local'  # 'local' or 'github'
    document_paths: list = []
    confluence_url: Optional[str] = None
    confluence_username: Optional[str] = None
    confluence_token: Optional[str] = None
    confluence_space_key: Optional[str] = None


class FeedbackRequest(BaseModel):
    """User feedback model."""
    feedback_type: str
    area: Optional[str] = None
    details: str


@app.get("/")
async def root():
    """Root endpoint."""
    return {
        "message": "MASTT Automation API",
        "version": "1.0.0",
        "status": "running"
    }


@app.get("/api/health")
async def health_check():
    """Health check endpoint."""
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat()
    }


@app.post("/api/project/start")
async def start_project(config: ProjectConfig, background_tasks: BackgroundTasks):
    """
    Start a new test automation project.
    
    Args:
        config: Project configuration
        background_tasks: FastAPI background tasks
    """
    global current_workflow, workflow_status
    
    try:
        # Validate Google API key
        if not os.getenv('GOOGLE_API_KEY'):
            raise HTTPException(
                status_code=400,
                detail="GOOGLE_API_KEY not configured"
            )
        
        # Create project config
        project_config = {
            'project_name': config.project_name,
            'repository_path': config.repository_path,
            'document_paths': config.document_paths,
            'output_dir': f'./output/{config.project_name}',
            'confluence': {
                'url': config.confluence_url,
                'username': config.confluence_username,
                'token': config.confluence_token,
                'space_key': config.confluence_space_key
            }
        }
        
        # Initialize workflow
        workflow_status = {
            'status': 'initializing',
            'progress': 5,
            'current_phase': 'Initialization',
            'message': 'Starting project...'
        }
        
        # Run workflow in background
        background_tasks.add_task(run_workflow, project_config)
        
        return {
            'status': 'started',
            'message': 'Project workflow started',
            'project_name': config.project_name
        }
        
    except Exception as e:
        logger.error(f"Error starting project: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


async def run_workflow(project_config: dict):
    """Run workflow in background."""
    global current_workflow, workflow_status
    
    try:
        # Update status
        workflow_status['status'] = 'running'
        workflow_status['progress'] = 10
        workflow_status['current_phase'] = 'Code Analysis'
        
        # Initialize application
        app_instance = MASTT(project_config)
        app_instance.initialize()
        current_workflow = app_instance
        
        # Run complete workflow with status updates
        workflow_status['progress'] = 20
        workflow_status['current_phase'] = 'Document Processing'
        
        result = app_instance.run_complete_workflow()
        
        # Update final status
        if result['status'] == 'success':
            workflow_status['status'] = 'completed'
            workflow_status['progress'] = 100
            workflow_status['current_phase'] = 'Complete'
            workflow_status['message'] = 'All deliverables generated successfully'
            workflow_status['output_directory'] = result['output_directory']
        else:
            workflow_status['status'] = 'failed'
            workflow_status['message'] = result.get('error', 'Unknown error')
        
    except Exception as e:
        logger.error(f"Workflow error: {str(e)}", exc_info=True)
        workflow_status['status'] = 'failed'
        workflow_status['message'] = str(e)


@app.get("/api/project/status")
async def get_project_status():
    """Get current project status."""
    return workflow_status


@app.get("/api/project/results")
async def get_project_results():
    """Get project results."""
    global current_workflow
    
    if not current_workflow:
        raise HTTPException(status_code=404, detail="No workflow running")
    
    if workflow_status['status'] != 'completed':
        raise HTTPException(
            status_code=400,
            detail="Workflow not completed yet"
        )
    
    try:
        results = {
            'test_plan': bool(current_workflow.orchestrator.results.get('test_plan')),
            'test_cases': bool(current_workflow.orchestrator.results.get('test_cases')),
            'automation_framework': bool(current_workflow.orchestrator.results.get('automation_framework')),
            'api_automation': bool(current_workflow.orchestrator.results['automation_code'].get('api')),
            'db_automation': bool(current_workflow.orchestrator.results['automation_code'].get('database')),
            'cli_automation': bool(current_workflow.orchestrator.results['automation_code'].get('cli')),
            'gui_automation': bool(current_workflow.orchestrator.results['automation_code'].get('gui')),
            'documentation': bool(current_workflow.orchestrator.results.get('documentation')),
            'output_directory': str(current_workflow.orchestrator.output_dir)
        }
        
        return results
        
    except Exception as e:
        logger.error(f"Error getting results: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/project/feedback")
async def submit_feedback(feedback: FeedbackRequest):
    """
    Submit user feedback for improvements.
    
    Args:
        feedback: User feedback
    """
    global current_workflow
    
    if not current_workflow:
        raise HTTPException(status_code=404, detail="No workflow running")
    
    try:
        feedback_dict = {
            'type': feedback.feedback_type,
            'area': feedback.area,
            'feedback': feedback.details
        }
        
        action_plan = current_workflow.handle_user_feedback(feedback_dict)
        
        return {
            'status': 'received',
            'message': 'Feedback processed',
            'action_plan': action_plan
        }
        
    except Exception as e:
        logger.error(f"Error processing feedback: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/files/list")
async def list_output_files():
    """List all generated output files."""
    global current_workflow
    
    if not current_workflow:
        raise HTTPException(status_code=404, detail="No workflow running")
    
    try:
        output_dir = current_workflow.orchestrator.output_dir
        files = []
        
        for root, dirs, filenames in os.walk(output_dir):
            for filename in filenames:
                file_path = Path(root) / filename
                rel_path = file_path.relative_to(output_dir)
                
                files.append({
                    'name': filename,
                    'path': str(rel_path),
                    'size': file_path.stat().st_size,
                    'modified': datetime.fromtimestamp(
                        file_path.stat().st_mtime
                    ).isoformat()
                })
        
        return {'files': files, 'total': len(files)}
        
    except Exception as e:
        logger.error(f"Error listing files: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/files/download/{file_path:path}")
async def download_file(file_path: str):
    """Download a specific output file."""
    global current_workflow
    
    if not current_workflow:
        raise HTTPException(status_code=404, detail="No workflow running")
    
    try:
        output_dir = current_workflow.orchestrator.output_dir
        full_path = output_dir / file_path
        
        if not full_path.exists():
            raise HTTPException(status_code=404, detail="File not found")
        
        # Read file content
        with open(full_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        return {
            'filename': full_path.name,
            'content': content,
            'size': len(content)
        }
        
    except Exception as e:
        logger.error(f"Error downloading file: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/config/check")
async def check_configuration():
    """Check if configuration is valid."""
    python_version = f"{sys.version_info.major}.{sys.version_info.minor}"
    python_version_valid = sys.version_info.major == 3 and sys.version_info.minor >= 9
    
    checks = {
        'google_api_key': bool(os.getenv('GOOGLE_API_KEY')),
        'python_version': python_version,
        'python_version_valid': python_version_valid,
        'output_dir_writable': os.access('./output', os.W_OK) if os.path.exists('./output') else True
    }
    
    checks['all_valid'] = all([
        checks['google_api_key'],
        python_version_valid
    ])
    
    return checks


if __name__ == "__main__":
    import uvicorn
    
    port = int(os.getenv('API_PORT', 8000))
    host = os.getenv('API_HOST', '0.0.0.0')
    
    logger.info(f"Starting API server on {host}:{port}")
    
    uvicorn.run(
        "api_server:app",
        host=host,
        port=port,
        reload=True,
        log_level="info"
    )
