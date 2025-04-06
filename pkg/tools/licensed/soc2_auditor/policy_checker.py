"""
Tool for checking policies against SOC 2 control requirements.
"""
import logging
from typing import Dict, List
import yaml

logger = logging.getLogger("vox")

class PolicyChecker:
    def __init__(self, control_requirements_path: str):
        """
        Initialize with control requirements.
        
        Args:
            control_requirements_path: Path to YAML file containing control requirements
        """
        with open(control_requirements_path, 'r') as f:
            self.requirements = yaml.safe_load(f)
    
    def check_policy(self, control_id: str, policy_content: str) -> Dict:
        """
        Check if a policy meets control requirements.
        
        Args:
            control_id: SOC 2 control identifier
            policy_content: Content of the policy document
            
        Returns:
            Dictionary containing compliance status and findings
        """
        if control_id not in self.requirements:
            return {"status": "error", "message": f"Unknown control ID: {control_id}"}
            
        control_reqs = self.requirements[control_id]
        findings = []
        
        # Check for required sections
        for section in control_reqs.get("required_sections", []):
            if section.lower() not in policy_content.lower():
                findings.append(f"Missing required section: {section}")
        
        # Check for required keywords
        for keyword in control_reqs.get("required_keywords", []):
            if keyword.lower() not in policy_content.lower():
                findings.append(f"Missing required keyword: {keyword}")
        
        return {
            "status": "compliant" if not findings else "non_compliant",
            "findings": findings
        } 