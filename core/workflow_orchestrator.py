"""
Workflow Orchestrator - Coordinates all agents and manages the testing workflow.
"""

import os
import json
from typing import Dict, List, Optional, Any
from pathlib import Path
from datetime import datetime
from loguru import logger
from enum import Enum

from .code_analyzer import CodeAnalyzer
from .document_processor import DocumentProcessor
from .rag_engine import RAGEngine


class WorkflowStage(Enum):
    """Stages in the testing workflow."""
    INITIALIZATION = "initialization"
    CODE_ANALYSIS = "code_analysis"
    DOCUMENT_PROCESSING = "document_processing"
    TEST_PLANNING = "test_planning"
    TEST_PLANNING_REVIEW = "test_planning_review"
    TEST_CASE_WRITING = "test_case_writing"
    TEST_CASE_REVIEW = "test_case_review"
    AUTOMATION_FRAMEWORK = "automation_framework"
    API_AUTOMATION = "api_automation"
    DB_AUTOMATION = "db_automation"
    CLI_AUTOMATION = "cli_automation"
    GUI_AUTOMATION = "gui_automation"
    DOCUMENTATION = "documentation"
    FINAL_REVIEW = "final_review"
    COMPLETE = "complete"


class WorkflowOrchestrator:
    """Orchestrates the multi-agent testing workflow."""
    
    def __init__(self, project_config: Dict):
        """
        Initialize workflow orchestrator.
        
        Args:
            project_config: Project configuration dictionary
        """
        self.project_config = project_config
        self.project_name = project_config.get('project_name', 'test_project')
        self.output_dir = Path(project_config.get('output_dir', './output'))
        
        # Create output directory structure
        self.setup_output_directories()
        
        # Initialize workflow state
        self.workflow_state = {
            'current_stage': WorkflowStage.INITIALIZATION.value,
            'completed_stages': [],
            'agent_outputs': {},
            'start_time': datetime.now().isoformat(),
            'end_time': None,
            'status': 'in_progress'
        }
        
        # Initialize core components
        self.code_analyzer = None
        self.document_processor = None
        self.rag_engine = None
        
        # Agent results storage
        self.results = {
            'code_analysis': None,
            'test_plan': None,
            'test_plan_review': None,
            'test_cases': None,
            'test_case_review': None,
            'automation_framework': None,
            'automation_code': {
                'api': None,
                'database': None,
                'cli': None,
                'gui': None
            },
            'documentation': None
        }
        
        logger.info(f"Workflow orchestrator initialized for project: {self.project_name}")
    
    def setup_output_directories(self):
        """Create output directory structure."""
        directories = [
            'test_plans',
            'test_cases',
            'automation_code/framework',
            'automation_code/api_tests',
            'automation_code/db_tests',
            'automation_code/cli_tests',
            'automation_code/gui_tests',
            'automation_code/integration_tests',
            'automation_code/e2e_tests',
            'automation_code/utilities',
            'reports',
            'documentation',
            'logs'
        ]
        
        for directory in directories:
            dir_path = self.output_dir / directory
            dir_path.mkdir(parents=True, exist_ok=True)
        
        logger.info(f"Output directories created at: {self.output_dir}")
    
    def initialize_components(self):
        """Initialize code analyzer, document processor, and RAG engine."""
        logger.info("Initializing workflow components...")
        
        # Initialize code analyzer
        repo_path = self.project_config.get('repository_path')
        if repo_path:
            self.code_analyzer = CodeAnalyzer(repo_path)
            logger.info("Code analyzer initialized")
        
        # Initialize document processor
        confluence_config = self.project_config.get('confluence', {})
        self.document_processor = DocumentProcessor(
            confluence_url=confluence_config.get('url'),
            confluence_username=confluence_config.get('username'),
            confluence_token=confluence_config.get('token')
        )
        logger.info("Document processor initialized")
        
        # Initialize RAG engine
        self.rag_engine = RAGEngine(
            vector_db_path=str(self.output_dir / 'vector_db'),
            collection_name=f"{self.project_name}_docs"
        )
        logger.info("RAG engine initialized")
    
    def run_code_analysis(self) -> Dict:
        """
        Run code analysis stage.
        
        Returns:
            Code analysis results
        """
        logger.info("=" * 60)
        logger.info("STAGE: Code Analysis")
        logger.info("=" * 60)
        
        self.update_stage(WorkflowStage.CODE_ANALYSIS)
        
        if not self.code_analyzer:
            logger.error("Code analyzer not initialized")
            return None
        
        # Run full analysis
        analysis_results = self.code_analyzer.full_analysis()
        
        # Save results
        self.code_analyzer.save_analysis(str(self.output_dir))
        self.results['code_analysis'] = analysis_results
        
        # Mark stage complete
        self.complete_stage(WorkflowStage.CODE_ANALYSIS, analysis_results)
        
        logger.info("Code analysis complete")
        return analysis_results
    
    def run_document_processing(self) -> List[Dict]:
        """
        Run document processing stage.
        
        Returns:
            List of processed documents
        """
        logger.info("=" * 60)
        logger.info("STAGE: Document Processing")
        logger.info("=" * 60)
        
        self.update_stage(WorkflowStage.DOCUMENT_PROCESSING)
        
        documents = []
        
        # Process local documents
        doc_paths = self.project_config.get('document_paths', [])
        for doc_path in doc_paths:
            if os.path.isdir(doc_path):
                docs = self.document_processor.process_directory(doc_path)
                documents.extend(docs)
            elif os.path.isfile(doc_path):
                doc = self.document_processor.process_file(doc_path)
                if doc:
                    documents.append(doc)
        
        # Fetch Confluence pages if configured
        confluence_config = self.project_config.get('confluence', {})
        if confluence_config.get('space_key'):
            confluence_docs = self.document_processor.fetch_confluence_space(
                confluence_config['space_key']
            )
            documents.extend(confluence_docs)
        
        # Add documents to RAG engine
        if documents:
            chunk_count = self.rag_engine.add_documents(documents)
            logger.info(f"Added {chunk_count} chunks to RAG engine")
        
        # Save processed documents
        self.document_processor.processed_documents = documents
        self.document_processor.save_processed_documents(str(self.output_dir))
        
        # Mark stage complete
        self.complete_stage(WorkflowStage.DOCUMENT_PROCESSING, {
            'total_documents': len(documents),
            'rag_chunks': chunk_count
        })
        
        logger.info(f"Document processing complete: {len(documents)} documents processed")
        return documents
    
    def update_stage(self, stage: WorkflowStage):
        """Update current workflow stage."""
        self.workflow_state['current_stage'] = stage.value
        logger.info(f"Current stage: {stage.value}")
    
    def complete_stage(self, stage: WorkflowStage, output: Any):
        """Mark a stage as complete and store its output."""
        self.workflow_state['completed_stages'].append(stage.value)
        self.workflow_state['agent_outputs'][stage.value] = {
            'completed_at': datetime.now().isoformat(),
            'output': output
        }
        logger.info(f"Stage complete: {stage.value}")
    
    def get_context_for_agent(self, 
                               agent_type: str, 
                               query: str,
                               include_code_analysis: bool = True) -> str:
        """
        Get relevant context for an agent.
        
        Args:
            agent_type: Type of agent requesting context
            query: Query for RAG retrieval
            include_code_analysis: Whether to include code analysis results
            
        Returns:
            Formatted context string
        """
        context_parts = []
        
        # Add code analysis if requested
        if include_code_analysis and self.results['code_analysis']:
            context_parts.append("=== CODE ANALYSIS RESULTS ===")
            context_parts.append(json.dumps(self.results['code_analysis']['summary'], indent=2))
            context_parts.append("")
        
        # Get RAG context
        if self.rag_engine:
            rag_context = self.rag_engine.get_context_for_agent(
                query=query,
                agent_type=agent_type
            )
            if rag_context:
                context_parts.append("=== RELEVANT DOCUMENTATION ===")
                context_parts.append(rag_context)
                context_parts.append("")
        
        # Add previous agent outputs if relevant
        if agent_type in ['test_case_writer', 'test_critic']:
            if self.results['test_plan']:
                context_parts.append("=== TEST PLAN ===")
                context_parts.append(str(self.results['test_plan']))
                context_parts.append("")
        
        if agent_type.endswith('_automation_agent'):
            if self.results['test_cases']:
                context_parts.append("=== TEST CASES ===")
                context_parts.append(str(self.results['test_cases']))
                context_parts.append("")
            
            if self.results['automation_framework']:
                context_parts.append("=== AUTOMATION FRAMEWORK ===")
                context_parts.append(str(self.results['automation_framework']))
                context_parts.append("")
        
        return "\n".join(context_parts)
    
    def save_agent_output(self, 
                          agent_name: str, 
                          output: Any, 
                          filename: str):
        """
        Save agent output to file.
        
        Args:
            agent_name: Name of the agent
            output: Output to save
            filename: Filename to save to
        """
        # Determine output directory based on agent type
        if 'architect' in agent_name.lower() or 'plan' in agent_name.lower():
            output_dir = self.output_dir / 'test_plans'
        elif 'test_case' in agent_name.lower():
            output_dir = self.output_dir / 'test_cases'
        elif 'automation' in agent_name.lower():
            output_dir = self.output_dir / 'automation_code'
        elif 'documentation' in agent_name.lower():
            output_dir = self.output_dir / 'documentation'
        else:
            output_dir = self.output_dir
        
        output_path = output_dir / filename
        
        # Save based on type
        if isinstance(output, (dict, list)):
            with open(output_path, 'w') as f:
                json.dump(output, f, indent=2)
        else:
            with open(output_path, 'w') as f:
                f.write(str(output))
        
        logger.info(f"Saved {agent_name} output to {output_path}")
    
    def get_workflow_status(self) -> Dict:
        """Get current workflow status."""
        return {
            'project_name': self.project_name,
            'current_stage': self.workflow_state['current_stage'],
            'completed_stages': self.workflow_state['completed_stages'],
            'total_stages': len(WorkflowStage),
            'progress_percentage': len(self.workflow_state['completed_stages']) / len(WorkflowStage) * 100,
            'status': self.workflow_state['status'],
            'start_time': self.workflow_state['start_time']
        }
    
    def finalize_workflow(self):
        """Finalize workflow and generate final report."""
        logger.info("=" * 60)
        logger.info("FINALIZING WORKFLOW")
        logger.info("=" * 60)
        
        self.workflow_state['end_time'] = datetime.now().isoformat()
        self.workflow_state['status'] = 'completed'
        self.update_stage(WorkflowStage.COMPLETE)
        
        # Generate final report
        report = {
            'project_name': self.project_name,
            'workflow_state': self.workflow_state,
            'results_summary': {
                'code_analysis': bool(self.results['code_analysis']),
                'test_plan_generated': bool(self.results['test_plan']),
                'test_cases_generated': bool(self.results['test_cases']),
                'automation_framework_generated': bool(self.results['automation_framework']),
                'api_tests_generated': bool(self.results['automation_code']['api']),
                'db_tests_generated': bool(self.results['automation_code']['database']),
                'cli_tests_generated': bool(self.results['automation_code']['cli']),
                'gui_tests_generated': bool(self.results['automation_code']['gui']),
                'documentation_generated': bool(self.results['documentation'])
            },
            'output_location': str(self.output_dir)
        }
        
        # Save final report
        report_path = self.output_dir / 'final_report.json'
        with open(report_path, 'w') as f:
            json.dump(report, f, indent=2)
        
        logger.info(f"Final report saved to {report_path}")
        logger.info("Workflow complete!")
        
        return report
    
    def handle_user_feedback(self, feedback: Dict) -> Dict:
        """
        Handle user feedback and coordinate fixes.
        
        Args:
            feedback: User feedback dictionary
            
        Returns:
            Response indicating what will be fixed
        """
        logger.info("Processing user feedback...")
        
        response = {
            'feedback_received': feedback,
            'actions_to_take': [],
            'agents_to_invoke': []
        }
        
        # Determine which agents need to be re-invoked
        feedback_type = feedback.get('type', 'general')
        
        if feedback_type == 'test_plan':
            response['agents_to_invoke'].extend(['architect_agent', 'architect_critic_agent'])
        elif feedback_type == 'test_cases':
            response['agents_to_invoke'].extend(['test_case_writer_agent', 'test_critic_agent'])
        elif feedback_type == 'automation':
            automation_area = feedback.get('area', 'all')
            if automation_area == 'api' or automation_area == 'all':
                response['agents_to_invoke'].append('api_automation_agent')
            if automation_area == 'database' or automation_area == 'all':
                response['agents_to_invoke'].append('db_automation_agent')
            if automation_area == 'cli' or automation_area == 'all':
                response['agents_to_invoke'].append('cli_automation_agent')
            if automation_area == 'gui' or automation_area == 'all':
                response['agents_to_invoke'].append('gui_automation_agent')
        
        response['actions_to_take'].append(f"Re-running agents: {', '.join(response['agents_to_invoke'])}")
        
        logger.info(f"Feedback processing complete. Will re-run: {response['agents_to_invoke']}")
        return response
