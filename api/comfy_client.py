import json
import requests
from copy import deepcopy

COMFY_URL = "http://127.0.0.1:8188"

def load_workflow():
    with open("workflows/sdxl.json", "r") as f:
        return json.load(f)


def generate_image(prompt: str):

    workflow = deepcopy(load_workflow())

    # Positive prompt node
    workflow["74"]["inputs"]["text"] = prompt

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