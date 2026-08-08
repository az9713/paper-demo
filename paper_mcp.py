"""Minimal MCP-over-HTTP client for Paper Desktop (port 29979)."""
import json, sys, urllib.request

URL = "http://127.0.0.1:29979/mcp"
SESSION_FILE = __file__ + ".session"

def _post(payload, session_id=None):
    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json, text/event-stream",
    }
    if session_id:
        headers["Mcp-Session-Id"] = session_id
    req = urllib.request.Request(URL, data=json.dumps(payload).encode(), headers=headers)
    with urllib.request.urlopen(req, timeout=120) as r:
        sid = r.headers.get("Mcp-Session-Id")
        body = r.read().decode("utf-8", "replace")
        ctype = r.headers.get("Content-Type", "")
    if "text/event-stream" in ctype:
        msgs = [json.loads(line[5:].strip()) for line in body.splitlines()
                if line.startswith("data:") and line[5:].strip()]
        result = msgs[-1] if msgs else None
    else:
        result = json.loads(body) if body.strip() else None
    return result, sid

def get_session():
    try:
        return open(SESSION_FILE).read().strip()
    except OSError:
        pass
    init = {"jsonrpc": "2.0", "id": 1, "method": "initialize", "params": {
        "protocolVersion": "2025-03-26", "capabilities": {},
        "clientInfo": {"name": "claude-code", "version": "1.0"}}}
    res, sid = _post(init)
    if sid:
        open(SESSION_FILE, "w").write(sid)
    _post({"jsonrpc": "2.0", "method": "notifications/initialized"}, sid)
    return sid

def rpc(method, params=None, _id=2):
    sid = get_session()
    payload = {"jsonrpc": "2.0", "id": _id, "method": method}
    if params is not None:
        payload["params"] = params
    res, _ = _post(payload, sid)
    return res

def call_tool(name, arguments=None):
    return rpc("tools/call", {"name": name, "arguments": arguments or {}})

if __name__ == "__main__":
    cmd = sys.argv[1]
    if cmd == "list":
        res = rpc("tools/list")
        for t in res["result"]["tools"]:
            print(t["name"], "-", t.get("description", "")[:150])
    elif cmd == "schema":
        res = rpc("tools/list")
        for t in res["result"]["tools"]:
            if t["name"] == sys.argv[2]:
                print(json.dumps(t, indent=2))
    elif cmd == "call":
        args = json.loads(sys.argv[3]) if len(sys.argv) > 3 else {}
        res = call_tool(sys.argv[2], args)
        print(json.dumps(res, indent=2)[:6000])
    elif cmd == "callfile":  # args JSON from file (for big HTML payloads)
        args = json.loads(open(sys.argv[3], encoding="utf-8").read())
        res = call_tool(sys.argv[2], args)
        print(json.dumps(res, indent=2)[:6000])
