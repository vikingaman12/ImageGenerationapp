import os
import requests
import base64
from dotenv import load_dotenv
import streamlit as st
import google.generativeai as genai

load_dotenv()
api_key = os.getenv("GOOGLE_API_KEY")
genai.configure()

models = [m for m in genai.list_models()]
model_name = 'gemini-pro'
model = genai.GenerativeModel(model_name)

st.title("Generate Images with AI")

def generate_image(question):
    template = f"You have to generate a prompt based on user Input, The prompt will be specifically used for Image generation. So keep in mind to exclude words that might affect the model's safety settings. And the generated prompt must have a realistic essence, but The prompt should be enough in words to catch all the beauty. : {question}"

    response = model.generate_content(template)

    # Display the generated prompt
    st.write("Generated Prompt:")
    st.write(response.text)

    # Create JSON data with the response from the user as the prompt
    json_data = {
        "instances": [
            {
                "prompt": response.text
            }
        ],
        "parameters": {
            "sampleCount": 1
        }
    }
    # Define the endpoint URL
    url = "https://us-central1-aiplatform.googleapis.com/v1/projects/elite-ethos-415705/locations/us-central1/publishers/google/models/imagegeneration@005:predict"

    # Set up the headers with the provided access token
    access_token = "ya29.a0AXooCgvZK3ZZLJG6CZh9Zp7qrg4Rj-9WH9VC20cuD8lGCcOkZLTTDYJ2zsAuPpoHur2lIMozsq5V3dL_hvtQrwssEwD9cc33O_avX-g9kVspqTOnNJfH18_aQx2FE81_TzomkWBuVJ12E9H_2dDBUkiEN8gdW_QFdaM37x0qFyf8aCgYKAfISARMSFQHGX2MiH1ovxILS67FZHPWR8VNVTQ0179"
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json; charset=utf-8"
    }

    # Make the POST request
    response = requests.post(url, headers=headers, json=json_data)

    # Check if the request was successful
    if response.status_code == 200:
        # Extract and decode the base64-encoded image data
        predictions = response.json().get('predictions', [])
        if predictions:
            for i, prediction in enumerate(predictions):
                if 'bytesBase64Encoded' in prediction:
                    encoded_image = prediction['bytesBase64Encoded']
                    decoded_image = base64.b64decode(encoded_image)
                    
                    # Display the decoded image in the Streamlit app
                    st.image(decoded_image, caption=f"Generated Image for '{question}'", use_column_width=True)
        else:
            st.write("No predictions found in the response.")
    else:
        st.write(f"Request failed with status code {response.status_code}.")

# Streamlit UI
question = st.text_input("Enter your prompt :")
if st.button("Generate Image"):
    generate_image(question)


# import os
# import requests
# import base64
# from dotenv import load_dotenv
# import streamlit as st
# import google.generativeai as genai
# import subprocess

# load_dotenv()
# api_key = os.getenv("GOOGLE_API_KEY")
# genai.configure()

# models = [m for m in genai.list_models()]
# model_name = 'gemini-pro'

# model = genai.GenerativeModel(model_name)

# st.title("Generate Images with AI")

# def get_access_token():
#     # Provide the full path to the gcloud executable
#     gcloud_path = r"C:\Windows\System32\cmd.exe"
#     # Execute the gcloud command to get the access token
#     result = subprocess.run([gcloud_path, 'auth', 'print-access-token'], capture_output=True, text=True)
#     if result.returncode == 0:
#         return result.stdout.strip()
#     else:
#         st.write("Failed to retrieve access token.")
#         return None

# def generate_image(question, access_token):
#     if access_token is None:
#         st.write("Access token is not available.")
#         return
    
#     template = f"You have to generate a prompt based on user Input: {question}"
#     response = model.generate_content(template)

#     # Create JSON data with the response from the user as the prompt
#     json_data = {
#         "instances": [
#             {
#                 "prompt": response.text
#             }
#         ],
#         "parameters": {
#             "sampleCount": 1
#         }
#     }

#     # Define the endpoint URL
#     url = "https://us-central1-aiplatform.googleapis.com/v1/projects/elite-ethos-415705/locations/us-central1/publishers/google/models/imagegeneration@005:predict"

#     # Set up the headers with the provided access token
#     headers = {
#         "Authorization": f"Bearer {access_token}",
#         "Content-Type": "application/json; charset=utf-8"
#     }

#     # Make the POST request
#     response = requests.post(url, headers=headers, json=json_data)

#     # Check if the request was successful
#     if response.status_code == 200:
#         # Extract and decode the base64-encoded image data
#         predictions = response.json().get('predictions', [])
#         if predictions:
#             for i, prediction in enumerate(predictions):
#                 if 'bytesBase64Encoded' in prediction:
#                     encoded_image = prediction['bytesBase64Encoded']
#                     decoded_image = base64.b64decode(encoded_image)

#                     # Display the decoded image in the Streamlit app
#                     st.image(decoded_image, caption=f"Generated Image for '{question}'", use_column_width=True)
#         else:
#             st.write("No predictions found in the response.")
#     else:
#         st.write(f"Request failed with status code {response.status_code}.")

# # Streamlit UI
# question = st.text_input("Enter your prompt :")
# if st.button("Generate Image"):
#     access_token = get_access_token()
#     generate_image(question, access_token)