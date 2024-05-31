import requests
import json

# Base URL and endpoint
base_url = "https://8501-129-0-189-24.ngrok-free.app/api/v1/index/company"

# Company ID you want to get
company_id = "2"

# Full URL with company ID
url = f"{base_url}/{company_id}"

try:
    # Perform the GET request
    response = requests.get(url)
    response.raise_for_status()  # Raise an HTTPError for bad responses
    
    # Extract the JSON data from the response
    data = response.json()
    
    # Print or process the data
    print(json.dumps(data, indent=4))

except requests.exceptions.HTTPError as http_err:
    print(f"HTTP error occurred: {http_err}")
except requests.exceptions.RequestException as err:
    print(f"Error occurred: {err}")
