import streamlit as st
import google.genai as genai
from PIL import Image

# 1. 페이지 설정
st.set_page_config(page_title="스마트 냉장고 파수꾼", page_icon="🥦", layout="wide")

# 2. 사이드바 API 키 입력
st.sidebar.title("⚙️ 설정")
api_key = st.sidebar.text_input("Gemini API Key를 입력하세요", type="password")

if not api_key:
    st.warning("👈 사이드바에 Gemini API Key를 입력해주어야 작동합니다.")
    st.info("💡 API 키는 https://aistudio.google.com/ 에서 무료로 발급받을 수 있습니다.")
    st.stop()

client = genai.Client(api_key=api_key)

# 3. 메인 화면
st.title("🥦 AI 스마트 냉장고 파수꾼")
st.caption("남은 식재료를 활용해 음식물 쓰레기를 줄이고 맛있는 요리를 만들어보세요!")

tab1, tab2 = st.tabs(["💡 AI 맞춤 레시피 추천", "📸 사진으로 식재료 인식"])

# TAB 1: 레시피 추천
with tab1:
    st.subheader("냉장고 속 재료 입력")
    col1, col2 = st.columns(2)
    with col1:
        ingredients = st.text_area("보유 중인 식재료를 입력하세요", placeholder="예: 계란 2개, 양파 반 개, 대파")
    with col2:
        meal_type = st.selectbox("원하는 요리 유형", ["상관없음", "간단한 한끼", "안주/야식", "다이어트식"])
        cooking_time = st.select_slider("최대 조리 시간 (분)", options=[10, 15, 20, 30, 45, 60], value=20)

    if st.button("🍳 레시피 추천받기", type="primary"):
        if not ingredients.strip():
            st.error("식재료를 입력해주세요.")
        else:
            with st.spinner("Gemini AI가 레시피를 만드는 중입니다..."):
                prompt = f"다음 재료로 만들 수 있는 추천 레시피 2가지를 알려줘.\n- 재료: {ingredients}\n- 유형: {meal_type}\n- 시간: {cooking_time}분 이내"
                try:
                    response = client.models.generate_content(model='gemini-2.5-flash', contents=prompt)
                    st.markdown("### 🍽️ AI 추천 레시피")
                    st.write(response.text)
                except Exception as e:
                    st.error(f"오류 발생: {e}")

# TAB 2: 이미지 인식
with tab2:
    st.subheader("식재료/영수증 사진 분석")
    uploaded_file = st.file_uploader("사진을 업로드하세요", type=["jpg", "jpeg", "png"])

    if uploaded_file is not None:
        image = Image.open(uploaded_file)
        st.image(image, caption="업로드한 이미지", use_column_width=True)

        if st.button("🔍 이미지 분석하기"):
            with st.spinner("분석 중입니다..."):
                prompt = "이미지에서 식재료 목록, 권장 보관 방법(냉장/냉동/실온), 보관 기한을 표(Table) 형태로 정돈해줘."
                try:
                    response = client.models.generate_content(model='gemini-2.5-flash', contents=[image, prompt])
                    st.markdown("### 📝 식재료 분석 및 보관 가이드")
                    st.write(response.text)
                except Exception as e:
                    st.error(f"오류 발생: {e}")
