"""
Model Context Protocol (MCP) Server Wrapper (Stretch Goal).
Exposes Eco-Loop Building Agents tools via standard MCP JSON-RPC protocol over STDIO.
"""
import sys
import json
import logging
from typing import Dict, Any

from ems_interface import callback_read, apply_action
from carbon_signal import get_carbon_intensity

logger = logging.getLogger("MCP_Server")

MCP_TOOLS = [
    {
        "name": "get_zone_state",
        "description": "Returns current building zone telemetry (temperature, PMV index, HVAC energy so far, outdoor temperature, occupancy).",
        "inputSchema": {
            "type": "object",
            "properties": {}
        }
    },
    {
        "name": "get_carbon_intensity",
        "description": "Returns current grid carbon intensity in gCO2/kWh for a given hour.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "hour": {"type": "integer", "description": "Hour of day (0-23)"}
            },
            "required": ["hour"]
        }
    },
    {
        "name": "set_thermostat_setpoint",
        "description": "Sets heating and cooling setpoints for a building zone.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "zone": {"type": "string"},
                "cooling_setpoint": {"type": "number"},
                "heating_setpoint": {"type": "number"}
            },
            "required": ["zone", "cooling_setpoint", "heating_setpoint"]
        }
    },
    {
        "name": "set_lighting_level",
        "description": "Sets the lighting level multiplier (0.5 to 1.0) for a zone.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "zone": {"type": "string"},
                "level": {"type": "number"}
            },
            "required": ["zone", "level"]
        }
    }
]

def handle_mcp_request(request: Dict[str, Any]) -> Dict[str, Any]:
    """
    Handles incoming MCP JSON-RPC 2.0 requests.
    """
    req_id = request.get("id")
    method = request.get("method")
    params = request.get("params", {})

    if method == "tools/list":
        return {
            "jsonrpc": "2.0",
            "id": req_id,
            "result": {"tools": MCP_TOOLS}
        }
    elif method == "tools/call":
        tool_name = params.get("name")
        arguments = params.get("arguments", {})

        if tool_name == "get_zone_state":
            result_data = callback_read({"zone_temp": 22.0, "outdoor_temp": 20.0, "energy_so_far": 5.0, "occupancy": 10})
        elif tool_name == "get_carbon_intensity":
            hour = arguments.get("hour", 12)
            result_data = {"hour": hour, "carbon_intensity_gco2_kwh": get_carbon_intensity(hour)}
        elif tool_name == "set_thermostat_setpoint":
            result_data = apply_action({"zone_temp": 22.0}, arguments)
        elif tool_name == "set_lighting_level":
            result_data = apply_action({"zone_temp": 22.0}, arguments)
        else:
            return {
                "jsonrpc": "2.0",
                "id": req_id,
                "error": {"code": -32601, "message": f"Tool '{tool_name}' not found."}
            }

        return {
            "jsonrpc": "2.0",
            "id": req_id,
            "result": {
                "content": [
                    {"type": "text", "text": json.dumps(result_data, indent=2)}
                ]
            }
        }
    else:
        return {
            "jsonrpc": "2.0",
            "id": req_id,
            "error": {"code": -32601, "message": f"Method '{method}' not implemented."}
        }

def run_stdio_mcp_server():
    """
    Runs STDIO loop reading MCP JSON-RPC requests.
    """
    for line in sys.stdin:
        if not line.strip():
            continue
        try:
            req = json.loads(line.strip())
            res = handle_mcp_request(req)
            sys.stdout.write(json.dumps(res) + "\n")
            sys.stdout.flush()
        except Exception as e:
            sys.stderr.write(f"MCP error: {e}\n")

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--test":
        print("[+] Testing MCP Server tools list:")
        print(json.dumps(handle_mcp_request({"jsonrpc": "2.0", "id": 1, "method": "tools/list"}), indent=2))
    else:
        run_stdio_mcp_server()
