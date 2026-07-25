"""
One-Command Full Live Demo Execution Script for Eco-Loop Building Agents.
Executes test suite -> runs baseline simulation -> runs closed-loop AI simulation -> launches Streamlit dashboard.
"""
import os
import sys
import subprocess
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent

def run_command_step(cmd_list, description):
    print("\n" + "=" * 70)
    print(f"[RUNNING STEP] {description}")
    print("=" * 70)
    result = subprocess.run(cmd_list, cwd=BASE_DIR)
    if result.returncode != 0:
        print(f"[ERROR] Failed in {description}. Exiting.")
        sys.exit(result.returncode)
    print(f"[OK] {description} completed successfully!")

def main():
    print("=" * 70)
    print("ECO-LOOP BUILDING AGENTS -- FULL HACKATHON LIVE DEMO LAUNCHER")
    print("=" * 70)
    
    # 1. Automated Test Suite
    run_command_step([sys.executable, "tests/test_bms.py"], "Automated Pytest Unit Suite")
    
    # 2. Multi-Zone Baseline Run
    run_command_step([sys.executable, "src/run_baseline.py"], "Multi-Zone Baseline Building Physics Run")
    
    # 3. Autonomous AI Closed-Loop Run
    run_command_step([sys.executable, "src/run_ai_loop.py"], "Autonomous Closed-Loop AI Simulation Run")
    
    # 4. Launch Dashboard
    print("\n" + "=" * 70)
    print("LAUNCHING MATERIAL DESIGN 3 STREAMLIT BEMS DASHBOARD...")
    print("=" * 70)
    subprocess.run(["streamlit", "run", "dashboard/app.py"], cwd=BASE_DIR)

if __name__ == "__main__":
    main()
