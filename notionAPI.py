import requests
from pprint import pprint
import json
import os
from dotenv import load_dotenv

# 환경변수 불러오기
load_dotenv()
# Notion API 키 설정
notion_api_key = os.getenv("NOTION_API_KEY")

# Notion API 헤더 설정
headers = {
    "Authorization": f"Bearer {notion_api_key}",
    "Content-Type": "application/json",
    "Notion-Version": "2022-06-28"
}
# 특정 데이터베이스 ID 설정
DATABASE_ID = 'b4e451f477354620ba19824b103abb06'

# API 요청 URL 설정
url = f"https://api.notion.com/v1/databases/{DATABASE_ID}/query"

# API 요청
response = requests.post(url, headers=headers)
data = response.json()

# 데이터 출력
# print(data)

# 데이터 추출 함수
def extract_data(data):
    extracted_data = []
    for result in data['results']:
        properties = result['properties']
        title = properties['Project name']['title'][0]['text']['content'] if properties['Project name']['title'] else 'No Title'
        date = properties['Dates']['date']['start'] if properties['Dates']['date'] else 'No Date'
        extracted_data.append({
            'Title': title,
            'Date': date
        })
    return extracted_data

# 데이터 추출
extracted_data = extract_data(data)

for item in extracted_data:
    print(f"Title: {item['Title']}, Date: {item['Date']}")
    

# pprint(data)
