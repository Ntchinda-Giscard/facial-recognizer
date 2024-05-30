import requests

# Define the URL of the webhook endpoint
url = "https://ntchinda-giscard-facial-reg.hf.space/webhook"

# Define the payload
payload = {
    "company_id": "12345",
    "company_name": "example_company"
}

# Set the headers
headers = {
    "Content-Type": "application/json"
}

# Send the POST request
response = requests.post(url, json=payload, headers=headers)

# Print the response
print("Status Code:", response.status_code)
print("Response JSON:", response.json())
