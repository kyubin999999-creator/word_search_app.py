import streamlit as st
import requests
import json

# Google Custom Search API 설정
API_KEY = "YOUR_GOOGLE_API_KEY"  # 여기에 실제 Google API 키 입력
CX = "YOUR_CUSTOM_SEARCH_ENGINE_ID"  # 여기에 실제 Custom Search Engine ID 입력

# Oxford API 설정
OXFORD_API_KEY = "YOUR_OXFORD_API_KEY"  # 여기에 실제 Oxford API Key 입력
OXFORD_APP_ID = "YOUR_OXFORD_APP_ID"  # 여기에 실제 Oxford App ID 입력

# 이미지 검색 함수
def get_image(query):
    url = f"https://www.googleapis.com/customsearch/v1?q={query}&searchType=image&key={API_KEY}&cx={CX}"
    response = requests.get(url)
    
    # API 응답 상태 확인
    if response.status_code != 200:
        st.write(f"Google API Error: {response.status_code} - {response.text}")
        return None
    
    results = response.json()
    
    # 응답 로그 출력
    st.write("Google Image Search Response:", results)  # API 응답을 확인합니다.
    
    try:
        image_url = results['items'][0]['link']
        return image_url
    except KeyError:
        st.write("No images found for this query.")
        return None

# 사전 설명 가져오기 함수
def get_definition(word):
    url = f"https://od-api.oxforddictionaries.com/api/v2/entries/en-us/{word.lower()}"
    headers = {
        "app_id": OXFORD_APP_ID,
        "app_key": OXFORD_API_KEY
    }
    
    response = requests.get(url, headers=headers)
    
    # API 응답 상태 확인
    if response.status_code != 200:
        st.write(f"Oxford API Error: {response.status_code} - {response.text}")
        return "Unable to fetch definition."
    
    data = response.json()
    
    # 응답 로그 출력
    st.write("Oxford API Response:", data)  # API 응답을 확인합니다.
    
    try:
        definition = data['results'][0]['lexicalEntries'][0]['entries'][0]['senses'][0]['definitions'][0]
        return definition
    except KeyError:
        return "No definition found."

# Streamlit UI 설정
st.title("단어 설명 및 이미지 검색")
st.write("단어를 입력하면 그에 대한 설명과 이미지를 보여줍니다.")

# 단어 입력 받기
word = st.text_input("단어를 입력하세요:")

if word:
    st.header(f"{word}에 대한 설명과 이미지")
    
    # 이미지 검색
    image_url = get_image(word)
    if image_url:
        st.image(image_url, caption=f"Image for {word}", use_column_width=True)
    else:
        st.write("이미지를 찾을 수 없습니다.")
    
    # 단어 설명
    definition = get_definition(word)
    st.write(f"설명: {definition}")
