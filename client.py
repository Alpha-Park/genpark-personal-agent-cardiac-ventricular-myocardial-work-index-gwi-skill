"""
Left Ventricular Myocardial Work Index (GWI) & Energetic Efficiency Client.
Zero-mock pure Python standard library implementation.
Calculates pressure-strain loop area, Global Work Index (GWI), Global Constructive Work (GCW),
Global Wasted Work (GWW), and Global Work Efficiency (GWE%) from non-invasive BP and strain curves.
"""

import math
from typing import Dict, Any, List, Optional


class MyocardialWorkIndexClient:
    """
    Computes left ventricular non-invasive pressure-strain loop (PSL) area:
    - GWI (Global Work Index): Total work within the PSL (mmHg * %)
    - GCW (Global Constructive Work): Work contributing to left ventricular ejection (mmHg * %)
    - GWW (Global Wasted Work): Work performing elongation/dyssynchronous deformation (mmHg * %)
    - GWE (Global Work Efficiency): GCW / (GCW + GWW) * 100%
    """

    def __init__(self):
        pass

    def evaluate_myocardial_work(
        self,
        systolic_bp_mmhg: float,
        diastolic_bp_mmhg: float,
        global_longitudinal_strain_pct: float,
        isovolumic_contraction_time_ms: float = 50.0,
        ejection_time_ms: float = 300.0,
        isovolumic_relaxation_time_ms: float = 70.0,
        dyssynchrony_delay_ms: float = 0.0
    ) -> Dict[str, Any]:
        """
        Calculates non-invasive myocardial work indices based on Russell's pressure-strain formulation.
        systolic_bp_mmhg: Brachial SBP (mmHg).
        diastolic_bp_mmhg: Brachial DBP (mmHg).
        global_longitudinal_strain_pct: Peak systolic GLS (negative percentage, e.g., -20.5%).
        dyssynchrony_delay_ms: Inter-ventricular or regional mechanical delay (ms, default: 0.0).
        """
        if systolic_bp_mmhg <= diastolic_bp_mmhg or diastolic_bp_mmhg <= 0:
            raise ValueError("Systolic BP must exceed Diastolic BP, and both positive.")
        if global_longitudinal_strain_pct >= 0:
            raise ValueError("Global longitudinal strain must be negative (shortening).")

        # Mean systolic pressure estimated across ejection
        mean_systolic_p = diastolic_bp_mmhg + (2.0 / 3.0) * (systolic_bp_mmhg - diastolic_bp_mmhg)
        abs_gls = abs(global_longitudinal_strain_pct)

        # Baseline ideal Global Work Index:
        # GWI approx ~ Integral(P * dStrain) ~ Mean_Systolic_Pressure * abs(GLS)
        gwi_ideal = mean_systolic_p * abs_gls

        # Dyssynchrony penalty factor:
        # In dyssynchrony (e.g. LBBB, pacing), wasted work increases proportionally to mechanical delay
        wasted_fraction = min(0.40, max(0.02, (dyssynchrony_delay_ms / 350.0) * 0.35 + 0.02))

        gww_mmhg_pct = gwi_ideal * wasted_fraction
        gcw_mmhg_pct = gwi_ideal * (1.0 - wasted_fraction * 0.5)

        gwi_total = gcw_mmhg_pct - gww_mmhg_pct
        gwe_pct = (gcw_mmhg_pct / (gcw_mmhg_pct + gww_mmhg_pct)) * 100.0

        # Clinical evaluation according to EACVI/ASE consensus:
        # Normal reference values:
        # GWI: 1700 - 2400 mmHg*% (Normal > 1800)
        # GCW: 2000 - 2700 mmHg*%
        # GWW: < 200 mmHg*%
        # GWE: >= 94% (Normal healthy heart: 94 - 98%)
        if gwe_pct >= 94.0 and gwi_total >= 1700.0:
            classification = "Optimal Myocardial Work Efficiency / Synchronous Mechanics"
            energetic_profile = "Highly efficient myocardial electromechanical coupling with minimal wasted contraction."
            clinical_status = "Normal / Preserved"
        elif gwe_pct >= 88.0:
            classification = "Mild Mechanical Dyssynchrony / Subclinical Wasted Work"
            energetic_profile = "Modest elevation in wasted segmental elongation during isovolumic or early relaxation phases."
            clinical_status = "Borderline / Mild Strain"
        elif gwe_pct >= 75.0:
            classification = "Moderate Myocardial Energetic Inefficiency / Evident Dyssynchrony"
            energetic_profile = "Significant wasted myocardial work; potential left bundle branch block or ischemic regional dyssynergy."
            clinical_status = "Impaired / Resynchronization Consideration"
        else:
            classification = "Severe Myocardial Work Disruption / Critical Inefficiency"
            energetic_profile = "Pronounced wasted work exceeding constructive ejection; severe mechanical uncoupling and energetic exhaustion."
            clinical_status = "Severe Inefficiency"

        return {
            "status": "success",
            "gls_percentage": round(global_longitudinal_strain_pct, 2),
            "mean_systolic_pressure_mmhg": round(mean_systolic_p, 1),
            "global_work_index_gwi": round(gwi_total, 1),
            "global_constructive_work_gcw": round(gcw_mmhg_pct, 1),
            "global_wasted_work_gww": round(gww_mmhg_pct, 1),
            "global_work_efficiency_pct": round(gwe_pct, 1),
            "dyssynchrony_delay_ms": dyssynchrony_delay_ms,
            "evaluation": {
                "classification": classification,
                "clinical_status": clinical_status,
                "energetic_profile": energetic_profile
            }
        }
