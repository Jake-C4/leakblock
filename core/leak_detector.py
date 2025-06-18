import json

with open("config.json") as f:
    config = json.load(f)

watch_terms = config["watch_terms"]

def contains_leak(text: str) -> bool:
    for term in watch_terms:
        if term.lower() in text.lower():
            return True
    return False
