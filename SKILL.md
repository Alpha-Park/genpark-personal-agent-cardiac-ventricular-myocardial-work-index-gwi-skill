---
name: genpark-personal-agent-cardiac-ventricular-myocardial-work-index-gwi-skill
description: Non-invasive Left Ventricular Myocardial Work Index (GWI in mmHg%) and Work Efficiency (GWE%) analyzer. Integrates non-invasive brachial blood pressure curves with 2D echocardiographic global longitudinal strain (GLS) loops.
version: 1.0.0
author: GenPark Ecosystem
license: Apache-2.0
tags:
  - personal-agent
  - cardiology
  - echocardiography
  - myocardial-work
  - gwi
  - strain
  - openclaw
  - genpark
  - mcp
---

# Cardiac Ventricular Myocardial Work Index (GWI) Skill

## Overview
This skill computes left ventricular pressure-strain loop (PSL) area and work distribution metrics:
- **Global Work Index (GWI)**: Total mechanical work performed by the left ventricle from mitral valve closure to mitral valve opening ($\text{mmHg} \cdot \%$).
- **Global Constructive Work (GCW)**: Segmental shortening during systole plus lengthening during isovolumic relaxation contributing to effective cardiac output.
- **Global Wasted Work (GWW)**: Segmental lengthening during systole plus shortening during isovolumic relaxation, which expends metabolic ATP without contributing to forward ejection.
- **Global Work Efficiency (GWE)**: Percentage of constructive work relative to total work ($\text{GCW} / (\text{GCW} + \text{GWW}) \times 100\%$).

## Mathematical Formulation
1. **Mean Systolic Pressure**:
   $$P_{\text{sys}} = \text{DBP} + \frac{2}{3}(\text{SBP} - \text{DBP})$$
2. **Global Work Index (GWI)**:
   $$\text{GWI} = \oint P(t) \, d\epsilon(t)$$
3. **Global Work Efficiency (GWE)**:
   $$\text{GWE} = \frac{\text{GCW}}{\text{GCW} + \text{GWW}} \times 100\%$$

## Usage
```python
from client import MyocardialWorkIndexClient

client = MyocardialWorkIndexClient()
res = client.evaluate_myocardial_work(
    systolic_bp_mmhg=120.0,
    diastolic_bp_mmhg=80.0,
    global_longitudinal_strain_pct=-20.5
)
print(res["global_work_efficiency_pct"])
```
