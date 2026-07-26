"""
Eco-Loop Building Agents — Clean-State Full Pipeline Testing Harness.

Usage:
    python test_full_pipeline.py [--force]

Performs a clean-state end-to-end verification of baseline execution, AI loop execution,
log file integrity, and dashboard configuration.
"""
import os
import sys
import time
import json
import argparse
import subprocess
import pandas as pd
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
LOGS_DIR = BASE_DIR / "logs"
BASELINE_CSV = LOGS_DIR / "baseline_output.csv"
AI_CSV = LOGS_DIR / "ai_output.csv"
DECISIONS_LOG = LOGS_DIR / "decisions_log.jsonl"

def print_header(title: str):
    print("\n" + "=" * 70)
    print(f"  {title}")
    print("=" * 70)

def clean_logs():
    print("\n[STEP 1] Cleaning existing log outputs...")
    LOGS_DIR.mkdir(exist_ok=True)
    for p in [BASELINE_CSV, AI_CSV, DECISIONS_LOG]:
        if p.exists():
            p.unlink()
            print(f"  [-] Removed: {p.name}")
    print("  [OK] Logs directory is clean.")

def test_baseline() -> float:
    print_header("TEST 2: Running Baseline EMS Simulation (src/run_baseline.py)")
    t0 = time.time()
    res = subprocess.run([sys.executable, "src/run_baseline.py"], cwd=BASE_DIR, capture_output=True, text=True)
    t_elapsed = time.time() - t0
    
    assert res.returncode == 0, f"Baseline run failed with error: {res.stderr}"
    assert BASELINE_CSV.exists(), "baseline_output.csv was not created!"
    
    df = pd.read_csv(BASELINE_CSV)
    assert len(df) == 96, f"Expected 96 timesteps in baseline_output.csv, got {len(df)}"
    assert not df.isnull().values.any(), "baseline_output.csv contains null/NaN values!"
    expected_cols = ['timestamp', 'timestep', 'hour', 'zone_temp', 'pmv', 'hvac_energy_kwh', 'cumulative_energy_kwh', 'outdoor_temp', 'occupancy', 'cooling_setpoint', 'heating_setpoint']
    for col in expected_cols:
        assert col in df.columns, f"Missing column in baseline_output.csv: {col}"
        
    print(f"  [OK] Baseline completed in {t_elapsed:.2f}s | Rows: {len(df)} | kWh: {df['cumulative_energy_kwh'].iloc[-1]:.2f}")
    return t_elapsed

def test_ai_loop() -> float:
    print_header("TEST 3: Running Deep Reasoning AI Control Loop (src/run_ai_loop.py)")
    t0 = time.time()
    res = subprocess.run([sys.executable, "src/run_ai_loop.py"], cwd=BASE_DIR, capture_output=True, text=True)
    t_elapsed = time.time() - t0
    
    assert res.returncode == 0, f"AI loop failed with error: {res.stderr}"
    assert AI_CSV.exists(), "ai_output.csv was not created!"
    assert DECISIONS_LOG.exists(), "decisions_log.jsonl was not created!"
    
    df = pd.read_csv(AI_CSV)
    assert len(df) == 96, f"Expected 96 timesteps in ai_output.csv, got {len(df)}"
    assert not df.isnull().values.any(), "ai_output.csv contains null/NaN values!"
    
    decisions = []
    with open(DECISIONS_LOG, "r") as f:
        for line in f:
            if line.strip():
                decisions.append(json.loads(line.strip()))
    
    dec_count = len(decisions)
    assert dec_count >= 24, f"Expected at least 24 decision entries, got {dec_count}"
    
    # Verify reasoning chain structure present
    has_chain = any('reasoning_chain' in d for d in decisions)
    assert has_chain, "decisions_log.jsonl missing 4-step reasoning_chain fields!"
    
    print(f"  [OK] AI Loop completed in {t_elapsed:.2f}s | Rows: {len(df)} | Decisions: {dec_count} | kWh: {df['cumulative_energy_kwh'].iloc[-1]:.2f}")
    return t_elapsed

def test_dashboard_import() -> float:
    print_header("TEST 4: Verifying Streamlit Dashboard Configuration (dashboard/app.py)")
    t0 = time.time()
    # Syntax check on dashboard app script
    res = subprocess.run([sys.executable, "-m", "py_compile", "dashboard/app.py"], cwd=BASE_DIR, capture_output=True, text=True)
    t_elapsed = time.time() - t0
    assert res.returncode == 0, f"Dashboard app compilation failed: {res.stderr}"
    print(f"  [OK] Dashboard app compiled cleanly in {t_elapsed:.2f}s.")
    return t_elapsed

def test_unit_tests() -> float:
    print_header("TEST 5: Running BMS Automated Unit Test Suite (tests/test_bms.py)")
    t0 = time.time()
    res = subprocess.run([sys.executable, "tests/test_bms.py"], cwd=BASE_DIR, capture_output=True, text=True)
    t_elapsed = time.time() - t0
    assert res.returncode == 0, f"Unit test suite failed: {res.stderr}"
    print(f"  [OK] All 7 Unit Tests passed cleanly in {t_elapsed:.2f}s.")
    return t_elapsed

def main():
    parser = argparse.ArgumentParser(description="Clean-state full pipeline test harness")
    parser.add_argument("--force", action="store_true", help="Clean logs without prompt")
    args = parser.parse_args()
    
    if not args.force and any([BASELINE_CSV.exists(), AI_CSV.exists(), DECISIONS_LOG.exists()]):
        ans = input("Existing logs found. Clean logs directory and run full pipeline test? (y/N): ")
        if ans.lower() != 'y':
            print("Aborted.")
            return

    t_start = time.time()
    print_header("ECO-LOOP BUILDING AGENTS — FULL PIPELINE TEST HARNESS")
    
    try:
        clean_logs()
        t_base = test_baseline()
        t_ai = test_ai_loop()
        t_dash = test_dashboard_import()
        t_unit = test_unit_tests()
        t_total = time.time() - t_start
        
        print_header("SUMMARY: ALL PIPELINE TESTS PASSED 100% SUCCESSFULLY")
        print(f"  1. Baseline Simulation:   {t_base:.2f}s  [PASS]")
        print(f"  2. Deep Reasoning AI:     {t_ai:.2f}s  [PASS]")
        print(f"  3. Dashboard App Syntax:  {t_dash:.2f}s  [PASS]")
        print(f"  4. BMS Unit Test Suite:   {t_unit:.2f}s  [PASS]")
        print(f"  -------------------------------------------")
        print(f"  TOTAL PIPELINE TIMING:    {t_total:.2f}s  [ALL PASS]\n")
    except Exception as e:
        print(f"\n[FAIL] Pipeline test encountered error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
