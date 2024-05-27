import os
import cv2
from facedb import FaceDB
from fastapi import FastAPI, File, Form, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

# Create a FaceDB instance and specify where to store the database
db = FaceDB(
    path="facedata",
)
UPLOAD_DIRECTORY = "UPLOAD"
FIND = "FIND"
os.makedirs(UPLOAD_DIRECTORY, exist_ok=True)
os.makedirs(FIND, exist_ok=True)



# Add a new face to the database
@app.post("/save-user")
async def save_user(image: UploadFile = File(...), name: str = Form(...)):
    # Save the image to disk
    image_path = os.path.join(UPLOAD_DIRECTORY, image.filename)
    with open(image_path, "wb") as buffer:
        buffer.write(await image.read())
    db.add(name, img=image_path)

    # Print the name
    print(name)

    return JSONResponse(content={"message": f"Image {image.filename} saved successfully and name '{name}' received."})

@app.post("/find-user")
async def find_user(image: UploadFile=File(...)):
    image_path = os.path.join(FIND, image.filename)
    with open(image_path, "wb") as buffer:
        buffer.write(await image.read())
    
    result = db.recognize(img=image_path)

    if result["confidence"] >= 79.00:
        return JSONResponse(content={"message": "User found","status_code": 200 , "data" : { "name": result['id'][:-23], 'conf': result['confidence'] }})
    else:
        JSONResponse(content={"message": "Unknown user", "status_code": 400})

        
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=7860)