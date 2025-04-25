from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import JSONResponse
import os
import temp


app = FastAPI()

# Enable CORS for your frontend URL
origins = [
    "http://localhost:3000",  # Frontend origin
    "http://127.0.0.1:3000"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount a static folder (make sure it exists)
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/generate-outfit")
async def generate_outfit():
    temp.main()  

    image_path = os.path.join("static", "result_image.webp")
    
    if os.path.exists(image_path):
        print("Image found and ready to display")
        return {"url": "http://127.0.0.1:8000/static/result_image.webp"}
    
    else:
        return JSONResponse(content={"error": "Image not found"}, status_code=404)
