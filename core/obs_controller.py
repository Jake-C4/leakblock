from obswebsocket import obsws, requests
import json

with open("config.json") as f:
    config = json.load(f)
obs_config = config["obs"]

def trigger_obs_scene():
    try:
        ws = obsws(obs_config["host"], obs_config["port"], obs_config["password"])
        ws.connect()
        ws.call(requests.SetCurrentScene(obs_config["scene_on_leak"]))
        ws.disconnect()
    except Exception as e:
        print(f"OBS Error: {e}")
