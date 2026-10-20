import json
import urllib.request
import urllib.error
from core.config import ROOT

def register(assistant):
    def services(_=""):
        items=assistant.config.get("homelab",{}).get("services",[])
        if not items: return "No homelab services configured. Add entries to homelab.services in config.json."
        return "Configured services:\n" + "\n".join(f"- {item.get('name','unnamed')}: {item.get('url','no URL')}" for item in items)

    def check_service(argument=""):
        items=assistant.config.get("homelab",{}).get("services",[])
        name=argument.strip().lower()
        if not name: return "Usage: run service <service-name>"
        item=next((s for s in items if s.get("name","").lower()==name),None)
        if not item: return f"Unknown service '{argument}'. Use 'run services' to list configured services."
        url=item.get("health_url") or item.get("url")
        if not url: return "This service has no URL configured."
        req=urllib.request.Request(url,headers={"User-Agent":"NyxAssistant/2.0"},method="GET")
        try:
            with urllib.request.urlopen(req,timeout=float(item.get("timeout_seconds",4))) as response:
                return f"{item.get('name',name)} responded with HTTP {response.status}."
        except Exception as exc: return f"Could not reach {item.get('name',name)} at {url}: {exc}"

    assistant.command("services", "List configured homelab service endpoints.", services)
    assistant.command("service", "Check a configured service URL: run service jellyfin.", check_service)
