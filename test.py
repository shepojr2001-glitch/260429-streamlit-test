import streamlit as st
import time

st.title("Streamlit 상태 & 캐싱")

# -------------------------------
# 1. cache_data
# -------------------------------
st.header("1. st.cache_data")

@st.cache_data
def load_data():
    time.sleep(2)  # 느린 작업 가정
    return {"data": [1, 2, 3]}

data = load_data()
st.write("데이터:", data)

# -------------------------------
# 2. cache_resource
# -------------------------------
st.header("2. st.cache_resource")

@st.cache_resource
def load_model():
    return "AI 모델 객체 (예시)"

model = load_model()
st.write("모델:", model)

# -------------------------------
# 3. session_state
# -------------------------------
st.header("3. st.session_state")

if "count" not in st.session_state:
    st.session_state.count = 0

if st.button("증가"):
    st.session_state.count += 1

st.write("현재 값:", st.session_state.count)

# -------------------------------
# 4. context
# -------------------------------
st.header("4. st.context")

st.write("Context 정보:", st.context)

# -------------------------------
# 5. query_params
# -------------------------------
st.header("5. st.query_params")

# URL에서 값 읽기
name = st.query_params.get("name", "없음")

st.write("URL name:", name)

# URL 값 설정
if st.button("URL 변경"):
    st.query_params["name"] = "streamlit"