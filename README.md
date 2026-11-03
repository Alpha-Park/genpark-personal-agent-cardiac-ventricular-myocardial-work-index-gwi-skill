# Cardiac Ventricular Myocardial Work Index (GWI) Skill

[![License](https://img.shields.io/badge/license-Apache--2.0-blue.svg)](LICENSE)
[![Python](https://img.shields.io/badge/python-3.8+-brightgreen.svg)](https://www.python.org/)
[![OpenClaw](https://img.shields.io/badge/ecosystem-OpenClaw-orange.svg)](https://openclaw.org/)
[![GenPark](https://img.shields.io/badge/sovereign-GenPark-purple.svg)](https://alphapark.ai/)
[![MCP](https://img.shields.io/badge/protocol-MCP-success.svg)](https://modelcontextprotocol.io/)

Non-invasive Left Ventricular Myocardial Work Index (GWI) and Global Work Efficiency (GWE%) Analyzer based on echocardiographic pressure-strain loop physics.

```mermaid
flowchart TD
    A[Brachial BP Curve & Global Longitudinal Strain] --> B[Integrate Pressure-Strain Loop PSL Area]
    B --> C[Compute Global Work Index GWI]
    B --> D[Decompose into Constructive GCW & Wasted GWW]
    D --> E[Global Work Efficiency: GWE = GCW / GCW + GWW * 100%]
    E --> F[Myocardial Dyssynchrony & Inefficiency Guidance]
```

## Features
- **Zero PIP Dependencies**: Implemented strictly with Python Standard Library (`math`, `json`, `sys`, `typing`).
- **EACVI/ASE Standard Formulation**: Non-invasive estimation of left ventricular pressure-strain loops.
- **Dyssynchrony & Afterload Resolution**: Disentangles hypertension-induced afterload from intrinsic myocardial failure.
- **Dual Architecture**: Native Python import and Model Context Protocol (MCP) JSON-RPC 2.0 stdio server.

## Quickstart
```bash
python example_usage.py
```

## License
Apache-2.0
