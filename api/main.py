from dotenv import load_dotenv
load_dotenv()

from fastapi import FastAPI
from api.schemas import GenerateRequest
from fastapi.staticfiles import StaticFiles
import api.comfy_client as comfy_client, os

API_PORT = os.getenv("API_PORT")
DOMAIN = os.getenv("DOMAIN")
OUTPUT_PATH = os.getenv("OUTPUT_PATH")

assert API_PORT, "API_PORT missing"
assert DOMAIN, "DOMAIN missing"
assert OUTPUT_PATH, "OUTPUT_PATH missing"

# Initialize FastAPI class
app = FastAPI()
app.mount(
    "/images",
    StaticFiles(directory=OUTPUT_PATH),
    name="images"
)

# api root
@app.get("/")
def health():
    return {"status": "running"}

# Text to image main execution
@app.post("/generate")
def generate(req: GenerateRequest):
    return comfy_client.generate_image(req.prompt)

# Get job Info
@app.get("/job/{prompt_id}")
def get_job(prompt_id: str):
    return comfy_client.get_job(prompt_id)

# Get download URL
@app.get("/image/{prompt_id}")
def get_image(prompt_id: str):

    image = comfy_client.get_image_info(prompt_id)
    filename = image["filename"]

    return {
        "prompt_id": "611f64ff-e5e0-4b33-83be-1971045abd9a",
        "filename": "ComfyUI_00003_.png",
        "image_url": "http://192.168.0.119:8000/images/ComfyUI_00003_.png"
    }
