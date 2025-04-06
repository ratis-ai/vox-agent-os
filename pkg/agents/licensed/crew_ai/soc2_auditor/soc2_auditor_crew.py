"""
Crew management for SOC 2 auditing coordination.
"""
import os
import json
import logging
from typing import Dict, List
from datetime import datetime
from dotenv import load_dotenv

from pkg.agents.licensed.crew_ai.soc2_auditor.specialized_agents import DocumentAnalyzer, TicketVerifier, ComplianceEvaluator
from pkg.tools.licensed.soc2_auditor.report_writer import ReportWriter

logger = logging.getLogger("vox")

class SOC2AuditorCrew:
    def __init__(self):
        load_dotenv()
        logger.debug("Initializing SOC2AuditorCrew")
        
        # Initialize specialized agents
        self.doc_analyzer = DocumentAnalyzer()
        self.ticket_verifier = TicketVerifier()
        self.compliance_evaluator = ComplianceEvaluator()
        self.report_writer = ReportWriter()
        
        logger.debug("SOC2AuditorCrew initialization complete")
    
    def load_checklist(self, checklist_path: str) -> List[Dict]:
        """Load and validate SOC 2 checklist configuration."""
        with open(checklist_path, 'r') as f:
            return json.load(f)
    
    def run_audit(self, checklist_path: str, data_dir: str) -> str:
        """
        Run a complete SOC 2 audit cycle.
        
        Args:
            checklist_path: Path to the checklist JSON file
            data_dir: Directory containing evidence files
            
        Returns:
            Path to the generated audit report
        """
        try:
            logger.info(f"Starting SOC 2 audit with checklist: {checklist_path}")
            
            # Load checklist
            controls = self.load_checklist(checklist_path)
            
            # Process each control
            results = []
            for control in controls:
                # Analyze required documents
                doc_status = self.doc_analyzer.analyze_documents(
                    {doc: f"{data_dir}/{doc}" for doc in control["required_docs"]}
                )
                
                # Verify required tickets
                ticket_status = self.ticket_verifier.verify_tickets(
                    control["required_tickets"]
                )
                
                # Evaluate compliance
                evaluation = self.compliance_evaluator.evaluate_control(
                    control["id"],
                    {"documents": doc_status, "tickets": ticket_status}
                )
                
                results.append(evaluation)
            
            # Generate report
            timestamp = datetime.now().strftime("%Y_%m_%d")
            report_path = f"./logs/audit_{timestamp}.md"
            self.report_writer.write_report(results, report_path)
            
            return report_path
            
        except Exception as e:
            error_msg = f"Error during SOC 2 audit: {str(e)}"
            logger.error(error_msg, exc_info=True)
            return error_msg
