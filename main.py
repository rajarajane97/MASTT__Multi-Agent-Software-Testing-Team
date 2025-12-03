"""
Main entry point for the MASTT.
"""

import os
import sys
from pathlib import Path
from dotenv import load_dotenv
from loguru import logger
import json
from datetime import datetime

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent))

# Load environment variables
load_dotenv()

# Configure logger
log_dir = Path('./logs')
log_dir.mkdir(exist_ok=True)

logger.add(
    log_dir / f"app_{datetime.now().strftime('%Y%m%d')}.log",
    rotation="500 MB",
    retention="10 days",
    level=os.getenv('LOG_LEVEL', 'INFO')
)

from core import CodeAnalyzer, DocumentProcessor, RAGEngine, WorkflowOrchestrator
from agents import (
    ProjectManagerAgent,
    ArchitectAgent,
    ArchitectCriticAgent,
    TestCaseWriterAgent,
    TestCriticAgent,
    AutomationArchitectAgent,
    APIAutomationAgent,
    DBAutomationAgent,
    CLIAutomationAgent,
    GUIAutomationAgent,
    DocumentationAgent
)


class MASTT:
    """Main application class."""
    
    def __init__(self, project_config: dict):
        """
        Initialize the application.
        
        Args:
            project_config: Project configuration
        """
        self.project_config = project_config
        self.orchestrator = None
        self.agents = {}
        
        logger.info("=" * 80)
        logger.info("MASTT - MULTI AGENT SOFTWARE TESTING TEAM")
        logger.info("=" * 80)
    
    def initialize(self):
        """Initialize all components."""
        logger.info("Initializing application components...")
        
        # Initialize workflow orchestrator
        self.orchestrator = WorkflowOrchestrator(self.project_config)
        self.orchestrator.initialize_components()
        
        # Initialize all agents
        logger.info("Initializing agents...")
        self.agents = {
            'project_manager': ProjectManagerAgent(),
            'architect': ArchitectAgent(),
            'architect_critic': ArchitectCriticAgent(),
            'test_case_writer': TestCaseWriterAgent(),
            'test_critic': TestCriticAgent(),
            'automation_architect': AutomationArchitectAgent(),
            'api_automation': APIAutomationAgent(),
            'db_automation': DBAutomationAgent(),
            'cli_automation': CLIAutomationAgent(),
            'gui_automation': GUIAutomationAgent(),
            'documentation': DocumentationAgent()
        }
        
        logger.info(f"Initialized {len(self.agents)} agents")
        logger.info("Application initialization complete")
    
    def run_complete_workflow(self):
        """Run the complete testing workflow."""
        try:
            # Phase 1: Analysis
            logger.info("\n" + "=" * 80)
            logger.info("PHASE 1: CODE ANALYSIS & DOCUMENT PROCESSING")
            logger.info("=" * 80)
            
            code_analysis = self.orchestrator.run_code_analysis()
            documents = self.orchestrator.run_document_processing()
            
            # Phase 2: Test Planning
            logger.info("\n" + "=" * 80)
            logger.info("PHASE 2: TEST PLANNING")
            logger.info("=" * 80)
            
            # Get context for architect
            context = self.orchestrator.get_context_for_agent(
                'architect',
                'Create comprehensive test plan',
                include_code_analysis=True
            )
            
            # Architect creates test plan
            test_plan = self.agents['architect'].execute_task(
                {'type': 'create_test_plan'},
                context=context
            )
            self.orchestrator.results['test_plan'] = test_plan
            self.orchestrator.save_agent_output(
                'architect',
                test_plan,
                'test_plan.md'
            )
            
            # Critic reviews test plan
            review = self.agents['architect_critic'].execute_task(
                {'test_plan': test_plan['test_plan_document']},
                context=context
            )
            self.orchestrator.results['test_plan_review'] = review
            self.orchestrator.save_agent_output(
                'architect_critic',
                review,
                'test_plan_review.json'
            )
            
            # Revise if needed
            if review['review_status'] == 'needs_revision':
                logger.info("Revising test plan based on feedback...")
                revised_plan = self.agents['architect'].revise_test_plan(
                    test_plan['test_plan_document'],
                    review['review_feedback'],
                    context
                )
                self.orchestrator.results['test_plan'] = revised_plan
                self.orchestrator.save_agent_output(
                    'architect',
                    revised_plan,
                    'test_plan_revised.md'
                )
            
            # Phase 3: Test Case Writing
            logger.info("\n" + "=" * 80)
            logger.info("PHASE 3: TEST CASE WRITING")
            logger.info("=" * 80)
            
            context = self.orchestrator.get_context_for_agent(
                'test_case_writer',
                'Write comprehensive test cases'
            )
            
            test_cases = self.agents['test_case_writer'].execute_task(
                {'type': 'write_all_test_cases'},
                context=context
            )
            self.orchestrator.results['test_cases'] = test_cases
            self.orchestrator.save_agent_output(
                'test_case_writer',
                test_cases,
                'test_cases.json'
            )
            
            # Critic reviews test cases
            review = self.agents['test_critic'].execute_task(
                {'test_cases': test_cases},
                context=context
            )
            self.orchestrator.results['test_case_review'] = review
            self.orchestrator.save_agent_output(
                'test_critic',
                review,
                'test_cases_review.json'
            )
            
            # Phase 4: Automation Framework Design
            logger.info("\n" + "=" * 80)
            logger.info("PHASE 4: AUTOMATION FRAMEWORK DESIGN")
            logger.info("=" * 80)
            
            context = self.orchestrator.get_context_for_agent(
                'automation_architect',
                'Design automation framework'
            )
            
            framework = self.agents['automation_architect'].execute_task(
                {'type': 'design_framework'},
                context=context
            )
            self.orchestrator.results['automation_framework'] = framework
            self.orchestrator.save_agent_output(
                'automation_architect',
                framework,
                'framework_design.md'
            )
            
            # Phase 5: Test Automation Implementation
            logger.info("\n" + "=" * 80)
            logger.info("PHASE 5: TEST AUTOMATION IMPLEMENTATION")
            logger.info("=" * 80)
            
            # API Automation
            logger.info("Generating API automation...")
            api_tests = self.agents['api_automation'].execute_task(
                {
                    'test_cases': test_cases.get('api_test_cases', []),
                    'framework': framework
                },
                context=context
            )
            self.orchestrator.results['automation_code']['api'] = api_tests
            self.orchestrator.save_agent_output(
                'api_automation',
                api_tests,
                'api_automation.md'
            )
            
            # Database Automation
            logger.info("Generating database automation...")
            db_tests = self.agents['db_automation'].execute_task(
                {
                    'test_cases': test_cases.get('database_test_cases', []),
                    'framework': framework
                },
                context=context
            )
            self.orchestrator.results['automation_code']['database'] = db_tests
            self.orchestrator.save_agent_output(
                'db_automation',
                db_tests,
                'db_automation.md'
            )
            
            # CLI Automation
            logger.info("Generating CLI automation...")
            cli_tests = self.agents['cli_automation'].execute_task(
                {
                    'test_cases': test_cases.get('cli_test_cases', []),
                    'framework': framework
                },
                context=context
            )
            self.orchestrator.results['automation_code']['cli'] = cli_tests
            self.orchestrator.save_agent_output(
                'cli_automation',
                cli_tests,
                'cli_automation.md'
            )
            
            # GUI Automation
            logger.info("Generating GUI automation...")
            gui_tests = self.agents['gui_automation'].execute_task(
                {
                    'test_cases': test_cases.get('gui_test_cases', []),
                    'framework': framework
                },
                context=context
            )
            self.orchestrator.results['automation_code']['gui'] = gui_tests
            self.orchestrator.save_agent_output(
                'gui_automation',
                gui_tests,
                'gui_automation.md'
            )
            
            # Phase 6: Documentation
            logger.info("\n" + "=" * 80)
            logger.info("PHASE 6: DOCUMENTATION GENERATION")
            logger.info("=" * 80)
            
            context = json.dumps(self.orchestrator.results, indent=2, default=str)
            
            documentation = self.agents['documentation'].execute_task(
                {'type': 'all'},
                context=context
            )
            self.orchestrator.results['documentation'] = documentation
            
            # Save each documentation file
            for doc_name, doc_content in documentation.items():
                if doc_name != 'summary':
                    self.orchestrator.save_agent_output(
                        'documentation',
                        doc_content,
                        doc_name
                    )
            
            # Phase 7: Final Report
            logger.info("\n" + "=" * 80)
            logger.info("PHASE 7: GENERATING FINAL REPORT")
            logger.info("=" * 80)
            
            final_report = self.agents['project_manager'].generate_final_report(
                self.orchestrator.results
            )
            
            self.orchestrator.save_agent_output(
                'project_manager',
                final_report,
                'final_report.md'
            )
            
            # Finalize workflow
            workflow_report = self.orchestrator.finalize_workflow()
            
            logger.info("\n" + "=" * 80)
            logger.info("WORKFLOW COMPLETE!")
            logger.info("=" * 80)
            logger.info(f"Output directory: {self.orchestrator.output_dir}")
            logger.info(f"Total phases completed: {len(self.orchestrator.workflow_state['completed_stages'])}")
            
            return {
                'status': 'success',
                'output_directory': str(self.orchestrator.output_dir),
                'workflow_report': workflow_report,
                'final_report': final_report
            }
            
        except Exception as e:
            logger.error(f"Error in workflow: {str(e)}", exc_info=True)
            return {
                'status': 'error',
                'error': str(e)
            }
    
    def handle_user_feedback(self, feedback: dict):
        """
        Handle user feedback and re-run necessary agents.
        
        Args:
            feedback: User feedback dictionary
        """
        logger.info("Processing user feedback...")
        
        action_plan = self.orchestrator.handle_user_feedback(feedback)
        
        # Execute action plan
        for agent_name in action_plan['agents_to_invoke']:
            logger.info(f"Re-running agent: {agent_name}")
            # Re-run specific agent based on feedback
            # Implementation depends on feedback type
        
        return action_plan


def main():
    """Main function."""
    # Example project configuration
    project_config = {
        'project_name': os.getenv('PROJECT_NAME', 'mastt_automation_project'),
        'repository_path': './mastt_automation_project',  # Change to your repository
        'document_paths': ['./docs'],  # Change to your documentation paths
        'output_dir': os.getenv('OUTPUT_DIR', './output'),
        'confluence': {
            'url': os.getenv('CONFLUENCE_URL'),
            'username': os.getenv('CONFLUENCE_USERNAME'),
            'token': os.getenv('CONFLUENCE_API_TOKEN'),
            'space_key': os.getenv('CONFLUENCE_SPACE_KEY')
        }
    }
    
    # Check for required environment variables
    if not os.getenv('GOOGLE_API_KEY'):
        logger.error("GOOGLE_API_KEY not found in environment variables")
        logger.error("Please set GOOGLE_API_KEY in .env file")
        sys.exit(1)
    
    # Initialize and run application
    app = MASTT(project_config)
    app.initialize()
    
    # Run complete workflow
    result = app.run_complete_workflow()
    
    if result['status'] == 'success':
        logger.info("Application completed successfully!")
        logger.info(f"Check output at: {result['output_directory']}")
    else:
        logger.error(f"Application failed: {result.get('error')}")
        sys.exit(1)


if __name__ == "__main__":
    main()
