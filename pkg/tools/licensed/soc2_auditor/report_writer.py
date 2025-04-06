"""
Tool for generating SOC 2 audit reports.
"""
import json
import logging
from datetime import datetime
from typing import Dict, List
import markdown2

logger = logging.getLogger("vox")

class ReportWriter:
    def __init__(self):
        self.template = """
# SOC 2 Audit Report
Generated: {timestamp}

## Summary
Total Controls Reviewed: {total_controls}
Compliant: {compliant_count}
Non-Compliant: {non_compliant_count}

## Detailed Findings
{detailed_findings}

## Recommendations
{recommendations}
"""

    def write_report(self, results: List[Dict], output_path: str, format: str = "md") -> None:
        """
        Generate and write audit report.
        
        Args:
            results: List of control evaluation results
            output_path: Path to write the report
            format: Output format ("md" or "json")
        """
        try:
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            
            compliant = sum(1 for r in results if r["status"] == "compliant")
            non_compliant = len(results) - compliant
            
            detailed_findings = "\n".join(
                f"### Control {r['control_id']}\n"
                f"Status: {'✅' if r['status'] == 'compliant' else '❌'}\n"
                f"Findings: {', '.join(r['findings']) if r['findings'] else 'None'}\n"
                for r in results
            )
            
            recommendations = "\n".join(
                f"- {r['control_id']}: {r['recommendation']}"
                for r in results
                if r.get('recommendation')
            )
            
            if format == "md":
                report = self.template.format(
                    timestamp=timestamp,
                    total_controls=len(results),
                    compliant_count=compliant,
                    non_compliant_count=non_compliant,
                    detailed_findings=detailed_findings,
                    recommendations=recommendations
                )
            else:  # json
                report = json.dumps({
                    "timestamp": timestamp,
                    "summary": {
                        "total_controls": len(results),
                        "compliant": compliant,
                        "non_compliant": non_compliant
                    },
                    "findings": results,
                    "recommendations": [r.get('recommendation') for r in results if r.get('recommendation')]
                }, indent=2)
            
            with open(output_path, 'w') as f:
                f.write(report)
                
        except Exception as e:
            logger.error(f"Error writing report: {str(e)}")
            raise 