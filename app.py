import os
# import cv2
from facedb import FaceDB
from fastapi import FastAPI, File, Form, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from fastapi.responses import JSONResponse
from pinecone import Pinecone
import face_recognition

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)


pc = Pinecone(api_key="bc89edcc-47ce-4528-8aa7-c8250226aeff")
index = pc.Index("image-search")

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
async def add_user(image: UploadFile = File(...), name: str = Form(...), id: str = Form(...)):

    try:
        image_path = os.path.join(UPLOAD_DIRECTORY, image.filename)
        with open(image_path, "wb") as buffer:
            buffer.write(await image.read())
        known_image = face_recognition.load_image_file(image_path)
        encoding = face_recognition.face_encodings(known_image)[0]

        index.upsert(
            vectors=[
                {
                    "id": id,
                    "values" : encoding,
                    "metadata" : {"name": name, "id": id}
                }
            ],
            namespace="ns1"
        )

        return JSONResponse(content={"message": f"Image {image.filename} saved successfully and name '{name}' received.", "status_code": 200})
    except Exception as e:
        return {"message": f"Internal server error {str(e)} ", "status_code" : 500}

@app.post("/recognize")
async def recognize(image: UploadFile=File(...)):
    try:
        image_path = os.path.join(FIND, image.filename)
        with open(image_path, "wb") as buffer:
            buffer.write(await image.read())
        print(f"[*]---- file path --> {image_path}")
        unknown_image = face_recognition.load_image_file(image_path)
        print(f"Load images")
        encoding = face_recognition.face_encodings(unknown_image)[0]
        print(f" [*]--- Load encodings ---> {encoding} ")
        print(f" [*] --- lenght of array ---> {len(encoding)}")

        result = index.query(
            namespace="ns1",
            vector=[-0.177282423, 0.0779956877, 0.109792665, 0.00617665425, 0.0677807331, -0.0773002356, 0.0731157139, -0.0840765685, 0.110675603, -0.0331197083, 0.28594014, -0.0525426567, -0.22281684, -0.110976391, 0.0485437401, 0.0948496461, -0.16208151, -0.106147163, -0.0994010866, -0.133423656, -0.0163490735, 0.0172741786, -0.0247669723, 0.111278996, -0.0864318758, -0.250517577, -0.104848593, -0.111471064, 0.0893681422, -0.0249204207, 0.0494290702, 0.0748323053, -0.143070549, -0.00411333516, -0.0755672157, 0.0127475243, 0.0865464285, -0.0562512912, 0.185795754, 0.0780271143, -0.110310525, -0.045456361, -0.0791164264, 0.329805613, 0.186107844, -0.0773472413, 0.0144710066, 0.0423617736, 0.0458734892, -0.201675951, 0.0292058475, 0.135238469, 0.192945987, 0.0479450449, -0.0327048413, -0.141337544, -0.0915190428, 0.0562040433, -0.155257955, 0.0283605233, -0.000245339237, -0.0927798823, -0.0529255196, -0.0585842915, 0.217891231, 0.153977275, -0.133425057, -0.145509079, 0.241988048, -0.0977423415, -0.0371253, 0.10976854, -0.159445882, -0.069229126, -0.24211669, 0.169314504, 0.343994439, 0.0454294682, -0.213917732, -0.0291881058, -0.256609201, 0.0355958082, -0.0315275267, 0.0356058367, -0.0829429775, -0.00329735968, -0.104100272, -0.0181150865, 0.126256317, 0.0193559751, -0.116362914, 0.208313271, 0.00243091397, -0.0328343958, 0.0580442622, -0.00436967937, 0.0103405844, -0.0381839685, -0.079671815, -0.0304331165, 0.0492436066, -0.0831696466, 0.00748518156, 0.0891408101, -0.164174, 0.171276435, 0.0744908452, 0.0186552927, 0.0494085103, 0.0855483562, -0.101028904, -0.0504076555, 0.180946961, -0.247279167, 0.13998051, 0.120105296, 0.048581738, 0.123323984, 0.013871545, 0.139534056, -0.0766166151, -0.0264646169, -0.0569715947, -0.0435993224, 0.0779949352, 0.0241264142, -0.00436109025, 0.0549896434],
            top_k=2,
            include_values=True,
            include_metadata=True,
        ) 
        print(f"[*]--- Query result ---> {result}") 
        return JSONResponse(content={"message": "Results", "data": result})
    except Exception as e:
        return {"message": f"Internal server error {str(e)} ", "status_code": 500 }


 



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