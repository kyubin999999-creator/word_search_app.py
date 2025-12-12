import streamlit as st
import requests
import json

# Google Custom Search API 설정
API_KEY = "YOUR_GOOGLE_API_KEY"  # 여기 API 키를 입력하세요
CX = "YOUR_CUSTOM_SEARCH_ENGINE_ID"  # 여기 CX 값을 입력하세요

# Oxford API 설정
OXFORD_API_KEY = "YOUR_OXFORD_API_KEY"  # 여기 API 키를 입력하세요
OXFORD_APP_ID = "YOUR_OXFORD_APP_ID"  # 여기 App ID를 입력하세요

# 이미지 검색 함수
def get_image(query):
    url = f"https://www.googleapis.com/customsearch/v1?q={query}&searchType=image&key={API_KEY}&cx={CX}"
    response = requests.get(url)
    results = response.json()
    
    try:
        image_url = results['items'][0]['link']
        return image_url
    except KeyError:
        return None

# 사전 설명 가져오기 함수
def get_definition(word):
    url = f"https://od-api.oxforddictionaries.com/api/v2/entries/en-us/{word.lower()}"
    headers = {
        "app_id": OXFORD_APP_ID,
        "app_key": OXFORD_API_KEY
    }
    response = requests.get(url, headers=headers)
    data = response.json()
    
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
