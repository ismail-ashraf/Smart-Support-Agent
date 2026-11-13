import json, re, pathlib

for p in pathlib.Path("n8n").glob("*.json"):
    d = json.loads(p.read_text(encoding="utf-8"))
    d.pop("pinData", None)
    d.pop("staticData", None)
    for n in d.get("nodes", []):
        n.pop("credentials", None)
        n.pop("webhookId", None)
    s = json.dumps(d, ensure_ascii=False, indent=2)
    s = re.sub(r"https://[\w.-]+\.ngrok[\w.-]*\.(?:dev|app|io)",
               "https://REPLACE-WITH-YOUR-API-URL", s)
    p.write_text(s, encoding="utf-8")
    print("cleaned", p.name)