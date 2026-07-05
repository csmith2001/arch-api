from fastapi import FastAPI
from app.schemas import GenerateRequest
import app.comfy_client as comfy_client

# Initialize FastAPI class
app = FastAPI()

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

    # TODO url will change but this is for testing - yeah, testing....
    return {
        "filename": filename,
        "url": f"http://127.0.0.1:8188/view?filename={filename}&type=output"
    }