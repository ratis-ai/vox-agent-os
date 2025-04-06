import argparse
from pkg.agents.licensed.crew_ai.soc2_auditor.soc2_auditor_crew import SOC2AuditorCrew

def main():
    parser = argparse.ArgumentParser(description='Run SOC 2 audit')
    parser.add_argument('--checklist', required=True, help='Path to checklist JSON file')
    parser.add_argument('--data_dir', required=True, help='Path to evidence directory')
    
    args = parser.parse_args()
    
    crew = SOC2AuditorCrew()
    report_path = crew.run_audit(args.checklist, args.data_dir)
    
    print(f"📝 Report saved to {report_path}")

if __name__ == "__main__":
    main() 