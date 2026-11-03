"""
MCP Server for Left Ventricular Myocardial Work Index (GWI) Skill.
Conforms to Model Context Protocol (MCP) JSON-RPC 2.0 stdio specification.
"""

import sys
import json
from client import MyocardialWorkIndexClient


def handle_request(line: str) -> None:
    try:
        req = json.loads(line)
    except Exception:
        return

    req_id = req.get("id")
    method = req.get("method")
    params = req.get("params", {})

    if method == "initialize":
        response = {
            "jsonrpc": "2.0",
            "id": req_id,
            "result": {
                "protocolVersion": "2024-11-05",
                "capabilities": {"tools": {}},
                "serverInfo": {
                    "name": "genpark-personal-agent-cardiac-ventricular-myocardial-work-index-gwi-skill",
                    "version": "1.0.0"
                }
            }
        }
        sys.stdout.write(json.dumps(response) + "\n")
        sys.stdout.flush()
    elif method == "tools/list":
        response = {
            "jsonrpc": "2.0",
            "id": req_id,
            "result": {
                "tools": [
                    {
                        "name": "evaluate_myocardial_work",
                        "description": "Calculate Left Ventricular Myocardial Work Index (GWI), Constructive Work (GCW), Wasted Work (GWW), and Work Efficiency (GWE%).",
                        "inputSchema": {
                            "type": "object",
                            "properties": {
                                "systolic_bp_mmhg": {"type": "number", "description": "Systolic blood pressure (mmHg)."},
                                "diastolic_bp_mmhg": {"type": "number", "description": "Diastolic blood pressure (mmHg)."},
                                "global_longitudinal_strain_pct": {"type": "number", "description": "Global longitudinal strain (negative %, e.g., -20.5)."},
                                "dyssynchrony_delay_ms": {"type": "number", "description": "Mechanical dyssynchrony delay in ms (default: 0.0)."}
                            },
                            "required": ["systolic_bp_mmhg", "diastolic_bp_mmhg", "global_longitudinal_strain_pct"]
                        }
                    }
                ]
            }
        }
        sys.stdout.write(json.dumps(response) + "\n")
        sys.stdout.flush()
    elif method == "tools/call":
        tool_name = params.get("name")
        args = params.get("arguments", {})
        if tool_name == "evaluate_myocardial_work":
            client = MyocardialWorkIndexClient()
            try:
                res = client.evaluate_myocardial_work(
                    systolic_bp_mmhg=float(args["systolic_bp_mmhg"]),
                    diastolic_bp_mmhg=float(args["diastolic_bp_mmhg"]),
                    global_longitudinal_strain_pct=float(args["global_longitudinal_strain_pct"]),
                    dyssynchrony_delay_ms=float(args.get("dyssynchrony_delay_ms", 0.0))
                )
                response = {
                    "jsonrpc": "2.0",
                    "id": req_id,
                    "result": {
                        "content": [{"type": "text", "text": json.dumps(res, indent=2)}]
                    }
                }
            except Exception as e:
                response = {
                    "jsonrpc": "2.0",
                    "id": req_id,
                    "error": {"code": -32000, "message": str(e)}
                }
            sys.stdout.write(json.dumps(response) + "\n")
            sys.stdout.flush()
    else:
        response = {
            "jsonrpc": "2.0",
            "id": req_id,
            "error": {"code": -32601, "message": f"Method {method} not found"}
        }
        sys.stdout.write(json.dumps(response) + "\n")
        sys.stdout.flush()


def main():
    for line in sys.stdin:
        if line.strip():
            handle_request(line)


if __name__ == "__main__":
    main()
