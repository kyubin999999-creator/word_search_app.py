import streamlit as st
import wikipedia
import requests
from io import BytesIO
from PIL import Image

# Streamlit 웹 앱 설정
st.title('단어 검색기')
st.write('단어를 입력하면 설명과 이미지를 가져옵니다.')

# 사용자가 입력한 단어 받기
search_word = st.text_input("검색할 단어를 입력하세요:")

if search_word:
    # Wikipedia API를 사용해서 설명 가져오기
    try:
        # Wikipedia에서 설명 가져오기
        summary = wikipedia.summary(search_word, sentences=3)  # 3문장으로 제한
        st.subheader(f"{search_word}에 대한 설명")
        st.write(summary)
        
        # Unsplash API로 이미지 검색
        url = f"https://api.unsplash.com/photos/random?query={search_word}&client_id=YOUR_ACCESS_KEY"
        response = requests.get(url)
        image_url = response.json()[0]['urls']['regular']  # 첫 번째 이미지 가져오기
        
        # 이미지 다운로드 및 표시
        image_response = requests.get(image_url)
        img = Image.open(BytesIO(image_response.content))
        
        st.subheader(f"{search_word} 관련 이미지")
        st.image(img, caption=f"{search_word} 이미지", use_column_width=True)
    
    except wikipedia.exceptions.DisambiguationError as e:
        st.error(f"검색어에 대해 여러 개의 결과가 있습니다: {e.options}")
    except wikipedia.exceptions.HTTPTimeoutError:
        st.error("Wikipedia API 호출에 실패했습니다. 나중에 다시 시도해 주세요.")
    except Exception as e:
        st.error(f"오류 발생: {str(e)}")
