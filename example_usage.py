"""
Example usage of Left Ventricular Myocardial Work Index (GWI) Skill.
Demonstrates normal synchronous high-efficiency work vs dyssynchronous wasted work.
"""

import json
from client import MyocardialWorkIndexClient


def main():
    print("=== Testing Left Ventricular Myocardial Work Index (GWI) Skill ===")
    client = MyocardialWorkIndexClient()

    # 1. Healthy adult heart (BP=120/80, GLS=-21.0%, no dyssynchrony delay)
    res_healthy = client.evaluate_myocardial_work(
        systolic_bp_mmhg=120.0,
        diastolic_bp_mmhg=80.0,
        global_longitudinal_strain_pct=-21.0,
        dyssynchrony_delay_ms=0.0
    )
    print("\n[Case 1: Healthy Synchronous Myocardial Work]")
    print(json.dumps(res_healthy, indent=2))

    # 2. Dyssynchronous left bundle branch block (BP=135/85, GLS=-15.0%, delay=120 ms -> elevated GWW, GWE drops)
    res_dyssynchronous = client.evaluate_myocardial_work(
        systolic_bp_mmhg=135.0,
        diastolic_bp_mmhg=85.0,
        global_longitudinal_strain_pct=-15.0,
        dyssynchrony_delay_ms=120.0
    )
    print("\n[Case 2: Dyssynchronous Left Ventricle with Wasted Work]")
    print(json.dumps(res_dyssynchronous, indent=2))

    # Assertions
    assert res_healthy["global_work_efficiency_pct"] >= 94.0
    assert res_dyssynchronous["global_wasted_work_gww"] > res_healthy["global_wasted_work_gww"]
    assert res_dyssynchronous["global_work_efficiency_pct"] < res_healthy["global_work_efficiency_pct"]
    print("\n[SUCCESS] Myocardial Work Index tests passed!")


if __name__ == "__main__":
    main()
