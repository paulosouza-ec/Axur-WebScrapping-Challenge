import requests
from bs4 import BeautifulSoup
import base64

# Step 1: Downloading img from the page (Scrapping):

PageUrl = 'https://intern.aiaxuropenings.com/scrape/565baf6b-dccd-4a76-aa19-1567a4e98fa7'


if (requests.get(PageUrl)).status_code == 200:

    HtmlPage = (requests.get(PageUrl)).text

    
    if (BeautifulSoup(HtmlPage, 'html.parser')).find('img'):

        ImgOrigin = (BeautifulSoup(HtmlPage, 'html.parser')).find('img').get('src')
        
        if ImgOrigin and ImgOrigin.startswith('data:image'):
            img_data_base64 = ImgOrigin.split(',')[1]
            img_data = base64.b64decode(img_data_base64)
            with open('downloaded_image.jpg', 'wb') as f:
                f.write(img_data)
            print('The file was found and downloaded.')
        else:
            print('Imagem não salva - não é uma imagem em base64 ou src está vazio')
    else: 
        print('Couldn\'t find any img tag')
else: 
    print(f'Access Error: {(requests.get(PageUrl)).status_code}')