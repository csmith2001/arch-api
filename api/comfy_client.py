import json
import requests
import json
import os
from copy import deepcopy
from pathlib import Path


COMFY_URL = os.getenv("COMFY_URL")
WORKFLOW_PATH = str(os.getenv("WORKFLOW_PATH"))
OUTPUT_PATH = os.getenv("OUTPUT_PATH")

assert COMFY_URL, "COMFY_URL missing"
assert WORKFLOW_PATH, "WORKFLOW_PATH missing"
assert OUTPUT_PATH, "OUTPUT_PATH missing"

WORKFLOW_PATH = Path(WORKFLOW_PATH)

def load_workflow():
    with open(WORKFLOW_PATH, "r") as f:
        return json.load(f)

def generate_image(prompt: str):

    workflow = deepcopy(load_workflow())

    # Positive prompt node
    workflow["74"]["inputs"]["text"] = prompt

    print(workflow)

    response = requests.post(
        f"{COMFY_URL}/prompt",
        json={"prompt": workflow}
    )

    print("Status:", response.status_code)
    print("Response:", response.text)

    return response.json()

def get_job(prompt_id: str):

    url = f"{COMFY_URL}/history/{prompt_id}"

    print("Calling:", url)

    response = requests.get(url)

    print("Status:", response.status_code)
    print("Body:", response.text)

    response.raise_for_status()

    return response.json()

def get_image_info(prompt_id: str):

    response = requests.get(
        f"{COMFY_URL}/history/{prompt_id}"
    )

    data = response.json()
    prompt_data = data[prompt_id]
    outputs = prompt_data["outputs"]
    save_node = outputs["79"]
    image = save_node["images"][0]

    return image