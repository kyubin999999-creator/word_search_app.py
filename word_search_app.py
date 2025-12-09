import streamlit as st
import wikipedia
import requests
from io import BytesIO
from PIL import Image

# CSS 스타일링을 위한 코드
st.markdown("""
    <style>
        body {
            background-color: #f0f4f8;
            font-family: 'Arial', sans-serif;
        }
        .main {
            padding: 2rem;
        }
        h1 {
            color: #2e3d49;
            text-align: center;
            font-size: 3rem;
        }
        h2 {
            color: #1d3557;
            font-size: 2rem;
        }
        .search-box {
            margin: auto;
            width: 50%;
            padding: 10px;
            font-size: 1.2rem;
            border-radius: 5px;
            border: 2px solid #ccc;
        }
        .description {
            background-color: #ffffff;
            border-radius: 8px;
            padding: 1rem;
            box-shadow: 0px 4px 6px rgba(0, 0, 0, 0.1);
        }
        .img-container {
            display: flex;
            justify-content: center;
            margin-top: 20px;
        }
    </style>
""", unsafe_allow_html=True)

# Streamlit 웹 앱 설정
st.title('단어 검색기')
st.write('단어를 입력하면 설명과 이미지를 가져옵니다.')

# 사용자 입력을 위한 텍스트 박스 스타일 추가
search_word = st.text_input("검색할 단어를 입력하세요:", key="search", label_visibility="visible")

if search_word:
    # Wikipedia API를 사용해서 설명 가져오기
    with st.spinner('정보를 가져오는 중...'):
        try:
            # Wikipedia에서 설명 가져오기
            summary = wikipedia.summary(search_word, sentences=3)  # 3문장으로 제한
            st.subheader(f"{search_word}에 대한 설명")
            st.markdown(f'<div class="description">{summary}</div>', unsafe_allow_html=True)
            
            # Unsplash API로 이미지 검색
            url = f"https://api.unsplash.com/photos/random?query={search_word}&client_id=YOUR_ACCESS_KEY"
            response = requests.get(url)
            image_url = response.json()[0]['urls']['regular']  # 첫 번째 이미지 가져오기
            
            # 이미지 다운로드 및 표시
            image_response = requests.get(image_url)
            img = Image.open(BytesIO(image_response.content))
            
            # 이미지를 화면에 맞게 출력
            st.subheader(f"{search_word} 관련 이미지")
            st.image(img, caption=f"{search_word} 이미지", use_column_width=True)
        
        except wikipedia.exceptions.DisambiguationError as e:
            st.error(f"검색어에 대해 여러 개의 결과가 있습니다: {e.options}")
        except wikipedia.exceptions.HTTPTimeoutError:
            st.error("Wikipedia API 호출에 실패했습니다. 나중에 다시 시도해 주세요.")
        except Exception as e:
            st.error(f"오류 발생: {str(e)}")
