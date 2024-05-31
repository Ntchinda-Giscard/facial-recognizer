import os
from typing import Any, Dict, List
# import cv2
# from facedb import FaceDB
from fastapi import FastAPI, File, Form, HTTPException, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from fastapi.responses import JSONResponse
from pinecone import Pinecone, ServerlessSpec
from deepface import DeepFace
from pydantic import BaseModel
import requests
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
# index = pc.Index("image-reg")
# index = None

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
                body {
            font-family: Arial, sans-serif;
            margin: 40px;
            background-color: #f4f4f4;
        }
        h1, h2, h3 {
            color: #333;
        }
        table {
            width: 100%;
            border-collapse: collapse;
            margin-bottom: 20px;
        }
        table, th, td {
            border: 1px solid #ddd;
        }
        th, td {
            padding: 8px;
            text-align: left;
        }
        th {
            background-color: #007FFF;
            color: white;
        }
        pre {
            background-color: #f9f9f9;
            border: 1px solid #ddd;
            padding: 10px;
        }
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
            <h1>Welcome to FACIAL-REG AI App! 😊</h1>
            <p class="text"> Explore the wonders of our OCR and ANPR APIs! These powerful tools utilize AI to effortlessly decipher and recognize elements within Cameroonian ID cards, extracting valuable information with just a simple call to the <code> "/idextract" </code> endpoint. With our technology, you'll gain the ability to see beyond the surface and effortlessly identify vehicle license plates using the <code>"/carplate"</code> endpoint. The power is now yours to wield. Unleash the full potential of these tools and revolutionize your workflow..</p>
            <p>Let this app be the beginning of your journey towards greatness!</p>
            <h1>API Documentation for <code>add_user</code></h1>
    
            <h2>Endpoint</h2>
            <p><code>POST /add-user</code></p>
            
            <h2>Description</h2>
            <p>This endpoint allows users to add a new user by uploading an image and providing additional information. The system checks for similar existing users based on the facial embedding generated from the uploaded image. If a similar user already exists, it returns a message indicating so. Otherwise, it saves the new user’s information.</p>
            
            <h2>Request Headers</h2>
            <p><code>Content-Type: multipart/form-data</code></p>
            
            <h2>Request Body</h2>
            <p>The request body should be sent as <code>multipart/form-data</code> and include the following fields:</p>
                <table>
            <thead>
                <tr>
                    <th>Name</th>
                    <th>Type</th>
                    <th>Description</th>
                </tr>
            </thead>
            <tbody>
                <tr>
                    <td>image</td>
                    <td>file (image)</td>
                    <td>The image file of the user to be uploaded.</td>
                </tr>
                <tr>
                    <td>name</td>
                    <td>string</td>
                    <td>The name of the user.</td>
                </tr>
                <tr>
                    <td>id</td>
                    <td>integer</td>
                    <td>The unique identifier for the user.</td>
                </tr>
                <tr>
                    <td>location_id</td>
                    <td>integer</td>
                    <td>The location identifier for the user.</td>
                </tr>
            </tbody>
        </table>
            <h2>Example</h2>
    <p>Here is an example of how to structure the request using <code>curl</code>:</p>
    <pre><code>curl -X POST "http://your-api-url/add-user" \
  -H "Content-Type: multipart/form-data" \
  -F "image=@/path/to/your/image.jpg" \
  -F "name=John Doe" \
  -F "id=12345" \
  -F "location_id=67890"</code></pre>
    
    <h2>Response</h2>
    
    <h3>Success Response (User added successfully)</h3>
    <p><code>Status Code: 200 OK</code></p>
    <p><code>Content-Type: application/json</code></p>
    <pre><code>{
    "message": "Image image.jpg saved successfully and name 'John Doe' received.",
    "status_code": 200
}</code></pre>
    
    <h3>Success Response (Similar user already exists)</h3>
    <p><code>Status Code: 202 Accepted</code></p>
    <p><code>Content-Type: application/json</code></p>
    <pre><code>{
    "message": "A similar user already exists",
    "status_code": 202,
    "data": {
        "matches": [
            {
                "score": 80.12,
                "metadata": {
                    "name": "Jane Doe",
                    "location_id": 67890,
                    "id": 12346
                }
            }
        ]
    }
}</code></pre>
    
    <h3>Error Response</h3>
    <p><code>Status Code: 500 Internal Server Error</code></p>
    <p><code>Content-Type: application/json</code></p>
    <pre><code>{
    "message": "Internal server error &lt;error_message&gt;",
    "status_code": 500
}</code></pre>
    
    <h2>Detailed Explanation</h2>
    <ul>
        <li><strong>Headers:</strong> The endpoint accepts a <code>Content-Type</code> header of <code>multipart/form-data</code>, indicating that the request body will contain multiple parts, including file uploads.</li>
        <li><strong>Request Body:</strong> The body includes the image file, name, id, and location_id. These parameters are necessary to create a new user entry and check for existing similar users.</li>
        <li><strong>Response:</strong> The response varies depending on whether a similar user already exists. If a similar user is found (based on a matching score of 79 or higher), it returns a 202 status code with a message and data about the match. If no similar user is found, it adds the new user and returns a 200 status code with a success message. If an error occurs, it returns a 500 status code with an error message.</li>
    </ul>

        </div>
        <div class="footer">
            <p>Made with ❤️ by Ntchinda Giscard</p>
        </div>
    </body>
    </html>
    """
    return HTMLResponse(content=html_content, status_code=200)



# Model for the form data
class AddUserForm(BaseModel):
    companyId: str
    name: str
    id: str
    location_id: str

# Model for the lookup user result
class Match(BaseModel):
    score: float
    id: str
    metadata: Dict[str, Any]

class LookupUserResult(BaseModel):
    matches: List[Match]

# Model for the add user response
class AddUserResponse(BaseModel):
    message: str
    status_code: int
    data: LookupUserResult = None

def lookup_user(index, embedding_vector):
    # Simulating a function that returns lookup data
    # You need to replace this with the actual lookup logic
    return {
        "matches": [
            {
                "score": 80.0,
                "id": "existing_user_id",
                "metadata": {"name": "Existing User"}
            }
        ]
    }

@app.post("/add-user", response_model=AddUserResponse)
async def add_user(
    image: UploadFile = File(...),
    company_id: str = Form(...),
    name: str = Form(...),
    id: str = Form(...),
    location_id: str = Form(...)
):
    base_url = "https://fe34-102-244-42-232.ngrok-free.app/api/v1/index/company"
    company_id = company_id
    url = f"{base_url}/{company_id}"

    try:
        # Perform the GET request
        response = requests.get(url)
        response.raise_for_status()  # Raise an HTTPError for bad responses
        
        # Extract the JSON data from the response
        data = response.json()
        
        # Print or process the data

    except requests.exceptions.HTTPError as e:
        raise HTTPException(status_code=500, detail=f"Internal server error {str(e)}")
    except requests.exceptions.RequestException as err:
       raise HTTPException(status_code=500, detail=f"Internal server error {str(e)}")
    try:
        # Ensure the upload directory exists
        os.makedirs(UPLOAD_DIRECTORY, exist_ok=True)

        image_path = os.path.join(UPLOAD_DIRECTORY, image.filename)
        with open(image_path, "wb") as buffer:
            buffer.write(await image.read())

        embedding = DeepFace.represent(img_path=image_path, model_name='DeepFace')
        embedding_vector = embedding[0]['embedding']
        print(data)

        index = data["data"]["data"][0]["index"]

        index = pc.Index(index)


        result_data = lookup_user(index, embedding_vector)
        if result_data["matches"][0]["score"] >= 79.00:
            return JSONResponse(
                content={"message": "A similar user already exist", "status_code": 202, "data": result_data},
                status_code=202
            )

        index.upsert(
            vectors=[
                {
                    "id": id,
                    "values": embedding_vector,
                    "metadata": {"name": name, "location_id": int(location_id), "id": id}
                }
            ],
            namespace="ns1"
        )

        return JSONResponse(
            content={"message": f"Image {image.filename} saved successfully and name '{name}' received."},
            status_code=200
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error {str(e)}")


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

        result_data = lookup_user("2-vmedia", encoding_list)

        if(result_data["matches"][0]["score"] >= 0.7900):
            return JSONResponse(content={"message": "User found", "data": result_data, "status_code" : 200})
        else:
            return JSONResponse(content={"message": "User not found", "status_code" : 404, "data": result_data})
        
    except Exception as e:
        return JSONResponse(content={"message": f"Internal server error {str(e)}", "status_code": 500})

# Define the webhook payload model
class WebhookPayload(BaseModel):
    company_id: int
    company_name: str

@app.post("/webhook")
async def create_pinecone_index(payload: WebhookPayload):
    company_id = payload.company_id
    company_name = payload.company_name.lower()

    # Create an index in Pinecone
    index_name = f"{company_id}-{company_name}"
    indexes = pc.list_indexes().index_list.to_dict()
    print(indexes["indexes"])
    print(f"[*] --- Index name {index_name} ")
    found = any(item.get('name') == index_name for item in indexes["indexes"])

    if not found:
        try:
            data = {
                "index": index_name,
                "companyId": payload.company_id
            }
            
            result = pc.create_index(
                name= index_name,
                dimension=4096,
                metric="cosine",
                spec=ServerlessSpec(
                    cloud="aws",
                    region="us-east-1"
                )
            )
            try:
                response = requests.post("https://8501-129-0-189-24.ngrok-free.app/api/v1/index/create", json=data)
            except Exception as e:
                raise HTTPException(status_code=500, detail=f"Failed to create index: {str(e)}")
            print(f" [*] --- Posting data {response} ")
            if (response):
                return JSONResponse(content={"message": f"Index {index_name} created successfully", "status_code": 201, "data" : response.json()})

            return {"message": f"Index '{index_name}' created successfully but writing to index table failed"}
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Failed to create index: {str(e)}")
    else:
        return HTTPException(status_code=405, detail=f"Index '{index_name}' already exists")
        
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=7860)