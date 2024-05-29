import requests

# Define the endpoint URL
url = "https://ntchinda-giscard-facial-reg.hf.space/recognize"

# Define the path to the image file you want to upload
file_path = "francisman.jpeg"

# Open the file in binary mode
with open(file_path, 'rb') as file:
    # Create a dictionary with the form data
    files = {'image': file}
    
    # Send the POST request
    response = requests.post(url, files=files)
    
    # Print the response from the server
    print(response.status_code)
    print(response.json())
