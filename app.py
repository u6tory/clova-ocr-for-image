import json
import base64
import requests
from dotenv import load_dotenv
import os

filename = "33" # 사진명과 동일한 이름의 txt가 만들어진다.
image_type = "jpg"

# For NAVER CLOVA OCR - General Premium
# Docs : https://www.ncloud.com/product/aiService/ocr
# refer to github.com/dev-sngwn

with open(f"./{filename}.{image_type}", "rb") as f:
    img = base64.b64encode(f.read())

load_dotenv(verbose=True)
URL = os.getenv("APIGW_INVOKE_URL")
KEY = os.getenv("SECRET_KEY")
    
headers = {
    "Content-Type": "application/json",
    "X-OCR-SECRET": KEY
}
    
data = {
    "version": "V1",
    "requestId": "sample_id", # 요청을 구분하기 위한 ID, 사용자가 정의
    "timestamp": 0, # 현재 시간
    "images": [
        {
            "name": "sample_image",
            "format": "jpg",
            "data": img.decode('utf-8')
        }
    ]
}
data = json.dumps(data)
response = requests.post(URL, data=data, headers=headers)
res = json.loads(response.text)

image = res["images"]
word_list = image[0]["fields"]

page = ""
for word in word_list:
    page += " " + word["inferText"]

with open(f"./{filename}.txt", "wt", encoding='utf-8') as f:
    f.write(page)

print("Done")
