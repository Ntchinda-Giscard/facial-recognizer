


import uuid
import requests

# Define the endpoint URL
url = "https://ntchinda-giscard-facial-reg.hf.space/recognize"

# Define the file and data to be sent
file_path = "IMG_0603.jpg"
name = "Giscard"
id = str(uuid.uuid4())

# Open the file in binary mode
# with open(file_path, 'rb') as file:
#     # Create a dictionary with the form data
#     files = {'image': file}
#     data = {'name': name, 'id': id}
    
#     # Send the POST request
#     response = requests.post(url, files=files, data=data)
    
#     # Print the response from the server
#     print(response.status_code)
#     print(response.json())

with open(file_path, 'rb') as file:
    # Create a dictionary with the form data
    files = {'image': file}
    data = {'name': name, 'id': id}
    
    # Send the POST request
    response = requests.post(url, 
                             files=files, 
                            #  data=data
                             )
    
    # Print the response from the server
    print(response.status_code)
    print(response.json())
