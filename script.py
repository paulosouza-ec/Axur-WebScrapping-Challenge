# Libs

import requests
from bs4 import BeautifulSoup
import requests
import base64
import json
import sys

# Initial configs

API_URL = "https://intern.aiaxuropenings.com/v1/chat/completions" 
SUBMIT_URL = "https://intern.aiaxuropenings.com/api/submit-response" 
TOKEN = "#"   
PageUrl = 'https://intern.aiaxuropenings.com/scrape/565baf6b-dccd-4a76-aa19-1567a4e98fa7' 
AcceptanceCode = 200 #Successful code 

#  --------------------------------------- #

# Step 1: Downloading img from the page (Web Scrapping):

if (requests.get(PageUrl)).status_code == AcceptanceCode: #Checking if I can access the page

    HtmlPage = (requests.get(PageUrl)).text #Getting all the page content as a text 

    
    if (BeautifulSoup(HtmlPage, 'html.parser')).find('img'): #Looking for an image in the page (searching for img tags)

        ImgAdress = (BeautifulSoup(HtmlPage, 'html.parser')).find('img').get('src') #Getting the img adress
        
        if ImgAdress and ImgAdress.startswith('data:image'): #Is the img coded in base64 instead of being an ordinary link?
            img_data = base64.b64decode(ImgAdress.split(',')[1]) #If so, the image is decoded and saved as a file
            with open('image.jpg', 'wb') as f:
                f.write(img_data)
            print('The file was found in the page and downloaded.')
        else:
            print('The img isn\'t can\'t suport base64 format')
    else: 
        print('Couldn\'t find any img tag')
else: 
    print(f'Access Error: {(requests.get(PageUrl)).status_code}')


# Step 2: Sending the Image to the AI Model and Submitting the Result

with open("image.jpg", "rb") as img_file: # Opening and saving the image in the format (text) where the API accepts (base 64)
    base64_image = base64.b64encode(img_file.read()).decode("utf-8")

headers = {  # These are the headers. They tell the API who I am through the TOKEN and that I will be sending a json file
    "Authorization": f"Bearer {TOKEN}",
    "Content-Type": "application/json"
}

payload = { #That's the msg body that I'll send to the AI. In simple words I'm sayin: Hey AI, here's a decoded img and I'm asking you to give me a detailed description of this img.
    "model": "microsoft-florence-2-large",
    "messages": [
        {
            "role": "user",
            "content": [
                {
                    "type": "text",
                    "text": "<DETAILED_CAPTION>"
                },
                {
                    "type": "image_url",
                    "image_url": {
                        "url": f"data:image/jpeg;base64,{base64_image}"
                    }
                }
            ]
        }
    ]
}

response = requests.post(API_URL, headers=headers, json=payload) # Sending the img and the request for the AI to analyze

if response.status_code == AcceptanceCode: #Checking if my request was accepted and saving the .json file
    print("Answer accepted from the Florence Model")
    
    with open("model_response.json", "w") as f: #Creating file .json file containing the answer
        json.dump(response.json(), f)
else:
    print(f"The model wasn't accepted. ERROR : {response.status_code}")
    print(response.text)
    sys.exit(1)
 
submit_response = requests.post(SUBMIT_URL,headers=headers, json=response.json()) #Getting the AI answer and submitting to the correction/validation in the Axur Platform

if submit_response.status_code == AcceptanceCode:    #Final check too ensure that the response was submited.
        print(f'Successifully submited: {submit_response.json()} ')
        print(submit_response.text)
        print(f'Status code: {submit_response.status_code}')
else:
    print(f"Failed: {submit_response.status_code}")
    print(submit_response.text)


''' Thank you for the oportunity! If you have any question, please contact me. 
Email: paulosouza.ec@gmail.com

'''