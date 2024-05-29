import os
# import cv2
from facedb import FaceDB
from fastapi import FastAPI, File, Form, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from fastapi.responses import JSONResponse
from pinecone import Pinecone
import face_recognition
from deepface import DeepFace
from utils import lookup_user


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)


pc = Pinecone(api_key="bc89edcc-47ce-4528-8aa7-c8250226aeff")
index = pc.Index("image-reg")

# Create a FaceDB instance and specify where to store the database
# db = FaceDB(
#     path="facedata",
# )

UPLOAD_DIRECTORY = "UPLOAD"
FIND = "FIND"
os.makedirs(UPLOAD_DIRECTORY, exist_ok=True)
os.makedirs(FIND, exist_ok=True)

@app.get("/", response_class=HTMLResponse)
async def read_items():
    html_content = """
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>API Documentation</title>
        <style>
        .text {
            font-family: Arial, sans-serif;
            font-size: 16px;
            font-weight: bold;
            color: #333;
            line-height: 1.5;
            text-align: center;
            text-decoration: none;
            text-transform: uppercase;
            letter-spacing: 1px;
            word-spacing: 2px;
            border: 2px solid #ccc;
            border-radius: 18px;
            padding: 25px;
            }


            .container {
                max-width: 800px;
                margin: 0 auto;
                padding: 20px;
                text-align: center;
            }
            body {
            font-family: Arial, sans-serif;
            margin: 0;
            padding: 0;
        }
        header {
            background-color: #333;
            color: white;
            padding: 20px;
            text-align: center;
        }
        main {
            padding: 20px;
        }
        h2 {
            color: #333;
        }
        ul {
            list-style: none;
            padding: 0;
        }
        li {
            margin-bottom: 20px;
        }
        pre {
            background-color: #f4f4f4;
            padding: 10px;
            border-radius: 5px;
            overflow-x: auto;
        }
        footer {
            background-color: #333;
            color: white;
            padding: 10px;
            text-align: center;
            position: fixed;
            bottom: 0;
            width: 100%;
        }
        </style>
    </head>
    <header>
        <h1>API Documentation</h1>
    </header>
    <body>
        <div class="container">
            <h1>Welcome to VVIMS AI App! 😊</h1>
            <p class="text"> Explore the wonders of our OCR and ANPR APIs! These powerful tools utilize AI to effortlessly decipher and recognize elements within Cameroonian ID cards, extracting valuable information with just a simple call to the <code> "/idextract" </code> endpoint. With our technology, you'll gain the ability to see beyond the surface and effortlessly identify vehicle license plates using the <code>"/carplate"</code> endpoint. The power is now yours to wield. Unleash the full potential of these tools and revolutionize your workflow..</p>
            <p>Let this app be the beginning of your journey towards greatness!</p>
        </div>
        <div class="footer">
            <p>Made with ❤️ by Ntchinda Giscard</p>
        </div>
    </body>
    </html>
    """
    return HTMLResponse(content=html_content, status_code=200)

# Add a new face to the database
# @app.post("/save-user")
# async def save_user(image: UploadFile = File(...), name: str = Form(...)):
#     # Save the image to disk
#     image_path = os.path.join(UPLOAD_DIRECTORY, image.filename)
#     with open(image_path, "wb") as buffer:
#         buffer.write(await image.read())
#     db.add(name, img=image_path)

#     # Print the name
#     print(name)

#     return JSONResponse(content={"message": f"Image {image.filename} saved successfully and name '{name}' received."})

@app.post("/add-user")
async def add_user(image: UploadFile = File(...), name: str = Form(...), id: int = Form(...), location_id: int = Form(...)):

    try:
        image_path = os.path.join(UPLOAD_DIRECTORY, image.filename)
        with open(image_path, "wb") as buffer:
            buffer.write(await image.read())

        embedding = DeepFace.represent(img_path=image_path, model_name='DeepFace')
        embedding_vector = embedding[0]['embedding']

        result_data = lookup_user(index, embedding_vector)

        if(result_data["matches"][0]["score"] >= 79.00):

            return JSONResponse(content={"message": "A similar user already exist", "status_code": 202, "data": result_data})



        index.upsert(
            vectors=[
                {
                    "id": id,
                    "values" : embedding_vector,
                    "metadata" : {"name": name, "location_id": int(location_id), "id": id}
                }
            ],
            namespace="ns1"
        )
        return JSONResponse(content={"message": f"Image {image.filename} saved successfully and name '{name}' received.", "status_code": 200})
    except Exception as e:
        return {"message": f"Internal server error {str(e)} ", "status_code" : 500}


@app.post("/recognize")
async def recognize(image: UploadFile = File(...)):
    try:
        image_path = os.path.join(FIND, image.filename)
        with open(image_path, "wb") as buffer:
            buffer.write(await image.read())
        
        embedding = DeepFace.represent(img_path=image_path, model_name='DeepFace')
        embedding_vector = embedding[0]['embedding']

        # Convert the encoding to a list
        encoding_list = embedding_vector

        result_data = lookup_user(index, encoding_list)

        if(result_data["matches"][0]["score"] >= 0.7900):
            return JSONResponse(content={"message": "User found", "data": result_data, "status_code" : 200})
        else:
            return JSONResponse(content={"message": "User not found", "status_code" : 404, "data": result_data})
        
    except Exception as e:
        return JSONResponse(content={"message": f"Internal server error {str(e)}", "status_code": 500})



 



# @app.post("/find-user")
# async def find_user(image: UploadFile=File(...)):
#     image_path = os.path.join(FIND, image.filename)
#     with open(image_path, "wb") as buffer:
#         buffer.write(await image.read())
    
#     result = db.recognize(img=image_path)

#     if result["confidence"] >= 79.00:
#         return JSONResponse(content={"message": "User found","status_code": 200 , "data" : { "name": result['id'][:-23], 'conf': result['confidence'] }})
#     else:
#         JSONResponse(content={"message": "Unknown user", "status_code": 400})

        
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=7860)